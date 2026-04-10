# Configuração de Impressões - Testes E2E PDV

## Visão Geral

O sistema de impressões permite controlar globalmente **4 tipos diferentes de impressão** através do Dashboard, sem necessidade de modificar cada teste individualmente.

---

## 🎯 Tipos de Impressão Disponíveis

| Tipo | Quando Aparece | Controle Dashboard | Padrão |
|------|----------------|-------------------|--------|
| **1. Cupom de Venda** | Automático após finalizar venda | `print_cupom_venda` | ☐ false (NÃO) |
| **2. Cupom de Troca (Diálogo)** | Pode aparecer ANTES da tela de sucesso* | `print_cupom_troca` | ☐ false (NÃO) |
| **3. NFC-E** | Botão na tela de sucesso | `print_nfce` | ☐ false (não clica) |
| **4. DANFE** | Botão na tela de sucesso | `print_danfe` | ☐ false (não clica) |
| **5. Cupom de Troca (Botão)** | Botão na tela de sucesso** | `print_cupom_troca` | ☐ false (não clica) |

\* *Depende de parâmetro no sistema. Se habilitado, aparece como diálogo antes da tela de sucesso.*
\*\* *Se não foi perguntado antes, o botão pode aparecer na tela de sucesso.*

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

**Nota:** Cupom de Troca controla tanto o diálogo (se aparecer antes) quanto o botão (se aparecer na tela de sucesso).

### Como Usar o Dashboard

1. **Abra o Dashboard** (QA Dashboard v2.0.21)
2. Vá na aba **"Configurações"**
3. Role até **"Configurações de Impressão"**
4. **Marque/Desmarque** os checkboxes conforme necessário
5. Ajuste o timeout se necessário (padrão: 20 segundos)
6. Clique em **"💾 Salvar Configurações"**

---

## 📋 Detalhamento de Cada Impressão

### 1. **Cupom de Venda** (Impressão Padrão)

**Quando aparece:** Automaticamente após finalizar qualquer venda.

**Comportamento:**
- ☐ **Desmarcado (padrão):** Clica em **NÃO** no diálogo
- ✓ **Marcado:** Clica em **SIM** no diálogo

**Locators:**
- Botão SIM: `android:id/button1`
- Botão NÃO: `android:id/button2`

**Fluxo:**
```
Venda Finalizada
    ↓
Diálogo Automático: "Deseja imprimir?"
    ↓
Dashboard desmarcado → Clica NÃO
Dashboard marcado → Clica SIM
```

---

### 2. **Cupom de Troca** (Diálogo ou Botão)

**IMPORTANTE:** Este é o mesmo controle para duas situações diferentes.

#### **Situação A: Diálogo ANTES da Tela de Sucesso**

**Quando aparece:** Se o sistema tiver **parâmetro habilitado**, o diálogo aparece ANTES da tela de sucesso.

**Comportamento:**
- ☐ **Desmarcado (padrão):** Clica em **NÃO** no diálogo
- ✓ **Marcado:** Clica em **SIM** no diálogo

**Locators:**
- Botão SIM: `android:id/button1`
- Botão NÃO: `android:id/button2`

**Fluxo:**
```
Cupom de Venda Respondido
    ↓
Diálogo Cupom Troca (se parâmetro habilitado)
    ↓
Dashboard desmarcado → Clica NÃO
Dashboard marcado → Clica SIM
    ↓
Tela de Sucesso
```

#### **Situação B: Botão NA Tela de Sucesso**

**Quando aparece:** Se o diálogo NÃO foi mostrado antes, o botão pode aparecer na tela de sucesso.

**Comportamento:**
- ☐ **Desmarcado (padrão):** **Não clica** no botão (ignora completamente)
- ✓ **Marcado:** Clica no botão `btn_print_cupom_troca` → Responde **SIM** no diálogo

**Locators:**
- Botão Principal: `btn_print_cupom_troca`
- Diálogo SIM: `android:id/button1`

