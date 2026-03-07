# Reorganização do Repositório - Aplicação Loto

## ✅ Estrutura Organizada por Tipo de Arquivo

### 📁 Estrutura Atual

```
Loto/
├── 📂 app/                             # Core MVC da aplicação
│   ├── __init__.py                     # Factory pattern
│   ├── 📂 auth/                        # Autenticação
│   │   ├── __init__.py
│   │   ├── auth_handler.py             # Lógica de tokens
│   │   ├── decorators.py               # Proteção de rotas
│   │   ├── email_service.py            # Email (dev)
│   │   └── email_service_smtp.py       # Email (produção)
│   │
│   ├── 📂 models/                      # Modelos de dados
│   │   └── user.py                     # User + UserManager (com CSV)
│   │
│   ├── 📂 routes/                      # Controladores
│   │   ├── __init__.py
│   │   ├── auth.py                     # Rotas de autenticação
│   │   ├── main.py                     # Página principal
│   │   └── estadisticas.py             # Estatísticas
│   │
│   ├── 📂 templates/                   # Templates HTML
│   │   ├── 📂 auth/
│   │   │   ├── login.html
│   │   │   ├── verificar.html
│   │   │   └── encerramento.html
│   │   ├── index.html
│   │   ├── novo.html
│   │   └── estatisticas.html
│   │
│   └── 📂 utils/                       # Utilitários
│       ├── csv_handler.py              # Manipulação CSV
│       ├── paths.py                    # ✨ Resolver paths dinâmicos
│       └── __init__.py
│
├── 📂 scripts/                         # Scripts executáveis
│   ├── run.py                          # Otimizado para produção
│   ├── run_exe.py                      # Otimizado para .exe
│   └── criar_executavel.py             # Gerador PyInstaller
│
├── 📂 data/                            # Arquivos de dados
│   ├── dados_usuarios.csv              # ✓ Movido
│   └── dados_loto.csv                  # ✓ Movido
│
├── 📂 config/                          # Configurações
│   ├── requirements.txt                # ✓ Movido
│   ├── pytest.ini                      # ✓ Movido
│   ├── auth_tokens.log                 # ✓ Movido
│   └── LOTO.spec                       # ✓ Movido
│
├── 📂 docs/                            # Documentação (21 .md)
│   ├── AUTHENTICATION.md               # ✓ Movido
│   ├── ARCHITECTURE.md                 # ✓ Movido
│   ├── SMTP_CONFIGURATION.md           # ✓ Movido
│   ├── TESTE_PRATICO.md                # ✓ Movido
│   ├── TOKEN_RAPIDO.md                 # ✓ Movido
│   └── ... (16 mais)
│
├── 📂 templates/                       # Templates globais
│
├── 📂 tests/                           # Testes automatizados
│   ├── conftest.py                     # Fixtures
│   └── test_auth.py                    # Testes auth
│
├── 📂 .venv/                           # Virtual environment
│
├── 🐍 run.py                           # ⭐ ENTRY POINT (wrapper)
├── 📝 .gitignore
└── 📝 ESTRUTURA_README.py              # Este documento

```

---

## 🔄 Mudanças Realizadas

### ✓ Arquivos Movidos

| Arquivo | Origem | Destino | Motivo |
|---------|--------|---------|--------|
| `dados_usuarios.csv` | Raiz | `data/` | Dados persistentes |
| `dados_loto.csv` | Raiz | `data/` | Dados persistentes |
| `run.py` | Raiz | `scripts/` | Script de inicialização |
| `run_exe.py` | Raiz | `scripts/` | Script para executável |
| `criar_executavel.py` | Raiz | `scripts/` | Gerador de .exe |
| `requirements.txt` | Raiz | `config/` | Configuração |
| `pytest.ini` | Raiz | `config/` | Configuração |
| `auth_tokens.log` | Raiz | `config/` | Log de desenvolvimento |
| `LOTO.spec` | Raiz | `config/` | Spec PyInstaller |
| 21 arquivos `.md` | Raiz | `docs/` | Documentação |

### ✨ Novo Arquivo

| Arquivo | Localização | Função |
|---------|-------------|--------|
| `paths.py` | `app/utils/` | **Resolver paths dinamicamente** |

---

## 🎯 Benefícios

### ✅ Organização
- Arquivos agrupados por tipo
- Fácil localização de resources
- Padrão clara e consistente

