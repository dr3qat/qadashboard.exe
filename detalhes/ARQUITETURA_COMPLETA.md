# ARQUITETURA COMPLETA - PDV AUTOMAÇÃO

**Documentação Técnica do Sistema de QA**

---

## 1. PIRÂMIDE ARQUITETURAL

O sistema possui 5 camadas que se conectam de cima para baixo.
Cada camada só depende das camadas abaixo dela, nunca acima.

```
                          +-----------------------+
                          |    QA DASHBOARD GUI   |        CAMADA 1
                          |     app_runner.py     |        (Interface)
                          +-----------+-----------+
                                      |
                      +---------------+---------------+
                      |                               |
              +-------+--------+            +---------+---------+
              | CONFIG MANAGER |            | UI COMPONENTS     |
              | config_mgr.py  |            | ui_components.py  |
              +----------------+            | test_parser.py    |
                                            | log_filter.py     |
                                            +-------------------+
                                      |
                          +-----------+-----------+
                          |    PYTEST ENGINE      |        CAMADA 2
                          |     conftest.py       |        (Orquestrador)
                          |   (Worker Mode EXE)   |
                          +-----------+-----------+
                                      |
          +---------------------------+---------------------------+
          |          |          |          |          |            |
     +----+---+ +---+----+ +--+---+ +----+---+ +---+---+ +------+------+
     | LOGIN  | | VENDA  | | TROCA| | PEDIDO | |CONSULT| |VENDA FUTURA |  CAMADA 3
     | PAGE   | | PAGE   | | PAGE | | PAGE   | |PEDIDO | |    PAGE     |  (Pages)
     +----+---+ +---+----+ +--+---+ +----+---+ +---+---+ +------+-----+
          |          |          |          |          |            |
     +----+---+ +---+----+    |     +----+---+      |     +------+------+
     |ESTOQUE | | BONUS  |    |     | HOME   |      |     | VENDA       |
     | PAGE   | | PAGE   |    |     | PAGE   |      |     | SUCESSO PG  |
     +----+---+ +---+----+    |     +----+---+      |     +------+------+
          |          |         |          |          |            |
          +----------+---------+----------+----------+------------+
                               |                                         |
                    +----------+----------+                              |
                    |     BASE PAGE       |        CAMADA 4              |
                    |    base_page.py     |        (Framework)           |
                    |   (40+ métodos)     |                              |
                    +----------+----------+                              |
                               |                                         |
                    +----------+-----------+                             |
                    |      framework.py    |  <-- Funções legadas -------+
                    | (compatibilidade)    |     (ainda usado por
                    +----------+-----------+      alguns testes)
                               |
          +--------------------+--------------------+
          |                    |                    |
  +-------+-------+   +-------+-------+   +-------+-------+
  |   config.py   |   |  test_data.py |   |  _NO_WINDOW   |   CAMADA 5
  | (dispositivos)|   | (dados teste) |   |  (padrão sub- |   (Configuração)
  | (logger/cores)|   | (prioridades) |   |   processos)  |
  +---------------+   +---------------+   +---------------+
```

---

## 2. DESCRIÇÃO DE CADA ARQUIVO

### CAMADA 1: GUI (Gerador_EXE/runner/)

#### **app_runner.py**
- **Descrição:** Aplicação principal do QA Dashboard (tkinter)
- **Tamanho:** ~1530 linhas
- **Função:** Interface gráfica que permite ao usuário:
  - Selecionar testes via Treeview com pastas e checkboxes (emojis: ⬜/✅ para toggle, 📂 pastas, 🐍 arquivos)
  - Configurar IP/Porta/Credenciais na aba Configurações
  - Configurar caminho manual do Appium (appium_path)
  - Executar testes com botão "RODAR NA ORDEM"
  - Ver logs em tempo real (modo Cliente ou Debug)
  - Acompanhar timer, aprovados/falhas e barra de progresso
  - Iniciar Appium Server automaticamente em background
  - Verificar ambiente (Java, Node, Allure, Appium, ADB)
  - Gerar relatórios Allure (base + arquivo único)
  - Abrir servidor Allure interativo
- **Versionamento:** Lê versão do arquivo VERSION usando `sys._MEIPASS` quando compilado, exibe no título e rodapé
- **Otimizações UI:** Processamento de logs em lotes de 5 linhas para evitar travamentos, filtra linhas muito longas (>500 chars)
- **Modo Debug:** Similar ao normal mas mostra stack traces completos em caso de erro, filtra ruído de bibliotecas
- **Exporta:** TestRunnerApp (classe principal)
- **Importa:** tkinter, subprocess, threading, json, socket, datetime, shutil, webbrowser, glob, time, re, io
- **Forced:** pytest_html, pytest_metadata, appium, urllib3, allure_combine (try/except para PyInstaller)
- **Especial:** Contém bloco WORKER MODE (linhas 10-54) que detecta arg "worker_pytest_runner" e roda pytest internamente. Worker DEVE vir antes dos imports de tkinter.

**INSTÂNCIAS DE PROCESSO:**
- `appium_proc`, `pytest_proc`, `allure_proc` (3 subprocessos gerenciados)

**CONFIG_VARS (18+ campos em settings.json):**
- `server_ip`, `server_port`, `company`, `user`, `password`
- `customer_id`, `customer_id_troca`, `customer_id_bonus`
- `product_code_sale`, `product_code`, `product_code_future_sale`, `product_size_future`
- `product_code_stock_1`, `product_code_stock_2`
- `appium_port`, `appium_path`, `qa_dev_path`, `timeout_default`
- `clean_logs` (BooleanVar), `auto_open` (BooleanVar)
- `use_allure` (BooleanVar), `generate_single_file` (BooleanVar)
- `open_allure_end` (BooleanVar)

