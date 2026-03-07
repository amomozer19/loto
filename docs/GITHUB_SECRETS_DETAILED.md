# 🔐 Configurar GitHub Secrets - Guia Detalhado

## 📍 Entender a Diferença: Repository vs Environment Secrets

### Environment Secrets vs Repository Secrets

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GITHUB SECRETS                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  REPOSITORY SECRETS (Global)                                        │
│  ├─ Acessível por: Qualquer workflow em qualquer branch            │
│  ├─ Usado para: Secrets compartilhados (GITGUARDIAN_API_KEY, etc)  │
│  ├─ Visibilidade: Todos os jobs veem                               │
│  └─ Exemplo: SLACK_WEBHOOK, CODECOV_TOKEN                          │
│                                                                     │
│  ENVIRONMENT SECRETS (Específico por Ambiente)                     │
│  ├─ Acessível por: Workflows que usam aquele environment           │
│  ├─ Usado para: Deploy keys separadas por ambiente                 │
│  ├─ Visibilidade: Apenas jobs que usam aquele environment          │
│  └─ Exemplo:                                                        │
│     - Staging: DEPLOY_KEY_STAGING, DEPLOY_HOST_STAGING             │
│     - Production: DEPLOY_KEY_PROD, DEPLOY_HOST_PROD                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Matriz de Configuração

| Secret | Tipo | Valor | Segurança | Precisa |
|--------|------|-------|-----------|---------|
| **DEPLOY_KEY_STAGING** | Environment (staging) | Sua chave SSH privada | 🔐 Alta | ✅ SIM |
| **DEPLOY_HOST_STAGING** | Environment (staging) | IP ou domínio do servidor | 🟡 Média | ✅ SIM |
| **DEPLOY_USER_STAGING** | Environment (staging) | Usuário SSH | 🟡 Média | ✅ SIM |
| **DEPLOY_KEY_PROD** | Environment (production) | Sua chave SSH privada | 🔐 Alta | ✅ SIM |
| **DEPLOY_HOST_PROD** | Environment (production) | IP ou domínio do servidor | 🔐 Alta | ✅ SIM |
| **DEPLOY_USER_PROD** | Environment (production) | Usuário SSH | 🔐 Alta | ✅ SIM |
| **SLACK_WEBHOOK** | Repository | URL do webhook Slack | 🟡 Média | ❌ Opcional |
| **GITGUARDIAN_API_KEY** | Repository | API Key GitGuardian | 🔐 Alta | ❌ Opcional |
| **CODECOV_TOKEN** | Repository | Token Codecov | 🟡 Média | ❌ Opcional |

---

## 🎯 Passo a Passo Detalhado

### OPÇÃO 1: Repository Secrets (Secrets Globais)

Esses secrets são compartilhados com TODOS os workflows.

#### Passo 1: Acessar Repository Secrets

```
1. Vá para seu repositório no GitHub
   https://github.com/seu-usuario/Loto

2. Clique em "Settings" (engrenagem no topo right)

3. Na barra lateral, clique em "Secrets and variables"

4. Expanda e clique em "Actions"

5. Você verá 3 abas:
   - Secrets (onde você está agora)
   - Variables
   - Dependabot secrets
```

**Caminho Visual:**
```
Seu Repositório
  ├─ Settings (engrenagem)
  │
  └─ Secrets and variables
      │
      └─ Actions
          ├─ Secrets (aqui você está)
          │   └─ New repository secret (botão azul)
          ├─ Variables
          └─ Dependabot secrets
```

#### Passo 2: Adicionar Repository Secrets

Clique em **"New repository secret"** (botão azul)

**Para SLACK_WEBHOOK (Opcional):**

```
Name: SLACK_WEBHOOK
Secret: https://hooks.slack.com/services/YOUR/WEBHOOK/URL

[Add secret] (botão)
```

**Para GITGUARDIAN_API_KEY (Opcional):**

```
Name: GITGUARDIAN_API_KEY
Secret: sua-api-key-do-gitguardian

[Add secret] (botão)
```

**Para CODECOV_TOKEN (Opcional):**

```
Name: CODECOV_TOKEN
Secret: seu-token-do-codecov

[Add secret] (botão)
```

