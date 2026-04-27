# Log de Mudanças - Testes PDV

Registro diário de alterações, correções e melhorias realizadas no projeto.

---

## 2026-04-16 — Qualidade e Manutenção: Auto-Sync + Timeout + Teardown + Rerunfailures

### Escopo: melhorias de infraestrutura de testes (zero risco, zero reescrita)

---

### P1 — app_runner.py: auto-sync staging antes de cada run

- Método `_sincronizar_staging()` adicionado à classe `TestRunnerApp`
- Executa `robocopy Testes_PDV/ staging/ /MIR` antes de cada `rodar_processo()`
- Variáveis de módulo: `_DEV_MODE` e `_TESTES_PDV_DIR` (try/except para compatibilidade com EXE)
- Resultado: editar apenas `Testes_PDV/` — staging nunca mais precisa ser tocado diretamente

---

### P2 — pytest.ini: timeout global + marker negativos

- `timeout = 180` — pytest-timeout mata teste travado em 3min (Appium hang protection)
- Marker `negativos` declarado (evitava `PytestUnknownMarkWarning` nos testes de borda)
- Impacto: zero em unit tests (completam em <1s); salva runs E2E de travamento eterno

---

### P3 — requirements.txt: novos pacotes pinados

- `pytest-timeout==2.3.1` — implementa `timeout = 180` do pytest.ini
- `pytest-rerunfailures==14.0` — disponível para re-rodar flaky tests com `--reruns N`
- Instalar: `pip install -r requirements.txt`

---

### P4 — conftest.py: teardown automático em driver_logado

- `driver_logado` mudou de `return driver` para `yield driver` + bloco de teardown
- Teardown: pressiona `driver.back()` até `home_page.tela_inicial_exibida()` (max 4x, timeout 2s)
- `try/except` garante que teardown nunca interrompe o runner
- Resultado: testes isolados — próximo teste sempre começa na home, mesmo se anterior falhou

---

### P5 — CLAUDE.md + docs: limpeza e atualização

- Removida regra "Espelhar em staging" do checklist de smoke (item 2 → eliminado, 3-8 → 2-7)
- Estrutura de diretórios: staging marcado como "somente leitura / auto-sincronizado"
- §12.1 atualizado com documentação de timeout, teardown e rerunfailures
- detalhes/README_DESENVOLVIMENTO.md: atualizado para refletir auto-sync

---

## 2026-04-15 — Discovery Completo de Atalhos + Dashboard UI

### Escopo: mapeamento automático de todos os 8 atalhos de pagamento

---

### P1 — venda_page.py: descoberta completa de formas

**Novos métodos:**
- `descobrir_formas_completo()` — mapeia TODOS os cards (inclui Personalizado + parcelas POS) → salva `formas_pagamento.json`
- `_descobrir_personalizado()` — abre bottom sheet `recycler_tipo_venda`, lê tipos_venda, clica credito para ler `recycler_plano_venda`
- `_descobrir_parcelas_pos_credito(titulo)` — abre bottom sheet de crédito, lê parcelas, fecha
- `selecionar_personalizado(tipo_venda, parcela=None)` — para tests usarem Personalizado
- `_classificar_tipo_completo()` — sem exclusões (TEF/PIX incluídos no JSON)
- `_salvar_formas_pagamento(formas)` — serializa em `formas_pagamento.json` ao lado do `settings.json`
- `_sincronizar_settings_de_formas(formas)` — backward compat: atualiza forma_debito/credito/dinheiro no settings.json

**Novos locators:**
- `RECYCLER_TIPO_VENDA = "recycler_tipo_venda"` — lista de tipos no Personalizado
- `BTN_FECHAR_SHEET = "btn_close"` — fecha bottom sheets

**TipoForma expandido:** adicionados `PERSONALIZADO`, `TEF`, `OUTRO`

---

### P2 — test_data.py: carregamento do formas_pagamento.json

- `_load_formas_pagamento()` — lê `formas_pagamento.json` do mesmo dir do `settings.json`
- `TestData.FORMAS_PAGAMENTO: list` — carregado na inicialização
- Removido: todo código `IS_CI` / GitHub Actions (projeto só roda localmente com device físico)