**ABA CONFIGURAÇÕES (setup_tab_config):**
- **Seção 1 "Dados do Sistema":** IP, Porta, Empresa, Usuário, Senha, ID Cliente (Vendas), ID Cliente (Trocas), ID Cliente (Bônus), Timeout
- **Seção 2 "Produtos para Testes":** Produto Vendas Normais, Produto Bônus/Cashback, Produto Venda Futura, Tamanho (Venda Futura), Produto Estoque 1, Produto Estoque 2
- **Seção 3 "Infraestrutura e Pastas":** Projeto QA Dev (seletor pasta), Porta Appium, Caminho Appium (seletor arquivo *.cmd/*.exe)
- **Seção 3 "Preferências de Execução":**
  - [x] Limpar logs/prints antigos antes de rodar
  - [x] Abrir relatório padrão automaticamente ao finalizar
- **Seção 4 "Allure"** (3 checkboxes):
  - [x] Gerar Relatório Allure (Base)
  - [x] Gerar Arquivo Único (allure-combine)
  - [x] Abrir Relatório Allure ao final
- **Botões:** Salvar | Verificar Ambiente | Recarregar Testes

**VERIFICAÇÃO DE AMBIENTE (verificar_dependencias_startup):**
- Parâmetro `silent=True` (startup) ou `False` (botão manual)
- Verifica 6 itens: Java, Node, Allure CLI, Allure Combine, Appium, ADB com caminhos completos
- Usa `appium_path` da config, auto-salva quando encontrado
- Salva log em `logs/verificacoes/ambiente_check.txt`
- Popula `faltantes_map` com itens e ações de instalação
- Se faltantes: oferece instalação automática (messagebox.askyesno)
- Se `silent=False` e tudo OK: mostra messagebox "Ambiente OK"
- `executar_instalacao_automatica()`: Executa scripts/winget/pip para cada item em `faltantes_map` (abre janelas CMD)

**TREEVIEW DE TESTES (seleção hierárquica):**
- `atualizar_lista_testes()`: Busca test_*.py recursivamente e monta árvore com pastas (📂) e arquivos (🐍)
- `on_tree_click()`: Toggle ⬜/✅ ao clicar em item
- `_propagar_selecao()`: Marca/desmarca todos os filhos de pasta
- `_recalcular_fila()`: Varre árvore e monta fila_de_execucao
- `atualizar_label_fila()`: Mostra fluxo abreviado

**GESTÃO APPIUM:**
- `_encontrar_appium_path()`: Prioridade: config > PATH > npm > fixo
- `_matar_appium()`: taskkill /F /T com CREATE_NO_WINDOW
- `_iniciar_appium_thread()`: Reinicia se processo já existe
- `selecionar_appium_manual()`: Dialog para *.cmd/*.exe/*.js

**ALLURE REPORTING:**
- `gerar_e_abrir_allure_unico()`: 3 passos:
  1. allure generate (CLI) → allure-report/
  2. combine_allure() (Python) → complete.html (se marcado)
  3. Abre arquivo único ou servidor (se marcado)
- `abrir_servidor_allure()`: Sobe allure serve em porta segura
- `_get_free_port()`: Busca porta livre (5000-5999) excluindo Appium

**LIMPEZA E RELATÓRIO:**
- `_limpar_logs_antigos()`: Esvazia pasta logs/ inteira (shutil). Chamado por `rodar_processo()` se `clean_logs` ativo
- `abrir_relatorio()`: Busca HTML em 3 caminhos, abre no browser. Chamado por `finalizar_execucao()` se `auto_open` ativo
- `fechar_programa()`: Chama `_matar_appium()` + termina `pytest_proc` + mata `allure_proc` (taskkill) antes de destruir a janela

**BOTÕES NA ABA TESTES:**
- "▶ RODAR NA ORDEM": Inicia execução dos testes selecionados
- "📄 Relatório Simples": Abre relatório HTML padrão (pytest-html)
- "📊 Relatório Funcional (Allure)": Gera e abre Allure

---

#### **config_manager.py** (198 linhas)
- **Descrição:** Gerenciador de configurações com persistência em JSON
- **Função:** Dataclass Settings com todos os campos configuráveis. Lê/escreve settings.json, suporta update parcial e reset.

**SETTINGS (14 campos no dataclass):**
- `appium_host` ("127.0.0.1"), `appium_port` (4723)
- `server_ip`, `server_port`, `company`, `user`, `password`
- `customer_id` ("1"), `product_code` ("123")
- `timeout_default` (30), `timeout_short` (5)
- `modo_debug` (False), `qa_dev_path` (""), `last_report_path` ("")

**MÉTODOS ConfigManager:**
- `load()`: Carrega settings.json ou cria com defaults
- `save()`: Salva Settings no arquivo JSON
- `update(**kwargs)`: Atualiza campos específicos
- `reset_to_defaults()`: Reseta para valores padrão
- `get_display_dict()`: Dict formatado para UI (mascara senha)

- **Exporta:** ConfigManager, Settings, get_config_manager(), get_settings
- **Importa:** json, os, dataclasses (dataclass, field, asdict), pathlib, typing

---

#### **ui_components.py**
- **Descrição:** Widgets reutilizáveis para o dashboard
- **Função:** Componentes visuais independentes:
  - **Cronômetro:** Timer MM:SS ou HH:MM:SS em tempo real
  - **Scoreboard:** Aprovados/Falhas/Pulados + Taxa de sucesso
  - **ProgressoIndeterminado:** Barra animada
  - **StatusBar:** Barra inferior com status Appium + versão
- **Exporta:** Cronometro, Scoreboard, ProgressoIndeterminado, StatusBar
- **Importa:** tkinter

---

#### **test_parser.py**
- **Descrição:** Parser de output do pytest em tempo real
- **Função:** Lê linhas stdout do pytest e extrai:
  - Resultados individuais (PASSED/FAILED/SKIPPED/ERROR)
  - Contagem total (linha de resumo "X passed, Y failed")
  - Mensagens de erro (stack traces)
  - Sistema de callbacks: `on_test_start`, `on_test_end`, `on_session_start`, `on_session_end`, `on_progress`
- **Exporta:** PytestOutputParser, TestResult, TestSession, TestStatus, create_scoreboard_updater()
- **Importa:** re, enum, dataclasses

---

#### **log_filter.py**
- **Descrição:** Filtro inteligente de logs para a GUI
- **Função:** Dois modos:
  - **CLIENT:** Filtra logs HTTP/Appium/Selenium verbosos
  - **DEBUG:** Mostra absolutamente tudo
  - Padrões "importantes" nunca são filtrados (PASSED/FAILED, [SYSTEM], nomes de testes, etc.)
- **Exporta:** LogFilter, LogMode, LogLevel, TestResultDetector, get_log_filter(), set_log_mode()
- **Importa:** re, enum

---

#### **__init__.py**
- **Descrição:** Package init do runner (25 linhas)
- **Função:** Exporta todos os componentes do runner via `__all__`: ConfigManager, Settings, get_settings, get_config_manager, LogFilter, LogMode, LogLevel, PytestOutputParser, TestStatus, TestResult, TestSession, Cronometro, Scoreboard, ProgressoIndeterminado, StatusBar
- **Importa:** .config_manager, .log_filter, .test_parser, .ui_components

---

### CAMADA 2: PYTEST ENGINE (Testes_PDV/)

#### **conftest.py**
- **Descrição:** Configuração central do pytest + fixtures compartilhadas
- **Tamanho:** ~450 linhas
- **Função:**
  1. **ORDEM_TESTES:** Lista que define sequência de execução
  2. **pytest_collection_modifyitems:** Hook que ordena testes
  3. **pytest_runtest_makereport:** Hook que captura screenshots e page source em falhas (integrado com Allure)
  4. **Fixtures:**
     - `driver`: Cria/destrói driver Appium (scope=function)
     - `driver_logado`: driver + login automático
     - `pagina_login`: instância LoginPage
     - `pagina_inicial`: instância HomePage
  5. **Opções CLI:** --device-id, --appium-port
  6. **Configuração Allure** (environment.properties, categories)
  7. **Funções auxiliares ADB** para coleta de info do device:
     - `_executar_adb_getprop()`: Executa getprop e retorna
     - `_obter_resolucao_tela()`: Obtém via 'wm size'
     - `_obter_densidade_tela()`: Obtém DPI via 'wm density'
     - `_obter_ram_total()`: Obtém RAM via /proc/meminfo
     - `_obter_info_device_adb()`: Coleta todas as infos
  8. **_criar_ambiente_allure():** Gera environment.properties com seções organizadas:
     - # === SISTEMA === (SO, Python, Servidor Appium)
     - # === EXECUÇÃO === (Data, Ambiente, GitHub CI info)
     - # === APLICATIVO === (App Package)
     - # === DISPOSITIVO === (ID, Modelo, Fabricante, Brand, Android, API Level, Security Patch, Build ID)
     - # === HARDWARE === (CPU, Resolução, DPI, RAM, Serial)
- **Exporta:** Fixtures (driver, driver_logado, pagina_login, pagina_inicial)
- **Importa:** config (APPIUM_SERVER_URL, get_appium_options, etc.), pages.login_page, pages.home_page, test_data

---

### CAMADA 3: PAGE OBJECTS (Testes_PDV/pages/)

#### **login_page.py** (90 linhas)
- **Descrição:** Automação da tela de login do app BShopPDV
- **Herda:** BasePage
- **Função:**
  - `pular_telas_introducao()`: Pula walkthrough inicial
  - `configurar_conexao_se_necessario(ip, porta)`: Config rede
  - `preencher_credenciais(empresa, usuario, senha)`: Login
  - `clicar_entrar()`: Clica no botão Entrar
  - `garantir_login()`: Detecta se já logado, senão faz login
  - `esta_logado()`: Verifica "Iniciar Venda" ou "Venda"
- **Locators:** BTN_ENTRAR, EDT_EMPRESA, EDT_USUARIO, EDT_SENHA, etc.

---

#### **home_page.py** (118 linhas)
- **Descrição:** Automação da tela inicial (pós-login)
- **Herda:** BasePage
- **Função:**
  - `iniciar_venda()`: Tenta "Iniciar Venda" ou "Venda"
  - `iniciar_troca()`: Navega para troca/devolução
  - `selecionar_vendedor()`: Dialog ou tela full-screen
  - `tela_inicial_exibida()`: Validação de estado
- **Nota:** Adaptado para múltiplas versões do app (L400/Stone/Play)

---

#### **venda_page.py** (163 linhas)
- **Descrição:** Automação do fluxo de venda
- **Herda:** BasePage
- **Função:**
  - `clicar_buscar_cliente()`, `iniciar_venda_sem_cliente()`
  - `selecionar_cliente()`, `adicionar_produto()`
  - `clicar_avancar()`, `selecionar_pagamento_dinheiro()`
  - `tratar_popup_bonus()`: Fecha popup bônus se aparecer
  - `finalizar_venda()`, `responder_impressao()`, `concluir_venda()`
  - `executar_venda_cliente()`, `executar_venda_consumidor()`
  - `venda_sucesso_exibida()`, `validar_sucesso_e_concluir()`
- **Locators:** BTN_BUSCAR_CLIENTE, EDT_BUSCA_PRODUTO, BTN_FINALIZAR, etc.

---

#### **troca_page.py** (204 linhas)
- **Descrição:** Automação do fluxo de troca/devolução
- **Herda:** BasePage
- **Função:**
  - `executar_troca()`: Troca para cliente (sem venda pós)
  - `executar_troca_consumidor()`: Troca + venda com bônus
  - `definir_data_inicial()`, `clicar_consultar()`
  - `selecionar_primeira_nota()`, `selecionar_cliente()`
  - `marcar_item_para_devolucao()`, `clicar_devolver_itens()`
  - `confirmar_dialogos()`, `adicionar_produto()`
  - `clicar_avancar()`, `selecionar_pagamento_bonus()`
  - `tratar_popup_bonus()`, `finalizar_venda()`
  - `responder_impressao_nao()`, `concluir_venda()`
  - `sucesso_exibido()`, `validar_e_fechar_sucesso()`
  - `venda_sucesso_exibida()`, `validar_venda_e_concluir()`
- **Depende:** test_data (CUSTOMER_ID para troca consumidor)

---

#### **pedido_page.py** (152 linhas)
- **Descrição:** Automação do fluxo de pedido de venda
- **Herda:** BasePage
- **Função:**
  - `executar_pedido_venda_consumidor()`: Pedido sem cliente
  - `executar_pedido_venda_cliente()`: Pedido com cliente
  - `executar_pedido_venda()`: Fluxo genérico
  - `selecionar_vendedor()`, `clicar_buscar_cliente()`
  - `iniciar_como_consumidor()`, `selecionar_cliente()`
  - `adicionar_produto()`, `clicar_avancar()`
  - `selecionar_pagamento_dinheiro()`, `tratar_popup_bonus()`
  - `finalizar_pedido()`, `confirmar_pedido_gerado()`
  - `pedido_sucesso_exibido()`

---

#### **consulta_pedido_page.py** (194 linhas)
- **Descrição:** Automação da consulta e finalização de pedidos
- **Herda:** BasePage
- **Função:**
  - `configurar_buscar_todos_pedidos()`: Habilita flag config (abrir_menu_lateral → acessar_configuracoes → garantir_flag_buscar_todos_pedidos → voltar_para_home)
  - `executar_consulta_e_finalizar_pedido()`: Fluxo completo
  - `acessar_consulta_pedido()`: Menu "Cons. Pedido"
  - `selecionar_primeiro_pedido()`: Clica no 1º da lista
  - `clicar_finalizar_pedido()`, `tratar_popup_bonus()`
  - `finalizar_venda()`, `responder_impressao()`, `concluir_venda()`
  - `venda_sucesso_exibida()`, `validar_sucesso_e_concluir()`

---

#### **estoque_page.py** (235 linhas)
- **Descrição:** Automação da consulta de estoque
- **Herda:** BasePage
- **Função:**
  - `acessar_estoque()`: Navega ao menu de estoque
  - `buscar_produto_por_codigo()`/`por_nome()`: Busca com filtro
  - `garantir_filtro()`: Alterna entre "Código" e "Descrição"
  - `clicar_pesquisar()`: Clica botão de busca
  - `obter_detalhes_completos()`: Extrai nome/marca/cor/etc.
  - `obter_quantidade_estoque()`, `obter_nome_produto()`
  - `obter_preco_produto()`, `obter_lista_produtos()`
  - `produto_encontrado()`, `mensagem_nao_encontrado_exibida()`
  - `executar_consulta_estoque()`: Busca + extrai tudo
- **Locators:** EDT_BUSCA_PRODUTO, TXT_NOME_PRODUTO, XPATH_PRECO_VALOR

---

#### **venda_futura_page.py** (204 linhas)
- **Descrição:** Automação do fluxo de venda futura
- **Herda:** BasePage
- **Função:**
  - `executar_venda_futura()`: Retirada em loja
  - `executar_venda_futura_domicilio()`: Entrega em domicílio
  - `clicar_venda_futura()`: Acessa menu Venda Futura
  - `selecionar_retirada_loja()`/`entrega_domicilio()`
  - `avancar_tipo_entrega()`, `selecionar_vendedor()`
  - `buscar_cliente_cpf()`: Busca por CPF
  - `adicionar_produto(codigo, tamanho)`: Com seleção tamanho
  - `clicar_avancar()`, `selecionar_pagamento_avista()`
  - `tratar_popup_bonus()`, `selecionar_forma_dinheiro()`
  - `finalizar_venda()`, `responder_impressao()`, `concluir_venda()`
  - `venda_sucesso_exibida()`, `validar_sucesso_e_concluir()`

---

#### **bonus_page.py** (210 linhas)
- **Descrição:** Automação de bônus/cashback durante pagamento
- **Herda:** BasePage
- **Função:**
  - `bonus_disponivel()`: Verifica se switch existe
  - `obter_valor_bonus()`: Lê texto do valor máximo
  - `bonus_ativado()`: Verifica estado do switch
  - `ativar_bonus()`: Liga o switch se desligado
  - `obter_valor_final()`, `obter_desconto_bonus()`
  - `bonus_foi_aplicado()`: Verifica se valor final = R$ 0,00
  - `buscar_cliente_por_cpf()`: Busca cliente com bônus
  - `iniciar_venda_com_cliente()`: Inicia venda com cliente
  - `adicionar_produto()`, `clicar_avancar_carrinho()`
  - `clicar_avancar_pagamento()`: Avança + scroll até Finalizar
  - `tela_pagamento_exibida()`, `venda_sucesso_exibida()`
  - `responder_impressao()`, `concluir_venda()`
- **Locators:** SWITCH_BONUS, TXT_MAX_BONUS, TXT_FINAL_AMOUNT

---

#### **venda_sucesso_page.py** (166 linhas)
- **Descrição:** Automação da tela de sucesso da venda e controle de impressões
- **Herda:** BasePage
- **Função:**
  - `imprimir_nfce()`: Imprime NFC-E (Nota Fiscal do Consumidor Eletrônica)
  - `imprimir_danfe()`: Imprime DANFE via servidor (Documento Auxiliar NF-e)
  - `imprimir_cupom_troca()`: Imprime cupom de troca (botão na tela)
  - `processar_todas_impressoes()`: Processa TODAS as impressões na ordem XML
  - `concluir_venda()`: Clica no botão confirmar venda
  - `tela_sucesso_exibida()`: Verifica se a tela de sucesso está exibida
  - `botao_nfce_disponivel()`, `botao_danfe_disponivel()`, `botao_cupom_troca_disponivel()`
- **Locators:** BTN_CONFIRMAR_VENDA, BTN_IMPRESSAO_NFCE, BTN_NFE_PRINT, BTN_PRINT_CUPOM_TROCA
- **Nota:** Gerencia impressões opcionais conforme configuração do Dashboard (PRINT_NFCE, PRINT_DANFE, PRINT_CUPOM_TROCA)

---

### CAMADA 4: FRAMEWORK (Testes_PDV/)

#### **base_page.py**
- **Descrição:** Classe base para todos os Page Objects (~576 linhas)
- **Função:** Fornece 35 métodos reutilizáveis:

**ENCONTRAR:**
- `encontrar_por_id()`, `encontrar_clicavel_por_id()`
- `encontrar_por_texto()`, `encontrar_por_xpath()`
- `encontrar_por_accessibility_id()`
- `encontrar_todos_por_id()`, `encontrar_todos_por_uiautomator()`
- `encontrar_todos_por_classe()`

**CLICAR:**
- `clicar_por_id()` (com retry), `clicar_por_texto()`
- `clicar_se_existir()`, `clicar_texto_se_existir()`
- `clicar_no_primeiro_da_lista_por_id()`

**DIGITAR:**
- `digitar_por_id()`, `digitar_por_xpath()`

**TECLADO:**
- `fechar_teclado()` (3 estratégias), `_teclado_visivel()`
- `pressionar_pesquisar()`

**SCROLL:**
- `realizar_scroll_para_baixo()`
- `realizar_scroll_ignorando_teclado()`
- `scroll_nativo_ate_id()`, `scroll_nativo_ate_texto()`
- `rolar_ate_texto()`, `rolar_ate_texto_ignorando_teclado()`
- `rolar_ate_id()`

**NAVEGAÇÃO:**
- `voltar_tela()` (com confirmação opcional)
- `_confirmar_dialogo_sair()`

**VALIDAÇÃO:**
- `texto_exibido()`, `aguardar_texto()`, `elemento_existe()`
- `_elemento_realmente_visivel()` (verifica displayed, enabled, tamanho > 0, dentro da área visível)

**HELPERS:**
- `_id_completo()` (monta package:id/xxx)
- `_capturar_tela_atual()` (page_source para comparação)
- `app_package` (property - obtém do driver capabilities)

- **Importa:** config (DEFAULT_WAIT, logger, LogStyle, Cores, _NO_WINDOW)

---

#### **framework.py**
- **Descrição:** Funções utilitárias legadas (pré-Page Object pattern)
- **Função:** Funções procedurais que eram usadas antes da refatoração:
  - `find_clickable_by_id()`, `find_element_by_text()`
  - `clicar_por_id()`, `clicar_por_texto()`
  - `digitar_texto_por_id()`, `digitar_texto_por_xpath()`
  - `realizar_scroll_para_baixo()`, `scroll_ate_encontrar_texto()`
  - `fechar_teclado_back()`, `selecionar_cliente()`
  - `garantir_login()`, `realizar_login_completo()`
  - `save_screenshot()`, `write_report()`, `executar_passo()`
  - `clicar_no_primeiro_da_lista_por_id()`
  - `garantir_switch_ativo_por_texto()`
- **Importa:** config.* (wildcard import)
- **Nota:** Mantido para compatibilidade. Funções similares existem na BasePage mas de forma orientada a objetos.

---

### CAMADA 5: CONFIGURAÇÃO (Testes_PDV/)

#### **config.py**
- **Descrição:** Configuração central do projeto (~340 linhas)
- **Função:** Define TUDO que o framework precisa para funcionar:

**_NO_WINDOW:**
- Dict com STARTUPINFO + CREATE_NO_WINDOW para Windows
- Usado em TODOS os subprocess calls (adb, etc.)
- Evita que janelas CMD apareçam durante execução

**CORES/LOG:**
- Classes Cores e LogStyle com cores ANSI e emojis
- Logger "appium_test" configurado com handler de arquivo

**DEVICES:**
- `get_connected_device_udid()`: Detecta device via adb
- `get_all_connected_devices()`: Lista todos os devices
- `discover_target_app()`: Detecta app instalado no device
- **APP_TARGETS:** Dicionário com 6 flavors do app (REDEL400, CieloDX800, Stone, Playstore, Pagseguro, N960K). Cada flavor com versões QA e PROD

**APPIUM:**
- `APPIUM_SERVER_URL = "http://127.0.0.1:4723"`
- `get_appium_options()`: Cria UiAutomator2Options
- `_calcular_porta_unica()`: SystemPort por device (hash)
- `DEFAULT_WAIT = 30`, `RETRY_ATTEMPTS = 2`

- **Exporta:** _NO_WINDOW, logger, Cores, LogStyle, DEVICE_NAME, APP_PACKAGE, APP_ACTIVITY, APPIUM_SERVER_URL, DEFAULT_WAIT, get_appium_options, SCREENSHOTS_DIR, REPORTS_DIR, etc.

---

#### **test_data.py** (~165 linhas)
- **Descrição:** Dados de teste externalizados com 3 níveis de prioridade
- **Função:** Fornece valores de configuração na ordem:
  1. Variáveis de ambiente (TEST_SERVER_IP, TEST_USER, etc.)
  2. settings.json (se existir no diretório)
  3. Valores padrão hardcoded

**DADOS (chave settings.json → atributo Python):**
- `server_ip` → `SERVER_IP` (padrão: "***SERVER_IP***")
- `server_port` → `SERVER_PORT` (padrão: "***SERVER_PORT***")
- `company` → `COMPANY` (padrão: "382")
- `user` → `USER` (padrão: "SERVER")
- `password` → `PASSWORD` (padrão: "***PASSWORD***")
- `customer_id` → `CUSTOMER_ID` (padrão: "1" local / "3" CI)
- `customer_id_troca` → `CUSTOMER_ID_TROCA` (padrão: igual CUSTOMER_ID)
- `customer_id_bonus` → `CUSTOMER_ID_BONUS` (padrão: igual CUSTOMER_ID) — usado em test_bonus, test_validar_bonus, test_validar_cashback
- `product_code` → `PRODUCT_CODE` (padrão: "123") — usado em test_bonus, test_estoque, test_opcoes_item
- `product_code_sale` → `PRODUCT_CODE_SALE` (padrão: "123") — usado em vendas normais e pedidos
- `product_code_future_sale` → `PRODUCT_CODE_FUTURE_SALE` (padrão: "1234")
- `product_size_future` → `PRODUCT_SIZE_FUTURE` (padrão: "38")
- `product_code_stock_1` → `PRODUCT_CODE_STOCK_1` (padrão: "123")
- `product_code_stock_2` → `PRODUCT_CODE_STOCK_2` (padrão: "1234")
- `timeout_default` → `DEFAULT_TIMEOUT` (padrão: 30)
- `timeout_short` → `SHORT_TIMEOUT` (padrão: 5)
- `print_cupom_venda` → `PRINT_CUPOM_VENDA` (padrão: False)
- `print_nfce` → `PRINT_NFCE` (padrão: False)
- `print_danfe` → `PRINT_DANFE` (padrão: False)
- `print_cupom_troca` → `PRINT_CUPOM_TROCA` (padrão: False)
- `print_dialog_timeout` → `PRINT_DIALOG_TIMEOUT` (padrão: 20)

**MÉTODOS:**
- `reload()`: Recarrega configurações do settings.json (classmethod que atualiza todos os campos em runtime)

**HELPERS:**
- `_load_settings()`: Busca settings.json em: CWD, diretório pai, diretório do arquivo, diretório do EXE (quando frozen)
- `_get_config()`: Resolve prioridade env var > settings.json > default

- **Exporta:** test_data (instância global de TestData)
- **Importa:** os, json, pathlib, typing
- **Nota:** Detecta CI/CD (GITHUB_ACTIONS) para ajustar customer_id. O settings.json gerado pelo Dashboard deve conter TODOS os campos acima para funcionar corretamente.

---

### BUILD PIPELINE (Gerador_EXE/build/)

#### **builder_pro.py**
- **Descrição:** Pipeline completo de compilação do QA Dashboard
- **Tamanho:** ~528 linhas
- **Função:** Automatiza todo o processo de build:
  1. `clean()`: Limpa builds anteriores
  2. `stage_runner()`: Copia runner/*.py + assets + scripts
  3. `stage_qa_dev()`: Copia artefatos do Testes_PDV
  4. `verify_build_environment()`: Verifica pacotes críticos
  5. `compile_pyinstaller()`: Compila EXE (--onefile --noconsole)
  6. `create_installer_iss()`: Gera script Inno Setup
  7. `build_installer()`: Compila instalador .exe (Busca Inno Setup em todos os drives C-Z)
- **Exporta:** BuilderPro
- **CLI:** `python builder_pro.py --qa-dev E:\Testes_PDV`

---

#### **whitelist.json**
- **Descrição:** Lista de arquivos a incluir no build
- **Função:** Define:
  - **core_files:** config.py, conftest.py, framework.py, etc.
  - **directories:** pages/*.py, tests/e2e/test_*.py, tests/smoke/test_*.py (required: false)
  - **exclude_patterns:** __pycache__, *.pyc, .git, .env, tests/unit/* (unit tests NÃO são incluídos no build)
  - **runner_files:** lista dos 5 arquivos do runner
  - **assets:** icon.ico
  - **templates:** settings.default.json

---

## 3. FLUXO DE EXECUÇÃO COMPLETO

Desde o usuário clicar "RODAR" até o resultado aparecer:

### PASSO 1: USUÁRIO CLICA "RODAR NA ORDEM"
```
app_runner.py -> iniciar_testes()
- Verifica se fila_de_execucao não está vazia
- Desabilita botão (state=DISABLED, texto="EXECUTANDO...")
- Limpa área de log
- Reseta dashboard (timer, contadores, progress bar)
- Inicia thread daemon: rodar_processo(test_files)
```

### PASSO 1.5: LIMPAR LOGS (OPCIONAL)
```
rodar_processo() verifica clean_logs:
  Se ativo: _limpar_logs_antigos() esvazia pasta logs/ inteira
  (deleta arquivos e subdiretórios via shutil.rmtree)
```

### PASSO 2: VERIFICAR APPIUM
```
rodar_processo() -> aguardar_appium(timeout=45)
- Tenta conexão TCP em 127.0.0.1:{porta} a cada 1 segundo
- Se não responder em 45s: ABORTA execução
- Se responder: continua
```

### PASSO 3: MONTAR COMANDO PYTEST
```
rodar_processo() monta o comando:

Se EXE (frozen=True):
  QA_Dashboard.exe worker_pytest_runner test_file1.py test_file2...

Se script Python:
  python app_runner.py worker_pytest_runner test_file1.py ...

Argumentos extras:
  -v -s                           (verbose, no capture)
  -o log_cli=true                 (logs no console)
  -o log_cli_level=INFO
  -o log_file=logs/execucao.log   (log em arquivo)
  --html=logs/reports/relatorio.html  (relatório HTML)
  --self-contained-html
  --alluredir=logs/allure-results     (SE use_allure ativo)

Variáveis de ambiente injetadas (credenciais de conexão):
  PYTHONPATH, TEST_SERVER_IP, TEST_SERVER_PORT,
  TEST_COMPANY, TEST_USER, TEST_PASSWORD

NOTA: Demais valores (customer_id, product_code_sale, etc.) NÃO
são injetados como env vars — os testes os leem diretamente do
settings.json via test_data.py (_load_settings).

Subprocess com CREATE_NO_WINDOW + STARTUPINFO
```

### PASSO 4: WORKER MODE ATIVA
```
O EXE (ou script) re-executa a si mesmo com arg "worker_pytest_runner"

app_runner.py linhas 10-35:
  - Detecta sys.argv[1] == "worker_pytest_runner"
  - Corrige sys.stdout se None (--noconsole)
  - import pytest
  - sys.exit(pytest.main(pytest_args))
  - NUNCA chega nos imports de tkinter
```

### PASSO 5: PYTEST EXECUTA
```
pytest.main() carrega conftest.py:
  1. pytest_addoption: registra --device-id e --appium-port
  2. pytest_configure: cria diretórios, Allure environment
  3. pytest_collection_modifyitems: ORDENA testes pela ORDEM_TESTES
  4. Para cada teste na ordem:
     a. Fixture "driver" cria sessão Appium (webdriver.Remote)
     b. Fixture "driver_logado" faz login se necessário
     c. Teste executa (usa Page Objects)
     d. Se FALHOU: pytest_runtest_makereport captura screenshot
     e. Fixture encerra driver (driver.quit())
```

### PASSO 6: OUTPUT EM TEMPO REAL
```
rodar_processo() lê stdout do subprocess linha a linha:
  for line in self.pytest_proc.stdout:
      self.root.after(0, self.processar_linha_log, line)

processar_linha_log():
  - Remove códigos ANSI (cores)
  - Detecta "PASSED" -> incrementa pass_count
  - Detecta "FAILED" -> incrementa fail_count
  - Detecta resumo final ("X passed, Y failed")
  - Aplica filtro: modo Cliente mostra só ações/resultados
                    modo Debug mostra tudo
  - Atualiza labels do dashboard (aprovados, falhas)
  - Escreve na log_area com cores (tags tkinter)
```

### PASSO 7: FINALIZAÇÃO
```
finalizar_execucao():
  - Para cronômetro e progress bar
  - Reabilita botão "RODAR NA ORDEM"
  - Se auto_open ativo E use_allure NÃO ativo:
    abrir_relatorio() abre HTML padrão no browser
  - Se use_allure ativo:
    Dispara gerar_e_abrir_allure_unico() em thread daemon
  - Avalia exit_code:
    * código != 0 e != 1: ERRO CRÍTICO (messagebox.showerror)
    * fail_count > 0: FALHOU (messagebox.showwarning)
    * pass_count > 0: SUCESSO TOTAL (messagebox.showinfo)
    * else: Nenhum teste rodou (messagebox.showwarning)
```

### PASSO 8: ALLURE REPORT (SE use_allure ATIVO)
```
gerar_e_abrir_allure_unico() (roda em thread separada):

8.1 GERAR BASE:
  allure generate logs/allure-results -o logs/allure-report
  (via subprocess com CREATE_NO_WINDOW)

8.2 GERAR ARQUIVO ÚNICO (se generate_single_file ativo):
  from allure_combine import combine_allure
  combine_allure(allure_report_dir)
  -> Gera complete.html dentro de logs/allure-report/
  -> Copia para logs/reports/Allure_Completo_YYYYMMDD_HHMMSS.html

8.3 ABRIR (se open_allure_end ativo):
  Prioridade: Arquivo único (webbrowser.open) >
              Servidor Allure (allure serve em porta segura)
```

---

## 4. TESTES - DETALHES E ORDEM DE EXECUÇÃO

A ordem de execução é definida em conftest.py (ORDEM_TESTES).
Testes que dependem de dados de testes anteriores DEVEM rodar na sequência.

**NOTA:** ORDEM_TESTES no conftest.py ainda referencia nomes antigos para login: "test_login_sucesso" e "test_login_falha_senha_invalida". Os nomes reais das funções são `test_garantir_login` e `test_verificar_sessao_ativa`. Como não batem, os testes de login NÃO são ordenados pelo hook e rodam por último junto com os testes não listados.

### Ordem de Execução

| ORDEM | ARQUIVO | TESTE | FIXTURE |
|-------|---------|-------|---------|
| 1 | test_venda_consumidor.py | test_venda_consumidor_sucesso | driver_logado |
| 2 | test_troca_consumidor.py | test_troca_consumidor_sucesso | driver_logado |
| 3 | test_venda_cliente.py | test_venda_cliente_sucesso | driver_logado |
| 4 | test_troca_cliente.py | test_troca_cliente_sucesso | driver_logado |
| 5 | test_pedido_vendaConsumidor.py | test_pedido_venda_consumidor_sucesso | driver_logado |
| 6 | test_consulta_pedidoConsumidor.py | test_consulta_pedido_consumidor_sucesso | driver_logado |
| 7 | test_pedido_vendaCliente.py | test_pedido_venda_cliente_sucesso | driver_logado |
| 8 | test_consulta_pedidoCliente.py | test_consulta_pedido_cliente_sucesso | driver_logado |
| 9 | test_venda_futura.py | test_venda_futura_sucesso | driver_logado |
| 10 | test_venda_futura.py | test_venda_futura_domicilio_sucesso | driver_logado |
| -- | (testes não listados rodam por último, na ordem original) |

**NOTA:** test_venda_futura.py agora contém AMBOS os testes de venda futura (retirada loja + domicílio). O arquivo test_venda_futura_domicilio.py também existe como arquivo separado com test_venda_futura_domicilio_sucesso (duplicado - pytest coleta ambos).

---

### DESCRIÇÃO DETALHADA DE CADA TESTE

#### 1. test_garantir_login (test_login.py)
- **Severity:** BLOCKER
- **Fixture:** driver
- **O que faz:** Garante que app está configurado e faz login com credenciais válidas (garantir_login). Valida que consegue acessar a tela inicial.
- **Page Objects:** LoginPage, HomePage
- **Dependência:** Nenhuma
- **NOTA:** Função renomeada (era test_login_sucesso). ORDEM_TESTES ainda referencia nome antigo.

#### 2. test_verificar_sessao_ativa (test_login.py)
- **Severity:** NORMAL
- **Fixture:** driver
- **O que faz:** Faz login via garantir_login e verifica que sessão está ativa. Se tela inicial exibida: sucesso. Senão: falha.
- **Page Objects:** LoginPage, HomePage
- **Dependência:** Nenhuma
- **NOTA:** Função renomeada (era test_login_falha_senha_invalida). ORDEM_TESTES ainda referencia nome antigo.

#### 3. test_venda_consumidor_sucesso
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Executa venda para consumidor (sem cadastro). Passos: Iniciar Venda → Selecionar Vendedor → Pular cliente → Adicionar produto → Pagamento DINHEIRO → Finalizar → Responde impressões conforme configuração.
- **Valida:** Retorno à tela inicial.
- **Page Objects:** HomePage, VendaPage, VendaSucessoPage
- **Dependência:** Login ativo

#### 4. test_troca_consumidor_sucesso
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Executa troca de venda anterior (consumidor). Passos: Realizar Troca → Vendedor → Definir data → Consultar → Selecionar nota → Selecionar cliente → Marcar item → Devolver → Confirmar → Venda pós-troca: Adicionar produto → Pagamento BONUS → Finalizar.
- **Valida:** Sucesso da troca + Sucesso da venda.
- **Page Objects:** HomePage, TrocaPage
- **Dependência:** REQUER venda consumidor IMEDIATAMENTE antes (teste 3)

#### 5. test_venda_cliente_sucesso
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Executa venda para cliente cadastrado. Passos: Iniciar Venda → Vendedor → Buscar Cliente (ID 1) → Adicionar produto → Pagamento DINHEIRO → Finalizar → Responde impressões conforme configuração.
- **Valida:** Retorno à tela inicial.
- **Page Objects:** HomePage, VendaPage, VendaSucessoPage
- **Dependência:** Login ativo

#### 6. test_troca_cliente_sucesso
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Executa troca de venda anterior (cliente). Passos: Realizar Troca → Vendedor → Definir data → Consultar → Selecionar nota → Marcar item → Devolver → Confirmar diálogos.
- **Valida:** Sucesso da troca (exibe "Sucesso!").
- **Page Objects:** HomePage, TrocaPage
- **Dependência:** REQUER venda cliente IMEDIATAMENTE antes (teste 5)

#### 7. test_pedido_venda_consumidor_sucesso (test_pedido_vendaConsumidor.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Cria pedido de venda sem cliente. Passos: Pedido Venda → Vendedor → Iniciar sem cliente → Adicionar produto → Pagamento DINHEIRO → Finalizar pedido.
- **Valida:** "Pedido gerado com sucesso!"
- **Page Objects:** HomePage, PedidoPage
- **Dependência:** Login ativo

#### 8. test_consulta_pedido_consumidor_sucesso (test_consulta_pedidoConsumidor.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Consulta e finaliza pedido anterior (consumidor). Passos: Configurar "Buscar todos os pedidos" → Cons. Pedido → Selecionar primeiro pedido → Finalizar Pedido → Finalizar venda.
- **Valida:** "Venda realizada com sucesso!"
- **Page Objects:** HomePage, ConsultaPedidoPage
- **Dependência:** REQUER pedido consumidor antes (teste 7)

#### 9. test_pedido_venda_cliente_sucesso (test_pedido_vendaCliente.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Cria pedido de venda para cliente cadastrado. Passos: Pedido Venda → Vendedor → Buscar Cliente → Adicionar produto → Pagamento DINHEIRO → Finalizar pedido.
- **Valida:** "Pedido gerado com sucesso!"
- **Page Objects:** HomePage, PedidoPage
- **Dependência:** Login ativo

#### 10. test_consulta_pedido_cliente_sucesso (test_consulta_pedidoCliente.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Consulta e finaliza pedido anterior (cliente). Passos: Cons. Pedido → Selecionar primeiro pedido → Finalizar Pedido → Finalizar venda.
- **Valida:** "Venda realizada com sucesso!"
- **Page Objects:** HomePage, ConsultaPedidoPage
- **Dependência:** REQUER pedido cliente antes (teste 9)

#### 11. test_venda_futura_sucesso (test_venda_futura.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Venda futura com retirada em loja. Passos: Venda Futura → Retirada Loja → executar_venda_futura(cpf, produto, tamanho) → Validar sucesso → Verificar retorno à tela inicial.
- **Valida:** "Venda realizada com sucesso!"
- **Page Objects:** HomePage, VendaFuturaPage
- **Dependência:** Login ativo

#### 12. test_venda_futura_domicilio_sucesso (test_venda_futura.py)
- **Severity:** CRITICAL
- **Fixture:** driver_logado
- **O que faz:** Venda futura com entrega em domicílio. Passos: Venda Futura → executar_venda_futura_domicilio(cpf, produto, tamanho) → Validar sucesso → Verificar retorno à tela inicial.
- **Valida:** "Venda realizada com sucesso!"
- **Page Objects:** HomePage, VendaFuturaPage
- **Dependência:** Login ativo
- **NOTA:** Este teste também existe em test_venda_futura_domicilio.py (70 linhas) como arquivo separado com implementação diferente (passos mais detalhados/granulares).

---

### TESTES SMOKE (tests/smoke/test_smoke_e2e.py - 308 linhas, 5 testes)

Gate de sanidade que valida o ambiente ANTES de rodar a suite E2E completa.

#### TestSmokeAmbiente (3 testes):
- **test_01_app_abre_corretamente** (BLOCKER) - Verifica se app abre sem crash
- **test_02_login_funciona** (BLOCKER) - Verifica login básico funciona
- **test_03_elementos_basicos_visiveis** (CRITICAL) - Botão "Venda" visível na home

#### TestSmokeNavegacao (1 teste):
- **test_04_consegue_iniciar_venda** (CRITICAL) - Navega para tela de venda

#### TestSmokeFinal (1 teste):
- **test_99_smoke_completo** (BLOCKER) - Gate final: resume status do smoke e libera execução E2E

---

### TESTES NÃO ORDENADOS (rodam por último)

#### test_estoque.py (4 testes)
- **test_consultar_estoque_produto** (NORMAL) - Busca por código, valida encontrado
- **test_consultar_estoque_produto_inexistente** (NORMAL) - Busca inexistente, valida erro
- **test_consultar_lista_produtos** (MINOR) - Busca por nome, valida lista
- **test_consultar_estoque_validar_informacoes** (NORMAL) - Valida detalhes completos (nome, marca, cor, material, preço)

#### test_bonus.py (2 testes)
- **test_verificar_bonus_disponivel** (NORMAL) - Verifica se bônus aparece na tela
- **test_venda_com_bonus** (CRITICAL) - Venda usando bônus (R$ 0,00)
- **Dependência:** Cliente deve ter bônus de troca anterior

#### test_cancelamento.py (6 testes)
- **test_cancelar_venda_vazia** (NORMAL) - Cancela venda sem produtos
- **test_cancelar_venda_com_itens** (CRITICAL) - Cancela venda com produtos
- **test_desistir_cancelamento** (NORMAL) - Desiste de cancelar
- **test_botao_voltar_durante_venda** (NORMAL) - Back button durante venda
- **test_cancelar_pedido_em_andamento** (CRITICAL) - Cancela pedido antes de finalizar
- **test_cancelar_troca_em_andamento** (CRITICAL) - Cancela troca antes de confirmar

---

### TESTES UNITÁRIOS (tests/unit/ - 11 arquivos)

Testes que rodam SEM device/Appium (mock/patch). Excluídos do build EXE.

- test_base_page_unit.py - Testa métodos da BasePage (mock driver)
- test_config_unit.py - Testa config.py (devices, _NO_WINDOW)
- test_consulta_pedido_page_unit.py - Testa ConsultaPedidoPage
- test_estoque_page_unit.py - Testa EstoquePage
- test_home_page_unit.py - Testa HomePage
- test_locators_unit.py - Testa locators/IDs dos elementos
- test_login_page_unit.py - Testa LoginPage
- test_pedido_page_unit.py - Testa PedidoPage
- test_troca_page_unit.py - Testa TrocaPage
- test_venda_futura_page_unit.py - Testa VendaFuturaPage
- test_venda_page_unit.py - Testa VendaPage

---

## 5. BUILD PIPELINE - COMO O EXE E O INSTALADOR SÃO GERADOS

```
                   COMPILAR.bat
                       |
                       v
            builder_pro.py --qa-dev E:\Testes_PDV
                       |
     +-----------------+-----------------+
     |                 |                 |
     v                 v                 v
  1. CLEAN         2. STAGE          3. VERIFY
  Limpa output/    Runner -> staging  Pacotes críticos
  staging, dist    QA Dev -> staging  instalados? Se
                   whitelist.json     não, pip install
     |                 |                 |
     +-----------------+-----------------+
                       |
                       v
               4. PYINSTALLER
               +----------------------------------------------+
               | python -m PyInstaller                         |
               |   --name QA_Dashboard                         |
               |   --onefile                                   |
               |   --noconsole                                 |
               |   --icon assets/icon.ico                      |
               |   --add-data pages;pages                      |
               |   --add-data tests;tests                      |
               |   --add-data assets;assets                    |
               |   --add-data xmls;xmls                        |
               |   --add-data config.py;.                      |
               |   --add-data test_data.py;.                   |
               |   --add-data framework.py;.                   |
               |   --add-data settings.json;.                  |
               |   --hidden-import pytest,pytest_metadata,...   |
               |   --hidden-import allure_commons,appium,...    |
               |   --hidden-import selenium,tkinter,...         |
               |   --collect-all pytest,_pytest,pluggy,...      |
               |   --collect-all pytest_metadata,allure_commons |
               |   --collect-all appium,selenium,...            |
               |   app_runner.py                               |
               +----------------------------------------------+
                       |
                       v
               output/dist/QA_Dashboard.exe (~60-80 MB)
                       |
                       v
               5. INNO SETUP
               +----------------------------------------------+
               | Gera qa_dashboard_installer.iss               |
               | Inclui:                                       |
               |   - QA_Dashboard.exe                          |
               |   - settings.json                             |
               |   - config.py, conftest.py, framework.py      |
               |   - test_data.py, requirements.txt            |
               |   - pages/*.py, tests/*.py                    |
               |   - assets/*, scripts/*                       |
               | Opções pós-install:                           |
               |   [ ] Instalar Java JDK, Node.js e Appium     |
               |   [ ] Instalar Android SDK (ADB)              |
               |   [ ] Verificar Ambiente Completo             |
               |   [x] Iniciar QA Dashboard                    |
               +----------------------------------------------+
                       |
                       v
               output/installer/Instalador_QA_Dashboard_YYYY_MM_DD.exe
```

---

### ESTRUTURA DE PASTAS APÓS INSTALAÇÃO

```
E:\QA Dashboard\
|-- QA_Dashboard.exe           <- Executável principal
|-- settings.json              <- Configurações (editável pela GUI)
|-- config.py                  <- Config de devices/Appium
|-- conftest.py                <- Fixtures pytest
|-- framework.py               <- Funções legadas
|-- test_data.py               <- Dados de teste
|-- requirements.txt           <- Dependências Python
|-- pages\                     <- Page Objects
|   |-- __init__.py
|   |-- base_page.py
|   |-- login_page.py
|   |-- home_page.py
|   |-- venda_page.py
|   |-- troca_page.py
|   |-- pedido_page.py
|   |-- consulta_pedido_page.py
|   |-- estoque_page.py
|   |-- venda_futura_page.py
|   |-- bonus_page.py
|   +-- venda_sucesso_page.py
|-- tests\
|   |-- e2e\
|   |   |-- test_login.py
|   |   |-- test_venda_consumidor.py
|   |   |-- test_venda_cliente.py
|   |   |-- test_troca_consumidor.py
|   |   |-- test_troca_cliente.py
|   |   |-- test_pedido_vendaConsumidor.py
|   |   |-- test_pedido_vendaCliente.py
|   |   |-- test_consulta_pedidoConsumidor.py
|   |   |-- test_consulta_pedidoCliente.py
|   |   |-- test_estoque.py
|   |   |-- test_venda_futura.py
|   |   |-- test_venda_futura_domicilio.py
|   |   |-- test_bonus.py
|   |   +-- test_cancelamento.py
|   |-- smoke\
|   |   +-- test_smoke_e2e.py
|   +-- unit\                     <- NÃO incluído no build EXE
|       |-- test_base_page_unit.py
|       |-- test_config_unit.py
|       |-- test_consulta_pedido_page_unit.py
|       |-- test_estoque_page_unit.py
|       |-- test_home_page_unit.py
|       |-- test_locators_unit.py
|       |-- test_login_page_unit.py
|       |-- test_pedido_page_unit.py
|       |-- test_troca_page_unit.py
|       |-- test_venda_futura_page_unit.py
|       +-- test_venda_page_unit.py
|-- templates\
|   +-- settings.default.json     <- Template de configuração padrão
|-- assets\
|   +-- icon.ico
|-- scripts\
|   |-- instalar_dependencias.bat
|   |-- instalar_android_sdk.bat
|   |-- instalar_allure.bat
|   |-- instalar_python.bat
|   |-- iniciar_programa.bat
|   +-- verificar_ambiente.bat
+-- logs\                      <- Criado em runtime
    |-- screenshots\
    |-- verificacoes\
    |   +-- ambiente_check.txt <- Log do "Verificar Ambiente"
    |-- allure-results\        <- Resultados brutos do pytest-allure
    |-- allure-report\         <- Relatório estático gerado (allure generate)
    |   +-- complete.html      <- Arquivo único (allure-combine)
    +-- reports\
        |-- relatorio_gui.html
        +-- Allure_Completo_*.html  <- Cópia do complete.html com timestamp
```

---

## 6. PADRÕES TÉCNICOS

### 6.1 WORKER MODE

**PROBLEMA:** O EXE empacotado com PyInstaller não tem Python externo. `sys.executable` aponta para o próprio EXE, não para python.exe. Não é possível chamar "python -m pytest" porque Python não existe.

**SOLUÇÃO:** O EXE detecta o argumento "worker_pytest_runner" e roda pytest internamente, usando o Python embutido pelo PyInstaller.

**FLUXO:**
```
QA_Dashboard.exe                    <- GUI (tkinter)
   |
   +--subprocess--> QA_Dashboard.exe worker_pytest_runner test_*.py
                       |
                       +-- Detecta argv[1] == "worker_pytest_runner"
                       +-- import pytest
                       +-- sys.exit(pytest.main(argv[2:]))
                       +-- NUNCA importa tkinter
```

**REGRA CRÍTICA:** O bloco worker DEVE estar ANTES de qualquer import tkinter. Se tkinter for importado no worker, causa erro no --noconsole porque tkinter tenta criar janela sem display.

---

### 6.2 _NO_WINDOW (Supressão de janelas CMD)

**PROBLEMA:** Chamadas `subprocess.run(['adb', ...])` abrem janelas CMD visíveis ao usuário, piscando na tela. Inaceitável para GUI profissional.

**SOLUÇÃO:** Definir `_NO_WINDOW` uma vez no módulo e usar em TODOS os subprocess:

```python
# No topo de config.py e conftest.py:
if sys.platform == 'win32':
    _si = subprocess.STARTUPINFO()
    _si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _si.wShowWindow = subprocess.SW_HIDE
    _NO_WINDOW = {
        'startupinfo': _si,
        'creationflags': subprocess.CREATE_NO_WINDOW
    }
else:
    _NO_WINDOW = {}

# Uso:
subprocess.run(['adb', 'devices'], **_NO_WINDOW)
```

**ONDE USA:** config.py (4 chamadas adb), conftest.py (4 chamadas adb), framework.py (1 chamada adb), base_page.py (2 chamadas adb), app_runner.py (Appium process, pytest process, _matar_appium, allure generate, allure serve)

---

### 6.3 FROZEN DETECTION (Detecção de EXE PyInstaller)

**PROBLEMA:** Caminhos de arquivos mudam entre desenvolvimento e EXE empacotado. No dev, `__file__` aponta para o .py. No EXE, não existe `__file__` real, e `sys.executable` aponta para o .exe.

**SOLUÇÃO:** Usar `getattr(sys, 'frozen', False)`:

```python
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

**ONDE USA:** app_runner.py (BASE_DIR, SETTINGS_FILE, SCRIPTS_DIR), config_manager.py (config_dir), test_data.py (busca settings.json ao lado do EXE), builder_pro.py (implicit - só roda em dev)

**REGRA:** `sys.executable` em app frozen = caminho do EXE, NÃO do Python. Por isso worker mode usa `sys.executable` para se re-executar.

---

### 6.4 MULTI-DEVICE (Suporte a Múltiplos Dispositivos)

**PROBLEMA:** Testes precisam rodar em diferentes devices Android simultaneamente. Cada device pode ter uma versão diferente do app (L400, Stone, etc.)

**SOLUÇÃO:** Arquitetura em 3 camadas:

#### 1. DETECÇÃO (config.py):
- `get_all_connected_devices()`: Lista UDIDs via "adb devices"
- `discover_target_app(device_id)`: Detecta qual flavor está instalado
- **APP_TARGETS:** 6 flavors x 2 ambientes (QA/PROD) = 12 packages possíveis

#### 2. ISOLAÇÃO (config.py + conftest.py):
- `get_appium_options(device_id)`: Cria options com udid específico
- `_calcular_porta_unica(device_id)`: SystemPort único por device (evita conflito UiAutomator2 entre sessões paralelas)
- conftest: --device-id e --appium-port via CLI

#### 3. PAGE OBJECTS (base_page.py):
- `app_package` property obtém package do driver.capabilities
- `_id_completo()` usa `app_package` da SESSÃO, não variável global
- Permite mesma page rodar em devices com packages diferentes

**EXEMPLO:**
```bash
pytest --device-id=RFCR20XXXXX --appium-port=4723 test_login.py
pytest --device-id=EMULATOR-5554 --appium-port=4725 test_login.py
```

---

### 6.5 NOCONSOLE STDOUT FIX

**PROBLEMA:** Com --noconsole no PyInstaller, `sys.stdout` e `sys.stderr` são None. Qualquer `print()` ou logging causa crash silencioso.

**SOLUÇÃO:** No início do worker mode (antes de qualquer output):

```python
if sys.stdout is None:
    sys.stdout = io.TextIOWrapper(open(os.devnull, "w"))
if sys.stderr is None:
    sys.stderr = io.TextIOWrapper(open(os.devnull, "w"))

# Também reconfigura encoding para UTF-8:
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
```

**NOTA:** O config.py também faz reconfigure de encoding no topo.

---

### 6.6 PAGE OBJECT PATTERN

**ESTRUTURA:** Cada tela do app tem sua própria classe Page Object:

```
BasePage (40+ métodos genéricos)
    |
    +-- LoginPage     (tela de login)
    +-- HomePage      (tela inicial)
    +-- VendaPage     (fluxo de venda)
    +-- TrocaPage     (troca/devolução)
    +-- PedidoPage    (pedido de venda)
    +-- ConsultaPedidoPage (consulta pedido)
    +-- EstoquePage   (consulta estoque)
    +-- VendaFuturaPage (venda futura)
    +-- BonusPage     (bônus/cashback)
```

**PADRÃO:** Cada Page Object tem:
- **LOCATORS:** Constantes de classe com IDs dos elementos
- **AÇÕES:** Métodos que interagem com a tela
- **FLUXOS:** Métodos que executam sequências completas
- **VALIDAÇÕES:** Métodos que verificam estado da tela

**BENEFÍCIO:** Testes ficam legíveis e manutenção centralizada:
```python
venda_page.adicionar_produto("123")
venda_page.selecionar_pagamento_dinheiro()
venda_page.finalizar_venda()
assert venda_page.venda_sucesso_exibida()
```

---

### 6.7 FIXTURE CHAIN (Cadeia de Fixtures)

```
       driver                driver_logado
       (Appium session)      (Appium + Login)
          |                      |
          |   LoginPage.         |
          +-- garantir_login()   |
          |   HomePage.          |
          +-- tela_inicial()     |
          |                      |
          +-- yield driver ------+-- yield driver
          |                      |
          +-- driver.quit()      +-- (mesmo driver.quit())
```

**driver:** Cria sessão Appium (scope=function). Cada teste recebe driver novo. Fixture encerra com `driver.quit()`.

**driver_logado:** Depende de driver. Faz login se necessário usando `LoginPage.garantir_login()` com dados de test_data. Retorna o mesmo driver (já logado).

---

### 6.8 ORDENAÇÃO DE TESTES

**MECANISMO:** conftest.py define ORDEM_TESTES (lista de nomes de função). Hook `pytest_collection_modifyitems` ordena items pela posição do nome na lista. Testes não listados recebem índice alto (`len(ORDEM_TESTES) + 1`) e rodam por último na ordem original.

**MOTIVO:** Trocas dependem de vendas recentes (nota fiscal mais recente). Consulta de pedido depende de pedido criado antes. A ordenação garante que dados de um teste estejam disponíveis para o próximo.

**ATENÇÃO:** ORDEM_TESTES referencia "test_login_sucesso" e "test_login_falha_senha_invalida", porém os testes de login foram renomeados para `test_garantir_login` e `test_verificar_sessao_ativa`. Como os nomes não batem, os testes de login efetivamente NÃO são ordenados pelo hook e rodam por último.

---

### 6.9 ALLURE REPORTING

**INTEGRAÇÃO:** conftest.py gera:
- `allure-results/environment.properties` (dados completos do device)
- `allure-results/categories.json` (categorias de falhas)
- Testes usam decorators `@allure.severity`, `@allure.feature`, etc.
- Screenshots de falha são anexados automaticamente.

**ENVIRONMENT.PROPERTIES (seções organizadas):**
```
# === SISTEMA ===
Sistema Operacional, Python, Servidor Appium

# === EXECUÇÃO ===
Data Execução, Ambiente (Local/CI), GitHub info (se CI)

# === APLICATIVO ===
App Package

# === DISPOSITIVO ===
Device ID, Modelo, Fabricante, Brand, Android, API Level,
Security Patch, Build ID

# === HARDWARE ===
Arquitetura CPU, Resolução Tela, Densidade Tela, RAM Total, Serial
```

**PARALELO:** pytest-html gera relatório standalone (--self-contained-html) que pode ser aberto pelo botão "Relatório Simples" na GUI.

**GUI ALLURE:** A aba Configurações possui 3 checkboxes para controlar Allure:
- [x] Gerar Relatório Allure (Base) → adiciona --alluredir ao pytest
- [x] Gerar Arquivo Único → chama allure-combine pós-teste
- [x] Abrir Relatório Allure ao final → abre arquivo ou servidor

Dois botões na aba Testes:
- "📄 Relatório Simples" → abre pytest-html (abrir_relatorio)
- "📊 Relatório Funcional (Allure)" → gerar_e_abrir_allure_unico()

**FLUXO gerar_e_abrir_allure_unico():**
1. **GERAR BASE:** `allure generate logs/allure-results -o logs/allure-report --clean` (subprocess com CREATE_NO_WINDOW, requer Allure CLI no PATH)
2. **COMBINE (se generate_single_file):**
   ```python
   from allure_combine import combine_allure
   combine_allure(allure_report_dir)
   ```
   → Gera complete.html (arquivo HTML único com todos os assets inline)
   → Copia para `logs/reports/Allure_Completo_YYYYMMDD_HHMMSS.html`
3. **ABRIR (se open_allure_end):** Prioridade: arquivo único (webbrowser.open) > servidor (allure serve)

**FLUXO abrir_servidor_allure():**
- Mata `allure_proc` anterior se existir (taskkill /F /T /PID)
- Busca porta livre (5000-5999) excluindo porta do Appium
- Inicia `allure serve logs/allure-results -p {porta}` (subprocess com CREATE_NO_WINDOW + STARTUPINFO)
- Servidor abre navegador automaticamente

---

### 6.10 DESCRIÇÕES BDD GHERKIN

**PADRÃO:** Todos os testes E2E usam formato BDD Gherkin padronizado nos decorators `@allure.description` para documentação clara.

**ESTRUTURA:**
```python
@allure.description("""
**Cenário:** [Descrição do cenário de teste]

**Pré-condições:**
- [Lista de pré-condições necessárias]

**Dado** que [contexto inicial]
**Quando** [ação executada]
**E** [ação adicional]
**Então** [resultado esperado]
**E** [validação adicional]
""")
```

**BENEFÍCIOS:**
- Documentação clara e consistente em todos os testes
- Renderiza corretamente no relatório Allure (markdown)
- Facilita entendimento do fluxo por stakeholders não-técnicos
- Alinha com docstrings BDD existentes nos métodos de teste

**ARQUIVOS:** Todos os testes em `tests/e2e/*.py` seguem este padrão:
- test_login.py (1 teste)
- test_venda_consumidor.py (1 teste)
- test_venda_cliente.py (1 teste)
- test_troca_consumidor.py (1 teste)
- test_troca_cliente.py (1 teste)
- test_pedido_venda.py (2 testes)
- test_consulta_pedido.py (2 testes)
- test_venda_futura.py (2 testes)
- test_venda_futura_domicilio.py (1 teste)
- test_bonus.py (2 testes)
- test_cancelamento.py (6 testes)
- test_estoque.py (4 testes)

---

## 7. OTIMIZAÇÕES E MELHORIAS RECENTES

### 7.1 VERSIONAMENTO DINÂMICO

**Problema resolvido:** Versão ficava fixa em "V2.0.0" no executável compilado.

**Solução implementada:**
- Arquivo VERSION é lido usando `sys._MEIPASS` quando em modo compilado (PyInstaller)
- Builder incrementa automaticamente patch version a cada build
- Versão exibida corretamente no título e rodapé da GUI

**Código em app_runner.py:**
```python
# Configuração de ambiente com suporte a _MEIPASS
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    MEIPASS_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
else:
    # Modo desenvolvimento
    MEIPASS_DIR = BASE_DIR

# VERSION fica no _MEIPASS quando compilado
VERSION_FILE = os.path.join(MEIPASS_DIR, "VERSION") if getattr(sys, 'frozen', False) else os.path.join(BASE_DIR, "VERSION")
```

---

### 7.2 OTIMIZAÇÃO DE PROCESSAMENTO DE LOGS

**Problema resolvido:** UI travando ao processar muitos logs rapidamente.

**Soluções implementadas:**

#### Buffer de Processamento (Lotes)
```python
# Processa logs em lotes de 5 linhas
BUFFER_SIZE = 5
buffer = []

for line in self.pytest_proc.stdout:
    buffer.append(line)

    if len(buffer) >= BUFFER_SIZE:
        for linha in buffer:
            self.processar_linha_log(linha)
        buffer.clear()
        self.root.update_idletasks()  # Atualiza UI a cada lote
```

#### Filtros Globais Otimizados
- Ignora logs de bibliotecas externas (Selenium, urllib3, Appium internals)
- Bloqueia linhas muito longas (>500 chars)
- Remove capturas stdout/stderr excessivas

---

### 7.3 MODO DEBUG MELHORADO

**Problema resolvido:** Modo debug muito verboso, travando ao exibir logs gigantes.

**Nova abordagem:**
- **Modo Normal e Debug usam a mesma lógica de exibição**
- **Diferença:** Debug mostra stack traces completos APENAS em caso de erro
- **Separadores reduzidos:** De 50+ caracteres para apenas 7 (`=======`)

**Comportamento:**
```
NORMAL:  Mostra ações do teste (cliques, digitação, validações)
DEBUG:   Igual ao normal + detalhes técnicos quando há ERRO/FALHA

Ambos filtram:
  ✅ Ruído de bibliotecas
  ✅ Linhas muito longas
  ✅ Capturas excessivas
```

---

### 7.4 SEPARADORES VISUAIS REDUZIDOS

**Problema resolvido:** Separadores com 50+ caracteres poluindo a interface.

**Solução:**
```python
# Antes: ==================================================
# Depois: =======

if linha_limpa.startswith("===") or linha_limpa.startswith("---"):
    texto = linha_limpa[0] * 7  # Apenas 7 caracteres
    mostrar, tag = True, 'SYSTEM'
```

**Resultado:**
```
Antes:
==================================================
🧪 Executando: Venda_Cliente_Sucesso ============
==================================================

Depois:
=======
🧪 Executando: Venda_Cliente_Sucesso =======
```

---

### 7.5 BUSCA ROBUSTA DE DEPENDÊNCIAS

**Melhorias nas funções auxiliares:**

- **`_buscar_node_instalado()`:** Busca Node.js em PATH, Program Files, NVM
- **`_buscar_allure_instalado()`:** Busca Allure em Scoop, Chocolatey, instalação manual
- **`_buscar_appium_instalado()`:** Usa `npm bin -g` + fallback em locais comuns
- **`_buscar_adb_instalado()`:** Busca ADB em ANDROID_HOME, SDK padrão, Android Studio

**Benefício:** Encontra ferramentas mesmo quando PATH não está configurado corretamente.

---

## FIM DO DOCUMENTO

**Atualizado em:** 2026-03-04
**Projeto:** PDV Automação - QA Dashboard
**Versão Atual:** 2.0.21 (última compilação: 03/03/2026)
**Total de arquivos fonte documentados:** 28
**Total de testes documentados:** 15 e2e + 5 smoke + 11 unit em 27 arquivos
**Última alteração:** Atualização de documentação com venda_sucesso_page.py e nomes corretos dos testes
