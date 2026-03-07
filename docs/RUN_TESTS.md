# 🏃 Executar Testes - Guia Rápido

Guia passo a passo para executar os testes do projeto Loto.

## 🎯 Começo Rápido

### 1. Navegar até a pasta do projeto
```powershell
cd "c:\Users\SAMSUNG\OneDrive\Meus Documentos\Python Projects\Loto"
```

### 2. Instalar ferramentas de teste (primeira vez)
```powershell
pip install pytest pytest-flask pytest-cov
```

**OU** instalar todas as dependências:
```powershell
pip install -r requirements.txt
```

### 3. Executar todos os testes
```powershell
pytest
```

## 📊 Comando Básico vs Completo

### Básico (mínimo)
```powershell
pytest
```

### Com Verbosidade (recomendado)
```powershell
pytest -v
```

### Com Cobertura
```powershell
pytest --cov=app --cov-report=html
```

### Completo (tudo)
```powershell
pytest -v --cov=app --cov-report=html --tb=short
```

---

## 🔍 Exemplos de Execução

### Testar apenas validators
```powershell
pytest tests/test_validators.py -v
```

### Testar apenas CSV handler
```powershell
pytest tests/test_csv_handler.py -v
```

### Testar apenas stats
```powershell
pytest tests/test_stats_calculator.py -v
```

### Testar apenas rotas
```powershell
pytest tests/test_routes.py -v
```

### Um teste específico
```powershell
pytest tests/test_validators.py::TestValidarNumeros::test_numeros_validos -v
```

### Parar no primeiro erro
```powershell
pytest -x
```

### Levar aos testes falhados anteriores
```powershell
pytest --lf -v
```

### Parar após 3 erros
```powershell
pytest --maxfail=3 -v
```

---

## 📈 Gerar Relatório de Cobertura

### 1. Executar com cobertura
```powershell
pytest --cov=app --cov-report=html
```

### 2. Abrir relatório no navegador
Vai criar pasta `htmlcov/`. Abra: `htmlcov/index.html`

### 3. Ver cobertura por módulo
```powershell
pytest --cov=app --cov-report=term-missing
```

Mostra qual linhas não estão cobertas.

---

## ✅ Resultado Esperado

Se tudo correr bem, você verá:

```
============================= test session starts ==============================
platform win32 -- Python 3.11.x, pytest-7.4.0, ...
rootdir: C:\Users\SAMSUNG\...\Loto, configfile: pytest.ini
collected 74 items

tests/test_validators.py ............                                    [ 16%]
tests/test_csv_handler.py ..................                            [ 40%]
tests/test_stats_calculator.py ................                         [ 61%]
tests/test_routes.py ...........................                        [ 95%]

============================== 74 passed in X.XXs =============================
```

---

## 🐛 Troubleshooting

### Problema: "pytest: command not found"
```powershell
# Solução: Instalar pytest
pip install pytest pytest-flask pytest-cov
```

### Problema: ModuleNotFoundError: No module named 'app'
```powershell
# Solução: Executar do diretório correto
cd "c:\Users\SAMSUNG\OneDrive\Meus Documentos\Python Projects\Loto"
pytest
```

### Problema: CSV test file not found
```powershell
# Solução: Teste de arquivo CSV depende da fixture
# Não modificar código do teste, fixture cria automaticamente
pytest -v
```

### Problema: "permission denied" ao criar arquivo temp
```powershell
# Solução: Permissão de escrita na pasta temp
# Usar conta com privilégios ou ajustar permissões
```

### Problema: Alguns testes não executam
```powershell
# Solução: Verificar síntaxe dos nomes dos testes
# Devem começar com "test_"
pytest -v --collect-only  # Mostra todos os coletados
```

---

## 🎓 Interpretando Resultados

### Status Verde ✅
```
tests/test_validators.py::TestValidarNumeros::test_numeros_validos PASSED
```
= Teste passou

