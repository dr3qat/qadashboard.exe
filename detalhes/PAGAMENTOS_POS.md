# Pagamentos — Formas de Pagamento e Automação

## Contexto

O app PDV exibe **8 atalhos fixos** de formas de pagamento na tela de seleção. **Cada loja configura os seus próprios atalhos com nomes livres** no caixa.exe. Os testes usam descoberta dinâmica por tipo semântico — nunca hardcode do nome.

---

## Arquitetura: Discovery Completo → formas_pagamento.json

### Problema resolvido
`selecionar_pagamento("BANRI POS")` → quebra se a loja renomear o atalho.  
`selecionar_pagamento_por_tipo(TipoForma.POS_CREDITO)` → funciona em qualquer loja.  
`test_venda_personalizado.py` → parametrizado a partir do JSON, 1 caso por tipo_venda habilitado.

### Fluxo completo

```
1. EXE abre → após 5s verifica formas_pagamento.json
2. Se não existe E Appium online → roda test_discovery_completo.py em background
3. test_discovery_completo chama venda.descobrir_formas_completo()
4. Salva formas_pagamento.json ao lado do settings.json
5. Dashboard exibe os 8 slots preenchidos
6. Testes seguintes leem test_data.FORMAS_PAGAMENTO (carregado do JSON)
```

### Classes e structs (venda_page.py)

```python
class TipoForma:
    DINHEIRO      = "dinheiro"
    POS_DEBITO    = "pos_debito"
    POS_CREDITO   = "pos_credito"
    PIX           = "pix"
    PERSONALIZADO = "personalizado"
    TEF           = "tef"
    OUTRO         = "outro"

FormaInfo = namedtuple("FormaInfo", ["titulo", "tipo", "tem_parcelamento"])
```

---

## formas_pagamento.json — Estrutura

```json
{
  "_discovery_timestamp": "2026-04-15T13:57:00",
  "formas": [
    {
      "titulo": "DINHEIRO",
      "subtitulo": "Dinheiro",
      "detalhes": "A VISTA",
      "tipo_auto": "dinheiro",
      "habilitado": true,
      "parcelas": [],
      "tipos_venda": []
    },
    {
      "titulo": "BANRI POS",
      "subtitulo": "Cartão de Crédito/Débito",
      "detalhes": "CREDITO",
      "tipo_auto": "pos_credito",
      "habilitado": true,
      "parcelas": ["A Prazo 0 + 1", "A Prazo 0 + 2", "A Prazo 0 + 3"],
      "tipos_venda": []
    },
    {
      "titulo": "Pagamento Personalizado",
      "subtitulo": "Selecione manualmente",
      "detalhes": "",
      "tipo_auto": "personalizado",
      "habilitado": true,
      "parcelas": [],
      "tipos_venda": [
        {"nome": "A VISTA", "habilitado": true},
        {"nome": "BANRICOMPRAS DEBITO", "habilitado": true},
        {"nome": "A VISTA CREDITO", "habilitado": true, "parcelas": ["A Prazo 0 + 1"]}
      ]
    }
  ]
}
```

O arquivo pode ser editado manualmente para habilitar/desabilitar formas e tipos_venda.

---

## Regras de Classificação

Baseadas em campos **fixos do app** (não configuráveis pela loja):

| `txt_payment_subtitle` | `txt_payment_details` | TipoForma |
|---|---|---|
| `"Dinheiro"` | qualquer | `DINHEIRO` |
| `"Cartão de Crédito/Débito"` | contém `"DEBITO"`, sem `"TEF"` | `POS_DEBITO` |
| `"Cartão de Crédito/Débito"` | contém `"CREDITO"`, sem `"TEF"` | `POS_CREDITO` |
| `"Cartão de Crédito/Débito"` | contém `"TEF"` | `TEF` |
| `"BshopPix"` | qualquer | `PIX` |
| `"Selecione manualmente..."` | qualquer | `PERSONALIZADO` |
| outros | qualquer | `OUTRO` |

**`descobrir_formas_tipadas()`** — exclui TEF/PIX/PERSONALIZADO (só retorna POS/DINHEIRO para testes clássicos)  
**`descobrir_formas_completo()`** — inclui TODOS, persiste no JSON

**ARMADILHA:** `txt_payment_details` **não existe** em todos os cards (ex: "Pagamento Personalizado").  
Por isso os detalhes são buscados via XPath sibling ancorado no título.

```python
xpath_det = (
    '//android.widget.TextView[contains(@resource-id,"txt_payment_title")'
    f' and @text="{titulo}"]'
    '/following-sibling::android.widget.TextView'
    '[contains(@resource-id,"txt_payment_details")]'
)
```

---

## Tela de Atalhos (estrutura XML)

**RecyclerView:** `recycler_payment_methods`

Cada card:
```
CardView (clicável)
  ViewGroup
    ImageView  → resource-id: "payment_icon"
    TextView   → resource-id: "txt_payment_title"     (nome livre, ex: "BANRI POS")
    TextView   → resource-id: "txt_payment_subtitle"  (tipo fixo, ex: "Cartão de Crédito/Débito")
    TextView   → resource-id: "txt_payment_details"   (movimentos — NEM SEMPRE PRESENTE)
```