---

### P3 — Novos testes E2E

**`test_discovery_completo.py`:**
- Navega até tela de pagamento → chama `descobrir_formas_completo()` → volta sem finalizar
- Usado pelo dashboard em auto-descoberta no startup

**`test_venda_personalizado.py`:**
- Lê `test_data.FORMAS_PAGAMENTO` em import time → gera um `pytest.param` por tipo_venda habilitado
- Skip automático se `formas_pagamento.json` ausente ou Personalizado não habilitado

---

### P4 — app_runner.py: UI e auto-descoberta no startup

**UI — "Atalhos de Pagamento":**
- Substituiu seções redundantes por 1 seção com 8 slots fixos (Atalho 1–8)
- Cada slot: Entry (nome), Label (tipo + parcelas/tipos_venda), Checkbutton (habilitado)
- Botões: "🔄 Descobrir Atalhos", "🔃 Recarregar", "📝 Abrir JSON", "💾 Salvar"

**Auto-descoberta no startup:**
- `_verificar_autodescoberta_formas()` — checa `formas_pagamento.json` após 5s
- Se já mapeado → mostra status verde
- Se Appium online → dispara discovery (pytest `test_discovery_completo` em thread daemon)
- Se Appium offline → retry a cada 10s, máximo 6× (60s), depois alerta vermelho
- `_autodescobrir_formas_bg()` — passa credenciais reais como env vars (TEST_SERVER_IP etc.) → pytest não usa settings.json placeholder do staging

**Arquivos modificados (ambas as cópias):**
- `Testes_PDV/pages/venda_page.py` + staging
- `Testes_PDV/test_data.py` + staging
- `Testes_PDV/tests/e2e/vendas/test_discovery_completo.py` (novo) + staging
- `Testes_PDV/tests/e2e/vendas/test_venda_personalizado.py` (novo) + staging
- `Testes_PDV/tests/e2e/vendas/test_venda_pos_cred1x/2x/3x.py` (ajuste PARCELAS_CREDITO)
- `Gerador_EXE/runner/app_runner.py`

---

## 2026-04-14 — Otimização de Login e Impressões

### Ganho estimado: ~3-4s por teste E2E (impressões todas False)

---

### P1 — login_page.py: timeout de detecção reduzido

**Mudança:** `esta_logado(timeout=5)` → `timeout=3` (default + chamada em `garantir_login`).

**Motivo:** `esta_logado` faz 2 chamadas sequenciais de `texto_exibido`. Quando NÃO logado, desperdiçava 10s (5+5) antes de iniciar o login. Com 3s: 6s total → economiza 4s no primeiro teste da sessão.

**Impacto quando já logado:** zero — `texto_exibido` retorna em ~0.5s ao encontrar o elemento.

---

### P2 — venda_page.py: sleep/timeout adaptativos em impressões

**Mudança em `responder_impressao()`:**
- `PRINT_CUPOM_VENDA=False`: timeout 20s → **12s**, sleep 2s → **0.5s**
- `PRINT_CUPOM_VENDA=True`: mantém valores originais (timeout `PRINT_DIALOG_TIMEOUT`, sleep 2s)

**Mudança em `responder_dialogo_cupom_troca()`:**
- Dialog aparece + `PRINT_CUPOM_TROCA=False`: sleep 2s → **0.5s**
- Dialog aparece + `PRINT_CUPOM_TROCA=True`: mantém sleep 2s

**Motivo:** Dialog de cupom sempre aparece rapidamente. Clicar NÃO fecha o dialog instantaneamente — sleep de 2s era desperdício puro. O próximo passo (`validar_sucesso_e_concluir`) usa `aguardar_texto`, então não precisa de sleep antes.

---

### P3 — venda_sucesso_page.py: fast-path em processar_todas_impressoes()

**Mudança:** Bloco de verificação no topo do método:
```python
if not (PRINT_NFCE or PRINT_DANFE or PRINT_CUPOM_TROCA or PRINT_GIFTBACK):
    return  # pula sem verificar nenhum botão na tela
```

