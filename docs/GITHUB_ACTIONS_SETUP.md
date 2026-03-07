# ⚙️ Configuração do GitHub Actions - Guia Completo

## 📋 Checklist de Configuração

### 1. Preparação do Repositório

- [ ] Repositório criado no GitHub
- [ ] `.github/workflows/` adicionado com arquivos YAML
- [ ] `.github/CODEOWNERS` configurado
- [ ] `.gitignore` atualizado
- [ ] README.md com badges de status

### 2. Configurar Repositório no GitHub

No seu repositório GitHub:

1. Vá para **Settings**
2. Selecione **Actions** > **General**
3. Configure:
   - [ ] Enable Actions: ✅ ON
   - [ ] Actions permissions: `Allow all actions and reusable workflows`
   - [ ] Workflow permissions: `Read and write permissions`

### 3. Adicionar Secrets

Vá para **Settings > Secrets and variables > Actions** e adicione:

#### Para Staging Deploy
```
DEPLOY_KEY_STAGING = seu-private-key
DEPLOY_HOST_STAGING = 192.168.1.100 ou staging.example.com
DEPLOY_USER_STAGING = deploy_user
```

#### Para Production Deploy
```
DEPLOY_KEY_PROD = seu-private-key
DEPLOY_HOST_PROD = 10.0.0.50 ou prod.example.com
DEPLOY_USER_PROD = deploy_user
```

#### Para Notificações (Opcional)
```
SLACK_WEBHOOK = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

#### Para Análise de Segurança (Opcional)
```
GITGUARDIAN_API_KEY = sua-api-key
SONAR_TOKEN = seu-sonar-token
```

### 4. Configurar Branch Protection Rules

1. Vá para **Settings > Branches**
2. Clique em "Add rule" para a branch `main`
3. Configure:
   - [ ] **Require a pull request before merging** ✅
   - [ ] **Require status checks to pass before merging** ✅
     - `test (3.8)`, `test (3.9)`, `test (3.10)`, `test (3.11)`
     - `code-quality`
     - `security`
     - `docker`
   - [ ] **Require code reviews** ✅ (mínimo 1 revisor)
   - [ ] **Require branches to be up to date before merging** ✅
   - [ ] **Include administrators** ✅

### 5. Configurar Environments

1. Vá para **Settings > Environments**
2. Crie `staging`:
   - Deployment branches: `main`
   - Add secrets: variáveis de staging
3. Crie `production`:
   - Deployment branches: Use tags semver (`v*`)
   - Add secrets: variáveis de production
   - Require reviewers: ✅ (pessoas que podem aprovar deploys)

## 🔄 Fluxo dos Workflows

### Trigger: Push para `develop`
```
┌─────────────────────────────────────────┐
│ 1. CI Workflow (ci.yml)                 │
│    - Test (multiversion)                │
│    - Code Quality                       │
│    - Docker Build                       │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 2. Security Workflow (security.yml)     │
│    - Bandit                             │
│    - Safety                             │
│    - Semgrep                            │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ 3. Lint Workflow (lint.yml)             │
│    - Black                              │
│    - isort                              │
│    - Flake8                             │
└─────────────────────────────────────────┘
```

### Trigger: Pull Request
```
┌─────────────────────────────────────────┐
│ Todos os workflows acima +              │
│ Branch protection rules verificam       │
│ - Status checks                         │
│ - Code reviews                          │
│ - Conflicts                             │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Merge permitido apenas se tudo passar   │
└─────────────────────────────────────────┘
```

### Trigger: Push para `main`
```
┌─────────────────────────────────────────┐
│ Todo workflow anterior +                │
│ Deploy Workflow (deploy.yml)            │
│    - Build Docker Image                 │
│    - Push para Registry                 │
│    - Deploy para Staging                │
│    - Health Check                       │
└─────────────────────────────────────────┘
```

### Trigger: Nova Tag (v*.*.*)
```
┌─────────────────────────────────────────┐
│ Deploy Workflow (deploy.yml)            │
│    - Build Docker Image                 │
│    - Push para Registry                 │
│    - Criar Release no GitHub            │
│    - Deploy para Production             │
│    - Health Check                       │
└─────────────────────────────────────────┘
```

## 🔐 Configuração de SSH para Deploy

### Gerar SSH Key Pair

```bash
# Gerar nova chave SSH
ssh-keygen -t ed25519 -C "github-actions" -f deploy_key -N ""

# Ou com RSA (compatibilidade)
ssh-keygen -t rsa -b 4096 -C "github-actions" -f deploy_key -N ""
```

### Adicionar Public Key no Servidor

```bash
# No servidor de deploy
cat deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Adicionar Private Key ao GitHub

