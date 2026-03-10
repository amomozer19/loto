# 🔐 Como Obter GitGuardian API Key - Guia Passo a Passo

## 📍 O que é GitGuardian?

**GitGuardian** é um serviço que detecta automaticamente **secrets vazados** em seu repositório GitHub:
- Chaves de API
- Tokens de acesso
- Senhas
- Chaves SSH
- Etc.

Ele escaneia histórico de commits e pull requests.

---

## 🚀 Passo 1: Acessar GitGuardian

### Opção A: Versão Grátis (Recomendado)

1. Vá para **[gitguardian.com](https://www.gitguardian.com)**

2. Clique em **"Start Free"** (botão no topo right)

```
Website: gitguardian.com
          ├─ [Start Free] ← CLIQUE AQUI
          └─ [Sign In]
```

---

## 🎯 Passo 2: Criar Conta GitGuardian

### Tela de Cadastro:

```
┌─────────────────────────────────────────────────────────┐
│ GitGuardian - Create your account                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ First Name *                                            │
│ [_______________________]                               │
│                                                         │
│ Last Name *                                             │
│ [_______________________]                               │
│                                                         │
│ Email *                                                 │
│ [_______________________]                               │
│ seu-email@example.com                                   │
│                                                         │
│ Password *                                              │
│ [_______________________]                               │
│ (mínimo 8 caracteres)                                   │
│                                                         │
│ Confirm Password *                                      │
│ [_______________________]                               │
│                                                         │
│ ☑ I agree to the Terms of Service                      │
│                                                         │
│ [Create Account] (botão azul)                           │
└─────────────────────────────────────────────────────────┘
```

**Preencha com:**
- First Name: Seu primeiro nome
- Last Name: Seu sobrenome
- Email: Seu email
- Password: Senha forte
- Confirme a senha

**Clique:** [Create Account]

---

## 📧 Passo 3: Verificar Email

1. Vá para sua caixa de entrada de email
2. Procure por email de **GitGuardian Support** ou **noreply@gitguardian.com**
3. Clique no link de **verificação/confirmação**
4. Volta ao navegador

---

## 🔑 Passo 4: Acessar Settings (Pessoal)

Após login, clique no seu **perfil/avatar** (canto superior direito):

```
┌─────────────────────────────────────────────────────────┐
│ GitGuardian Dashboard                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ No topo direito:                                        │
│ [👤 seu-usuario] ← CLIQUE AQUI (dropdown)              │
│                                                         │
│ Opções do menu:                                         │
│ ├─ My Workspace                                         │
│ ├─ Settings ← CLIQUE AQUI                              │
│ ├─ Profile                                              │
│ └─ Logout                                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Clique em:** Settings

---

## 🔗 Passo 5: Acessar Personal Access Token

Na página de Settings, você verá várias seções. Procure por:

```
Settings
├─ Account
├─ Workspace
├─ Quota ← (mostra seu uso)
├─ Personal Access Tokens ← CLIQUE AQUI
└─ ...
```

**Clique em:** Personal Access Tokens

---

## ⚙️ Passo 6: Gerar Personal Access Token

Na página de **Personal Access Tokens**, você vê:

```
┌─────────────────────────────────────────────────────────┐
│ Settings > Personal Access Tokens                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Personal Access Tokens                                  │
│                                                         │
│ [+ Create Token] (botão azul) ← CLIQUE AQUI             │
│                                                         │
│ No tokens yet                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Clique em:** [+ Create Token]

---

## 🏷️ Passo 7: Nomear a API Key

```
┌─────────────────────────────────────────────────────────┐
│ Create a new API key                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ API Key Name *                                          │
│ [_______________________]                               │
│ GitHub Actions                                          │
│ (ou qualquer nome descritivo)                           │
│                                                         │
│ [Create] (botão)                                        │
│                      o Token

```
┌─────────────────────────────────────────────────────────┐
│ Create Personal Access Token                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Token Name *                                            │
│ [_______________________]                               │
│ GitHub Actions                                          │
│ (ou: LOTO_CI, CI/CD,o Personal Access Token

A tela mostrará seu token gerado:

```
┌─────────────────────────────────────────────────────────┐
│ Personal Access Token Created                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ⚠️  IMPORTANTE: Copie o token agora!                    │
│ Depois de sair desta página, você NÃO conseguirá        │
│ ver o token completo novamente.                         │
│                                                         │
│ Personal Access Token:                                  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ggshield_70f3c... (mascarado, mas aparece inteiro)  │ │
│ │ Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx             │ │
│ │                                                     │ │
│ │ [📋 Copy] (clique para copiar)                      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [Done] ou [Close]                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### ⚠️ IMPORTANTE:
```
🔴 COPIE O TOKEN AGORA
   Você não conseguirá vê-lo novamente após sair!

✅ CLIQUE EM [📋 Copy] para copiar automaticamente
   OU
   Selecione e pressione Ctrl+C (Windows/Linux)
   ou Cmd+C (Mac)

📝 Formato esperado:
   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   (Aprox. 40-50 caracteres de texto aleatório

### ⚠️ IMPORTANTE:
```
🔴 COPIE A CHAVE AGORA
   Você não conseguirá vê-la novamente após sair

✅ CLIQUE EM [📋 Copy] para copiar automaticamente
   OU
   Selecione e pressione Ctrl+C (Windows/Linux)
   ou Cmd+C (Mac)
```

---

## 🔐 Passo 9: Adicionar ao GitHub Secrets

Com a chave copiada, vá para seu repositório GitHub:

```
GitHub.com
├─ SEU-USUARIO/Loto
│  └─ Settings
│     └─ Secrets and variables
│        └─ Actions
│           └─ Secrets
│              └─ [New repository secret] ← CLIQUE AQUI
```

**Preencha:**

```
┌─────────────────────────────────────────────────────────┐
│ New repository secret                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Name *                          Secret *                │
│ [________________]          [_________________]         │
│ GITGUARDIAN_API_KEY        (cole a chave aqui)        │
│                             ghp_xxxxxxxxxxxxxxx        │
│                                                         │
│ [Add secret] (botão azul)                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Passos:**
1. **Name:** Digite `GITGUARDIAN_API_KEY`
2. **Secret:** Cole a chave copiada do GitGuardian
3. **Clique:** [Add secret]

---

## ✅ Verificar se Funcionou

Depois de adicionar, você verá na lista:

```
REPOSITORY SECRETS
├─ GITGUARDIAN_API_KEY ✅
│  Criado em 7 de março de 2026
```
e token automaticamente:

```yaml
- name: GitGuardian - Secret detection
  uses: GitGuardian/ggshield-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}  # ← Personal Access Token
```

Para testar:
1. Faça um commit
2. Vá para **Actions** no GitHub
3. Clique em **security** workflow
4. Expanda o job **secrets-scan**
5. Veja se **GitGuardian - Secret detection** rodou sem erros
6. Verifique logs para mensagens de sucesso
1. Faça um commit
2. Vá para **Actions** no GitHub
3. Clique em **security** workflow
4. Expanda o job **secrets-scan**
5. Veja se **GitGuardiatoken" ou "Unauthorized"

**Causa:** Token foi copiado incorretamente, expirou ou erro de digitação

**Solução:**
```
1. Volte para GitGuardian.com > Settings > Personal Access Tokens
2. Verifique se o token está listado (Status: Active)
3. Se expirou: Delete e crie um novo
4. Copie exatamente (todo o conteúdo)
5. Atualize no GitHub Secret:
   Settings > Secrets > GITGUARDIAN_API_KEY > Update
6. Re-run o workflow:
   Actions > security > Re-run all jobs
```

### Problema: "Token not set"

**Causa:** Secret não foi criado no GitHub

**Solução:**
```
1. GitHub > Settings > Secrets and variables > Actions
2. Verifique se GITGUARDIAN_API_KEY está na lista
3. Se não tiver, crie novo repository secret:
   Name: GITGUARDIAN_API_KEY
   Secret: (cole o token do GitGuardian)
4``
1. Volte para GitGuardian.com > Settings > API
2. Delete a chave antiga
3. Crie uma nova chave
4. Copie exatamente
5. Atualize no GitHub Secret
6. Re-run o workflow
```

### Problema: GitGuardian ação não aparece nos logs

**Causa:** Secret não foi criado ou workflow não usa

**Solução:**
```
1. Verifique se secret existe: Settings > Secrets
2. Verifique se workflDetecção de secrets, 1 Personal Access Token, API básica | Hobby/Pequenos projetos |
| **Pro** | €10-20/mês | Repositórios privados, suporte prioritário, mais tokens | Freelancers/Equipes |
| **Team** | €50+/mês | Múltiplos workspaces, gerenciamento de equipe | Empresas |

**Para você:** O plano **Free** é suficiente! ✅  
**Bônus:** Personal Access Tokens são gratuitos em todos os planos
### Problema: "Rate limit exceeded"

**Causa:** Muitos requests em pouco tempo

**Solução:**
```
1. Aguarde 1 hora
2. Use a API Key apenas em um workflow
3. Configure retry na ação
```

---

## 💰 Planos GitGuardian

| Plano | Custo | Features | Ideal Para |
|-------|-------|----------|-----------|
| **Free** | Grátis | 1 workspace, repos públicos | Hobby/Pequenos projetos |
| **Pro** | €10-20/mês | Repos privados, melhor suporte | Freelancers/Pequenas equipes |
| **Team** | €50+/mês | Múltiplos workspaces, alertas | Empresas/Grandes equipes |

**Para você:** O plano **Free** é suficiente! ✅

---

## 🔄 Próximas Etapas

Agora que você tem a API Key:

```
1. ✅ Adicionar ao GitHub Secret (GITGUARDIAN_API_KEY)
2. ⏭️  Adicionar outros Repository Secrets (opcional)
   - SLACK_WEBHOOK (notificações)
   - CODECOV_TOKEN (cobertura)
3. ⏭️  Fazer primeiro commit para testar
4. ⏭️  Verificar se security.yml rodou com sucesso
```

---

## 📊 RHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}  # ← Personal Access Token
  continue-on-error: true
```

**Benefícios:**
- ✅ Detecta secrets (chaves, tokens, senhas) acidentalmente commitados
- ✅ Previne vazamento de dados sensíveis
- ✅ Avisa em tempo real durante CI/CD
- ✅ Funciona em todo histórico Git (histórico de commits)
- ✅ Integrado no GitHub Actions automaticamente
- ✅ Grátis para plano Community/Open Source Codecov.io (automático) |
| **DEPLOY_KEY_STAGING** | Environment | SSH keygen local |
| **DEPLOY_KEY_PROD** | Environment | SSH keygen local |
| E mais... | Environment | - |

---

## 🎓 Por Que GitGuardian?

Seu workflow `security.yml` já está configurado para usar:

```yaml
- name: GitGuardian - Secret detection
  uses: GitGuardian/ggshield-action@master
  env:
    GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}
  continue-on-error: true
```

**Benefícios:**
- ✅ Detecta secrets acidentalmente commitados
- ✅ Previne vazamento de dados
- ✅ Avisa em tempo real
- ✅ Funciona em todo histórico Git

---

**Próximo:** Depois de obter a chave, adicione ao GitHub e teste! 🚀

Ver: [GITHUB_SECRETS_DETAILED.md](GITHUB_SECRETS_DETAILED.md)