---

### OPÇÃO 2: Environment Secrets (Específico por Ambiente)

Esses secrets são **isolados por ambiente** (staging vs produção).

#### Passo 1: Criar Environments

Primeiro, você precisa criar os environments:

```
1. Settings > Environments (na barra lateral)

2. Clique em "New environment"

3. Nome: staging
   [Configure protection rules] (opcional)
   [Create environment]

4. Repita o processo para "production"
```

**Caminho Visual:**
```
Settings
  ├─ Environments
  │   ├─ [New environment]
  │   └─ staging
  │   └─ production
```

#### Passo 2: Adicionar Secrets ao Environment Staging

```
1. Settings > Environments > staging

2. Clique em "Add secret" (ou "New environment secret")

3. Adicione os 3 secrets obrigatórios:
```

**Secret 1 - Deploy Key:**
```
Name: DEPLOY_KEY_STAGING
Secret: (copie conteúdo de deploy_key privada)
        -----BEGIN OPENSSH PRIVATE KEY-----
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ...
        -----END OPENSSH PRIVATE KEY-----

[Add secret]
```

**Secret 2 - Deploy Host:**
```
Name: DEPLOY_HOST_STAGING
Secret: seu-server-staging.com
        ou: 192.168.1.100
        ou: 10.0.0.50

[Add secret]
```

**Secret 3 - Deploy User:**
```
Name: DEPLOY_USER_STAGING
Secret: deploy
        ou: ubuntu
        ou: seu-usuario

[Add secret]
```

#### Passo 3: Adicionar Secrets ao Environment Production

Repita o mesmo processo em **Settings > Environments > production**:

```
DEPLOY_KEY_PROD
DEPLOY_HOST_PROD
DEPLOY_USER_PROD
```

---

## 🔑 Como Obter as Chaves SSH

### Gerar SSH Key Pair (se não tiver)

No seu computador local:

```bash
# Gerar chave SSH (Linux/Mac/Windows Git Bash)
ssh-keygen -t ed25519 -C "github-actions-staging" -f deploy_key_staging -N ""

# Ou com RSA (compatibilidade maior)
ssh-keygen -t rsa -b 4096 -C "github-actions-staging" -f deploy_key_staging -N ""
```

**Resultado:**
```
deploy_key_staging (privada - para GitHub)
deploy_key_staging.pub (pública - para servidor)
```

### Adicionar Chave Pública no Servidor

```bash
# No seu servidor de staging
ssh seu-usuario@seu-server-staging.com

# Adicionar chave pública
cat deploy_key_staging.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Verificar que funciona
exit
ssh -i deploy_key_staging seu-usuario@seu-server-staging.com
# Deve conectar sem pedir senha
```

### Adicionar Chave Privada no GitHub

```bash
# No seu computador local
cat deploy_key_staging

# Copiar toda a saída, incluindo:
# -----BEGIN OPENSSH PRIVATE KEY-----
# ... linhas ...
# -----END OPENSSH PRIVATE KEY-----

# Colar no campo Secret do GitHub
```

---

## 🎬 Resumo Visual em Screenshots (Texto)

### Passo 1: Ir para Settings

```
GitHub
├─ Repositório
│  ├─ Code
│  ├─ Issues
│  ├─ Pull requests
│  ├─ Discussions
│  ├─ Actions ← (aqui você verá os workflows rodando)
│  ├─ ...
│  └─ Settings ← CLIQUE AQUI
```

### Passo 2: Secrets and Variables

```
Settings
├─ General
├─ Access
│  └─ Collaborators
├─ Code and automation
│  ├─ Branches
│  ├─ Tags
│  ├─ Ruleset
│  ├─ Actions
│  │  └─ General
│  ├─ Secrets and variables ← CLIQUE AQUI
│  │  ├─ Actions
│  │  │  ├─ Secrets (abra esta aba)
│  │  │  ├─ Variables
│  │  │  └─ Dependabot secrets
```

### Passo 3: Adicionar Secrets

