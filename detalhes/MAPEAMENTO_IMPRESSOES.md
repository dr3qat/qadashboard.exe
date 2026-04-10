# Mapeamento de Impressões - PDV Mobile

## Visão Geral

Este documento mapeia **todos os tipos de impressão** disponíveis no aplicativo PDV Mobile e como controlá-los via Dashboard.

---

## 📋 Tipos de Impressão Identificados

| Tipo | Localização | Botão Principal | Diálogo | Controle Dashboard |
|------|------------|-----------------|---------|-------------------|
| **1. Cupom de Venda** | Após finalizar venda | Diálogo automático | `android:id/button1` (SIM)<br>`android:id/button2` (NÃO) | ✅ `print_cupom_venda` |
| **2. Cupom de Troca (Diálogo)** | ANTES da tela de sucesso* | Diálogo condicional | `android:id/button1` (SIM)<br>`android:id/button2` (NÃO) | ✅ `print_cupom_troca` |
| **3. NFC-E** | Tela de sucesso (1º botão) | `btn_impressao_nfce` | `android:id/button1` (SIM)<br>`android:id/button2` (NÃO) | ✅ `print_nfce` |
| **4. DANFE via Servidor** | Tela de sucesso (2º botão) | `btn_nfe_print` | `md_buttonDefaultPositive` (OK) | ✅ `print_danfe` |
| **5. Cupom de Troca (Botão)** | Tela de sucesso (3º botão)** | `btn_print_cupom_troca` | `android:id/button1` (SIM)<br>`android:id/button2` (NÃO) | ✅ `print_cupom_troca` |

\* *Depende de parâmetro no sistema. Se habilitado, aparece como diálogo ANTES da tela de sucesso.*
\*\* *Se não foi perguntado antes, o botão aparece na tela de sucesso.*

---

## 🎯 Testes com Impressões Implementadas

### ✅ **Testes com Controle COMPLETO de Impressões**

Estes testes processam **TODOS os 5 tipos de impressão** conforme configuração do Dashboard:

| Teste | Arquivo | Status | Impressões Processadas |
|-------|---------|--------|------------------------|
| **test_venda_consumidor_sucesso** | `tests/e2e/test_venda_consumidor.py` | ✅ **COMPLETO** | 1. Cupom Venda<br>2. Cupom Troca Diálogo<br>3. NFC-E<br>4. DANFE<br>5. Cupom Troca Botão |
| **test_venda_cliente_sucesso** | `tests/e2e/test_venda_cliente.py` | ✅ **COMPLETO** | 1. Cupom Venda<br>2. Cupom Troca Diálogo<br>3. NFC-E<br>4. DANFE<br>5. Cupom Troca Botão |

### ⏳ **Testes Pendentes de Atualização**

Estes testes processam **APENAS cupom de venda** (não têm os outros botões de impressão implementados):

| Teste | Arquivo | Status | Impressões Processadas |
|-------|---------|--------|------------------------|
| **test_venda_futura_*** | `tests/e2e/test_venda_futura.py` | ⏳ Pendente | Apenas Cupom Venda |
| **test_venda_futura_domicilio_*** | `tests/e2e/test_venda_futura_domicilio.py` | ⏳ Pendente | Apenas Cupom Venda |
| **test_bonus_*** | `tests/e2e/test_bonus.py` | ⏳ Pendente | Apenas Cupom Venda |
| **test_troca_*** | `tests/e2e/test_troca.py` (se existir) | ⏳ Pendente | Apenas Cupom Venda |

**Nota:** Quando mexer nestes testes futuramente, atualizar este mapeamento.

---

## 🔍 Detalhamento por Tipo de Impressão

### 1. **Cupom de Venda** (Implementado em TODOS os testes)

**Contexto:** Aparece automaticamente após finalizar qualquer venda.

**Fluxo:**
```
Venda Finalizada
    ↓
Diálogo de Impressão Aparece (automático)
    ↓
┌─────────────────────────────┐
│ Deseja imprimir o cupom?    │
│                              │
│  [NÃO]           [SIM]      │
│ button2         button1     │
└─────────────────────────────┘
    ↓
Clica conforme configuração Dashboard
```

**Locators:**
- Botão SIM: `android:id/button1`
- Botão NÃO: `android:id/button2`

**Configuração Dashboard:**
- Campo JSON: `print_cupom_venda`
- Padrão: **false** (NÃO)
- Timeout: Configurável via `print_dialog_timeout` (padrão: 20s)

