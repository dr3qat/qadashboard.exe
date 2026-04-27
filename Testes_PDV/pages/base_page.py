"""
Base Page - Classe base para todos os Page Objects.
Contém métodos comuns de interação com elementos.
"""
import time
import subprocess
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from config import (
    DEFAULT_WAIT, logger, LogStyle, Cores, _NO_WINDOW,
    log_acao, log_tecnico, SimbolosASCII, LOG_MODE_DEBUG
)


class BasePage:
    """Classe base com métodos comuns para todas as páginas."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT)
        # Obtém app_package do driver (sessão atual) - funciona com múltiplos devices
        self._app_package = None

    @property
    def app_package(self) -> str:
        """Retorna o app_package da sessão atual do driver."""
        if self._app_package is None:
            try:
                # Pega do capabilities da sessão atual
                caps = self.driver.capabilities
                self._app_package = caps.get('appPackage') or caps.get('app_package')
            except:
                pass
        return self._app_package

    # --- Helpers de locators ---
    def _id_completo(self, element_id: str) -> str:
        """Retorna ID completo com package."""
        if ':id/' in element_id:
            return element_id
        # Usa app_package da sessão, não variável global
        pkg = self.app_package
        if not pkg:
            logger.warning(f"[AVISO] app_package não detectado, usando ID direto: {element_id}")
            return element_id
        return f"{pkg}:id/{element_id}"

    def _capturar_tela_atual(self) -> str:
        """Captura identificador da tela atual para comparação."""
        try:
            return self.driver.page_source[:500]
        except:
            return ""

    def _elemento_realmente_visivel(self, elemento) -> bool:
        """
        Verifica se elemento está REALMENTE visível e interativo.
        Não apenas presente no DOM, mas visível na tela.
        """
        try:
            if not elemento:
                return False

            # Verifica se está displayed
            if not elemento.is_displayed():
                return False

            # Verifica se está enabled
            if not elemento.is_enabled():
                return False

            # Verifica se tem tamanho (não é invisível)
            size = elemento.size
            if size['width'] <= 0 or size['height'] <= 0:
                return False

            # Verifica se está dentro da área visível da tela
            location = elemento.location
            window_size = self.driver.get_window_size()

            if location['y'] < 0 or location['y'] > window_size['height']:
                return False
            if location['x'] < 0 or location['x'] > window_size['width']:
                return False

            return True
        except StaleElementReferenceException:
            return False
        except Exception:
            return False

    # --- Encontrar elementos ---
    def encontrar_por_id(self, element_id: str, tempo_espera: int = None):
        """Encontra elemento por ID."""
        timeout = tempo_espera or DEFAULT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, self._id_completo(element_id)))
        )

    def encontrar_clicavel_por_id(self, element_id: str, tempo_espera: int = None):
        """Encontra elemento clicável por ID com validação rigorosa."""
        timeout = tempo_espera or DEFAULT_WAIT
        full_id = self._id_completo(element_id)

        # Primeiro aguarda estar clicável
        elemento = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ID, full_id))
        )

        # Validação extra: verifica se realmente está visível
        if not self._elemento_realmente_visivel(elemento):
            raise Exception(f"Elemento '{element_id}' encontrado mas NAO está visivel/clicavel na tela")

        return elemento

    def encontrar_por_texto(self, texto: str, tempo_espera: int = None):
        """Encontra elemento por texto visível."""
        timeout = tempo_espera or DEFAULT_WAIT
        locator = f'new UiSelector().textContains("{texto}")'
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, locator))
        )

    def encontrar_por_xpath(self, xpath: str, tempo_espera: int = None):
        """Encontra elemento por XPath."""
        timeout = tempo_espera or DEFAULT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )

    def encontrar_por_accessibility_id(self, accessibility_id: str, tempo_espera: int = None):
        """Encontra elemento por Accessibility ID."""
        timeout = tempo_espera or DEFAULT_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
        )

    def encontrar_todos_por_id(self, element_id: str, tempo_espera: int = None) -> list:
        """Encontra todos os elementos com mesmo ID."""
        timeout = tempo_espera or DEFAULT_WAIT
        full_id = self._id_completo(element_id)
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((AppiumBy.ID, full_id))
            )
        except:
            return []

    def encontrar_todos_por_uiautomator(self, locator: str, tempo_espera: int = None) -> list:
        """Encontra todos os elementos por UiAutomator."""
        timeout = tempo_espera or DEFAULT_WAIT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((AppiumBy.ANDROID_UIAUTOMATOR, locator))
            )
        except:
            return []

    def encontrar_todos_por_classe(self, class_name: str, tempo_espera: int = None) -> list:
        """Encontra todos os elementos por nome de classe."""
        timeout = tempo_espera or DEFAULT_WAIT
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, class_name))
            )
        except:
            return []

    # --- Ações de clique ---
    def clicar_por_id(self, element_id: str, max_tentativas: int = 3):
        """
        Clica em elemento por ID com validação.
        Tenta múltiplas vezes se necessário.
        """
        # Log de ação (modo normal) - mostra apenas uma vez
        log_acao(f"{SimbolosASCII.CLICK} Clicando em '{element_id}'")

        for tentativa in range(max_tentativas):
            try:
                tela_antes = self._capturar_tela_atual()

                # Log técnico (modo debug)
                log_tecnico(f"   Tentativa {tentativa + 1}/{max_tentativas}", "info")

                elemento = self.encontrar_clicavel_por_id(element_id, tempo_espera=5)
                log_tecnico(f"   {LogStyle.CLICK} Clicando em {LogStyle.elemento(element_id)}...", "info")
                elemento.click()

                # Verifica se a tela mudou (clique teve efeito)
                tela_depois = self._capturar_tela_atual()
                if tela_antes != tela_depois:
                    log_tecnico(f"   {LogStyle.OK} Tela mudou após clique", "info")
                    return True

                # Se tela não mudou, pode ser ok (ex: checkbox)
                log_tecnico(f"   {LogStyle.OK} Clique em {LogStyle.elemento(element_id)} executado", "info")
                return True

            except Exception as e:
                if tentativa < max_tentativas - 1:
                    log_tecnico(f"   {LogStyle.RETRY} Tentativa {tentativa + 1} falhou: {e}", "warning")
                    time.sleep(0.5)
                else:
                    log_acao(f"{SimbolosASCII.ERRO} Falha ao clicar em '{element_id}'", "error")
                    log_tecnico(f"   {LogStyle.ERRO} Detalhes: {e}", "error")
                    raise Exception(f"Nao foi possivel clicar em '{element_id}': {e}")

    def clicar_no_primeiro_da_lista_por_id(self, element_id: str, tempo_espera: int = None):
        """Clica no primeiro elemento de uma lista com mesmo ID."""
        timeout = tempo_espera or DEFAULT_WAIT
        full_id = self._id_completo(element_id)

        log_acao(f"{SimbolosASCII.CLICK} Clicando no primeiro da lista '{element_id}'")
        log_tecnico(f"   {LogStyle.LISTA} Buscando elementos com ID {LogStyle.elemento(element_id)}...", "info")

        lista_de_elementos = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((AppiumBy.ID, full_id))
        )

        if not lista_de_elementos:
            raise Exception(f"Nenhum elemento encontrado com o ID '{element_id}'")

        # Encontra o primeiro elemento realmente visível
        for i, elemento in enumerate(lista_de_elementos):
            if self._elemento_realmente_visivel(elemento):
                log_tecnico(f"   {LogStyle.OK} Encontrado elemento visivel na posicao {i}. Clicando...", "info")
                elemento.click()
                return

        raise Exception(f"Nenhum elemento com ID '{element_id}' esta visivel na tela")

    def clicar_por_texto(self, texto: str, tempo_espera: int = None):
        """Clica em elemento por texto."""
        log_acao(f"{SimbolosASCII.CLICK} Clicando em texto '{texto}'")
        log_tecnico(f"   {LogStyle.CLICK} Buscando texto {LogStyle.elemento(texto)}...", "info")

        elemento = self.encontrar_por_texto(texto, tempo_espera)

        if not self._elemento_realmente_visivel(elemento):
            raise Exception(f"Texto '{texto}' encontrado mas NAO esta visivel na tela")

        elemento.click()

        log_tecnico(f"   {LogStyle.OK} Clicado em {LogStyle.elemento(texto)}", "info")

    def clicar_se_existir(self, element_id: str, tempo_espera: int = 3) -> bool:
        """Clica se elemento existir e estiver visível, senão ignora."""
        try:
            elemento = WebDriverWait(self.driver, tempo_espera).until(
                EC.element_to_be_clickable((AppiumBy.ID, self._id_completo(element_id)))
            )

            if self._elemento_realmente_visivel(elemento):
                log_acao(f"{SimbolosASCII.CLICK} Clicando em '{element_id}' (se existir)")
                log_tecnico(f"   {LogStyle.CLICK} Elemento {LogStyle.elemento(element_id)} encontrado. Clicando...", "info")
                elemento.click()
                return True
            else:
                log_tecnico(f"   {LogStyle.SKIP} Elemento {LogStyle.elemento(element_id)} existe mas nao esta visivel", "info")
                return False
        except:
            log_tecnico(f"   {LogStyle.SKIP} Elemento {LogStyle.elemento(element_id)} nao encontrado", "info")
            return False

    def clicar_texto_se_existir(self, texto: str, tempo_espera: int = 3) -> bool:
        """Clica em texto se existir e estiver visível, senão ignora."""
        try:
            elemento = self.encontrar_por_texto(texto, tempo_espera)

            if self._elemento_realmente_visivel(elemento):
                log_acao(f"{SimbolosASCII.CLICK} Clicando em texto '{texto}' (se existir)")
                log_tecnico(f"   {LogStyle.CLICK} Texto {LogStyle.elemento(texto)} encontrado. Clicando...", "info")
                elemento.click()
                return True
            else:
                log_tecnico(f"   {LogStyle.SKIP} Texto {LogStyle.elemento(texto)} existe mas nao esta visivel", "info")
                return False
        except:
            log_tecnico(f"   {LogStyle.SKIP} Texto {LogStyle.elemento(texto)} nao encontrado", "info")
            return False

    def clicar_no_enesimo_texto(self, texto: str, indice: int = 0, tempo_espera: int = None) -> bool:
        """
        Clica no n-ésimo elemento visível com o texto especificado.

        Args:
            texto: Texto a buscar
            indice: Índice do elemento (0 = primeiro, 1 = segundo, etc)
            tempo_espera: Tempo máximo de espera em segundos

        Returns:
            True se clicou com sucesso, False caso contrário

        Raises:
            Exception se não encontrar elementos suficientes
        """
        timeout = tempo_espera or DEFAULT_WAIT
        locator = f'new UiSelector().textContains("{texto}")'

        log_acao(f"{SimbolosASCII.CLICK} Clicando no {indice + 1}º texto '{texto}'")
        log_tecnico(f"   {LogStyle.LISTA} Buscando todos os elementos com texto {LogStyle.elemento(texto)}...", "info")

        try:
            # Busca todos os elementos com o texto
            elementos = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((AppiumBy.ANDROID_UIAUTOMATOR, locator))
            )

            # Filtra apenas os elementos realmente visíveis
            elementos_visiveis = [el for el in elementos if self._elemento_realmente_visivel(el)]

            if not elementos_visiveis:
                raise Exception(f"Nenhum elemento com texto '{texto}' está visível na tela")

            log_tecnico(f"   {LogStyle.OK} Encontrados {len(elementos_visiveis)} elementos visíveis com texto '{texto}'", "info")

            if indice >= len(elementos_visiveis):
                raise Exception(f"Índice {indice} inválido. Apenas {len(elementos_visiveis)} elementos visíveis encontrados")

            elemento_alvo = elementos_visiveis[indice]
            log_tecnico(f"   {LogStyle.CLICK} Clicando no elemento {indice + 1}º com texto {LogStyle.elemento(texto)}...", "info")
            elemento_alvo.click()
            log_tecnico(f"   {LogStyle.OK} Clicado no {indice + 1}º '{texto}'", "info")
            return True

        except TimeoutException:
            log_tecnico(f"   {LogStyle.ERRO} Timeout ao buscar texto '{texto}'", "error")
            raise Exception(f"Elemento com texto '{texto}' não encontrado após {timeout}s")
        except Exception as e:
            logger.error(f"   {LogStyle.ERRO} Erro ao clicar no {indice + 1}º texto '{texto}': {e}")
            raise

    def contar_elementos_visiveis_por_texto(self, texto: str, tempo_espera: int = 3) -> int:
        """
        Conta quantos elementos com determinado texto estão visíveis na tela.

        Args:
            texto: Texto a buscar
            tempo_espera: Tempo máximo de espera em segundos

        Returns:
            Número de elementos visíveis (0 se nenhum encontrado)
        """
        locator = f'new UiSelector().textContains("{texto}")'

        try:
            elementos = WebDriverWait(self.driver, tempo_espera).until(
                EC.presence_of_all_elements_located((AppiumBy.ANDROID_UIAUTOMATOR, locator))
            )
            elementos_visiveis = [el for el in elementos if self._elemento_realmente_visivel(el)]
            count = len(elementos_visiveis)
            log_tecnico(f"   {LogStyle.INFO} {count} elementos com texto '{texto}' visíveis na tela", "info")
            return count
        except TimeoutException:
            log_tecnico(f"   {LogStyle.INFO} Nenhum elemento com texto '{texto}' encontrado", "info")
            return 0
        except Exception as e:
            log_tecnico(f"   {LogStyle.AVISO} Erro ao contar elementos: {e}", "warning")
            return 0

    # --- Ações de digitação ---
    def digitar_por_id(self, element_id: str, texto: str):
        """Digita texto em campo por ID."""
        log_acao(f"{SimbolosASCII.DIGITAR} Digitando '{texto}' no campo '{element_id}'")
        log_tecnico(f"   {LogStyle.DIGITAR} Campo {LogStyle.elemento(element_id)} ← {LogStyle.valor(texto)}", "info")

        campo = self.encontrar_clicavel_por_id(element_id)
        campo.clear()
        campo.send_keys(texto)

    def digitar_por_xpath(self, xpath: str, texto: str):
        """Digita texto em campo por XPath."""
        log_acao(f"{SimbolosASCII.DIGITAR} Digitando '{texto}' via XPath")
        log_tecnico(f"   {LogStyle.DIGITAR} XPath ← {LogStyle.valor(texto)}", "info")

        campo = self.encontrar_por_xpath(xpath)
        campo.clear()
        campo.send_keys(texto)

    # --- Ações de teclado ---
    def fechar_teclado(self, max_tentativas: int = 3) -> bool:
        """
        Fecha o teclado virtual usando múltiplas estratégias.
        Compatível com diferentes ROMs Android (Stone, Cielo, etc).
        """
        for tentativa in range(max_tentativas):
            try:
                if not self._teclado_visivel():
                    return True

                log_tecnico(f"   {LogStyle.TECLADO} Tentativa {tentativa + 1}/{max_tentativas} de fechar...", "info")

                # Método 1: Appium hide_keyboard
                try:
                    self.driver.hide_keyboard()
                    time.sleep(0.3)
                    if not self._teclado_visivel():
                        log_tecnico(f"   {LogStyle.OK} Teclado fechado via hide_keyboard.", "info")
                        return True
                except:
                    pass

                # Método 2: KEYCODE_BACK via ADB
                try:
                    subprocess.run(['adb', 'shell', 'input', 'keyevent', '4'],
                                  timeout=3, capture_output=True, **_NO_WINDOW)
                    time.sleep(0.3)
                    if not self._teclado_visivel():
                        log_tecnico(f"   {LogStyle.OK} Teclado fechado via KEYCODE_BACK.", "info")
                        return True
                except:
                    pass

                # Método 3: KEYCODE_ESCAPE (algumas ROMs respondem melhor)
                try:
                    subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_ESCAPE'],
                                  timeout=3, capture_output=True, **_NO_WINDOW)
                    time.sleep(0.3)
                    if not self._teclado_visivel():
                        log_tecnico(f"   {LogStyle.OK} Teclado fechado via KEYCODE_ESCAPE.", "info")
                        return True
                except:
                    pass

            except:
                pass

        return False

    def _teclado_visivel(self) -> bool:
        """Verifica se teclado está visível."""
        try:
            return self.driver.execute_script('mobile: isKeyboardShown')
        except:
            return False

    def pressionar_pesquisar(self):
        """Pressiona tecla de pesquisa do teclado."""
        self.driver.execute_script('mobile: performEditorAction', {'action': 'search'})

    # --- Ações de scroll ---
    def realizar_scroll_para_baixo(self):
        """Realiza scroll para baixo."""
        size = self.driver.get_window_size()
        x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.2)
        actions.w3c_actions.pointer_action.move_to_location(x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def realizar_scroll_ignorando_teclado(self, direcao: str = 'baixo'):
        """
        Realiza scroll MESMO COM TECLADO ABERTO.
        Usa coordenadas na parte superior da tela para evitar o teclado.
        Universal - funciona em qualquer dispositivo.
        """
        try:
            size = self.driver.get_window_size()
            x = size['width'] // 2

            if direcao == 'baixo':
                # Área superior da tela (acima do teclado)
                # Usa 35% a 10% para garantir que funciona com teclado grande
                y_inicial = int(size['height'] * 0.35)
                y_final = int(size['height'] * 0.10)
            else:
                y_inicial = int(size['height'] * 0.10)
                y_final = int(size['height'] * 0.35)

            log_tecnico(f"   {LogStyle.SCROLL} {direcao} - De Y:{y_inicial} ate Y:{y_final}", "info")

            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(
                self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
            )
            actions.w3c_actions.pointer_action.move_to_location(x, y_inicial)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.3)
            actions.w3c_actions.pointer_action.move_to_location(x, y_final)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            time.sleep(0.5)

        except Exception as e:
            log_tecnico(f"   {LogStyle.aviso('Erro ao fazer scroll:')} {e}", "warning")

    def scroll_nativo_ate_id(self, element_id: str):
        """
        Usa UiScrollable nativo do Android para rolar até elemento.
        Mais confiável em qualquer dispositivo.
        """
        try:
            full_id = self._id_completo(element_id)
            locator = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().resourceId("{full_id}"))'

            log_tecnico(f"   {LogStyle.SCROLL_NATIVO} Buscando ID {LogStyle.elemento(element_id)}...", "info")

            elemento = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator)

            log_tecnico(f"   {LogStyle.OK} ID {LogStyle.elemento(element_id)} encontrado via scroll nativo!", "info")
            return elemento
        except Exception as e:
            log_tecnico(f"   {LogStyle.aviso('Scroll nativo falhou:')} {e}", "warning")
            return None

    def scroll_nativo_ate_texto(self, texto: str):
        """
        Usa UiScrollable nativo do Android para rolar até texto.
        Mais confiável em qualquer dispositivo.
        """
        try:
            locator = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("{texto}"))'
            log_tecnico(f"   {LogStyle.SCROLL_NATIVO} Buscando texto {LogStyle.elemento(texto)}...", "info")
            elemento = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator)
            log_tecnico(f"   {LogStyle.OK} Texto {LogStyle.elemento(texto)} encontrado via scroll nativo!", "info")
            return elemento
        except Exception as e:
            log_tecnico(f"   {LogStyle.aviso('Scroll nativo falhou:')} {e}", "warning")
            return None

    def rolar_ate_texto(self, texto: str, max_scrolls: int = 5):
        """
        Rola até encontrar texto.
        Usa scroll nativo do Android primeiro (mais confiável).
        """
        log_acao(f"{SimbolosASCII.SCROLL} Rolando até texto '{texto}'")
        log_tecnico(f"   {LogStyle.BUSCA} Procurando texto {LogStyle.elemento(texto)}...", "info")

        # Primeiro tenta scroll nativo do Android
        elemento = self.scroll_nativo_ate_texto(texto)
        if elemento and self._elemento_realmente_visivel(elemento):
            return elemento

        # Fallback: scroll manual
        log_tecnico(f"   {LogStyle.FALLBACK} Tentando scroll manual...", "info")
        for tentativa in range(max_scrolls):
            try:
                elemento = self.encontrar_por_texto(texto, tempo_espera=2)
                if self._elemento_realmente_visivel(elemento):
                    log_tecnico(f"   {LogStyle.OK} Texto {LogStyle.elemento(texto)} encontrado e visivel!", "info")
                    return elemento
            except:
                pass

            if tentativa < max_scrolls - 1:
                log_tecnico(f"   {LogStyle.SCROLL} Tentativa {tentativa + 1}: Texto nao visivel. Rolando...", "info")
                self.realizar_scroll_para_baixo()
                time.sleep(0.3)

        raise Exception(f"Texto '{texto}' nao encontrado apos {max_scrolls} scrolls")

    def rolar_ate_texto_ignorando_teclado(self, texto: str, max_scrolls: int = 10):
        """
        Rola ate encontrar texto MESMO COM TECLADO ABERTO.
        Versao melhorada que funciona com teclado na tela.
        """
        log_tecnico(f"   {LogStyle.BUSCA} Procurando {LogStyle.elemento(texto)} (pode ter teclado aberto)...", "info")

        for tentativa in range(max_scrolls):
            try:
                elemento = self.encontrar_por_texto(texto, tempo_espera=2)
                if self._elemento_realmente_visivel(elemento):
                    log_tecnico(f"   {LogStyle.OK} Elemento {LogStyle.elemento(texto)} encontrado e visivel!", "info")
                    return elemento
            except:
                pass

            if tentativa < max_scrolls - 1:
                log_tecnico(f"   {LogStyle.SCROLL} Tentativa {tentativa + 1}: Elemento nao encontrado. Rolando...", "info")
                self.realizar_scroll_ignorando_teclado(direcao='baixo')

        raise Exception(f"Texto '{texto}' nao encontrado apos {max_scrolls} scrolls")

    def rolar_ate_id(self, element_id: str, max_scrolls: int = 10):
        """
        Rola até encontrar elemento por ID.
        Funciona MESMO COM TECLADO ABERTO - não tenta fechar.
        Usa scroll nativo do Android primeiro (mais confiável).
        """
        log_tecnico(f"   {LogStyle.BUSCA} Procurando ID {LogStyle.elemento(element_id)}...", "info")

        # Primeiro tenta scroll nativo do Android (mais confiável)
        elemento = self.scroll_nativo_ate_id(element_id)
        if elemento and self._elemento_realmente_visivel(elemento):
            return elemento

        # Fallback: scroll manual
        log_tecnico(f"   {LogStyle.FALLBACK} Tentando scroll manual...", "info")
        for tentativa in range(max_scrolls):
            try:
                elemento = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((AppiumBy.ID, self._id_completo(element_id)))
                )
                if self._elemento_realmente_visivel(elemento):
                    log_tecnico(f"   {LogStyle.OK} ID {LogStyle.elemento(element_id)} encontrado e visivel!", "info")
                    return elemento
            except:
                pass

            if tentativa < max_scrolls - 1:
                log_tecnico(f"   {LogStyle.SCROLL} Tentativa {tentativa + 1}: Rolando...", "info")
                self.realizar_scroll_ignorando_teclado(direcao='baixo')

        raise Exception(f"ID '{element_id}' nao encontrado apos {max_scrolls} scrolls")

    def ver_e_clicar(self, element_id: str, max_scrolls: int = 5):
        """
        Viu o botão? Aperta. Não viu? Scroll para baixo até ver. Viu? Aperta.
        Sem delays desnecessários — rápido em devices grandes, robusto em devices pequenos.
        Primeiro check usa 3s (render inicial); após scroll usa 2s.
        """
        for tentativa in range(max_scrolls + 1):
            timeout = 3 if tentativa == 0 else 2
            if self.elemento_existe(element_id, tempo_espera=timeout):
                return self.clicar_por_id(element_id)
            if tentativa < max_scrolls:
                log_tecnico(f"   {LogStyle.SCROLL} '{element_id}' nao visivel, rolando para baixo ({tentativa + 1}/{max_scrolls})...", "info")
                self.realizar_scroll_para_baixo()
                time.sleep(0.1)
        return self.clicar_por_id(element_id)

    def ver_e_clicar_texto(self, texto: str, max_scrolls: int = 5):
        """
        Viu o texto? Aperta. Não viu? Scroll para baixo até ver. Viu? Aperta.
        Mesma lógica de ver_e_clicar mas por texto visível.
        Primeiro check usa 3s (render inicial); após scroll usa 2s.
        """
        for tentativa in range(max_scrolls + 1):
            timeout = 3 if tentativa == 0 else 2
            if self.texto_exibido(texto, tempo_espera=timeout):
                return self.clicar_por_texto(texto)
            if tentativa < max_scrolls:
                log_tecnico(f"   {LogStyle.SCROLL} '{texto}' nao visivel, rolando para baixo ({tentativa + 1}/{max_scrolls})...", "info")
                self.realizar_scroll_para_baixo()
                time.sleep(0.1)
        return self.clicar_por_texto(texto)

    # --- Navegação ---
    def voltar_tela(self, confirmar: bool = False) -> bool:
        """Volta para tela anterior usando driver (funciona com múltiplos devices)."""
        log_acao("Voltando para tela anterior")
        log_tecnico(f"{LogStyle.ACAO} Voltando tela...", "info")
        try:
            # Usa driver.back() que funciona no device correto
            self.driver.back()
            time.sleep(0.5)
            if confirmar:
                self._confirmar_dialogo_sair()
            log_tecnico(f"   {LogStyle.OK} Voltou tela", "info")
            return True
        except Exception as e:
            log_tecnico(f"   {LogStyle.aviso('Erro ao voltar tela:')} {e}", "warning")
            return False

    def _confirmar_dialogo_sair(self):
        """Confirma diálogo de sair se aparecer."""
        time.sleep(0.5)
        pkg = self.app_package or ""
        botoes_confirmar = [
            ("android:id/button1", AppiumBy.ID),
            (f"{pkg}:id/md_buttonDefaultPositive", AppiumBy.ID),
        ]

        for locator, by in botoes_confirmar:
            try:
                elemento = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((by, locator))
                )
                elemento.click()
                return
            except:
                continue

    # --- Validações ---
    def texto_exibido(self, texto: str, tempo_espera: int = 5) -> bool:
        """Verifica se texto está visível na tela."""
        try:
            elemento = self.encontrar_por_texto(texto, tempo_espera)
            return self._elemento_realmente_visivel(elemento)
        except:
            return False

    def aguardar_texto(self, texto: str, tempo_espera: int = None):
        """Aguarda texto aparecer na tela."""
        return self.encontrar_por_texto(texto, tempo_espera)

    def elemento_existe(self, element_id: str, tempo_espera: int = 3) -> bool:
        """Verifica se elemento existe e está visível."""
        try:
            elemento = self.encontrar_por_id(element_id, tempo_espera)
            return self._elemento_realmente_visivel(elemento)
        except:
            return False

    def _aguardar_sucesso_event_driven(
        self,
        texto_sucesso: str = "Venda realizada com sucesso!",
        imprimir_cupom: bool = None,
        imprimir_troca: bool = None,
        timeout: int = 45,
    ):
        """
        Event-driven pós-pagamento: monitora o que aparece e age imediatamente.

        Substitui o padrão antigo:
          responder_impressao(timeout=12s fixo)
          + responder_dialogo_cupom_troca(timeout=3s fixo)
          + aguardar_texto(timeout=30s fixo)
        → budget único de 45s, sem wasted time em dialogs ausentes.

        - Dialog SIM/NÃO detectado → responde por TEXTO (evita Bug #3: button2=SIM em alguns devices)
        - "Venda realizada com sucesso!" visível → retorna
        """
        from test_data import test_data
        if imprimir_cupom is None:
            imprimir_cupom = test_data.PRINT_CUPOM_VENDA
        if imprimir_troca is None:
            imprimir_troca = test_data.PRINT_CUPOM_TROCA

        deadline = time.time() + timeout
        dialogs_tratados = 0

        logger.info(f"{LogStyle.ACAO} Aguardando resultado ({timeout}s budget, event-driven)...")

        while time.time() < deadline:
            # 1. Tela de sucesso visível?
            if self.texto_exibido(texto_sucesso, 1):
                logger.info(f"{LogStyle.OK} Sucesso detectado ({dialogs_tratados} dialog(s) tratados)")
                return

            # 2. Dialog de impressão visível? (android:id/button1 = AlertDialog padrão Android)
            if self.elemento_existe("android:id/button1", 1):
                imprimir = imprimir_cupom if dialogs_tratados == 0 else imprimir_troca
                resposta = "SIM" if imprimir else "NÃO"
                # Click por texto evita Bug #3 (button2=SIM em alguns devices)
                if not self.clicar_texto_se_existir(resposta, 1):
                    btn = "android:id/button1" if imprimir else "android:id/button2"
                    self.clicar_se_existir(btn, 1)
                logger.info(f"{LogStyle.OK} Dialog {dialogs_tratados + 1} respondido: {resposta}")
                dialogs_tratados += 1
                time.sleep(0.5 if not imprimir else 2.0)
                continue

            time.sleep(0.3)

        raise TimeoutException(
            f"'{texto_sucesso}' não apareceu em {timeout}s ({dialogs_tratados} dialog(s) tratados)"
        )
