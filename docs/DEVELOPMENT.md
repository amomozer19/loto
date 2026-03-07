# 🚀 Guia de Desenvolvimento - LOTO

## Índice
1. [Configuração Inicial](#configuração-inicial)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Fluxo de Desenvolvimento](#fluxo-de-desenvolvimento)
4. [Esteira CI/CD](#esteira-cicd)
5. [Testando Localmente](#testando-localmente)
6. [Deploying](#deploying)

## Configuração Inicial

### Pré-requisitos
- Python 3.8+
- Docker & Docker Compose
- Git
- Make (opcional, mas recomendado)

### Setup do Ambiente

```bash
# 1. Clone o repositório
git clone <repository-url>
cd Loto

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instale dependências
make install-dev
# ou
pip install -r config/requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações locais

# 5. Inicie os containers de desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# 6. Execute a aplicação
make dev-run
# ou
python run.py
```

## Estrutura do Projeto

```
Loto/
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD
│   │   ├── ci.yml         # Testes e análise
│   │   ├── security.yml   # Segurança
│   │   ├── deploy.yml     # Deploy
│   │   └── lint.yml       # Lint e formatação
│   ├── CODEOWNERS         # Proprietários do código
│   └── pull_request_template.md
├── app/
│   ├── auth/              # Sistema de autenticação
│   ├── models/            # Modelos de dados
│   ├── routes/            # Rotas e endpoints
│   ├── templates/         # Templates HTML
│   └── utils/             # Utilitários
├── tests/                 # Testes automatizados
├── config/                # Configurações
├── docs/                  # Documentação
├── Dockerfile             # Container production
├── Dockerfile.dev         # Container development
├── docker-compose.yml     # Orquestração production
├── docker-compose.dev.yml # Orquestração development
├── Makefile               # Automação de tarefas
├── pyproject.toml         # Configuração Python
└── .pylintrc              # Configuração Pylint
```

## Fluxo de Desenvolvimento

### 1. Criar uma Branch
```bash
# Crie uma branch com nome descritivo
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bug
```

### 2. Fazer Mudanças
```bash
# Edite seus arquivos
# Adicione testes para suas mudanças
```

### 3. Testar Localmente
```bash
# Execute os testes
make test

# Ou execute testes específicos
make test-unit
make test-int

# Faça lint
make lint

# Formate o código
make format
```

### 4. Commit e Push
```bash
# Commit suas mudanças
git add .
git commit -m "feat: descrição da sua feature"
git push origin feature/sua-feature

# Ou siga a convenção padrão:
# feat: nova funcionalidade
# fix: correção de bug
# docs: atualização de documentação
# style: formatação de código
# refactor: refatoração sem mudança funcional
# perf: melhoria de performance
# test: adição de testes
```

### 5. Criar Pull Request
- No GitHub, crie um PR para a branch `develop`
- Descreva suas mudanças usando o template
- Aguarde as verificações de CI passar
- Solicite revisão (review)

### 6. Merge
Após aprovação:
```bash
# O PR será merged automaticamente após todas as verificações passarem
```

## Esteira CI/CD

### GitHub Actions Workflows

#### 1. **CI (ci.yml)**
Executado em: `push` para `main`/`develop`, `pull_request`

O que faz:
- ✅ Executa testes com pytest
- 📊 Calcula cobertura de código
- 🔍 Análise estática de código (Pylint, Flake8)
- 🐳 Build da imagem Docker

```yaml
Tests:
  - Python 3.8, 3.9, 3.10, 3.11
  - Cobertura de código (Codecov)
  - Code Quality (Pylint, Bandit)
```

#### 2. **Security (security.yml)**
Executado: Diariamente (2 AM UTC) + push/PR

O que faz:
- 🔒 Bandit - Análise de segurança
- 🛡️ Safety - Verificação de dependências vulneráveis
- 🔎 Semgrep - Análise estática avançada
- 🔐 GitGuardian/TruffleHog - Detecção de segredos

#### 3. **Lint (lint.yml)**
Executado: `push`/`pull_request`

O que faz:
- 🎨 Black - Formatação de código
- 📦 isort - Organização de importações
- 🚨 Flake8 - Verificação de estilo
- 📝 Pydocstyle - Verificação de docstrings

#### 4. **Deploy (deploy.yml)**
Executado: `push` para `main`, `tags` (releases)

O que faz:
- 🐳 Build e push da imagem Docker
- 📦 Deploy para Staging (push main)
- 🚀 Deploy para Produção (tags v*)

### Badges de Status
```markdown
[![CI](https://github.com/seu-usuario/Loto/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/ci.yml)
[![Security](https://github.com/seu-usuario/Loto/actions/workflows/security.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/security.yml)
```

## Testando Localmente

### Executar Testes

```bash
# Todos os testes
make test

# Testes unitários apenas
make test-unit

# Testes de integração
make test-int

# Testes rápidos (excluindo lentos)
make test-fast

# Teste específico
pytest tests/test_auth.py -v
pytest tests/test_routes.py::test_index -v
```

### Cobertura de Código

```bash
# Gerar relatório HTML
pytest --cov=app --cov-report=html

# Abrir no navegador
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Lint e Formatação

```bash
# Verificar lint
make lint

# Formatar código
make format

# Verificar se código está formatado
make format-check

# Análise de segurança
make security
```

## Docker

### Desenvolvimento com Docker

```bash
# Iniciar containers
docker-compose -f docker-compose.dev.yml up -d

# Logs
docker-compose -f docker-compose.dev.yml logs -f web

# Parar containers
docker-compose -f docker-compose.dev.yml down

# Verificar status
docker-compose -f docker-compose.dev.yml ps
```

### Build Production

```bash
# Build imagem
docker build -t loto:latest .

# Run container
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=... \
  loto:latest
```

## Deploying

### Staging (Automático com push para main)

1. Commits em `main` acionam o workflow de deploy
2. Imagem Docker é buildada e pushada
3. Deploy para staging é executado automaticamente

Acesse: `https://staging.loto.example.com`

### Production (Manual via Tags)

1. Crie uma tag de release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. Isso acionará:
   - Build da imagem Docker
   - Criação de release no GitHub
   - Deploy para produção

Acesse: `https://loto.example.com`

## Variáveis de Ambiente Necessárias

### Para CI/CD no GitHub Actions

Adicione os secrets em `Settings > Secrets and variables > Actions`:

```
# Deploy Staging
DEPLOY_KEY_STAGING       # SSH private key
DEPLOY_HOST_STAGING      # IP ou hostname
DEPLOY_USER_STAGING      # SSH user

# Deploy Production
DEPLOY_KEY_PROD          # SSH private key
DEPLOY_HOST_PROD         # IP ou hostname
DEPLOY_USER_PROD         # SSH user

# Notificações
SLACK_WEBHOOK            # Webhook do Slack (opcional)

# Segurança
GITGUARDIAN_API_KEY      # API key GitGuardian (opcional)
```

## Troubleshooting

### Testes falhando localmente

```bash
# Limpe cache e reconstrua
make clean

# Reinstale dependências
pip install -r config/requirements.txt --force-reinstall

# Reinicie containers
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

### GitHub Actions falhando

1. Verifique os logs da action: `Actions > workflow > run`
2. Verifique se as secrets estão configuradas
3. Verifique se o branch está correto
4. Faça rerun do workflow: `Re-run all jobs`

### Problemas de Banco de Dados

```bash
# Resetar banco de dados (desenvolvimento)
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

## Recursos Úteis

- [Python Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)

## Contato e Suporte

Para dúvidas ou problemas, abra uma issue no GitHub com:
- Descrição clara do problema
- Passos para reproduzir
- Logs relevantes
- Seu ambiente (OS, Python version, etc.)

---

**Última atualização:** 2024
**Versão:** 1.0
