# 🧪 Testes Unitários - Documentação

Testes unitários validam os Page Objects de forma isolada, sem interação com o Appium ou dispositivo real.

---

## 🎯 Objetivo

Garantir que cada Page Object funciona corretamente:
- ✅ Métodos chamam as funções corretas
- ✅ Parâmetros são passados corretamente
- ✅ Retornos são os esperados
- ✅ Lógica de negócio está correta

**Vantagem**: Execução ultra-rápida (< 10 segundos para 200 testes)

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de Testes** | 200 |
| **Tempo de Execução** | < 10 segundos |
| **Cobertura** | 100% dos Page Objects (10/10) |
| **Status** | 197 passando, 3 com issues conhecidos |

### Testes por Page Object

| Page Object | Testes | Arquivo |
|------------|--------|---------|
| BasePage | 23 | `test_base_page_unit.py` |
| LoginPage | 7 | `test_login_page_unit.py` |
| HomePage | 7 | `test_home_page_unit.py` |
| VendaPage | 15 | `test_venda_page_unit.py` |
| PedidoPage | 10 | `test_pedido_page_unit.py` |
| EstoquePage | 23 | `test_estoque_page_unit.py` |
| TrocaPage | 19 | `test_troca_page_unit.py` |
| **BonusPage** | **29** | `test_bonus_page_unit.py` ✨ **NOVO** |
| ConsultaPedidoPage | 7 | `test_consulta_pedido_page_unit.py` |
| VendaFuturaPage | 20 | `test_venda_futura_page_unit.py` |
| Config/Framework | 40 | `test_config_unit.py`, `test_locators_unit.py` |

---

## 🚀 Execução

```bash
# Todos os testes unitários
pytest tests/unit/ -v

# Teste específico de um Page Object
pytest tests/unit/test_bonus_page_unit.py -v

# Com duração dos testes
pytest tests/unit/ -v --durations=10

# Parar no primeiro erro
pytest tests/unit/ -x
```

---

## 🏗️ Estrutura de um Teste Unitário

### Padrão AAA (Arrange-Act-Assert)

```python
from unittest.mock import MagicMock, patch

class TestBonusPageAtivarBonus:
    """Testes para o método ativar_bonus."""

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_ativar_bonus_clica_quando_desativado(self, mock_time, mock_logger, mock_base_init):
        """
        Deve clicar no switch quando o bonus está desativado.
        """
        from pages.bonus_page import BonusPage

        # ========== ARRANGE ==========
        # Cria instância sem chamar __init__
        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()

        # Configura comportamento dos mocks
        page.bonus_ativado = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()

        # ========== ACT ==========
        # Executa o método a ser testado
        page.ativar_bonus()

        # ========== ASSERT ==========
        # Valida comportamento
        page.bonus_ativado.assert_called_once()
        page.clicar_por_id.assert_called_once_with(BonusPage.SWITCH_BONUS)
        mock_time.sleep.assert_called_once_with(4)
```

---

## 📝 Nomenclatura

### Classes de Teste

```python
# Formato: TestNomePageMetodoTestado
class TestBonusPageAtivarBonus:
class TestVendaPageAdicionarProduto:
class TestEstoquePageBuscarProduto:
```

### Métodos de Teste

```python
# Formato: test_metodo_cenario_resultado_esperado

def test_ativar_bonus_clica_quando_desativado(self):
    """Cenário: bonus desativado → Resultado: clica no switch"""

def test_ativar_bonus_nao_clica_quando_ja_ativado(self):
    """Cenário: bonus já ativado → Resultado: não clica"""

def test_bonus_foi_aplicado_retorna_true_quando_valor_zerado(self):
    """Cenário: valor final = R$ 0,00 → Resultado: retorna True"""
```

---

## 🎯 Tipos de Testes

### 1. Testes de Chamada de Método

Validam que métodos são chamados corretamente:

```python
def test_adicionar_produto_chama_metodos_corretos(self):
    # Arrange
    page.clicar_por_id = MagicMock()
    page.digitar_por_id = MagicMock()

    # Act
    page.adicionar_produto("456")

    # Assert
    page.clicar_por_id.assert_called_with(BonusPage.BTN_ADICIONAR_PRODUTOS)
    page.digitar_por_id.assert_called_with("editText", "456")
```

### 2. Testes de Retorno

Validam valores de retorno:

```python
def test_obter_valor_bonus_retorna_texto_do_elemento(self):
    # Arrange
    mock_elemento = MagicMock()
    mock_elemento.text = "R$ 50,00"
    page.encontrar_por_id = MagicMock(return_value=mock_elemento)

    # Act
    valor = page.obter_valor_bonus()

    # Assert
    assert valor == "R$ 50,00"
```

### 3. Testes de Condições