```
Actions > Secrets
├─ Repository secrets
│  ├─ SLACK_WEBHOOK (opcional)
│  ├─ GITGUARDIAN_API_KEY (opcional)
│  └─ CODECOV_TOKEN (opcional)
│
└─ Environment secrets
   ├─ staging
   │  ├─ DEPLOY_KEY_STAGING ✅ OBRIGATÓRIO
   │  ├─ DEPLOY_HOST_STAGING ✅ OBRIGATÓRIO
   │  └─ DEPLOY_USER_STAGING ✅ OBRIGATÓRIO
   │
   └─ production
      ├─ DEPLOY_KEY_PROD ✅ OBRIGATÓRIO
      ├─ DEPLOY_HOST_PROD ✅ OBRIGATÓRIO
      └─ DEPLOY_USER_PROD ✅ OBRIGATÓRIO
```

---

## 📋 Checklist Completo

### Repository Secrets (Globais)

- [ ] Ir para Settings > Secrets and variables > Actions
- [ ] Clique em "New repository secret"
- [ ] Adicione SLACK_WEBHOOK (opcional, mas recomendado)
  ```
  Name: SLACK_WEBHOOK
  Secret: https://hooks.slack.com/services/...
  ```
- [ ] Adicione GITGUARDIAN_API_KEY (opcional)
  ```
  Name: GITGUARDIAN_API_KEY
  Secret: sua-chave-aqui
  ```

### Environment Secrets - Staging

- [ ] Ir para Settings > Environments
- [ ] Clique em "New environment" > Nome: **staging**
- [ ] Configure protection rules (opcional):
  - [ ] Require reviewers: (deixe vazio ou adicione pessoas)
  - [ ] Restrict deployments to specific branches: main
- [ ] Clique em "Add secret" 3 vezes:
  ```
  1️⃣ DEPLOY_KEY_STAGING = sua-chave-privada-ssh
  2️⃣ DEPLOY_HOST_STAGING = seu-ip-ou-dominio
  3️⃣ DEPLOY_USER_STAGING = seu-usuario-ssh
  ```

### Environment Secrets - Production

- [ ] Ir para Settings > Environments
- [ ] Clique em "New environment" > Nome: **production**
- [ ] Configure protection rules (RECOMENDADO):
  - [ ] Require reviewers: adicione pessoas que podem aprovar deploy
  - [ ] Restrict deployments to specific branches: main (ou apenas tags)
- [ ] Clique em "Add secret" 3 vezes:
  ```
  1️⃣ DEPLOY_KEY_PROD = sua-chave-privada-ssh
  2️⃣ DEPLOY_HOST_PROD = seu-ip-ou-dominio
  3️⃣ DEPLOY_USER_PROD = seu-usuario-ssh
  ```

---

## 🛡️ Melhores Práticas de Segurança

### ✅ Faça

```
✅ Use chaves SSH Ed25519 (mais seguras)
✅ Use chaves diferentes para staging e production
✅ Use nomes descritivos e claros
✅ Ative protection rules para production
✅ Requer código review antes de deploy em production
✅ Rotacione chaves regulamente (a cada 3-6 meses)
✅ Monitore quem tem acesso aos secrets
✅ Use variáveis para valores não-sensíveis
```

### ❌ Não Faça

```
❌ Usar a mesma chave para staging e production
❌ Colar secrets em código ou commits
❌ Compartilhar chaves privadas por email
❌ Usar passwords simples como secrets
❌ Deixar secrets em repositórios públicos
❌ Guardar backups de chaves em local inseguro
❌ Usar secrets quando deveria usar variables
```

---

## 🔄 Fluxo Automático com Secrets

### Como os Secrets são Usados no Workflow

Seu arquivo `deploy.yml` usa esses secrets assim:

```yaml
deploy-staging:
  name: Deploy para Staging
  runs-on: ubuntu-latest
  environment:
    name: staging          # ← Usa environment secrets do "staging"
    url: https://staging.loto.example.com

  steps:
    - name: Deploy to staging
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY_STAGING }}      # ← Repository ou Environment?
        DEPLOY_HOST: ${{ secrets.DEPLOY_HOST_STAGING }}     # ← GitHub procura em order
        DEPLOY_USER: ${{ secrets.DEPLOY_USER_STAGING }}
      run: |
        # Usa os secrets aqui
        ssh -i /tmp/key $DEPLOY_USER@$DEPLOY_HOST "docker pull && restart"
```

