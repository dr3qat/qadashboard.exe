# 🚀 Getting Started - Guia de Início Rápido

Este guia vai te ajudar a configurar o ambiente e executar seu primeiro teste em menos de 15 minutos.

---

## ✅ Pré-requisitos

### Software Necessário

1. **Python 3.8 ou superior**
   - Download: https://www.python.org/downloads/
   - Verificar: `python --version`

2. **Java JDK 11 ou superior**
   - Download: https://www.oracle.com/java/technologies/downloads/
   - Verificar: `java -version`

3. **Node.js 16 ou superior**
   - Download: https://nodejs.org/
   - Verificar: `node --version`

4. **Android SDK**
   - Via Android Studio: https://developer.android.com/studio
   - Configure ANDROID_HOME nas variáveis de ambiente

5. **Appium 2.0**
   - Instalação: `npm install -g appium`
   - Driver: `appium driver install uiautomator2`
   - Verificar: `appium --version`

### Hardware Necessário

- **Dispositivo Android** (físico ou emulador)
  - Android 8.0+ (API 26+)
  - Modo Desenvolvedor ativado
  - Depuração USB habilitada
- **Cabo USB** (para dispositivo físico)

---

## 📦 Instalação

### Passo 1: Preparar o Projeto

```bash
# Navegar para o diretório do projeto
cd D:\PDV_AUTOMACAO\Testes_PDV

# (Opcional) Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Passo 2: Instalar Dependências

```bash
# Instalar pacotes Python
pip install -r requirements.txt

# Verificar instalação
pytest --version
```

### Passo 3: Configurar Variáveis de Ambiente

**Windows:**
```cmd
# ANDROID_HOME
setx ANDROID_HOME "C:\Users\%USERNAME%\AppData\Local\Android\Sdk"

# JAVA_HOME
setx JAVA_HOME "C:\Program Files\Java\jdk-11"
```

**Linux/Mac:**
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export ANDROID_HOME=$HOME/Android/Sdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### Passo 4: Configurar Dados de Teste

Edite o arquivo `test_data.py`:

```python
# Servidor
SERVER_IP = "192.168.1.100"  # IP do seu servidor PDV
SERVER_PORT = "8080"

# Credenciais
COMPANY = "1"
USER = "admin"
PASSWORD = "senha123"

# Dados para testes
CUSTOMER_ID = "1"  # CPF ou ID de cliente cadastrado
PRODUCT_CODE = "123"  # Código de produto válido
```

---

## 🎯 Executando Seu Primeiro Teste

### Teste 1: Testes Unitários (Rápido - 10s)

```bash
# Executar todos os testes unitários
pytest tests/unit/ -v

# Resultado esperado:
# ======================== 200 passed in 8.50s ========================
```

**O que validar:**
- ✅ Todos os 200 testes devem passar
- ✅ Tempo de execução < 10 segundos
- ✅ Nenhum erro de import

### Teste 2: Smoke Test (Requer dispositivo - 5 min)

#### Pré-requisitos
1. Conectar dispositivo Android via USB
2. Habilitar "Depuração USB"
3. Instalar o APK do PDV

#### Executar Appium Server

```bash
# Terminal 1 - Iniciar Appium
appium

# Deve aparecer:
# [Appium] Welcome to Appium v2.x.x
# [Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

#### Verificar Dispositivo

```bash
# Terminal 2 - Listar dispositivos
adb devices

# Resultado esperado:
# List of devices attached
# ABC123DEF456    device
```

#### Executar Smoke Test

```bash
# Executar smoke tests
pytest tests/smoke/ -v -m smoke

# Resultado esperado:
# ======================== 10 passed in 4m 30s ========================
```

**O que será testado:**
1. ✅ App abre corretamente
2. ✅ Login funciona
3. ✅ Elementos básicos visíveis
4. ✅ Navegação funciona
5. ✅ Servidor respondendo
6. ✅ Venda básica funciona
7. ✅ Cancelamento funciona
8. ✅ Pedido básico funciona
9. ✅ Navegação entre módulos
10. ✅ Botão back funciona

---

## 🎨 Visualizando Relatórios

### Relatório Allure

```bash
# 1. Executar testes gerando resultados Allure
pytest tests/smoke/ -v -m smoke --alluredir=logs/allure-results

# 2. Abrir relatório no navegador
allure serve logs/allure-results
```

**Recursos do Allure:**
- 📊 Gráficos de sucesso/falha
- 📸 Screenshots de falhas
- 📝 Logs detalhados
- ⏱️ Tempo de execução
- 📈 Histórico de execuções

---

## 🐛 Problemas Comuns

### Erro: "No module named 'appium'"

```bash
# Solução: Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Could not find Appium server"

```bash
# Solução: Verificar se Appium está rodando
appium

# Em outro terminal:
netstat -an | find "4723"
```

### Erro: "Device not found"

```bash
# Solução 1: Verificar conexão USB
adb devices

# Solução 2: Reiniciar ADB
adb kill-server
adb start-server
adb devices
```

### Erro: "Session not created"

```bash
# Solução: Reinstalar driver
appium driver uninstall uiautomator2
appium driver install uiautomator2
```

### Testes falhando com "Timeout"

**Solução**: Aumentar tempos de espera em `config.py`:

```python
DEFAULT_WAIT = 15  # Aumentar de 10 para 15
```

---

## 📚 Próximos Passos

Agora que você já executou seus primeiros testes, explore:

1. **[Arquitetura](ARCHITECTURE.md)** - Entenda como o projeto está organizado
2. **[Testes Unitários](UNIT_TESTS.md)** - Aprenda a criar testes unitários
3. **[Smoke Tests](SMOKE_TESTS.md)** - Entenda os smoke tests
4. **[Testes E2E](E2E_TESTS.md)** - Guia completo dos testes E2E
5. **[Page Objects](PAGE_OBJECTS.md)** - Referência dos Page Objects

---

## 🎓 Comandos Úteis

```bash
# Executar teste específico
pytest tests/e2e/test_venda_consumidor.py -v

# Executar com marcador
pytest -v -m venda

# Parar no primeiro erro
pytest tests/smoke/ -x

# Executar em paralelo (requer pytest-xdist)
pytest tests/unit/ -n 4

# Ver duração dos testes mais lentos
pytest tests/ --durations=10

# Executar com verbose máximo
pytest tests/smoke/ -vv

# Limpar cache do pytest
pytest --cache-clear
```

---

## ✅ Checklist de Verificação

Antes de começar a trabalhar com testes, certifique-se de que:

- [ ] Python 3.8+ instalado
- [ ] Java JDK 11+ instalado
- [ ] Node.js 16+ instalado
- [ ] Appium 2.0+ instalado
- [ ] ADB instalado e no PATH
- [ ] Dispositivo Android conectado
- [ ] Depuração USB habilitada
- [ ] APK do PDV instalado
- [ ] Dependências Python instaladas (`pip install -r requirements.txt`)
- [ ] Testes unitários passando (`pytest tests/unit/ -v`)
- [ ] Appium Server iniciando sem erros (`appium`)
- [ ] `adb devices` mostra dispositivo conectado
- [ ] Smoke tests passando (`pytest tests/smoke/ -v -m smoke`)

---

**Precisando de ajuda?** Entre em contato com a equipe de QA Mobile.

**Última atualização**: 24/02/2026
