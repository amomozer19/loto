# 🎰 LOTO - Sistema de Análise de Sorteios

Aplicação Flask para análise, geração e gerenciamento de sorteios de loteria com estatísticas avançadas e gerador inteligente de apostas.

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- pip ou conda
- Docker (opcional, para Keycloak)

### Instalação

1. **Clone o repositório** (se aplicável)
```bash
cd "Python Projects/Loto"
```

2. **Crie ambiente virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. **Instale dependências**
```bash
pip install -r config/requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. **Execute a aplicação**
```bash
python run.py
```

Acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
Loto/
├── app/                    # Aplicação Flask
│   ├── __init__.py
│   ├── auth/              # Sistema de autenticação
│   ├── models/            # Modelos de dados
│   ├── routes/            # Rotas da aplicação
│   ├── templates/         # Templates HTML
│   └── utils/             # Utilitários e helpers
│
├── config/                # Configurações
│   ├── pytest.ini
│   ├── requirements.txt
│   └── Loto.spec          # Spec para compilação
│
├── data/                  # Dados da aplicação
│   ├── dados_loto.csv
│   └── dados_usuarios.csv
│
├── docs/                  # Documentação
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── ... (outros docs)
│
├── scripts/               # Scripts utilitários
│   ├── criar_executavel.py
│   ├── run_exe.py
│   └── run.py
│
├── tests/                 # Testes automatizados
│   ├── test_*.py
│   └── conftest.py
│
├── build/                 # Build output (PyInstaller)
├── dist/                  # Distribuição (PyInstaller)
│
├── .venv/                 # Virtual environment
├── .env.example           # Template de variáveis de ambiente
├── .gitignore             # Git ignore patterns
├── docker-compose.yml     # Docker Compose (Keycloak)
├── run.py                 # Entry point principal
└── README.md              # Este arquivo
```

## 🔐 Autenticação

### Local (Padrão)
Usuário: `antonio.m.13@live.com`  
Senha: Configurada no `.env`

### Keycloak OAuth2/OIDC (Opcional)
Para ativar Keycloak:

1. **Inicie o Keycloak**
```bash
docker-compose up -d
```

2. Configure as variáveis no `.env`:
```
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_CLIENT_ID=loto-app
KEYCLOAK_CLIENT_SECRET=seu_secret
```

Ver: [docs/KEYCLOAK_SETUP.md](docs/KEYCLOAK_SETUP.md)

## 🎯 Funcionalidades Principales

### 📊 Dashboard Inicial
- Visualização de sorteios recentes
- Estatísticas gerais
- Histórico de 20 últimos sorteios

### ➕ Novo Sorteio
- Interface para registrar novos sorteios
- Validação automática de números
- Armazenamento em CSV

### 📈 Estatísticas Avançadas
- Análise de frequência de números
- Estatísticas por dia da semana
- Gráficos interativos com Chart.js
- Previsões baseadas em histórico

### 💫 Sorte! (Análise de Números)
- Analisa 7 números inseridos
- Gera score de compatibilidade (0-100)
- Fornece recomendações baseadas em dados
- Identifica duplas e tripletas interessantes

### 🎲 Gerador de Apostas
- Gera apostas automáticas
- Analisa potencial de cada aposta
- Baseado em padrões históricos

## 🧪 Testes

```bash
pytest
pytest -v                    # Verbose
pytest tests/test_*.py      # Arquivo específico
pytest --cov                 # Com cobertura
```

Ver: [docs/RUN_TESTS.md](docs/RUN_TESTS.md)

## 📚 Documentação

Documentação completa em: [`docs/`](docs/)

- [Architecture](docs/ARCHITECTURE.md) - Documentação da arquitetura
- [Authentication](docs/AUTHENTICATION.md) - Sistema de autenticação
- [Keycloak Setup](docs/KEYCLOAK_SETUP.md) - Configuração del Keycloak
- [Quick Start](docs/QUICK_START_AUTH.md) - Início rápido
- [Testing](docs/TESTING.md) - Guia de testes

## ⚙️ Configuração

### Variáveis de Ambiente (`.env`)

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui

# Autenticação
AUTH_METHOD=local  # ou keycloak
DEFAULT_USER_EMAIL=antonio.m.13@live.com
DEFAULT_USER_PASSWORD=sua_senha

# Keycloak (se usar)
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_CLIENT_ID=loto-app
KEYCLOAK_CLIENT_SECRET=seu_client_secret
KEYCLOAK_REALM=master
KEYCLOAK_REDIRECT_URI=http://localhost:5000/auth/keycloak/callback

# SMTP Email
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@outlook.com
SMTP_PASSWORD=sua_senha_app
SMTP_FROM_EMAIL=noreply@loto.com
```

## 🛡️ Segurança

- Variáveis sensíveis ignoradas (ver `.gitignore`)
- Autenticação decorador em rotas protegidas
- CSRF protection em formulários
- Hash de senhas com werkzeug.security
- OAuth2/OIDC com Keycloak (opcional)

## 🐛 Troubleshooting

### Erro de Permissão no PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro de Import
```bash
pip install -r config/requirements.txt -U
```

### Porta 5000 Ocupada
```bash
python run.py --port 5001
```

### Problema com SMTP
Ver: [docs/SMTP_CONFIGURATION.md](docs/SMTP_CONFIGURATION.md)

## 📝 Changelog

Ver: [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)

## 📆 Versão

**Versão Atual:** 2.0.0  
**Última Atualização:** 06/03/2026

## 👨‍💻 Desenvolvimento

### Stack Tecnológico

- **Backend:** Flask, Python 3.8+
- **Frontend:** Bootstrap 5, JavaScript Vanilla
- **Database:** CSV (pode usar SQLite/PostgreSQL)
- **Auth:** OAuth2/OIDC (Keycloak) ou Local
- **Containers:** Docker/Docker Compose
- **Charts:** Chart.js
- **Testing:** pytest, pytest-cov

### Contribuindo

1. Crie uma branch (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto é privado.

## 📧 Suporte

Para dúvidas ou problemas, verifique a [documentação](docs/).

---

**Desenvolvido com ❤️ em 2026**
