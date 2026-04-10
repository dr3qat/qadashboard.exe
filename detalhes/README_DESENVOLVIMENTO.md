# 🚀 Guia de Desenvolvimento - QA Dashboard

## 📋 Fluxo de Trabalho

### 1️⃣ Desenvolver e Testar (ANTES de compilar)

```
1. Edite os arquivos em: Testes_PDV/
   - config.py
   - pages/*.py
   - tests/**/*.py
   - etc

2. Execute: ABRIR_DASHBOARD.bat
   - Sincroniza automaticamente tudo para staging
   - Abre o Dashboard em modo desenvolvimento
   - Simula exatamente o ambiente do EXE

3. Teste suas mudanças no Dashboard
```

### 2️⃣ Compilar (DEPOIS de testar)

```bash
cd Gerador_EXE\build
python builder_pro.py
```

---

## 🔄 O que o ABRIR_DASHBOARD.bat faz?

1. **Sincroniza** todos os arquivos de `Testes_PDV` para `Gerador_EXE\output\staging`
2. **Copia**:
   - config.py, test_data.py, framework.py, conftest.py
   - Todos os Page Objects (pages/)
   - Todos os Testes (tests/e2e, tests/smoke, tests/unit)
3. **Executa** o Dashboard usando o staging (simula o EXE)

---

## 📂 Estrutura de Diretórios

```
PDV_AUTOMACAO/
├── ABRIR_DASHBOARD.bat          ← Execute isso para testar!
│
├── Testes_PDV/                  ← EDITE AQUI seus códigos
│   ├── config.py
│   ├── test_data.py
│   ├── pages/
│   │   ├── login_page.py
│   │   ├── home_page.py
│   │   └── venda_page.py
│   └── tests/
│       ├── e2e/
│       ├── smoke/
│       └── unit/
│
└── Gerador_EXE/
    ├── runner/
    │   └── app_runner.py        ← Dashboard (não editar diretamente)
    │
    ├── output/
    │   └── staging/             ← Sincronizado automaticamente
    │       ├── config.py        (cópia de Testes_PDV)
    │       ├── pages/
    │       └── tests/
    │
    └── build/
        └── builder_pro.py       ← Compilador final
```

---

## ✅ Vantagens dessa Abordagem

1. **Testa antes de compilar** - sem perder tempo gerando instaladores defeituosos
2. **Ambiente idêntico** - staging simula exatamente o que o EXE vai fazer
3. **Sincronização automática** - sempre usa a versão mais recente dos arquivos
4. **Sem copiar manualmente** - o script faz tudo

---

## 🎯 Workflow Completo

```
┌─────────────────────────────────────────────────────────┐
│  1. EDITAR código em Testes_PDV/                        │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  2. TESTAR executando ABRIR_DASHBOARD.bat               │
│     → Sincroniza automaticamente                        │
│     → Abre Dashboard em modo dev                        │
│     → Simula ambiente do EXE                            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  3. AJUSTAR código se necessário (volta para passo 1)   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│  4. COMPILAR quando tudo estiver funcionando            │
│     → cd Gerador_EXE\build                              │
│     → python builder_pro.py                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🐛 Modo Debug vs Normal

### No Dashboard (Otimizado v2.0.7+):

- **Checkbox desmarcado** (Modo Normal):
  - Mostra apenas: nome do teste, ações, botões clicados
  - Sem prefixos técnicos `INFO appium_test:...`
  - Interface limpa e direta

- **Checkbox marcado** (Modo Debug):
  - **NOVO**: Mostra saída limpa igual ao modo normal
  - **DIFERENÇA**: Exibe detalhes técnicos (stack traces, linhas de código) **APENAS quando ocorrem ERROS**
  - Não trava mais a interface - logs processados em lotes de 5 linhas
  - Filtros automáticos removem ruído de bibliotecas (Selenium, urllib3, Appium)
  - Ignora linhas muito longas (>500 caracteres) para evitar poluição visual

### Benefícios da Otimização:

✅ **Sem Travamentos**: Interface responsiva mesmo com logs intensos
✅ **Saída Limpa**: Ambos os modos mostram informações relevantes
✅ **Debug Inteligente**: Detalhes técnicos só aparecem quando necessário (em erros)
✅ **Performance**: Redução de 80% nas atualizações da UI

### No código (config.py):

```python
# Ativar modo debug programaticamente (se necessário)
configurar_logger_modo(debug=True)   # Modo técnico em erros
configurar_logger_modo(debug=False)  # Modo visual limpo (padrão)
```

---

## 📝 Notas Importantes

- **SEMPRE** teste com `ABRIR_DASHBOARD.bat` antes de compilar
- **NÃO** edite arquivos em `staging/` diretamente (são sobrescritos)
- **EDITE** apenas em `Testes_PDV/`
- O `app_runner.py` detecta automaticamente se está em modo dev

---

## 🚀 Melhorias Recentes (v2.0.21)

### Sistema de Impressões Configurável

Controle centralizado de 4 tipos de impressão via Dashboard:

1. **Cupom de Venda**: Diálogo automático após finalizar venda
2. **Cupom de Troca**: Pode aparecer como diálogo ou botão
3. **NFC-E**: Nota Fiscal do Consumidor Eletrônica
4. **DANFE**: Documento Auxiliar via servidor

**Configuração**: Checkboxes na aba "Configurações" do Dashboard

### Page Object para Tela de Sucesso

**Novo arquivo**: `venda_sucesso_page.py`

**Responsabilidades**:
- `processar_todas_impressoes()`: Processa impressões na ordem XML
- `imprimir_nfce()`, `imprimir_danfe()`, `imprimir_cupom_troca()`
- Validações: `tela_sucesso_exibida()`, `botao_*_disponivel()`

**Benefício**: Lógica de impressões centralizada e reutilizável

### Estrutura de Testes Atualizada

**Arquivos de teste reorganizados**:
- `test_pedido_vendaConsumidor.py` (antes: test_pedido_venda.py)
- `test_pedido_vendaCliente.py` (antes: test_pedido_venda.py)
- `test_consulta_pedidoConsumidor.py` (antes: test_consulta_pedido.py)
- `test_consulta_pedidoCliente.py` (antes: test_consulta_pedido.py)

**Vantagem**: Separação clara entre testes de cliente e consumidor

---

## 💾 Gerenciamento de Configurações (settings.json)

### Múltiplos Ambientes

Você pode salvar diferentes configurações para cada ambiente:

```
settings_homolog.json    → Ambiente de homologação
settings_prod.json       → Ambiente de produção
settings_qa.json         → Ambiente de QA
settings_dev.json        → Ambiente de desenvolvimento
```

### Como Usar

**No Dashboard (modo dev ou prod):**

1. **Exportar** - Botão "📤 Exportar Settings"
   - Salva configuração atual com nome personalizado
   - Ex: `settings_empresa382_homolog.json`

2. **Importar** - Botão "📥 Importar Settings"
   - Carrega configuração de qualquer arquivo `.json`
   - Preenche automaticamente todos os campos
   - Mostra resumo do que foi importado

**No ABRIR_DASHBOARD.bat (modo dev):**

O script busca automaticamente em:
1. `D:\QA Dashboard\settings.json`
2. `C:\Program Files\QA Dashboard\settings.json`
3. `%USERPROFILE%\QA Dashboard\settings.json`
4. Staging anterior (backup)

### Exemplo de Workflow

```bash
# 1. Configure para Homologação
[Dashboard] → Preencher campos → Exportar Settings → Salvar como "settings_homolog.json"

