# 📊 Visão Geral da Esteira de CI/CD - LOTO

## 🎯 O que foi configurado?

Uma esteira completa de desenvolvimento automatizada com:

```
DESENVOLVIMENTO LOCAL
        ↓
PUSH PARA GITHUB
        ↓
GITHUB ACTIONS WORKFLOWS
    ├─ CI (Testes)
    ├─ Security (Segurança)
    ├─ Lint (Formatação)
    └─ Deploy (Automático)
        ↓
AMBIENTE STAGING
        ↓
PULL REQUEST REVIEW
        ↓
MERGE E DEPLOY PRODUCTION
```

## 📁 Arquivos Criados

### Workflows do GitHub Actions (`.github/workflows/`)

| Arquivo | Propósito | Quando Executa |
|---------|-----------|-----------------|
| **ci.yml** | Testes e análise de código | Push / PR / Schedule |
| **security.yml** | Verificação de segurança | Push / PR / Daily |
| **lint.yml** | Formatação e linting | Push / PR |
| **deploy.yml** | Build e deploy Docker | Push main / Tags |

### Arquivos de Configuração

| Arquivo | Descrição |
|---------|-----------|
| **Dockerfile** | Container production (otimizado) |
| **Dockerfile.dev** | Container desenvolvimento (com ferramentas) |
| **docker-compose.dev.yml** | Orquestração para desenvolvimento |
| **pyproject.toml** | Configuração de ferramentas Python |
| **.pylintrc** | Configuração para Pylint |
| **sonar-project.properties** | Integração com SonarQube |
| **Makefile** | Automação de tarefas comuns |
| **.env.example** | Variáveis de ambiente (atualizado) |

### Documentação

| Arquivo | Conteúdo |
|---------|----------|
| **docs/DEVELOPMENT.md** | Guia completo de desenvolvimento |
| **docs/GITHUB_ACTIONS_SETUP.md** | Configuração do GitHub Actions |
| **docs/COMMIT_CONVENTIONS.md** | Convenção de commits |
| **.github/CODEOWNERS** | Proprietários do código |
| **.github/pull_request_template.md** | Template para PRs |

---

## 🔄 Workflows Detalhados

### 1️⃣ CI Workflow (ci.yml)

**Executa em:** `push` para main/develop, `pull_request`

**Jobs:**
```
┌─ test
│   ├─ Python 3.8, 3.9, 3.10, 3.11
│   ├─ Pytest com cobertura
│   ├─ Upload para Codecov
│   └─ PostgreSQL test database
├─ code-quality
│   ├─ Pylint
│   ├─ Safety (vulnerabilidades)
│   └─ Bandit (segurança)
└─ docker
    └─ Build imagem Docker
```

**Tempo estimado:** 3-5 minutos

### 2️⃣ Security Workflow (security.yml)

**Executa em:** `push` / `pull_request` / Diariamente às 2 AM UTC

**Jobs:**
```
┌─ security
│   ├─ Bandit (vulnerabilidades)
│   ├─ Safety (dependências)
│   └─ Semgrep (análise estática)
├─ dependency-check
│   ├─ Dependências outdated
│   └─ Dependency tree
└─ secrets-scan
    ├─ TruffleHog
    └─ GitGuardian
```

**Tempo estimado:** 2-3 minutos

### 3️⃣ Lint Workflow (lint.yml)

**Executa em:** `push` / `pull_request`

**Jobs:**
```
┌─ lint
│   ├─ Black (formatação)
│   ├─ isort (imports)
│   ├─ Flake8 (estilo)
│   ├─ Pylint
│   └─ Commit automatizado de formatação
└─ docstring-check
    └─ Pydocstyle
```

**Tempo estimado:** 1-2 minutos

### 4️⃣ Deploy Workflow (deploy.yml)

**Executa em:** `push` para main, nova `tag` (v*.*.*)

**Jobs - Staging (push main):**
```
┌─ build-and-push (Docker)
│   └─ Push para GitHub Container Registry
├─ deploy-staging
│   ├─ SSH deploy
│   ├─ docker-compose up
│   └─ Health check
└─ notify
    └─ Slack notification
```

**Jobs - Production (tags):**
```
┌─ build-and-push (Docker)
│   └─ Push para GitHub Container Registry
├─ deploy-production
│   ├─ Criar release no GitHub
│   ├─ SSH deploy
│   ├─ DB migrations
│   └─ Health check
└─ notify
    └─ Slack notification
```

**Tempo estimado:** 5-10 minutos

---

## 🚀 Como Usar

### Desenvolvimento Local

```bash
# 1. Setup inicial
make install-dev
docker-compose -f docker-compose.dev.yml up -d

# 2. Desenvolver
python run.py          # Rodar aplicação
make test              # Testar
make lint              # Lint
make format            # Formatar
```

