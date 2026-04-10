# 🔥 Smoke Tests - Documentação

Os Smoke Tests são testes rápidos de sanidade executados para validar se o ambiente está funcional **ANTES** de rodar a suite completa de testes E2E.

---

## 🎯 Objetivo

Garantir que as funcionalidades críticas do sistema estão operacionais:
- ✅ App abre sem crashar
- ✅ Login funciona
- ✅ Servidor está respondendo
- ✅ Funcionalidades críticas (venda, cancelamento, pedido) funcionam
- ✅ Navegação básica está funcional

**Se o smoke test falhar → Não adianta rodar testes E2E completos**

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de Testes** | 18 |
| **Arquivos** | 12 (11 individuais + test_smoke_e2e.py consolidado) |
| **Tempo de Execução** | 8-10 minutos |
| **Cobertura Crítica** | ~70% das funcionalidades |
| **Localização** | `tests/smoke/` |

---

## 🧪 Testes Implementados

### TestSmokeAmbiente (4 testes)

#### 1. `test_01_app_abre_corretamente`
- **Severidade**: BLOCKER
- **Duração**: 5s
- **Valida**:
  - Driver foi inicializado
  - App não crashou
  - Page source não está vazio

#### 2. `test_02_login_funciona`
- **Severidade**: BLOCKER
- **Duração**: 30s
- **Valida**:
  - Consegue preencher credenciais
  - Login é bem-sucedido
  - Tela inicial aparece

#### 3. `test_03_elementos_basicos_visiveis`
- **Severidade**: CRITICAL
- **Duração**: 10s
- **Valida**:
  - Botão "Iniciar Venda" visível
  - Módulos principais visíveis:
    - Pedido Venda
    - Consultar Estoque
    - Realizar Troca
    - Consultar Pedido

#### 4. `test_04_consegue_iniciar_venda`
- **Severidade**: CRITICAL
- **Duração**: 15s
- **Valida**:
  - Consegue clicar em "Iniciar Venda"
  - Próxima tela carrega (seleção de vendedor/cliente)
  - Sistema não trava

### TestSmokeFuncionalidades (6 testes)

#### 5. `test_05_servidor_respondendo`
- **Severidade**: BLOCKER
- **Duração**: 5s
- **Valida**:
  - Servidor está acessível
  - Tela inicial carregou (prova que servidor retornou dados)

#### 6. `test_06_venda_basica_consumidor`
- **Severidade**: CRITICAL
- **Duração**: 45s
- **Valida**:
  - Fluxo completo de venda:
    1. Iniciar venda
    2. Selecionar vendedor
    3. Adicionar produto
    4. Selecionar pagamento em dinheiro
    5. Finalizar venda
  - Venda é concluída com sucesso
  - Retorna à tela inicial

#### 7. `test_07_cancelamento_com_dialogo`
- **Severidade**: CRITICAL
- **Duração**: 20s
- **Valida**:
  - Consegue iniciar venda
  - Consegue adicionar produto
  - Consegue cancelar venda
  - Retorna à tela inicial

#### 8. `test_08_pedido_venda_basico`
- **Severidade**: NORMAL
- **Duração**: 40s
- **Valida**:
  - Consegue acessar módulo de pedidos
  - Fluxo de pedido funciona
  - Pedido é gerado com sucesso

#### 9. `test_09_navegacao_entre_modulos`
- **Severidade**: NORMAL
- **Duração**: 30s
- **Valida**:
  - Consegue acessar "Pedido Venda"
  - Consegue acessar "Realizar Troca"
  - Consegue voltar de cada módulo

#### 10. `test_10_recuperacao_botao_back`
- **Severidade**: NORMAL
- **Duração**: 20s
- **Valida**:
  - Botão back do Android funciona
  - Diálogo de confirmação aparece (ou volta direto)
  - Sistema não trava

---

## 🚀 Execução

### Executar Smoke Tests

```bash
# Executar todos os smoke tests
pytest tests/smoke/ -v -m smoke

# Com relatório Allure
pytest tests/smoke/ -v -m smoke --alluredir=logs/allure-results
allure serve logs/allure-results

# Parar no primeiro erro
pytest tests/smoke/ -v -m smoke -x
```

### Pré-requisitos

1. ✅ Appium Server rodando (`appium`)
2. ✅ Dispositivo Android conectado (`adb devices`)
3. ✅ APK do PDV instalado
4. ✅ `test_data.py` configurado

---