Validam lógica condicional:

```python
def test_bonus_ativado_retorna_true_quando_checked_true(self):
    # Arrange
    mock_elemento = MagicMock()
    mock_elemento.get_attribute.return_value = "true"
    page.encontrar_por_id = MagicMock(return_value=mock_elemento)

    # Act
    resultado = page.bonus_ativado()

    # Assert
    assert resultado is True
    mock_elemento.get_attribute.assert_called_with("checked")
```

### 4. Testes de Erro

Validam tratamento de exceções:

```python
def test_obter_valor_bonus_retorna_na_quando_erro(self):
    # Arrange
    page.encontrar_por_id = MagicMock(side_effect=Exception("Não encontrado"))

    # Act
    valor = page.obter_valor_bonus()

    # Assert
    assert valor == "N/A"
```

---

## 🔧 Técnicas de Mocking

### Mockar Driver

```python
page = BonusPage.__new__(BonusPage)
page.driver = MagicMock()
```

### Mockar Métodos

```python
page.clicar_por_id = MagicMock()
page.digitar_por_id = MagicMock(return_value="texto")
```

### Mockar Comportamento Condicional

```python
# Retorna valores diferentes em chamadas sequenciais
page.texto_exibido = MagicMock(side_effect=[True, False, True])

# Retorna baseado no parâmetro
def texto_exibido_mock(texto, tempo_espera):
    return texto == "Selecionar Cliente"

page.texto_exibido = MagicMock(side_effect=texto_exibido_mock)
```

### Mockar Exceções

```python
page.encontrar_por_id = MagicMock(side_effect=Exception("Erro"))
```

---

## ✅ Exemplo Completo: BonusPage

### Método a Testar

```python
# pages/bonus_page.py
def ativar_bonus(self):
    """Ativa o bonus se estiver disponível e desativado."""
    if not self.bonus_ativado():
        self.clicar_por_id(self.SWITCH_BONUS)
        time.sleep(4)
    else:
        logger.info("Bonus já estava ativado")
```

### Testes Criados

```python
# tests/unit/test_bonus_page_unit.py
class TestBonusPageAtivarBonus:

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_ativar_bonus_clica_quando_desativado(self, mock_time, mock_logger, mock_base_init):
        """Deve clicar no switch quando o bonus está desativado."""
        from pages.bonus_page import BonusPage

        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.bonus_ativado = MagicMock(return_value=False)
        page.clicar_por_id = MagicMock()

        page.ativar_bonus()

        page.bonus_ativado.assert_called_once()
        page.clicar_por_id.assert_called_once_with(BonusPage.SWITCH_BONUS)
        mock_time.sleep.assert_called_once_with(4)

    @patch('pages.bonus_page.BasePage.__init__', return_value=None)
    @patch('pages.bonus_page.logger')
    @patch('pages.bonus_page.time')
    def test_ativar_bonus_nao_clica_quando_ja_ativado(self, mock_time, mock_logger, mock_base_init):
        """Não deve clicar no switch quando o bonus já está ativado."""
        from pages.bonus_page import BonusPage

        page = BonusPage.__new__(BonusPage)
        page.driver = MagicMock()
        page.bonus_ativado = MagicMock(return_value=True)
        page.clicar_por_id = MagicMock()

        page.ativar_bonus()

        page.bonus_ativado.assert_called_once()
        page.clicar_por_id.assert_not_called()
```

---

## 🎓 Boas Práticas

### ✅ DO

- **Testar comportamento**, não implementação
- **Um assert por conceito** (pode ter múltiplos asserts, mas relacionados)
- **Nomenclatura descritiva** nos testes
- **Mockar TODAS as dependências externas**
- **Testes independentes** (não dependem de ordem de execução)
- **Documentar cenários** com docstrings

### ❌ DON'T

- Não criar testes com dependências entre si
- Não mockar a função que está sendo testada
- Não usar dados reais do Appium (sempre mock)
- Não testar código de bibliotecas externas
- Não criar testes longos e complexos
- Não ignorar testes falhando

---

## 🔍 Debugging

### Ver Saída Detalhada

```bash
pytest tests/unit/test_bonus_page_unit.py -vv
```

### Ver Traceback Completo

```bash
pytest tests/unit/ -v --tb=long
```

### Executar com PDB

```python
def test_metodo(self):
    import pdb; pdb.set_trace()
    # código do teste
```

---

## 📈 Cobertura

### Medir Cobertura (Opcional)

```bash
pip install pytest-cov

pytest tests/unit/ --cov=pages --cov-report=html
```

**Meta**: 100% dos Page Objects com testes unitários ✅ **ALCANÇADO**

---

**Última atualização**: 24/02/2026
**Versão**: 2.1 (adicionado BonusPage com 29 testes)
