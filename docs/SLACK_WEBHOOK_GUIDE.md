# 🛎️ Como Obter Slack Webhook - Guia Passo a Passo

## 📍 O que é Slack Webhook?

Um **Webhook** do Slack permite que aplicações enviem mensagens automaticamente para um canal do Slack.

Seu workflow `deploy.yml` usará isso para notificar quando:
- ✅ Deploy para staging foi bem-sucedido
- ❌ Deploy para produção falhou
- 🔒 Segurança: vulnerabilidades encontradas

---

## 🚀 Passo 1: Ter Workspace Slack

Você precisa ter acesso a um workspace Slack.

### Se não tiver conta Slack:

1. Vá para **[slack.com](https://slack.com)**
2. Clique em **"Create your Slack workspace"**
3. Siga as instruções para criar workspace
4. Confirme email

### Se já tiver ou tiver acesso:

Vá para seu workspace: `https://seu-workspace.slack.com`

---

## 🔧 Passo 2: Acessar Slack Apps

Para criar um webhook, você precisa criar um "App" no Slack:

1. Vá para **[api.slack.com](https://api.slack.com)**

```
api.slack.com
├─ Your Apps (no topo)
└─ [Create New App] ← CLIQUE AQUI (botão azul)
```

---

## ⚙️ Passo 3: Criar Novo App

```
┌─────────────────────────────────────────────────────────┐
│ Create an app                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ○ From scratch    ← SELECIONE ESTA                      │
│ ○ From an app manifest                                  │
│                                                         │
│ [Next]                                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Selecione:** From scratch

**Clique:** [Next]

---

## 🏷️ Passo 4: Nomear o App

```
┌─────────────────────────────────────────────────────────┐
│ Create an app                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ App Name *                                              │
│ [_______________________]                               │
│ Loto CI/CD                                              │
│ (ou: Loto Bot, GitHub Actions, etc)                    │
│                                                         │
│ Pick a workspace to develop your app in *              │
│ [Dropdown]                                              │
│ seu-workspace                                           │
│                                                         │
│ [Create App]                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Preencha:**
- App Name: `Loto CI/CD` (ou qualquer nome)
- Workspace: Selecione seu workspace

**Clique:** [Create App]

---

## 🔑 Passo 5: Habilitar Webhooks

Após criar o app, você vê o dashboard:

```
┌─────────────────────────────────────────────────────────┐
│ Loto CI/CD App Configuration                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Left Sidebar:                                           │
│ ├─ Settings                                             │
│ │  ├─ Basic Information                                │
│ │  └─ Incoming Webhooks ← CLIQUE AQUI                 │
│ ├─ Features                                             │
│ └─ ...                                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Clique em:** Incoming Webhooks (no left sidebar)

---

## 📍 Passo 6: Ativar Incoming Webhooks

```
┌─────────────────────────────────────────────────────────┐
│ Incoming Webhooks                                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Incoming Webhooks                                       │
│ [OFF] ← TOGGLE AQUI para ON                             │
│                                                         │
│ Depois de ativar, você verá:                            │
│ [Add New Webhook to Workspace]                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Clique no toggle:** ON

---

## 🎯 Passo 7: Criar Webhook URL

```
┌─────────────────────────────────────────────────────────┐
│ Incoming Webhooks (Ativado)                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [Add New Webhook to Workspace] (botão) ← CLIQUE AQUI    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Clique em:** [Add New Webhook to Workspace]

---

## 💬 Passo 8: Escolher Canal

Você vê um popup pedindo qual canal:

```
┌─────────────────────────────────────────────────────────┐
│ Select a Channel                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Choose a channel to post to:                            │
│ [Dropdown]                                              │
│ ├─ #general ← RECOMENDADO                              │
│ ├─ #random                                              │
│ ├─ #devops                                              │
│ └─ (outros canais)                                      │
│                                                         │
│ [Authorize] (botão verde)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Selecione:** Um canal (ex: #general ou crie #loto-ci)

**Clique:** [Authorize]

---

## 🔗 Passo 9: Copiar Webhook URL

Após autorizar, você vê a URL do webhook:

```
┌─────────────────────────────────────────────────────────┐
│ Webhook URL                                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ⚠️  IMPORTANTE: Copie a URL agora!                      │
│ Depois de sair, será difícil encontrar novamente.       │
│                                                         │
│ Webhook URL:                                            │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ https://hooks.slack.com/services/T00000000/        │ │
│ │ B00000000/XXXXXXXXXXXXXXXXXXXXXXXX                 │ │
│ │                                                     │ │
│ │ [📋 Copy] (clique para copiar)                      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [Done]                                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ⚠️ IMPORTANTE:
```
🔴 COPIE A URL COMPLETA AGORA
   Formato: https://hooks.slack.com/services/T.../B.../XXX...

✅ CLIQUE [📋 Copy] ou selecione e Ctrl+C
```

---

## 🔐 Passo 10: Adicionar ao GitHub Secrets

Com a URL copiada, vá para seu repositório GitHub:

```
GitHub.com
├─ SEU-USUARIO/Loto
│  └─ Settings
│     └─ Secrets and variables
│        └─ Actions
│           └─ Secrets
│              └─ Repository secrets
│                 └─ [New repository secret] ← CLIQUE AQUI
```

**Preencha:**

```
┌─────────────────────────────────────────────────────────┐
│ New repository secret                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Name *                          Secret *                │
│ [________________]          [_________________]         │
│ SLACK_WEBHOOK              (cole a URL aqui)           │
│                            https://hooks.slack.com/... │
│                                                         │
│ [Add secret] (botão azul)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Passos:**
1. **Name:** Digite `SLACK_WEBHOOK`
2. **Secret:** Cole a URL completa do Slack
3. **Clique:** [Add secret]

---

## ✅ Verificar se Funcionou

Depois de adicionar, você verá:

```
REPOSITORY SECRETS
├─ SLACK_WEBHOOK ✅
│  Criado em 7 de março de 2026
```

---

## 🧪 Teste: Enviar Mensagem de Teste

### Opção 1: Fazer um Commit

```bash
git checkout -b test/slack-webhook
echo "# Test" >> README.md
git add .
git commit -m "test: slack webhook"
git push origin test/slack-webhook
```

Vá para **Actions** no GitHub e veja se o workflow `deploy` roda.

Se tudo funcionar, você receberá uma notificação no Slack! 🎉

### Opção 2: Testar Manualmente (curl)

```bash
# No seu terminal (substitua a URL)
curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"Test message from GitHub Actions"}' \
    https://hooks.slack.com/services/SEU_WEBHOOK_URL

# Você verá a mensagem aparecer no Slack instantaneamente
```

---

## 💬 Personalizar Mensagens

Seu workflow `deploy.yml` envia mensagens assim:

```yaml
- name: Send Slack notification
  uses: slackapi/slack-github-action@v1.24.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Deploy Status: ${{ job.status }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Deploy Status*\nRepository: ${{ github.repository }}\nBranch: ${{ github.ref }}\nStatus: ${{ job.status }}"
            }
          }
        ]
      }
```

### Exemplo de Mensagens Esperadas:

**Sucesso:**
```
✅ Deploy Status: success
Repository: seu-usuario/Loto
Branch: refs/heads/main
Status: success
Timestamp: 2024-03-07 18:30:00
```

**Falha:**
```
❌ Deploy Status: failure
Repository: seu-usuario/Loto
Branch: refs/heads/main
Status: failure
Timestamp: 2024-03-07 18:35:00
```

---

## 🐛 Troubleshooting

### Problema: Webhook URL não funciona

**Causa:** URL foi copiada incorretamente ou parcialmente

**Solução:**
```
1. Volte para api.slack.com
2. Seu app > Incoming Webhooks
3. Copie a URL novamente (completa)
4. Atualize o secret no GitHub
5. Re-run o workflow
```

### Problema: Mensagens não chegam ao Slack

**Causa:** Webhook URL inválida no GitHub

**Solução:**
```
1. Verifique se secret está criado: Settings > Secrets
2. Teste com curl (veja acima)
3. Verifique se canal foi autorizado
4. Re-run o workflow
```

### Problema: "Invalid webhook URL"

**Causa:** URL foi editada ou truncada

**Solução:**
```
1. Delete o webhook antigo em api.slack.com
2. Crie um novo webhook
3. Copie a URL completa (com cuidado)
4. Atualize no GitHub
```

---

## 🔄 Próximas Etapas

Agora que você tem Slack Webhook:

```
1. ✅ Adicionar ao GitHub Secret (SLACK_WEBHOOK)
2. ⏭️  Adicionar GitGuardian API Key (opcional)
3. ⏭️  Adicionar outros secrets (deploy keys)
4. ⏭️  Fazer primeiro commit para testar
5. ⏭️  Verificar notificações no Slack
```

---

## 📊 Resumo: Secrets do Seu Projeto

Após completar, você terá:

| Secret | Tipo | Onde Obter |
|--------|------|-----------|
| **SLACK_WEBHOOK** | Repository | Slack.com API > Incoming Webhooks |
| **GITGUARDIAN_API_KEY** | Repository | GitGuardian.com > Settings > API |
| **CODECOV_TOKEN** | Repository | Codecov.io (automático) |
| **DEPLOY_KEY_STAGING** | Environment (staging) | SSH keygen |
| **DEPLOY_HOST_STAGING** | Environment (staging) | Seu servidor |
| **DEPLOY_USER_STAGING** | Environment (staging) | usuário SSH |
| **DEPLOY_KEY_PROD** | Environment (production) | SSH keygen |
| **DEPLOY_HOST_PROD** | Environment (production) | Seu servidor |
| **DEPLOY_USER_PROD** | Environment (production) | usuário SSH |

---

## 🎓 Por Que Slack Webhook?

Benefícios:
- ✅ Notificações em tempo real de depoys
- ✅ Toda equipe vê status
- ✅ Integrado ao workflow
- ✅ Sem custo adicional
- ✅ Fácil de configurar

---

**Próximo:** Depois de obter a chave, adicione ao GitHub e teste! 🚀

Ver: [GITHUB_SECRETS_DETAILED.md](GITHUB_SECRETS_DETAILED.md)
