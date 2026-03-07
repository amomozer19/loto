# 🎬 Configurar Secrets - Guia Visual Rápido (5 minutos)

## Mapa Mental: Onde Colocar Cada Secret

```
                          GITHUB SECRETS
                                │
                ┌───────────────┴───────────────┐
                │                               │
        REPOSITORY SECRETS          ENVIRONMENT SECRETS
        (Global - Todos veem)       (Isolado por ambiente)
                │                               │
                │                        ┌──────┴──────┐
                │                        │             │
          SLACK_WEBHOOK         STAGING          PRODUCTION
    GITGUARDIAN_API_KEY     3 Secrets            3 Secrets
       CODECOV_TOKEN


QUAL USAR?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ É um secret igual para TODOS os ambientes?
   └─→ ✅ REPOSITORY SECRETS (ex: SLACK_WEBHOOK)

❓ É um secret DIFERENTE para staging vs production?
   └─→ ✅ ENVIRONMENT SECRETS (ex: DEPLOY_KEY_STAGING vs DEPLOY_KEY_PROD)

❓ Precisa de separação de segurança/aprovações?
   └─→ ✅ ENVIRONMENT SECRETS (ativa protection rules)
```

---

## 🚀 Passo a Passo Visual (3 minutos)

### PASSO 1: Ir para Settings > Secrets

```
https://github.com/SEU-USUARIO/Loto
                                    │
                                    └─→ [Settings] (engrenagem)
                                        │
                                        └─→ "Secrets and variables" (left sidebar)
                                            │
                                            └─→ "Actions" (tab)
```

**Tela do GitHub:**
```
┌─────────────────────────────────────────────────────────────┐
│ SEU-USUARIO / Loto                                          │
├─────────────────────────────────────────────────────────────┤
│ Code | Issues | Pull requests | Discussions | Actions      │
│ Settings                                                    │
├─────────────────────────────────────────────────────────────┤
│ Left Sidebar:                                               │
│ ├─ General                                                  │
│ ├─ Access                                                   │
│ ├─ Code and automation                                      │
│ │  ├─ Branches                                              │
│ │  ├─ Ruleset                                               │
│ │  ├─ Actions                                               │
│ │  └─ Secrets and variables ← CLIQUE AQUI                  │
│ ├─ Integrations                                             │
│ └─ ...                                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### PASSO 2A: Adicionar REPOSITORY SECRETS (Opcional)

Quando você clicar em "Secrets and variables > Actions", você verá:

```
┌─────────────────────────────────────────────────────────────┐
│ Actions secrets and variables                               │
├─────────────────────────────────────────────────────────────┤
│ [Secrets] [Variables] [Dependabot secrets]                  │
│                                                             │
│ REPOSITORY SECRETS                                          │
│ (New repository secret)  ← CLIQUE PARA ADICIONAR           │
│                                                             │
│ Repository secrets accessible to Actions workflows         │
│                                                             │
│ ENVIRONMENT SECRETS                                         │
│ (configurar mais abaixo)                                    │
└─────────────────────────────────────────────────────────────┘
```

**Clique em "New repository secret":**

```
┌─────────────────────────────────────────────────────────────┐
│ Actions secrets and variables / New secret                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Name *                          Secret *                    │
│ [_______________]           [_________________]             │
│                                                             │
│ SLACK_WEBHOOK               (seu-webhook-url)              │
│                                                             │
│                             [Add secret] (verde)            │
└─────────────────────────────────────────────────────────────┘
```

**Opcional - Adicione estes Repository Secrets:**
- SLACK_WEBHOOK (para notificações)
- GITGUARDIAN_API_KEY (para segurança)
- CODECOV_TOKEN (para cobertura)

---

### PASSO 2B: Configurar ENVIRONMENT SECRETS (Obrigatório)

Ainda em Settings, clique em **"Environments"** (no left sidebar):

```
Left Sidebar:
├─ General
├─ Access
├─ Code and automation
│  └─ Secrets and variables
│
├─ Environments ← CLIQUE AQUI
│  ├─ [New environment]
│  ├─ staging (criar isto)
│  └─ production (criar isto)
```

**Tela de Environments:**

```
┌─────────────────────────────────────────────────────────────┐
│ Environments                                                │
├─────────────────────────────────────────────────────────────┤
│ Environment secrets accessible to Actions workflows         │
│                                                             │
│ [New environment] (botão azul)                              │
│                                                             │
│ No environments yet                                         │
└─────────────────────────────────────────────────────────────┘
```

---

### PASSO 3A: Criar Environment "staging"

Clique em **[New environment]**:

```
┌─────────────────────────────────────────────────────────────┐
│ New environment                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Name *                                                      │
│ [________________]                                          │
│  staging                                                    │
│                                                             │
│ [Configure protection rules] (opcional)                     │
│                                                             │
│ [> Create environment] (botão)                              │
└─────────────────────────────────────────────────────────────┘
```

**Digite:** `staging`  
**Clique:** [Create environment]

---

### PASSO 3B: Adicionar Secrets ao Environment "staging"

Depois de criar, você vê:

```
┌─────────────────────────────────────────────────────────────┐
│ staging                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Environment secrets                                         │
│ [Add secret]  ← CLIQUE 3 VEZES                              │
│                                                             │
│ No environment secrets yet                                  │
└─────────────────────────────────────────────────────────────┘
```

**Clique em [Add secret] primeira vez:**

```
┌─────────────────────────────────────────────────────────────┐
│ staging / New environment secret                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Secret name *           Value *                             │
│ [________________]   [_________________]                    │
│ DEPLOY_KEY_STAGING  (copie sua chave SSH privada aqui)     │
│                     -----BEGIN OPENSSH...                   │
│                     ...                                     │
│                     -----END OPENSSH...                     │
│                                                             │
│                         [Add secret]                        │
└─────────────────────────────────────────────────────────────┘
```

**Clique em [Add secret] segunda vez:**

```
Secret name: DEPLOY_HOST_STAGING
Value: seu-servidor-staging.com
       (ou IP: 192.168.1.100)

