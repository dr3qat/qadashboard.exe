"""
Cliente Page - Page Object para tela de Cadastro de Cliente.
"""
import time
import random
from pages.base_page import BasePage
from config import logger, LogStyle, SimbolosASCII, log_acao, log_tecnico
from faker import Faker
import requests


class ClientePage(BasePage):
    """Page Object para funcionalidade de Cadastro de Cliente."""

    # ========== LOCATORS ==========
    TXT_NOVO_CADASTRO = "Novo Cadastro"

    # Radio buttons tipo de pessoa
    RB_PESSOA_FISICA = "rb_create_client_individual"
    RB_PESSOA_JURIDICA = "rb_create_client_entity"

    # Campos de dados principais
    EDT_DOCUMENTO = "edt_create_client_cpf_cnpj"
    EDT_NOME = "edt_create_client_name"
    EDT_EMAIL = "edt_create_client_email"
    EDT_TELEFONE = "edt_create_fone"
    EDT_CELULAR = "edt_create_cellphone"
    EDT_NUMERO_SAPATO = "til_numero_sapato"
    TIL_DATA_NASCIMENTO = "textInputLayout9"

    # Botões e ações
    BTN_ADICIONAR_ENDERECO = "btn_adicionar_endereco"
    BTN_SALVAR_CLIENTE = "btn_create_client"

    # Campos de endereço
    EDT_CEP = "edt_create_client_cep"
    EDT_RUA = "edt_create_client_address"
    EDT_NUMERO = "edt_create_client_number"
    EDT_CIDADE = "edt_create_client_city"
    EDT_BAIRRO = "edt_create_client_region"
    EDT_ESTADO = "edt_create_client_admin_area"

    # Validação
    MD_CONTENT = "md_content"
    TXT_SUCESSO = "Cliente cadastrado com sucesso!"

    # ========== METODOS AUXILIARES ==========

    def _fechar_teclado_seguro(self):
        """Fecha teclado apenas se estiver visível."""
        try:
            if self.driver.execute_script('mobile: isKeyboardShown'):
                self.fechar_teclado()
        except Exception:
            pass

    def _inserir_campo_e_avancar(self, descricao: str, id_layout: str, valor: str, fechar_teclado: bool = True):
        """
        Insere valor em campo com scroll inteligente se necessário.

        Args:
            descricao: Descrição da ação para log
            id_layout: ID do layout/campo
            valor: Valor a ser inserido
            fechar_teclado: Se deve fechar teclado após digitação
        """
        log_acao(f"{SimbolosASCII.DIGITAR} {descricao}: {valor}")

        # Tenta encontrar elemento, rola se necessário
        elemento_visivel = False
        for tentativa in range(3):
            try:
                elemento = self.encontrar_por_id(id_layout, tempo_espera=1.5)
                if self._elemento_realmente_visivel(elemento):
                    elemento_visivel = True
                    break
            except:
                log_tecnico(f"   Campo '{id_layout}' não visível. Rolando...", "info")
                # Scroll suave na área superior (evita teclado)
                self.realizar_scroll_ignorando_teclado(direcao='baixo')
                time.sleep(0.5)

        if not elemento_visivel:
            log_tecnico(f"   Campo {id_layout} não encontrado, tentando interagir mesmo assim", "warning")

        # Digita o texto no layout
        self._digitar_em_layout(id_layout, valor)

        # Fecha teclado se solicitado
        if fechar_teclado:
            self._fechar_teclado_seguro()
            time.sleep(0.5)

    def _digitar_em_layout(self, id_layout: str, texto: str):
        """
        Digita texto em layout que contém EditText/AutoComplete sem ID próprio.

        Args:
            id_layout: ID do container (layout)
            texto: Texto a digitar
        """
        # Clica no layout para dar foco
        self.clicar_por_id(id_layout)

        # XPath para encontrar campo editável dentro do layout
        xpath_campo = f"//*[@resource-id='{self.app_package}:id/{id_layout}']//*[@clickable='true']"

        # Digita o texto
        self.digitar_por_xpath(xpath_campo, texto)

    # ========== GERACAO DE DADOS ==========

    def gerar_dados_cliente(self, tipo_pessoa: str = "PF") -> dict:
        """
        Gera dados aleatórios de cliente com endereço válido (API ViaCEP).

        Args:
            tipo_pessoa: "PF" para Pessoa Física ou "PJ" para Pessoa Jurídica

        Returns:
            Dicionário com todos os dados do cliente
        """
        fake = Faker('pt_BR')

        # Dados pessoais/empresariais
        if tipo_pessoa == "PF":
            documento = fake.cpf().replace('.', '').replace('-', '')
            nome = fake.name()
        else:
            documento = fake.cnpj().replace('.', '').replace('-', '').replace('/', '')
            nome = fake.company()

        # CEPs reais validados
        ceps_reais = [
            "01001000",  # São Paulo/SP
            "20040002",  # Rio de Janeiro/RJ
            "30140071",  # Belo Horizonte/MG
            "80010000",  # Curitiba/PR
            "90020010",  # Porto Alegre/RS
            "70040010",  # Brasília/DF
            "40020000",  # Salvador/BA
            "60030000",  # Fortaleza/CE
            "50010000",  # Recife/PE
            "69010000"   # Manaus/AM
        ]

        cep_escolhido = random.choice(ceps_reais)

        # Consome API ViaCEP
        try:
            resposta = requests.get(f"https://viacep.com.br/ws/{cep_escolhido}/json/", timeout=5)
            dados_endereco = resposta.json()

            rua = dados_endereco.get("logradouro", "Rua Principal")
            bairro = dados_endereco.get("bairro", "Centro")
            cidade = dados_endereco.get("localidade", "São Paulo")
            estado = dados_endereco.get("uf", "SP")
        except Exception as e:
            log_tecnico(f"   Falha ao consultar ViaCEP: {e}. Usando dados fallback.", "warning")
            # Fallback de segurança
            rua = "Praça da Sé"
            bairro = "Sé"
            cidade = "São Paulo"
            estado = "SP"
            cep_escolhido = "01001000"

        # Gera telefones
        ddd = str(random.randint(11, 99))

        dados = {
            "tipo": tipo_pessoa,
            "documento": documento,
            "nome": nome,
            "email": fake.ascii_free_email(),
            "telefone": f"{ddd}{random.randint(20000000, 59999999)}",
            "celular": f"{ddd}9{random.randint(10000000, 99999999)}",
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%d/%m/%Y'),
            "numero_sapato": str(random.randint(35, 44)),
            "cep": cep_escolhido,
            "rua": rua,
            "numero": str(random.randint(1, 9999)),
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }

        log_tecnico(f"   Dados gerados para {tipo_pessoa}: {dados['nome']}", "info")
        return dados

    # ========== ACOES ==========

    def navegar_novo_cadastro(self):
        """Navega até a tela de Novo Cadastro."""
        log_acao(f"{SimbolosASCII.SCROLL} Navegando até Novo Cadastro")
        self.ver_e_clicar_texto(self.TXT_NOVO_CADASTRO)

    def selecionar_tipo_pessoa(self, tipo: str):
        """
        Seleciona tipo de pessoa (PF ou PJ).

        Args:
            tipo: "PF" para Pessoa Física ou "PJ" para Pessoa Jurídica
        """
        if tipo == "PF":
            log_acao(f"{SimbolosASCII.CLICK} Selecionando Pessoa Física")
            self.clicar_por_id(self.RB_PESSOA_FISICA)
        else:
            log_acao(f"{SimbolosASCII.CLICK} Selecionando Pessoa Jurídica")
            self.clicar_por_id(self.RB_PESSOA_JURIDICA)

    def preencher_dados_principais(self, dados: dict):
        """
        Preenche dados principais do cliente.

        Args:
            dados: Dicionário com dados do cliente
        """
        log_acao(f"{SimbolosASCII.INICIO} Preenchendo dados principais")

        self._inserir_campo_e_avancar("Digitar Documento", self.EDT_DOCUMENTO, dados["documento"])
        self._inserir_campo_e_avancar("Digitar Nome", self.EDT_NOME, dados["nome"])
        self._inserir_campo_e_avancar("Digitar Email", self.EDT_EMAIL, dados["email"])
        self._inserir_campo_e_avancar("Digitar Telefone", self.EDT_TELEFONE, dados["telefone"])
        self._inserir_campo_e_avancar("Digitar Celular", self.EDT_CELULAR, dados["celular"])
        self._inserir_campo_e_avancar("Digitar Número Sapato", self.EDT_NUMERO_SAPATO, dados["numero_sapato"])
        self._inserir_campo_e_avancar("Digitar Data Nascimento", self.TIL_DATA_NASCIMENTO, dados["data_nascimento"])

    def adicionar_endereco(self):
        """Clica no botão Adicionar Endereço."""
        log_acao(f"{SimbolosASCII.SCROLL} Acessando formulário de endereço")
        self.rolar_ate_texto("ADICIONAR")
        self.clicar_por_id(self.BTN_ADICIONAR_ENDERECO)

    def preencher_endereco(self, dados: dict):
        """
        Preenche dados de endereço do cliente.

        Args:
            dados: Dicionário com dados do cliente (incluindo endereço)
        """
        log_acao(f"{SimbolosASCII.INICIO} Preenchendo endereço")

        self._inserir_campo_e_avancar("Digitar CEP", self.EDT_CEP, dados["cep"], fechar_teclado=False)
        self._inserir_campo_e_avancar("Digitar Rua", self.EDT_RUA, dados["rua"], fechar_teclado=False)
        self._inserir_campo_e_avancar("Digitar Número", self.EDT_NUMERO, dados["numero"], fechar_teclado=False)
        self._inserir_campo_e_avancar("Digitar Cidade", self.EDT_CIDADE, dados["cidade"], fechar_teclado=False)
        self._inserir_campo_e_avancar("Digitar Bairro", self.EDT_BAIRRO, dados["bairro"], fechar_teclado=False)
        self._inserir_campo_e_avancar("Digitar Estado", self.EDT_ESTADO, dados["estado"], fechar_teclado=False)

        # Fecha teclado após preencher todos os campos
        self._fechar_teclado_seguro()
        time.sleep(1)

    def salvar_endereco(self):
        """Salva o endereço cadastrado."""
        log_acao(f"{SimbolosASCII.CLICK} Salvando endereço")
        self.ver_e_clicar_texto("SALVAR")
        time.sleep(2)

    def salvar_cliente(self):
        """Salva o cliente cadastrado."""
        log_acao(f"{SimbolosASCII.CLICK} Salvando cliente")
        self.ver_e_clicar(self.BTN_SALVAR_CLIENTE)

    def cadastrar_cliente_completo(self, tipo_pessoa: str = "PF") -> dict:
        """
        Fluxo completo de cadastro de cliente.

        Args:
            tipo_pessoa: "PF" para Pessoa Física ou "PJ" para Pessoa Jurídica

        Returns:
            Dicionário com os dados do cliente cadastrado
        """
        log_acao(f"{SimbolosASCII.INICIO} Iniciando cadastro de cliente {tipo_pessoa}")

        # Gera dados
        dados_cliente = self.gerar_dados_cliente(tipo_pessoa)

        # Seleciona tipo de pessoa
        self.selecionar_tipo_pessoa(tipo_pessoa)

        # Preenche dados principais
        self.preencher_dados_principais(dados_cliente)

        # Adiciona endereço
        self.adicionar_endereco()

        # Preenche endereço
        self.preencher_endereco(dados_cliente)

        # Salva endereço
        self.salvar_endereco()

        # Salva cliente
        self.salvar_cliente()

        log_acao(f"{SimbolosASCII.FIM} Cadastro de cliente concluído")
        return dados_cliente

    # ========== VALIDACOES ==========

    def validar_mensagem_sucesso(self) -> bool:
        """
        Valida se mensagem de sucesso foi exibida e confirma.

        Returns:
            True se mensagem foi exibida e confirmada, False caso contrário
        """
        try:
            log_acao(f"{SimbolosASCII.VALIDAR} Validando mensagem de sucesso")

            # Aguarda modal de sucesso
            elemento_msg = self.encontrar_clicavel_por_id(self.MD_CONTENT, tempo_espera=10)
            texto_tela = elemento_msg.text

            if self.TXT_SUCESSO not in texto_tela:
                log_tecnico(f"   Mensagem incorreta! Esperado: '{self.TXT_SUCESSO}', Encontrado: '{texto_tela}'", "error")
                return False

            log_tecnico(f"   Mensagem validada: '{texto_tela}'", "info")

            # Clica em OK para fechar modal
            self.clicar_por_texto("OK")

            # Aguarda retorno para tela inicial
            log_tecnico("   Aguardando retorno para tela inicial...", "info")
            self.aguardar_texto(self.TXT_NOVO_CADASTRO, tempo_espera=10)
            log_tecnico("   Retorno confirmado!", "info")

            return True
        except Exception as e:
            log_tecnico(f"   Falha na validação: {e}", "error")
            return False

    def cadastro_concluido_com_sucesso(self) -> bool:
        """
        Verifica se cadastro foi concluído com sucesso.

        Returns:
            True se cadastro foi bem-sucedido, False caso contrário
        """
        return self.validar_mensagem_sucesso()