**Implementação:**
- Método: `VendaPage.responder_impressao()`
- Chamado em: `executar_venda_cliente()`, `executar_venda_consumidor()`

---

### 2. **Cupom de Troca** (Diálogo ANTES da Tela de Sucesso)

**Contexto:** Pode aparecer ANTES da tela de sucesso (depende de parâmetro do sistema).

**Fluxo:**
```
Cupom de Venda Respondido
    ↓
Parâmetro do Sistema Habilitado?
    ├─ SIM → Diálogo Cupom Troca aparece
    │          ↓
    │       Dashboard controla: SIM ou NÃO
    │          ↓
    │       Tela de Sucesso
    │
    └─ NÃO → Vai direto para Tela de Sucesso
                ↓
             (Botão pode aparecer na tela)
```

**Locators:**
- Botão SIM: `android:id/button1`
- Botão NÃO: `android:id/button2`

**Configuração Dashboard:**
- Campo JSON: `print_cupom_troca`
- Padrão: **false** (NÃO)

**Comportamento:**
- **Desmarcado:** Clica NÃO no diálogo
- **Marcado:** Clica SIM no diálogo

**Implementação:**
- Método: `VendaPage.responder_dialogo_cupom_troca()`
- Chamado em: `executar_venda_cliente()`, `executar_venda_consumidor()`
- Validação: Se não aparecer, ignora silenciosamente (log informativo)

---

### 3. **NFC-E** (Nota Fiscal do Consumidor Eletrônica)

**Contexto:** Primeiro botão na tela de sucesso (conforme XML).

**Posição XML:** Node index 12, bounds Y: 764

**Fluxo:**
```
Tela de Sucesso
    ↓
Dashboard Marcado?
    ├─ SIM → Clica no botão btn_impressao_nfce
    │          ↓
    │       Diálogo de Confirmação
    │          ↓
    │       Clica em "SIM" (button1)
    │
    └─ NÃO → Ignora o botão (não clica)
```

**Locators:**
- Botão Principal: `btn_impressao_nfce`
- Diálogo SIM: `android:id/button1`
- Diálogo NÃO: `android:id/button2`

**Configuração Dashboard:**
- Campo JSON: `print_nfce`
- Padrão: **false** (não clica no botão)

**Comportamento:**
- **Desmarcado:** Não clica no botão (ignora completamente)
- **Marcado:** Clica no botão + responde SIM no diálogo

**Implementação:**
- Método: `VendaSucessoPage.imprimir_nfce()`
- Chamado em: `processar_todas_impressoes()`
- Validação: Se botão não existir, ignora silenciosamente

---

### 4. **DANFE via Servidor** (Documento Auxiliar NF-e)

**Contexto:** Segundo botão na tela de sucesso (conforme XML).

**Posição XML:** Node index 13, bounds Y: 876

**Fluxo:**
```
Tela de Sucesso
    ↓
Dashboard Marcado?
    ├─ SIM → Clica no botão btn_nfe_print
    │          ↓
    │       Mensagem de Sucesso
    │          ↓
    │       Clica em "OK" (md_buttonDefaultPositive)
    │
    └─ NÃO → Ignora o botão (não clica)
```

**Locators:**
- Botão Principal: `btn_nfe_print`
- Botão OK (sucesso): `md_buttonDefaultPositive`

**Configuração Dashboard:**
- Campo JSON: `print_danfe`
- Padrão: **false** (não clica no botão)

**Comportamento:**
- **Desmarcado:** Não clica no botão (ignora completamente)
- **Marcado:** Clica no botão + clica OK na mensagem de sucesso

**Observação:** Não há diálogo de confirmação SIM/NÃO, apenas mensagem de sucesso.

**Implementação:**
- Método: `VendaSucessoPage.imprimir_danfe()`
- Chamado em: `processar_todas_impressoes()`
- Validação: Se botão não existir, ignora silenciosamente

---

### 5. **Cupom de Troca** (Botão NA Tela de Sucesso)

**Contexto:** Terceiro botão na tela de sucesso (conforme XML).

**Posição XML:** Node index 15, bounds Y: 1100

**Quando aparece:** Só aparece se o diálogo NÃO foi mostrado antes da tela de sucesso.

**Fluxo:**
```
Tela de Sucesso (cupom troca NÃO foi perguntado antes)
    ↓
Dashboard Marcado?
    ├─ SIM → Clica no botão btn_print_cupom_troca
    │          ↓
    │       Diálogo de Confirmação
    │          ↓
    │       Clica em "SIM" (button1)
    │
    └─ NÃO → Ignora o botão (não clica)
```