**Ordem de Busca dos Secrets:**
```
1. Environment secrets (se definido "environment")
2. Repository secrets (global)
3. Erro (secret não encontrado)
```

---

## 🐛 Troubleshooting

### Problema: "Secret not found"

**Causa:** Secret foi adicionado em Repository mas o workflow procura em Environment

**Solução:**
```
1. Verifique se o secret foi criado em "Environment secrets"
2. Ou crie em "Repository secrets"
3. Aguarde ~1 minuto pelo cache do GitHub ser limpo
4. Re-run o workflow
```

### Problema: Deploy falha, mas secret existe

**Causa:** Valor do secret está incompleto ou com espaços extras

**Solução:**
```bash
# Teste local
cat deploy_key_staging | wc -c  # Deve ter ~3000 caracteres

# Verifique início e fim
head -1 deploy_key_staging  # -----BEGIN OPENSSH PRIVATE KEY-----
tail -1 deploy_key_staging  # -----END OPENSSH PRIVATE KEY-----

# Copie exatamente, sem espaços extras
cat deploy_key_staging | pbcopy  # Mac
cat deploy_key_staging | xclip   # Linux
```

### Problema: Workflow vê secretos diferentes em staging e prod

**Solução esperada!** Isso é correto:
```
Staging usa: DEPLOY_KEY_STAGING (do environment "staging")
Production usa: DEPLOY_KEY_PROD (do environment "production")
```

---

## 📊 Exemplo Completo Passo a Passo

### Cenário Real: Configurar Staging

**1. Gerar SSH Keys localmente:**
```bash
cd ~/.ssh
ssh-keygen -t ed25519 -C "github-actions-staging" -f loto_staging -N ""

# Resultado:
# loto_staging (privada)
# loto_staging.pub (pública)
```

**2. Adicionar ao servidor staging:**
```bash
# No seu servidor
ssh seu-usuario@seu-servidor-staging.com
mkdir -p ~/.ssh
cat >> ~/.ssh/authorized_keys << 'EOF'
<conteúdo de loto_staging.pub>
EOF
chmod 600 ~/.ssh/authorized_keys
exit

# Teste
ssh -i ~/.ssh/loto_staging seu-usuario@seu-servidor-staging.com
# Deve conectar sem pedir senha
```

**3. Adicionar ao GitHub:**

No GitHub:
```
Settings > Environments > staging > Add secret

Name: DEPLOY_KEY_STAGING
Secret: 
-----BEGIN OPENSSH PRIVATE KEY-----
... (copie conteúdo de loto_staging)
-----END OPENSSH PRIVATE KEY-----

[Add secret]

Name: DEPLOY_HOST_STAGING
Secret: seu-servidor-staging.com

[Add secret]

Name: DEPLOY_USER_STAGING
Secret: seu-usuario

[Add secret]
```

**4. Verificar workflow:**
```
Actions > Deploy > Último run

Vá para "deploy-staging" job
Vá para "Deploy to staging" step
Veja os logs
```

---

## 🎓 Resumo Final

| Tipo | Uso | Quantidade | Criado em |
|------|-----|-----------|----------|
| **Repository Secrets** | Globais, compartilhados | 3 (opcional) | Settings > Secrets |
| **Environment Secrets (staging)** | Só para staging | 3 | Settings > Environments > staging |
| **Environment Secrets (prod)** | Só para production | 3 | Settings > Environments > production |
| **Total** | - | **9 secrets** | - |

### Checklist Final Antes de Fazer Deploy

- [ ] ✅ Todos os 6 environment secrets criados (3 staging + 3 prod)
- [ ] ✅ SSH keys testadas localmente
- [ ] ✅ Servidor pode conectar com SSH
- [ ] ✅ Usuário SSH existe no servidor
- [ ] ✅ Diretários necessários existem (`/app`, `/app/.git`, etc)
- [ ] ✅ Repository secrets criados (opcional mas recomendado)
- [ ] ✅ Environment protection rules configuradas
- [ ] ✅ Primeiro workflow de deploy pode ser executado

---

**Próximo:** Depois de configurar todos os secrets, faça seu primeiro PR para testar! 🚀