[Add secret]
```

**Clique em [Add secret] terceira vez:**

```
Secret name: DEPLOY_USER_STAGING
Value: deploy
       (ou seu-usuario)

[Add secret]
```

---

### PASSO 4: Repetir para Environment "production"

Volte para **Environments** e clique **[New environment]** novamente:

```
Name: production

[Create environment]
```

**Adicione os 3 mesmos secrets (production):**
1. DEPLOY_KEY_PROD = (sua chave SSH privada)
2. DEPLOY_HOST_PROD = seu-servidor-prod.com
3. DEPLOY_USER_PROD = deploy

---

## ✅ Checklist Rápido

### Repository Secrets (Opcional)
```
☐ SLACK_WEBHOOK
☐ GITGUARDIAN_API_KEY
☐ CODECOV_TOKEN
```

### Environment "staging" (Obrigatório)
```
☐ DEPLOY_KEY_STAGING
☐ DEPLOY_HOST_STAGING
☐ DEPLOY_USER_STAGING
```

### Environment "production" (Obrigatório)
```
☐ DEPLOY_KEY_PROD
☐ DEPLOY_HOST_PROD
☐ DEPLOY_USER_PROD
```

---

## 🔑 Como Preparar as Chaves SSH

### No seu computador (gerar chaves):

```bash
# Criar pasta se não existir
mkdir -p ~/.ssh
cd ~/.ssh

# Gerar chave para STAGING
ssh-keygen -t ed25519 -C "github-loto-staging" -f loto_staging -N ""

# Gerar chave para PRODUCTION
ssh-keygen -t ed25519 -C "github-loto-production" -f loto_prod -N ""

# Resultado:
# loto_staging (arquivo privado)
# loto_staging.pub (arquivo público)
# loto_prod (arquivo privado)
# loto_prod.pub (arquivo público)
```

### Ver conteúdo das chaves:

```bash
# Para copiar e colar no GitHub
cat ~/.ssh/loto_staging
cat ~/.ssh/loto_prod

# Copiar para clipboard (conforme seu SO)
# Mac:
cat ~/.ssh/loto_staging | pbcopy

# Linux:
cat ~/.ssh/loto_staging | xclip -selection clipboard

# Windows (Git Bash):
cat ~/.ssh/loto_staging | clip
```

### Adicionar ao seu servidor:

```bash
# SSH no servidor staging
ssh seu-usuario@seu-servidor-staging.com

# Adicionar chave pública
mkdir -p ~/.ssh
cat >> ~/.ssh/authorized_keys << 'EOF'
<COPIE O CONTEÚDO DE loto_staging.pub AQUI>
EOF

chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Testar (sair e reconectar)
exit
ssh -i ~/.ssh/loto_staging seu-usuario@seu-servidor-staging.com
# Deve conectar SEM pedir senha
```

---

## 🎯 Ordem Correta para Fazer

```
1️⃣  Gerar SSH keys localmente
    ssh-keygen ...

2️⃣  Adicionar chaves públicas no servidor
    cat loto_staging.pub >> ~/.ssh/authorized_keys

3️⃣  Testar SSH funciona
    ssh -i loto_staging seu-usuario@servidor

4️⃣  Ir para GitHub > Settings > Environments

5️⃣  Criar "staging" environment
    + adicionar 3 secrets

6️⃣  Criar "production" environment
    + adicionar 3 secrets

7️⃣  (Opcional) Adicionar repository secrets
    + SLACK_WEBHOOK, etc

8️⃣  Pronto! Fazer primeiro commit e PR
```

---

## 🐛 Checklist de Teste

Depois de configurar tudo:

```bash
# Teste 1: Arquivo SSH gerado corretamente?
ls -la ~/.ssh/loto_*
# Output: 4 arquivos (2 pares)

# Teste 2: SSH conecta sem senha?
ssh -i ~/.ssh/loto_staging seu-usuario@servidor
# Sucesso = conectou
# Fracasso = pede senha

# Teste 3: Servidor preparado?
ssh seu-usuario@servidor
mkdir -p /app
ls /app
# Deve existir ou você pode criar

# Teste 4: GitHub tem os secrets?
GitHub > Settings > Environments > staging
# Deve mostrar: 3 secrets (keys selecionados)

# Teste 5: Fazer PR e verificar Actions
git checkout -b test-ci
echo "# test" >> README.md
git commit -m "test: ci workflow"
git push origin test-ci
# GitHub > Actions > Vê o workflow rodando?
```

---

## 🎓 Diferença Prática Resumida

Seu workflow faz isso:

```yaml
jobs:
  deploy-staging:
    environment: staging          # ← Procura secrets aqui PRIMEIRO
    steps:
      - run: |
          KEY=${{ secrets.DEPLOY_KEY_STAGING }}
          HOST=${{ secrets.DEPLOY_HOST_STAGING }}
          # Se não achar em staging, procura em repository
```

**Resumo:**
- ✅ **Environment Secrets:** Isolado por ambiente (staging ≠ production)
- ✅ **Repository Secrets:** Compartilhado em TODOS os ambientes

---

**Próximo:** Fazer primeiro commit e testar! 🚀