### Criar Feature

```bash
# 1. Criar branch
git checkout -b feature/minha-feature

# 2. Fazer mudanças e testar
make test
make lint
make format

# 3. Commit (seguindo convenções)
git commit -m "feat(api): nova funcionalidade"

# 4. Push
git push origin feature/minha-feature

# 5. Criar PR no GitHub
# GitHub Actions executarão automaticamente
# - Testes
# - Segurança
# - Formatação

# 6. Aguardar aprovação e merge
# Após merge: deploy automático para staging
```

### Fazer Release

```bash
# 1. Criar tag (segue semver)
git tag v1.2.0

# 2. Push tag
git push origin v1.2.0

# 3. GitHub Actions automaticamente:
# - Build Docker image
# - Cria release no GitHub
# - Faz deploy para produção
# - Envia health check
```

---

## 🔐 Segurança

### Proteções Habilitadas

```
main branch:
  ✅ Require pull request before merging
  ✅ Require status checks to pass
     - All CI/CD jobs
  ✅ Require code reviews (1 approved)
  ✅ Require branches up to date
```

### Secret Management

Secrets armazenados em GitHub:
- `DEPLOY_KEY_STAGING`
- `DEPLOY_HOST_STAGING`
- `DEPLOY_USER_STAGING`
- `DEPLOY_KEY_PROD`
- `DEPLOY_HOST_PROD`
- `DEPLOY_USER_PROD`
- `SLACK_WEBHOOK` (opcional)
- `GITGUARDIAN_API_KEY` (opcional)

---

## 📊 Métricas e Monitoramento

### Código Coverage
- GitHub Actions integrado com **Codecov**
- Relatório automático em PRs
- Badges de status no README

### Análise de Código Estático
- **Pylint** - Python linting
- **Black** - Formatação
- **isort** - Organização de imports
- **Flake8** - Estilo de código
- **SonarQube** - Qualidade geral (opcional)

### Segurança
- **Bandit** - Vulnerabilidades Python
- **Safety** - Dependências desatualizadas
- **Semgrep** - Análise de padrões
- **GitGuardian** - Detecção de secrets
- **TruffleHog** - Histórico de git

---

## 📝 Checklist de Configuração

Antes de usar, configure no GitHub:

### Repositório Settings

- [ ] Actions > General > Enable Actions
- [ ] Settings > Branches > Add rule for `main`
  - [ ] Require PR before merging
  - [ ] Require status checks

### Secrets

- [ ] DEPLOY_KEY_STAGING
- [ ] DEPLOY_HOST_STAGING  
- [ ] DEPLOY_USER_STAGING
- [ ] DEPLOY_KEY_PROD
- [ ] DEPLOY_HOST_PROD
- [ ] DEPLOY_USER_PROD
- [ ] SLACK_WEBHOOK (opcional)
- [ ] GITGUARDIAN_API_KEY (opcional)

### Environments

- [ ] Criar `staging` environment
- [ ] Criar `production` environment

### Integrações (Opcional)

- [ ] Codecov ([codecov.io](https://codecov.io))
- [ ] SonarCloud ([sonarcloud.io](https://sonarcloud.io))
- [ ] Slack ([slack.com](https://slack.com/apps))
- [ ] GitGuardian ([gitguardian.com](https://gitguardian.com))

---

## 🆘 Troubleshooting Rápido

### Workflow não executa
```bash
# Verificar sintaxe YAML
pip install yamllint
yamllint .github/workflows/*.yml

# Ou usar act localmente
act -l  # listar workflows
act push  # simular push
```

### Testes falham no CI mas passam localmente
```bash
# Usar mesma Python version
python -m venv .venv
pip install -r config/requirements.txt

# Rodar com pytest igualmente
pytest tests/ -v --cov=app
```

### Deploy falha
```bash
# Verificar secrets estão configurados
# Verificar SSH key é válida
# Verificar servidor está acessível
ssh -i key user@host "docker -v"
```

---

## 📚 Arquivos de Referência

- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Guia de desenvolvimento
- [docs/GITHUB_ACTIONS_SETUP.md](docs/GITHUB_ACTIONS_SETUP.md) - Configuração GitHub Actions
- [docs/COMMIT_CONVENTIONS.md](docs/COMMIT_CONVENTIONS.md) - Convenção de commits
- [Makefile](Makefile) - Comandos úteis
- [pyproject.toml](pyproject.toml) - Configuração Python

---

## 🎓 Próximos Passos

1. ✅ Arquivos de workflow criados
2. ✅ Documentação completa
3. ⏭️ **Configurar GitHub secrets**
4. ⏭️ **Testar workflows rodando**
5. ⏭️ **Integrar Codecov (opcional)**
6. ⏭️ **Integrar SonarCloud (opcional)**

---

**Data de Criação:** Março 2025  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