**Fluxo:**
```
Tela de Sucesso (cupom troca NÃO foi perguntado antes)
    ↓
Dashboard desmarcado → Ignora botão Cupom Troca
Dashboard marcado → Clica botão → Diálogo → Clica SIM
```

---

### 3. **NFC-E** (Nota Fiscal do Consumidor Eletrônica)

**Quando aparece:** Primeiro botão na tela de sucesso (conforme XML).

**Comportamento:**
- ☐ **Desmarcado (padrão):** **Não clica** no botão (ignora completamente)
- ✓ **Marcado:** Clica no botão `btn_impressao_nfce` → Responde **SIM** no diálogo

**Locators:**
- Botão Principal: `btn_impressao_nfce`
- Diálogo SIM: `android:id/button1`

**Posição XML:** Node index 12, bounds Y: 764

---

### 4. **DANFE via Servidor** (Documento Auxiliar NF-e)

**Quando aparece:** Segundo botão na tela de sucesso (conforme XML).

**Comportamento:**
- ☐ **Desmarcado (padrão):** **Não clica** no botão (ignora completamente)
- ✓ **Marcado:** Clica no botão `btn_nfe_print` → Clica **OK** na mensagem de sucesso

**Locators:**
- Botão Principal: `btn_nfe_print`
- Botão OK: `md_buttonDefaultPositive`

**Posição XML:** Node index 13, bounds Y: 876

**Observação:** Não há diálogo SIM/NÃO, apenas mensagem de sucesso.

---

## 🔄 Fluxo Completo de Venda com Impressões (ORDEM CORRETA)

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
│    ☐ Desmarcado → Clica NÃO                                │
│    ✓ Marcado → Clica SIM                                   │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CUPOM DE TROCA (diálogo - se parâmetro habilitado)      │
│    ☐ Desmarcado → Clica NÃO                                │
│    ✓ Marcado → Clica SIM                                   │
│    (Se não aparecer, segue para tela de sucesso)            │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. TELA DE SUCESSO                                          │
│    - Mensagem: "Venda realizada com sucesso!"               │
│    - Botões disponíveis (ordem XML):                        │
│      • btn_impressao_nfce (Node 12)                         │
│      • btn_nfe_print (Node 13)                              │
│      • btn_print_cupom_troca (Node 15)*                     │
│    *Só aparece se não foi perguntado antes                  │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. PROCESSAMENTO AUTOMÁTICO (ordem XML)                     │
│                                                              │
│ 5.1. NFC-E (primeiro botão)                                 │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + SIM                        │
│         ↓                                                    │
│ 5.2. DANFE (segundo botão)                                  │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + OK                         │
│         ↓                                                    │
│ 5.3. CUPOM TROCA (terceiro botão - se não foi antes)       │
│      ☐ Desmarcado → Ignora                                 │
│      ✓ Marcado → Clica botão + SIM                        │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. CONCLUIR VENDA                                           │
│    - Clica btn_confirmar_venda                              │
│    - Retorna para tela inicial                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Uso nos Testes

### Exemplo Completo (Ordem Correta Implementada)

```python
from pages.venda_page import VendaPage
from pages.venda_sucesso_page import VendaSucessoPage

def test_venda_completa_com_impressoes(self, driver_logado):
    """Teste completo com processamento automático de todas as impressões."""
    venda_page = VendaPage(driver_logado)
    sucesso_page = VendaSucessoPage(driver_logado)

    # 1. Executa venda (cupom venda + cupom troca diálogo respondidos automaticamente)
    venda_page.executar_venda_consumidor()

    # 2. Valida sucesso
    assert sucesso_page.tela_sucesso_exibida(), "Tela de sucesso não apareceu"

    # 3. Processa TODAS as impressões na ORDEM CORRETA (NFC-E, DANFE, Cupom Troca)
    sucesso_page.processar_todas_impressoes()

    # 4. Confirma venda
    sucesso_page.concluir_venda()
```

