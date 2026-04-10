"""
Test Cadastro Cliente - Testes E2E para cadastro de clientes PF e PJ.
"""
import pytest
import allure
from pages.cliente_page import ClientePage


@allure.epic("PDV Mobile")
@allure.feature("Cadastro de Cliente")
@allure.story("Cadastro de Pessoa Física")
class TestCadastroClientePF:
    """Testes E2E para cadastro de Pessoa Física."""

    @allure.title("Cadastrar Pessoa Física com Sucesso")
    @allure.description("""
    Cenário: Cadastrar novo cliente Pessoa Física

    Pré-condições:
    - Usuário logado no sistema
    - Dados do cliente gerados aleatoriamente (Faker)
    - Endereço válido obtido via API ViaCEP

    Passos:
    1. Navegar até "Novo Cadastro"
    2. Selecionar "Pessoa Física"
    3. Preencher dados principais (CPF, nome, email, telefone, etc)
    4. Adicionar endereço
    5. Preencher dados de endereço (CEP, rua, número, etc)
    6. Salvar endereço
    7. Salvar cliente
    8. Validar mensagem de sucesso

    Resultado esperado:
    - Cliente cadastrado com sucesso
    - Mensagem "Cliente cadastrado com sucesso!" exibida
    - Retorno para tela inicial
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cadastro", "cliente", "pf", "pessoa-fisica")
    def test_cadastrar_pessoa_fisica(self, driver_logado):
        """
        Cenário: Cadastrar novo cliente Pessoa Física
        Dado que o usuário está logado
        Quando acessar "Novo Cadastro"
        E preencher todos os dados de Pessoa Física
        E salvar o cadastro
        Então o cliente deve ser cadastrado com sucesso
        E a mensagem de sucesso deve ser exibida
        """
        # Arrange
        cliente_page = ClientePage(driver_logado)

        # Act
        with allure.step("Navegar até Novo Cadastro"):
            cliente_page.navegar_novo_cadastro()

        with allure.step("Cadastrar cliente Pessoa Física"):
            dados_cliente = cliente_page.cadastrar_cliente_completo(tipo_pessoa="PF")

        # Anexa dados do cliente ao relatório
        allure.attach(
            str(dados_cliente),
            name="Dados do Cliente PF Cadastrado",
            attachment_type=allure.attachment_type.TEXT
        )

        # Assert
        with allure.step("Verificar se cadastro foi concluído com sucesso"):
            assert cliente_page.cadastro_concluido_com_sucesso(), \
                "Cadastro de Pessoa Física não foi concluído com sucesso"


@allure.epic("PDV Mobile")
@allure.feature("Cadastro de Cliente")
@allure.story("Cadastro de Pessoa Jurídica")
class TestCadastroClientePJ:
    """Testes E2E para cadastro de Pessoa Jurídica."""

    @allure.title("Cadastrar Pessoa Jurídica com Sucesso")
    @allure.description("""
    Cenário: Cadastrar novo cliente Pessoa Jurídica

    Pré-condições:
    - Usuário logado no sistema
    - Dados da empresa gerados aleatoriamente (Faker)
    - Endereço válido obtido via API ViaCEP

    Passos:
    1. Navegar até "Novo Cadastro"
    2. Selecionar "Pessoa Jurídica"
    3. Preencher dados principais (CNPJ, razão social, email, telefone, etc)
    4. Adicionar endereço
    5. Preencher dados de endereço (CEP, rua, número, etc)
    6. Salvar endereço
    7. Salvar cliente
    8. Validar mensagem de sucesso

    Resultado esperado:
    - Empresa cadastrada com sucesso
    - Mensagem "Cliente cadastrado com sucesso!" exibida
    - Retorno para tela inicial
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("cadastro", "cliente", "pj", "pessoa-juridica")
    def test_cadastrar_pessoa_juridica(self, driver_logado):
        """
        Cenário: Cadastrar novo cliente Pessoa Jurídica
        Dado que o usuário está logado
        Quando acessar "Novo Cadastro"
        E preencher todos os dados de Pessoa Jurídica
        E salvar o cadastro
        Então a empresa deve ser cadastrada com sucesso
        E a mensagem de sucesso deve ser exibida
        """
        # Arrange
        cliente_page = ClientePage(driver_logado)

        # Act
        with allure.step("Navegar até Novo Cadastro"):
            cliente_page.navegar_novo_cadastro()

        with allure.step("Cadastrar cliente Pessoa Jurídica"):
            dados_cliente = cliente_page.cadastrar_cliente_completo(tipo_pessoa="PJ")

        # Anexa dados do cliente ao relatório
        allure.attach(
            str(dados_cliente),
            name="Dados da Empresa PJ Cadastrada",
            attachment_type=allure.attachment_type.TEXT
        )

        # Assert
        with allure.step("Verificar se cadastro foi concluído com sucesso"):
            assert cliente_page.cadastro_concluido_com_sucesso(), \
                "Cadastro de Pessoa Jurídica não foi concluído com sucesso"