**Motivo:** Quando tudo desabilitado, os 4 métodos individuais já retornavam cedo, mas geravam 4 chamadas + 4 logs. O fast-path torna o comportamento explícito e mais rápido.

**Arquivos modificados (ambas as cópias):**
- `Testes_PDV/pages/login_page.py`
- `Testes_PDV/pages/venda_page.py`
- `Testes_PDV/pages/venda_sucesso_page.py`
- `Gerador_EXE/output/staging/pages/login_page.py`
- `Gerador_EXE/output/staging/pages/venda_page.py`
- `Gerador_EXE/output/staging/pages/venda_sucesso_page.py`

---

## 2026-04-10 — Refatoração de Performance e Estrutura

### Ganho estimado: ~90s por suite E2E completa

---

### F1 — requirements.txt: removidos pacotes CI/inúteis
**Removidos:** `pytest-xdist`, `execnet`, `playwright`, `pytest-playwright`, `pytest-base-url`, `python-telegram-bot`, `pyee`
**Motivo:** CI nunca será usado. Pacotes playwright/telegram não são referenciados em nenhum teste.
**Impacto:** instalação mais rápida, menos conflitos de dependência.

---

### F1 — config.py: cache em `discover_target_app()`
**Mudança:** dict global `_discover_cache` — segunda chamada por device_id retorna do cache sem ADB.
**Ganho:** ~3-5s por sessão (evita `adb pm list packages` duplicado no startup).

---

### F1 — app_runner.py: mascarar credenciais em logs
**Mudança:** `_CHAVES_SENSIVEIS` filtra `TEST_PASSWORD`, `TEST_USER`, `TEST_COMPANY`, `TEST_SERVER_IP` do dict de env antes de qualquer log.
**Motivo:** segurança — senha não aparece mais em `execucao_tecnica.log`.

---

### F2 — Sleeps → waits explícitos (6 arquivos de page objects)

| Arquivo | Sleeps removidos/reduzidos | Ganho |
|---|---|---|
| `estoque_page.py` | 7 sleeps (1-3s) removidos | ~10s |
| `opcoes_item_page.py` | 8 sleeps (1-1.5s) removidos, 4 reduzidos | ~9s |
| `venda_futura_page.py` | 4 sleeps (1-3s) removidos/reduzidos | ~8s |
| `troca_page.py` | 4 sleeps (0.5-2s) removidos/reduzidos | ~6s |
| `consulta_pedido_page.py` | 4 sleeps (2-5s) → waits explícitos | ~14s |
| `base_page.py` | 3 sleeps(0.3s) removidos, 2 reduzidos 0.3→0.1 | ~4s |

**Regra aplicada:** sleeps antes de métodos com `tempo_espera` interno → removidos. Sleeps proteção de animação/servidor → mantidos.

---

### F3 — conftest.py: limpeza e unificação

1. **`_NO_WINDOW`**: removida definição local duplicada, importado de `config.py`
2. **`IS_CI`**: removido — projeto é 100% local
3. **`_criar_ambiente_allure`**: `Ambiente=Local` fixo, removidas linhas GitHub env vars
4. **`_criar_driver_appium()`**: helper criado com toda lógica comum de driver
5. **`driver` / `driver_limpo`**: refatorados para usar `_criar_driver_appium()`
6. **`pytest_collection_modifyitems`**: warning automático se teste em `ORDEM_TESTES` não for coletado
7. **`import sys`**: removido (não usado após remoção de `_NO_WINDOW` local)

---

### Testes unitários corrigidos
- `test_config_unit.py`: `setup_method` limpa `_discover_cache` entre testes (isolamento)
- `test_troca_page_unit.py`: mock de `encontrar_por_id` adicionado ao test de `selecionar_primeira_nota`
- `test_venda_futura_page_unit.py`: expected `tempo_espera` atualizado de 2 → 4

**Resultado final:** 236/236 unitários passando.

---

## 2026-03-10 (Segunda-feira)

### ✅ Correção dos Testes de Troca

**Problema:** Testes de troca quebrando ao procurar `switch_bonus` - elemento não encontrado.