O CardView pai é `clickable="true"`. Os TextViews internos têm `clickable="false"` mas `ver_e_clicar_texto()` funciona pois o tap cai nas coordenadas do pai clicável.

---

## Bottom Sheet de Personalizado

Aparece após clicar o card "Pagamento Personalizado" + `btn_proceed`.

**Lista de tipos:** `recycler_tipo_venda`  
Cada item: `LinearLayout (clickable=true)` → `TextView` com nome do tipo_venda

**Se o tipo_venda selecionado é crédito** → `recycler_plano_venda` aparece para seleção de parcela.

**Fechar sheet sem selecionar:** `btn_close` ou `voltar_tela()`

```python
# Uso nos testes
venda.selecionar_personalizado("A VISTA")                        # sem parcela
venda.selecionar_personalizado("A VISTA CREDITO", "A Prazo 0 + 1")  # com parcela
```

---

## Bottom Sheet de Parcelamento (Crédito POS)

Aparece **depois** de clicar `btn_proceed` no card de crédito — nunca antes.

**Container:** `design_bottom_sheet`  
**Lista:** `recycler_plano_venda`

Cada linha:
```
LinearLayout (clickable=true) ← ESTE é o clicável
  RadioButton → resource-id: "radio_option" (clickable=false)
  TextView    → resource-id: "txt_option_title" (texto da parcela, ex: "A Prazo 0 + 1")
```

**Detecção do sheet (8s timeout):**
```python
XPATH_QUALQUER_PARCELA = '//android.widget.TextView[contains(@resource-id,"txt_option_title") and contains(@text,"A Prazo")]'
```

**Seleção de parcela específica:**
```python
XPATH_PARCELA = '//android.widget.TextView[contains(@resource-id,"txt_option_title") and @text="{parcela}"]'
```

---

## API dos Testes

### POS Débito / Crédito — `selecionar_pagamento_por_tipo`

```python
from pages.venda_page import TipoForma

venda.selecionar_pagamento_por_tipo(TipoForma.POS_DEBITO,  com_cliente=False)
venda.selecionar_pagamento_por_tipo(TipoForma.POS_CREDITO, com_cliente=False, parcela="A Prazo 0 + 1")
venda.selecionar_pagamento_por_tipo(TipoForma.DINHEIRO,    com_cliente=True)
```

### Personalizado — `selecionar_personalizado`

```python
# tipos_venda e parcelas variam por loja — leia do formas_pagamento.json
venda.selecionar_personalizado(tipo_venda, parcela=None)
```

### Discovery manual (debug / mapeamento)

```python
# Apenas POS/DINHEIRO — uso em testes rápidos
formas = venda.descobrir_formas_tipadas()
# → {"pos_debito": FormaInfo(...), "pos_credito": FormaInfo(...)}

# TODOS os 8 atalhos + Personalizado + parcelas → salva JSON
formas = venda.descobrir_formas_completo()

# Parcelas disponíveis — quando bottom sheet de crédito está aberto
parcelas = venda.obter_parcelas_disponiveis()
```

---

## Cache de Sessão

`_formas_cache` (variável de módulo em `venda_page.py`):
- `None` no início de cada sessão pytest (`pytest_sessionstart` em conftest.py)
- Preenchido na primeira chamada a `descobrir_formas_tipadas()`
- Reutilizado em todos os testes subsequentes

Para forçar redescoberta:
```python
import pages.venda_page as vp
vp._formas_cache = None
```

**formas_pagamento.json** é persistente entre sessões — sobrevive ao restart do EXE.

---

## Testes Existentes

| Arquivo | Tipo | Parcela | Comportamento |
|---|---|---|---|
| `test_venda_pos_debito.py` | `POS_DEBITO` | — | Skip se POS Débito não existe |
| `test_venda_pos_cred1x.py` | `POS_CREDITO` | `PARCELAS_CREDITO[0]` ou `"A Prazo 0 + 1"` | Skip se não existe |
| `test_venda_pos_cred2x.py` | `POS_CREDITO` | `PARCELAS_CREDITO[1]` ou `"A Prazo 0 + 2"` | Skip se não existe |
| `test_venda_pos_cred3x.py` | `POS_CREDITO` | `PARCELAS_CREDITO[2]` ou `"A Prazo 0 + 3"` | Skip se não existe |
| `test_venda_pos_credito_parcelas.py` | `POS_CREDITO` | dinâmico | Mapeia + testa 1ª parcela disponível |
| `test_discovery_completo.py` | — (mapeia) | — | Salva formas_pagamento.json |
| `test_venda_personalizado.py` | `PERSONALIZADO` | dinâmico | 1 caso por tipo_venda habilitado |

Todos: consumidor (sem cliente), produto `PRODUCT_CODE_SALE`.

---

## Override Manual em settings.json (opcional)

Se configurado, pula descoberta dinâmica para POS:

```json
{
  "forma_dinheiro": "DINHEIRO",
  "forma_debito": "BANRI DEB POS",
  "forma_credito": "BANRI POS",
  "parcelas_credito": ["A Prazo 0 + 1", "A Prazo 0 + 2"]
}
```

`formas_pagamento.json` sempre tem precedência para `FORMAS_PAGAMENTO` e Personalizado.