**Locators:**
- Botão Principal: `btn_print_cupom_troca`
- Diálogo SIM: `android:id/button1`
- Diálogo NÃO: `android:id/button2`

**Configuração Dashboard:**
- Campo JSON: `print_cupom_troca` (MESMO do diálogo)
- Padrão: **false** (não clica no botão)

**Comportamento:**
- **Desmarcado:** Não clica no botão (ignora completamente)
- **Marcado:** Clica no botão + responde SIM no diálogo

**Implementação:**
- Método: `VendaSucessoPage.imprimir_cupom_troca()`
- Chamado em: `processar_todas_impressoes()`
- Validação: Se botão não existir, ignora silenciosamente

---

## ⚙️ Configuração no Dashboard

### Interface Visual (Aba "Configurações")

```
┌────────────────────────────────────────────────────────────┐
│  Configurações de Impressão                                │
├────────────────────────────────────────────────────────────┤
│  ☐ Cupom de Venda (padrão após finalizar)                 │
│  ☐ NFC-E (Nota Fiscal Consumidor)                         │
│  ☐ DANFE via Servidor (NF-e)                              │
│  ☐ Cupom de Troca                                         │
│                                                            │
│  Timeout Diálogo (seg): [20]                              │
└────────────────────────────────────────────────────────────┘
```

**Nota:** "Cupom de Troca" controla tanto o diálogo (se aparecer antes) quanto o botão (se aparecer na tela de sucesso).

### Campos no settings.json

```json
{
  "print_cupom_venda": false,
  "print_nfce": false,
  "print_danfe": false,
  "print_cupom_troca": false,
  "print_dialog_timeout": 20
}
```

---

## 🔄 Fluxo Completo de Venda com Impressões (ORDEM CORRETA)

### Para testes **test_venda_consumidor** e **test_venda_cliente**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. VENDA EXECUTADA                                          │
│    - Produto adicionado                                     │
│    - Pagamento selecionado                                  │
│    - Venda finalizada                                       │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. CUPOM DE VENDA (diálogo automático)                      │
│    Método: executar_venda_*() → responder_impressao()       │
│    ☐ Desmarcado → Clica NÃO                                │
│    ✓ Marcado → Clica SIM                                   │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CUPOM DE TROCA (diálogo - se parâmetro habilitado)      │
│    Método: executar_venda_*() → responder_dialogo_cupom_troca()│
│    ☐ Desmarcado → Clica NÃO                                │
│    ✓ Marcado → Clica SIM                                   │
│    (Se não aparecer, segue para tela de sucesso)            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. TELA DE SUCESSO                                          │
│    Método: validar_sucesso_e_concluir() aguarda tela        │
│    - Mensagem: "Venda realizada com sucesso!"               │
│    - Botões disponíveis (ordem XML):                        │
│      • btn_impressao_nfce (Node 12, Y:764)                  │
│      • btn_nfe_print (Node 13, Y:876)                       │
│      • btn_print_cupom_troca (Node 15, Y:1100)*             │
│    *Só aparece se não foi perguntado antes                  │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. PROCESSAMENTO AUTOMÁTICO (ordem XML)                     │
│    Método: processar_todas_impressoes()                     │
│                                                              │
│ 5.1. NFC-E (primeiro botão)                                 │
│      Método: imprimir_nfce()                                │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + SIM                        │
│         ↓                                                    │
│ 5.2. DANFE (segundo botão)                                  │
│      Método: imprimir_danfe()                               │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + OK                         │
│         ↓                                                    │
│ 5.3. CUPOM TROCA (terceiro botão - se não foi antes)       │
│      Método: imprimir_cupom_troca()                         │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + SIM                        │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. CONCLUIR VENDA                                           │
│    Método: concluir_venda()                                 │
│    - Clica btn_confirmar_venda                              │
│    - Retorna para tela inicial                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Estrutura de Implementação

### 1. **Page Objects**

| Page Object | Arquivo | Responsabilidade |
|-------------|---------|------------------|
| **VendaPage** | `pages/venda_page.py` | • `responder_impressao()` - Cupom Venda<br>• `responder_dialogo_cupom_troca()` - Cupom Troca Diálogo<br>• `validar_sucesso_e_concluir()` - Processa tudo |
| **VendaSucessoPage** | `pages/venda_sucesso_page.py` | • `imprimir_nfce()` - NFC-E<br>• `imprimir_danfe()` - DANFE<br>• `imprimir_cupom_troca()` - Cupom Troca Botão<br>• `processar_todas_impressoes()` - Orquestra tudo |