**Causa Raiz:** Código estava pulando validação do popup "Sucesso!" após confirmar a devolução, impedindo progressão do fluxo.

**Correções Aplicadas:**

1. **`pages/troca_page.py`**
   - ✅ Criado método `validar_sucesso_troca()` - valida e fecha popup "Sucesso!" da troca
   - ✅ Reescrito `executar_troca()` para CLIENTE - apenas devolução, sem venda pós-troca
   - ✅ Reescrito `executar_troca_consumidor()` - devolução + venda com bônus (fluxo completo)
   - ✅ Simplificado `selecionar_pagamento_bonus()` - removida espera redundante
   - ✅ Documentado `confirmar_dialogos()` com fluxo detalhado

2. **`tests/e2e/test_troca_cliente.py`**
   - ✅ Removida validação de venda (não faz venda pós-troca)
   - ✅ Atualizada descrição para refletir fluxo correto
   - ✅ Ajustado docstring do teste

3. **`tests/e2e/test_troca_consumidor.py`**
   - ✅ Separada validação em steps distintos
   - ✅ Adicionado step de concluir venda
   - ✅ Atualizada descrição do teste

**Resultado:** Testes de troca agora seguem fluxo legado que funciona corretamente.

**Referência:** Scripts legados `trocaCliente.py` e `trocaConsumidor.py`

**Ajuste Adicional (09:20 - INCORRETO, revertido):**
- ❌ Tornado método `validar_sucesso_troca()` OPCIONAL - **ERRO**: No legado é OBRIGATÓRIO!

**Correção Final (09:30 - Baseado 100% no Legado):**
- ✅ **REESCRITO COMPLETO** seguindo EXATAMENTE os legados `trocaCliente.py` e `trocaConsumidor.py`
- ✅ `validar_sucesso_troca()` agora é **OBRIGATÓRIO** - aguarda "Sucesso!" por até 30s (como `validar_texto_e_clicar_por_id`)
- ✅ `clicar_avancar()` com sleep 1.5s antes do click (evita clique fantasma)
- ✅ `finalizar_venda()` com scroll até "Finalizar" (como legado linha 82-83)
- ✅ `voltar_com_confirmacao()` - volta e confirma se aparecer popup SIM
- ✅ Fluxo `executar_troca_consumidor()` segue exatamente linhas 72-89 do legado
- ✅ Fluxo `executar_troca()` (cliente) segue exatamente linhas 67-70 do legado
- ✅ Sleep de 3s ANTES de selecionar bônus (linha 79 do legado - CRUCIAL!)
- ✅ Todos os delays e ordem de passos IDÊNTICOS ao legado

**Arquivos Modificados:**
- `Testes_PDV/pages/troca_page.py` - Métodos reescritos baseado no legado
- `Testes_PDV/tests/e2e/test_troca_consumidor.py` - Validações corretas
- `Testes_PDV/tests/e2e/test_troca_cliente.py` - Fluxo simplificado (só devolução)