```bash
# Copiar conteúdo da chave privada
cat deploy_key

# Colar em: Settings > Secrets and variables > Actions
# Nome: DEPLOY_KEY_STAGING ou DEPLOY_KEY_PROD
```

## 📊 Integração com Serviços Externos

### SonarQube (Análise de Código)

1. Crie conta em [SonarCloud.io](https://sonarcloud.io)
2. Obtenha SONAR_TOKEN
3. Crie `sonar-project.properties` ✅ (já existe)
4. Adicione ao workflow:

```yaml
- name: SonarQube Scan
  uses: SonarSource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Codecov (Cobertura de Código)

1. Vá para [codecov.io](https://codecov.io)
2. Conecte seu repositório GitHub
3. Obtenha o token (opcional, público por padrão)
4. Workflow já está configurado ✅

Acesse: `https://app.codecov.io/gh/seu-usuario/Loto`

### Slack Notifications

1. Crie um Webhook no Slack:
   - Vá para seu workspace
   - Acesse "Apps" > "Custom Integration"
   - Create "Incoming Webhook"
2. Copie o URL do webhook
3. Adicione como secret: `SLACK_WEBHOOK`

### GitGuardian (Detecção de Secrets)

1. Registre em [gitguardian.com](https://www.gitguardian.com)
2. Obtenha API Key
3. Adicione como secret: `GITGUARDIAN_API_KEY`

## 🚀 Test Drive dos Workflows

### 1. Testar Localmente

```bash
# Instalar act (executor local de GitHub Actions)
# https://github.com/nektos/act

# Testar workflow específico
act -j test -l

# Testar com arquivo de secrets
act -j test -s GITHUB_TOKEN=seu-token
```

### 2. Simular Pull Request

```bash
# Fazer alteração em branch
git checkout -b test/workflow
echo "# Test" >> README.md

# Fazer commit
git add .
git commit -m "test: trigger workflow"
git push origin test/workflow

# Criar PR no GitHub
# Observar workflow rodar em Settings > Actions
```

### 3. Simular Deploy

```bash
# Criar tag
git tag v0.0.1-test
git push origin v0.0.1-test

# Observar deploy workflow executar
# Remover tag se não quiser fazer deploy real
git tag -d v0.0.1-test
git push origin --delete v0.0.1-test
```

## 📈 Monitoramento

### Acessar Logs dos Workflows

1. Vá para **Actions** no repositório
2. Selecione o workflow desejado
3. Clique no run específico
4. Expanda cada job para ver logs detalhados

### Badges de Status

Adicione ao README.md:

```markdown
<!-- Badges -->
[![CI Tests](https://github.com/seu-usuario/Loto/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/ci.yml)
[![Security](https://github.com/seu-usuario/Loto/actions/workflows/security.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/security.yml)
[![Lint](https://github.com/seu-usuario/Loto/actions/workflows/lint.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/lint.yml)
[![Deploy](https://github.com/seu-usuario/Loto/actions/workflows/deploy.yml/badge.svg)](https://github.com/seu-usuario/Loto/actions/workflows/deploy.yml)

<!-- Coverage Badge via Codecov -->
[![codecov](https://codecov.io/gh/seu-usuario/Loto/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/Loto)
```

## ⚡ Performance Tips

### Aumentar Velocidade dos Workflows

```yaml
# 1. Use cache de pip
- uses: actions/setup-python@v4
  with:
    cache: 'pip'

# 2. Use cache de Docker layers
- uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# 3. Paralelizar jobs
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']

# 4. Usar continue-on-error para não-críticos
- name: Optional Check
  run: some-command
  continue-on-error: true
```

## 🐛 Troubleshooting

### Actions não são executadas

**Problema:** Workflows não aparecem em Actions tab

**Solução:**
1. Verifique se os arquivos estão em `.github/workflows/`
2. Verifique sintaxe YAML: `act --list`
3. Commit e push para GitHub
4. Aguarde alguns segundos

### Build falha aleatoriamente

**Problema:** Testes passam localmente mas falham no GitHub Actions

**Solução:**
1. Verifique diferenças do ambiente (Python version, dependências)
2. Recrie venv localmente igual ao CI
3. Execute com mesmas dependências: `pip install -r requirements.txt --exact`
4. Verifique if tests dependem de tempo/ordem

### Out of Storage

**Problema:** Erro "No space left on device"

**Solução:**
1. Limpe cache: Settings > Actions > General > Show runner usage > Clear repository cache
2. Remova dependências desnecessárias
3. Use builds paralelos com menos jobs

## 📚 Recursos Adicionais

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Act - Local GitHub Actions](https://github.com/nektos/act)
- [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments)

---

**Última atualização:** 2024