**Observação:** O método `executar_venda_consumidor()` já trata:
- Cupom de venda (diálogo automático)
- Cupom de troca (diálogo antes da tela, se aparecer)

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

## 📁 Campos no settings.json

```json
{
  "print_cupom_venda": false,
  "print_nfce": false,
  "print_danfe": false,
  "print_cupom_troca": false,
  "print_dialog_timeout": 20
}
```

### Exemplo com Todas Habilitadas

```json
{
  "print_cupom_venda": true,
  "print_nfce": true,
  "print_danfe": true,
  "print_cupom_troca": true,
  "print_dialog_timeout": 30
}
```

---

## 📝 Page Objects Envolvidos

| Page Object | Arquivo | Responsabilidade |
|-------------|---------|------------------|
| **VendaPage** | `pages/venda_page.py` | Responde diálogos: Cupom Venda + Cupom Troca (antes tela) |
| **BonusPage** | `pages/bonus_page.py` | Responde diálogos: Cupom Venda + Cupom Troca (antes tela) |
| **VendaFuturaPage** | `pages/venda_futura_page.py` | Responde diálogos: Cupom Venda + Cupom Troca (antes tela) |
| **VendaSucessoPage** | `pages/venda_sucesso_page.py` | Processa botões NA ORDEM: NFC-E, DANFE, Cupom Troca |

---

## 🚨 Observações Importantes

### Diferenças de Comportamento

| Tipo | Aparece Sempre? | Posição | Se Desmarcado | Se Marcado |
|------|----------------|---------|---------------|------------|
| **Cupom Venda** | ✅ Sim (diálogo) | Após finalizar venda | Clica NÃO | Clica SIM |
| **Cupom Troca (Diálogo)** | ❓ Depende do parâmetro | Antes da tela sucesso | Clica NÃO | Clica SIM |
| **NFC-E** | ❌ Não (botão) | 1º botão (Node 12, Y:764) | Ignora botão | Clica botão + SIM |
| **DANFE** | ❌ Não (botão) | 2º botão (Node 13, Y:876) | Ignora botão | Clica botão + OK |
| **Cupom Troca (Botão)** | ❌ Não (botão) | 3º botão (Node 15, Y:1100) | Ignora botão | Clica botão + SIM |

### Ordem de Processamento (CRÍTICO)

A ordem é baseada no **XML da tela** (posição Y dos bounds):

1. **NFC-E** - Y: 764 (primeiro)
2. **DANFE** - Y: 876 (segundo)
3. **ENVIAR EMAIL** - Y: 988 (ignorado pelo Dashboard)
4. **CUPOM TROCA** - Y: 1100 (terceiro)
5. **CONCLUIR** - Y: 0,0 (precisa scroll)

### Validação de Botões

Os métodos verificam automaticamente se os botões estão visíveis:
- Se o botão **não existir** na tela → Ignora silenciosamente (log informativo)
- Se o botão **existir** → Processa conforme configuração

---

## 📚 Referências

- **Mapeamento Completo:** `D:\PDV_AUTOMACAO\MAPEAMENTO_IMPRESSOES.md`
- **XML da Tela Final:** `c:\Users\serverQAMobile\Desktop\ui4.xml`
- **Configuração Global:** `D:\PDV_AUTOMACAO\Testes_PDV\test_data.py`
- **Exemplo de Settings:** `D:\PDV_AUTOMACAO\settings_EXEMPLO.json`
- **Page Objects:** `D:\PDV_AUTOMACAO\Testes_PDV\pages\`
- **Dashboard:** `D:\PDV_AUTOMACAO\Gerador_EXE\runner\app_runner.py`

---

**Última Atualização:** 2026-03-04
**Versão do Sistema:** 2.0.21 (última compilação: 03/03/2026)
**Versão da Documentação:** 3.0 (Ordem correta conforme XML)