**Verificado:** ✅ Todos os arquivos editados estão em `D:\PDV_AUTOMACAO\Testes_PDV\` (produção)

**Problema Adicional - Bônus Já Usado (10:00):**

**Sintoma:** Teste `test_troca_consumidor_sucesso` funciona manual, mas automatizado dá erro "bônus já usado".

**Causa Raiz:**
- Teste pegava a última nota fiscal da lista (pode ser de execução anterior)
- Se nota já teve bônus usado → erro ao tentar usar novamente
- Em teste manual, sempre se usa nota nova/válida

**Solução Aplicada:**
- ✅ Adicionada **PRÉ-CONDIÇÃO** no teste: cria venda NOVA antes da troca
- ✅ Garante que sempre há nota fiscal com bônus válido disponível
- ✅ Teste agora pode rodar **isoladamente** sem depender de test_venda_consumidor_sucesso
- ✅ Documentação atualizada explicando a pré-condição

**Fluxo Corrigido:**
```python
0. PRE-CONDICAO: Criar venda consumidor (nota nova)
1. Iniciar troca
2. Selecionar nota mais recente (acabou de criar)
3. Fazer devolução
4. Usar bônus na venda pós-troca ✅ (bônus válido garantido)
```

**Arquivo Modificado:**
- `tests/e2e/test_troca_consumidor.py` - Revertida pré-condição (problema era outro)

**Problema REAL Identificado (10:15):**

**Erro ocorre em:** Ao clicar em "Finalizar venda" → Sistema diz "bônus já usado"

**Causa Raiz:**
- Mesmo rodando test_venda_consumidor.py ANTES, a lista de notas não estava atualizada
- Estava pegando nota ANTIGA (com bônus já usado) em vez da nota NOVA (recém-criada)
- Faltava delay para servidor processar e retornar lista atualizada

**Solução Aplicada:**
- ✅ Aumentado delay após "Consultar" de 1s para **5s** (aguardar servidor)
- ✅ Aumentado delay antes de selecionar nota de 1s para **2s**
- ✅ Adicionado delay de 1s após selecionar nota (aguardar detalhes carregar)
- ✅ Adicionados logs detalhados em pontos críticos para debug
- ✅ Verificação se switch_bonus existe antes de tentar clicar
- ✅ Documentação explicando que primeira nota = mais recente

**Arquivos Modificados:**
- `pages/troca_page.py` - Delays aumentados + logs detalhados + verificações

---

### 🧹 Sistema de Limpeza de Cache

**Problema:** Após compilação, testes antigos (removidos) ainda apareciam no menu do executável.

**Causa Raiz:** Cache Python (`.pyc` e `__pycache__`) não era limpo completamente antes de compilar/instalar.

**Correções Aplicadas:**

1. **`limpar_cache_completo.py`** (NOVO)
   - ✅ Script Python robusto para limpeza recursiva completa
   - ✅ Remove `.pytest_cache/` recursivamente
   - ✅ Remove `__pycache__/` em TODAS as pastas recursivamente
   - ✅ Remove `*.pyc` recursivamente
   - ✅ Limpa `allure-results/`
   - ✅ Remove `.version_atual` para forçar redetecção
   - ✅ Relatório detalhado do que foi removido

2. **`clean_cache.bat`** (ATUALIZADO)
   - ✅ Agora chama `limpar_cache_completo.py` automaticamente
   - ✅ Fallback para limpeza básica se Python não disponível

3. **`install_update.bat`** (ATUALIZADO)
   - ✅ Integrado script Python para limpeza robusta
   - ✅ Fallback para limpeza básica se necessário

4. **`scripts/post_install.bat`** (ATUALIZADO)
   - ✅ Hook pós-instalação melhorado
   - ✅ Tenta usar script Python primeiro
   - ✅ Limpa `allure-results` também

**Resultado:** Cache sempre limpo antes de compilar/instalar, garantindo que apenas testes atuais apareçam no menu.

**Processo:** `python limpar_cache_completo.py` → Build/Compile → Distribuir

**Arquivos movidos para pasta raiz:**
- ✅ `limpar_cache_completo.py` movido para `D:\PDV_AUTOMACAO\` (não deve ser compilado)
- ✅ `MUDANCAS.md` movido para `D:\PDV_AUTOMACAO\` (log de desenvolvimento)
- ✅ Scripts `.bat` atualizados para referenciar `../limpar_cache_completo.py`

**Motivo:** Pasta `Testes_PDV/` é ambiente de produção. Arquivos de desenvolvimento/logs devem ficar na raiz.

---

## Template para Próximas Entradas

```markdown
## YYYY-MM-DD (Dia da Semana)

### 📌 Título da Mudança

**Problema:** Descrição do problema encontrado

**Causa Raiz:** Causa identificada

**Correções Aplicadas:**

1. **`arquivo.py`**
   - ✅ Mudança 1
   - ✅ Mudança 2

**Resultado:** Resultado obtido

**Referência:** Links, issues, docs relacionados

---
```

## Legenda

- ✅ Concluído
- 🚧 Em progresso
- ⚠️ Requer atenção
- 🐛 Bug fix
- ✨ Nova feature
- 🧹 Limpeza/refatoração
- 📝 Documentação
- ⚡ Performance
- 🔒 Segurança