### 2. **Métodos Principais**

```python
# VendaPage
def executar_venda_consumidor(self, codigo_produto: str = "123"):
    # ... executa venda ...
    self.responder_impressao()              # Cupom Venda (diálogo)
    self.responder_dialogo_cupom_troca()    # Cupom Troca (diálogo se aparecer)

def validar_sucesso_e_concluir(self):
    self.aguardar_texto("Venda realizada com sucesso!")

    # PROCESSA TODAS AS IMPRESSÕES DA TELA
    sucesso_page = VendaSucessoPage(self.driver)
    sucesso_page.processar_todas_impressoes()

    self.concluir_venda()

# VendaSucessoPage
def processar_todas_impressoes(self):
    self.imprimir_nfce()          # 1º - NFC-E
    self.imprimir_danfe()         # 2º - DANFE
    self.imprimir_cupom_troca()   # 3º - Cupom Troca Botão
```

---

## 🚨 Validação Automática de Botões

Todos os métodos verificam automaticamente se os botões existem:

```python
# Exemplo: imprimir_nfce()
if self.clicar_se_existir(self.BTN_IMPRESSAO_NFCE, tempo_espera=5):
    logger.info("Botão NFC-E clicado")
    # ... processa impressão
else:
    logger.info("Botão NFC-E não encontrado (pode não estar disponível)")
    # NÃO QUEBRA O TESTE - apenas ignora
```

**Resultado:**
- ✅ Se o botão **existir** → Processa conforme configuração
- ✅ Se o botão **NÃO existir** → Ignora silenciosamente
- ✅ **Nenhum teste quebra** independente da tela

---

## 📊 Matriz de Decisão

| Configuração Dashboard | Cupom Venda | Cupom Troca (Diálogo) | NFC-E | DANFE | Cupom Troca (Botão) |
|----------------------|-------------|----------------------|-------|-------|---------------------|
| **Tudo Desmarcado (padrão)** | NÃO | NÃO | Não clica | Não clica | Não clica |
| **Só Cupom Venda** | SIM | NÃO | Não clica | Não clica | Não clica |
| **Só Cupom Troca** | NÃO | SIM | Não clica | Não clica | SIM (se botão aparecer) |
| **Só NFC-E** | NÃO | NÃO | SIM | Não clica | Não clica |
| **NFC-E + DANFE** | NÃO | NÃO | SIM | SIM | Não clica |
| **Todos Marcados** | SIM | SIM | SIM | SIM | SIM (se botão aparecer) |

---

## 📚 Referências

- **XML da Tela Final:** `c:\Users\serverQAMobile\Desktop\ui4.xml`
- **Configuração Global:** `D:\PDV_AUTOMACAO\Testes_PDV\test_data.py`
- **Exemplo de Settings:** `D:\PDV_AUTOMACAO\settings_EXEMPLO.json`
- **Page Objects:** `D:\PDV_AUTOMACAO\Testes_PDV\pages\`
- **Dashboard:** `D:\PDV_AUTOMACAO\Gerador_EXE\runner\app_runner.py`
- **Documentação de Uso:** `D:\PDV_AUTOMACAO\CONFIGURACAO_IMPRESSAO.md`

---

## 🔄 Histórico de Atualizações

| Data | Versão | Descrição |
|------|--------|-----------|
| 2026-02-27 | 1.0 | Criação inicial do mapeamento |
| 2026-02-27 | 2.0 | Adicionada ordem XML correta dos botões |
| 2026-02-27 | 3.0 | ✅ **Implementação completa** em test_venda_consumidor e test_venda_cliente |
| 2026-03-04 | 3.1 | 📝 Atualização de documentação (versão sistema: 2.0.21) |

---

**Última Atualização:** 2026-03-04
**Versão do Sistema:** 2.0.21 (última compilação: 03/03/2026)
**Versão da Documentação:** 3.0 (Implementação completa em testes de venda)
**Status:** ✅ Funcional em test_venda_consumidor e test_venda_cliente

---

## ⏰ Próximos Passos

- [ ] Atualizar `test_venda_futura.py` com impressões da tela de sucesso
- [ ] Atualizar `test_venda_futura_domicilio.py` com impressões da tela de sucesso
- [ ] Atualizar `test_bonus.py` com impressões da tela de sucesso
- [ ] Verificar outros testes de venda e atualizar conforme necessário
- [ ] Atualizar este documento quando mexer em outros testes

**Nota:** Sempre que atualizar um novo teste, marcar neste documento e atualizar a tabela de testes implementados.