### Status Vermelho ❌
```
tests/test_validators.py::TestValidarNumeros::test_invalido FAILED
AssertionError: assert False == True
```
= Teste falhou. Ler mensagem de erro.

### Status Pulado ⏭️
```
tests/test_routes.py::TestRotaPrincipal::test_aleatorio SKIPPED
```
= Teste foi pulo (pode ter `@pytest.mark.skip`)

---

## 📝 Opções Úteis de Linha de Comando

| Comando | O que faz |
|---------|-----------|
| `pytest -v` | Mostra cada teste individualmente |
| `pytest -s` | Mostra prints durante execução |
| `pytest -x` | Para no primeiro erro |
| `pytest -k validar` | Executa testes com "validar" no nome |
| `pytest --collect-only` | Lista testes sem executar |
| `pytest --tb=short` | Erro resumido |
| `pytest --tb=long` | Erro completo |
| `pytest -m unit` | Executa testes com marca @pytest.mark.unit |
| `pytest --lf` | Executa últimos testes falhados |
| `pytest --maxfail=3` | Para após 3 erros |

---

## 🚀 Script Automático

Crie arquivo `run_tests.ps1`:

```powershell
# run_tests.ps1
param(
    [switch]$Coverage,
    [switch]$Html,
    [switch]$Verbose
)

# Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Cyan
pip install -r requirements.txt

# Executar testes
if ($Coverage) {
    Write-Host "Executando testes com cobertura..." -ForegroundColor Green
    pytest --cov=app --cov-report=html --cov-report=term-missing $(if ($Verbose) {'-v'})
    
    if ($Html) {
        Write-Host "Abrindo relatório HTML..." -ForegroundColor Green
        Start-Process htmlcov\index.html
    }
} else {
    Write-Host "Executando testes..." -ForegroundColor Green
    pytest $(if ($Verbose) {'-v'})
}

Write-Host "Pronto!" -ForegroundColor Green
```

Executar:
```powershell
# Básico
.\run_tests.ps1

# Com cobertura
.\run_tests.ps1 -Coverage

# Com cobertura e HTML
.\run_tests.ps1 -Coverage -Html

# Com verbosidade
.\run_tests.ps1 -Verbose
```

---

## 🎯 Cenários Comuns

### Cenário 1: Primeiro teste
```powershell
cd "c:\Users\SAMSUNG\OneDrive\Meus Documentos\Python Projects\Loto"
pip install -r requirements.txt
pytest -v
# Esperar 70+ testes passarem ✅
```

### Cenário 2: Testes em desenvolvimento
```powershell
# Modificou arquivo, quer testar rápido
pytest tests/test_validators.py::TestValidarNumeros -v
```

### Cenário 3: Erro em teste específico
```powershell
# Qual teste falhou? Veja com modo verbose
pytest tests/test_csv_handler.py -v
# Depois de corrigir:
pytest tests/test_csv_handler.py::TestSalvarDados -v
```

### Cenário 4: Análise de cobertura
```powershell
pytest --cov=app --cov-report=html
# Abrir htmlcov/index.html para ver visualmente
```

### Cenário 5: Debugging
```powershell
# Modo com prints
pytest -s -v

# Modo com debugger
pytest --pdb -v
# Abre Python debugger em erro
```

---

## 💾 Salvar Resultados

### Salvar em arquivo de texto
```powershell
pytest -v > test_results.txt 2>&1
```

### Salvar relatório JUnit XML
```powershell
pytest --junit-xml=test_report.xml
```

### Salvar em JSON
```powershell
pytest --json-report --json-report-file=report.json
```

---

## 🔗 Referências Rápidas

- **Docs pytest**: https://docs.pytest.org/
- **pytest-flask**: https://pytest-flask.readthedocs.io/
- **pytest-cov**: https://pytest-cov.readthedocs.io/

---

**Dica**: Salve este arquivo e use como referência quando executar testes!