## 📊 Interpretando Resultados

### ✅ Todos os Testes Passaram

```
======================== 10 passed in 4m 30s ========================
```

**Significado**: ✅ Ambiente APROVADO para testes E2E!

**Próximos passos**:
- Pode executar suite completa de testes E2E
- Ambiente está estável

### ❌ Algum Teste Falhou

```
======================== 1 failed, 9 passed in 3m 50s ========================
```

**Ações**:
1. **Identificar qual teste falhou**
2. **Analisar o erro no relatório Allure**
3. **Corrigir o problema antes de rodar testes E2E**

### Falhas Comuns e Soluções

| Teste Falhando | Causa Provável | Solução |
|----------------|----------------|---------|
| `test_01_app_abre` | APK não instalado | Instalar APK: `adb install pdv.apk` |
| `test_02_login` | Credenciais inválidas | Verificar `test_data.py` |
| `test_05_servidor` | Servidor offline | Verificar IP e porta em `test_data.py` |
| `test_06_venda_basica` | Produto não existe | Usar código de produto válido |

---

## 🎯 Quando Executar

### Sempre Execute Smoke Tests Antes de:

1. ✅ **Release/Deploy**
   - Validar que build não quebrou funcionalidades críticas

2. ✅ **Atualização do APK**
   - Garantir compatibilidade da nova versão

3. ✅ **Mudança de Servidor**
   - Validar conectividade com novo servidor

4. ✅ **Início do Dia de Testes**
   - Verificar se ambiente está OK antes de começar

5. ✅ **CI/CD Pipeline**
   - Primeiro estágio do pipeline de testes

### Não Execute Smoke Tests Quando:

- ❌ Já sabe que há problema grave (app não abre, servidor offline)
- ❌ Está desenvolvendo testes localmente (use testes unitários)
- ❌ Está testando funcionalidade específica (use teste E2E específico)

---

## 🔧 Customização

### Adicionar Novo Smoke Test

```python
@allure.title("SMOKE: Seu novo teste")
@allure.description("Descrição do que será validado")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "sua-funcionalidade")
def test_11_seu_novo_teste(self, driver_logado):
    """
    SMOKE TEST 11: Descrição do cenário.

    Criterios de sucesso:
    - Item 1
    - Item 2
    """
    logger.info("=" * 50)
    logger.info("SMOKE TEST: Seu novo teste")
    logger.info("=" * 50)

    driver = driver_logado
    page = SuaPage(driver)

    with allure.step("1. Ação 1"):
        page.acao_1()

    with allure.step("2. Validação"):
        assert page.validacao()

    logger.info("[OK] Seu teste funcionou!")
```

### Configurar Tempo Limite

Edite `pytest.ini`:

```ini
[pytest]
timeout = 600  # 10 minutos para smoke tests
```

---

## 📈 Histórico de Evolução

| Versão | Data | Testes | Cobertura | Mudanças |
|--------|------|--------|-----------|----------|
| 1.0 | 06/02/2026 | 5 | ~30% | Versão inicial |
| 2.0 | 24/02/2026 | 10 | ~70% | Expandido para cobertura crítica |

### Versão 2.0 - Mudanças

#### ✨ Adicionado
- Teste de conectividade com servidor
- Teste de venda básica completa
- Teste de cancelamento com confirmação
- Teste de geração de pedido
- Teste de navegação entre módulos
- Teste de recuperação de botão back

#### 🔧 Melhorado
- `test_03_elementos_basicos_visiveis` agora valida TODOS os módulos principais
- Documentação expandida
- Resumo final atualizado

---

## 🎓 Boas Práticas

### ✅ DO

- Manter smoke tests **rápidos** (< 5 minutos)
- Validar **apenas** funcionalidades críticas
- Executar **antes** dos testes E2E completos
- Usar **dados de teste simples** (produto "123", cliente "1")
- **Limpar estado** após cada teste

### ❌ DON'T

- Não adicionar testes muito longos
- Não validar funcionalidades secundárias
- Não usar dados complexos ou dependentes
- Não deixar o ambiente sujo após teste
- Não adicionar mais de 20 testes (mantenha focado)

---

## 📞 Suporte

Problemas com Smoke Tests? Consulte:
- [Troubleshooting](GETTING_STARTED.md#-problemas-comuns)
- Logs em `logs/allure-results`
- Equipe de QA Mobile

---

**Última atualização**: 10/04/2026
**Versão**: 2.0.108