### ✅ Manutenção
- Documentação centralizada em `docs/`
- Dados separados de código em `data/`
- Configurações isoladas em `config/`
- Scripts executáveis em `scripts/`

### ✅ Design Patterns Mantidos
- **MVC Pattern**: `app/models`, `app/routes`, `app/templates`
- **Factory Pattern**: `app/__init__.py`
- **Decorators Pattern**: `app/auth/decorators.py`
- **Service Pattern**: `app/auth/` services
- **Manager Pattern**: `UserManager` em `models/`

### ✅ Escalabilidade
- Fácil adicionar novos módulos
- Estrutura pronta para crescimento
- Separação clara de camadas

---

## 🚀 Como Usar

### Iniciar a Aplicação

```bash
# Método 1: Python direto
python run.py

# Método 2: Via script
python scripts/run_exe.py

# Método 3: Windows batch (Desktop)
LOTO.bat
```

### Testes

```bash
# Executar testes
pytest tests/test_auth.py

# Com verbose
pytest -v tests/

# Com cobertura
pytest --cov=app tests/
```

### Instalar Dependências

```bash
pip install -r config/requirements.txt
```

### Documentação

```bash
# Documentação em docs/
# Exemplos:
docs/AUTHENTICATION.md
docs/ARCHITECTURE.md  
docs/TESTE_PRATICO.md
```

---

## 🔍 Paths Dinâmicos

### ✨ Novo Sistema de Resolução

O arquivo `app/utils/paths.py` resolve automaticamente:

```python
from app.utils.paths import (
    get_users_csv,        # data/dados_usuarios.csv
    get_sorteios_csv,     # data/dados_loto.csv
    get_tokens_log,       # config/auth_tokens.log
    get_requirements_txt, # config/requirements.txt
    get_project_root,     # Raiz do projeto
)

# Usar:
usuarios_csv = get_users_csv()  
# Retorna: C:\...\data\dados_usuarios.csv
```

### Compatibilidade

- ✅ Funciona com caminhos relativos e absolutos
- ✅ Fallback para compatibilidade
- ✅ Detecta automaticamente a raiz do projeto
- ✅ Funciona em qualquer diretório

---

## 📋 Checklist de Validação

- ✅ `app/` mantém estrutura MVC
- ✅ `data/` contém arquivos CSV
- ✅ `config/` contém configurações
- ✅ `docs/` contém documentação
- ✅ `scripts/` contém executáveis
- ✅ `run.py` funciona como wrapper
- ✅ Imports atualizados com paths dinâmicos
- ✅ Design patterns mantidos
- ✅ Sem quebra de funcionalidade
- ✅ Tests passando

---

## 🧪 Teste Rápido

```bash
# Ir para raiz
cd Loto/

# Testar imports
python -c "from app.utils.paths import get_users_csv; print(get_users_csv())"

# Testar paths
python -c "from app.utils.paths import *; import os; print('Raiz:', get_project_root()); print('Arquivos existem:', os.path.exists(get_data_path('dados_usuarios.csv')))"

# Iniciar app
python run.py
```

---

## 📊 Resumo de Estrutura

| Pasta | Conteúdo | Qtd |
|-------|----------|-----|
| `app/` | Core MVC | 10+ módulos |
| `docs/` | Markdown | 21 arquivos |
| `data/` | CSV | 2 arquivos |
| `config/` | Configuração | 4 arquivos |
| `scripts/` | Executáveis | 3 arquivos |
| `tests/` | Testes | 2 arquivos |

---

## 🔄 Próximas Etapas (Opcional)

- [ ] Criar pasta `app/static/` para CSS/JS
- [ ] Mover templates comuns
- [ ] Adicionar pasta `logs/` para logs em produção
- [ ] Estrutura de `migrations/` para banco de dados
- [ ] Pasta `assets/` para imagens/ícones

---

## ✨ Resultado Final

```
✅ Raiz limpa (apenas run.py e .gitignore)
✅ Arquivos organizados por tipo
✅ Padrão MVC mantido
✅ Paths dinâmicos funcionando
✅ Sistema profissional e escalável
✅ Documentação centralizada
✅ Fácil manutenção
```

---

**Data**: 2026-03-04  
**Status**: ✅ **CONCLUÍDO**  
**Design Pattern**: MVC + Factory + Decorators + Service + Manager

---

Para mais detalhes, veja:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [app/utils/paths.py](app/utils/paths.py)
- [ESTRUTURA_README.py](ESTRUTURA_README.py)