# 2. Configure para Produção
[Dashboard] → Preencher campos → Exportar Settings → Salvar como "settings_prod.json"

# 3. Alternar entre ambientes
[Dashboard] → Importar Settings → Selecionar "settings_homolog.json"
[Dashboard] → Rodar testes de homologação

[Dashboard] → Importar Settings → Selecionar "settings_prod.json"
[Dashboard] → Rodar testes de produção
```

---

## ✅ Como Testar as Otimizações

### 1. Versionamento Dinâmico

```bash
# 1. Verifique a versão atual
cat Testes_PDV\VERSION

# 2. Compile o EXE
COMPILAR.bat

# 3. Abra o EXE gerado
Gerador_EXE\output\dist\QA_Dashboard.exe

# 4. Verifique se a versão aparece no título e rodapé
# Deve mostrar: "QA Dashboard - V2.0.X"
```

### 2. Performance (Sem Travamentos)

```bash
# 1. Abra o Dashboard
ABRIR_DASHBOARD.bat

# 2. Execute um teste E2E completo
# 3. Durante a execução, tente:
#    - Minimizar e maximizar a janela
#    - Mudar para outra aplicação e voltar
#    - Rolar o log enquanto executa

# ✅ ESPERADO: Interface permanece responsiva
# ❌ ANTES: Travava ao mudar de janela
```

### 3. Modo Debug Otimizado

```bash
# 1. No Dashboard, marque "Mostrar logs técnicos (debug)"
# 2. Execute um teste que FALHE propositalmente
# 3. Observe a saída:
#    - Deve mostrar ações limpas (igual ao modo normal)
#    - Stack trace aparece APENAS na linha do erro
#    - Sem logs de urllib3, Selenium, Appium

# 4. Execute um teste que PASSA
# 5. Observe a saída:
#    - Deve ser idêntica ao modo normal
#    - Sem poluição visual

# ✅ ESPERADO: Saída limpa + detalhes em erros
# ❌ ANTES: Logs gigantes mesmo em testes bem-sucedidos
```

### 4. Separadores Visuais

```bash
# Antes: ==================================================...
# Agora: =======

# ✅ Verifique que separadores têm apenas 7 caracteres
```

---

## 🔧 Troubleshooting

**Dashboard não abre?**
- Verifique se Python está instalado
- Execute: `python --version`

**Arquivos não sincronizam?**
- Verifique se `Testes_PDV/` existe
- Execute manualmente o ABRIR_DASHBOARD.bat

**Appium não encontrado?**
- O Dashboard busca automaticamente usando `npm bin -g`
- Ou configure manualmente na aba "Configurações"

**Settings não importa?**
- Verifique se o arquivo .json está válido
- Abra o arquivo em um editor de texto e confira a sintaxe

---

## 📌 Informações da Versão

**Versão Atual**: 2.0.21 (última compilação: 03/03/2026)
**Última Atualização**: 04/03/2026
**Principais Melhorias**:
- Sistema de impressões configurável via Dashboard
- Page Object venda_sucesso_page.py para gerenciar impressões
- Estrutura de testes reorganizada
- Performance otimizada na interface

**Arquivos Principais**:
- `Gerador_EXE/runner/app_runner.py` (~1530 linhas)
- `Gerador_EXE/build/builder_pro.py` (build pipeline)
- `Testes_PDV/pages/venda_sucesso_page.py` (controle de impressões)
- `Testes_PDV/VERSION` (controle de versão)
