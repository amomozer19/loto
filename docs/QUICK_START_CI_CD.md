# ⚡ Quick Start - Esteira de CI/CD

## 1️⃣ Primeiros Passos (5 minutos)

### Adicionar ao seu repositório:

```bash
git add .github/ Dockerfile* docker-compose.dev.yml
git add Makefile pyproject.toml .pylintrc sonar-project.properties
git add docs/DEVELOPMENT.md docs/GITHUB_ACTIONS_SETUP.md docs/COMMIT_CONVENTIONS.md docs/CI_CD_PIPELINE_OVERVIEW.md
git commit -m "ci: configurar esteira de CI/CD"
git push origin main
```

### Verificar no GitHub:

1. Vá para seu repositório
2. Clique em **Actions**
3. Você verá os workflows sendo executados! ✅

---

## 2️⃣ Configurar Secrets (5 minutos)

**Settings > Secrets and variables > Actions**

### Obrigatório para Deploy:
```
DEPLOY_KEY_STAGING = <sua-ssh-private-key>
DEPLOY_HOST_STAGING = seu-server.com ou IP
DEPLOY_USER_STAGING = seu-usuario

DEPLOY_KEY_PROD = <sua-ssh-private-key>
DEPLOY_HOST_PROD = prod-server.com ou IP
DEPLOY_USER_PROD = seu-usuario
```

### Opcional (Notifications):
```
SLACK_WEBHOOK = https://hooks.slack.com/...
```

---

## 3️⃣ Ativar Branch Protection (2 minutos)

**Settings > Branches > Add rule** para `main`:

```
✅ Require a pull request before merging
✅ Require status checks to pass before merging
   - test (3.8)
   - test (3.9)
   - test (3.10)
   - test (3.11)
   - code-quality
   - security
   - docker
✅ Require code reviews (1 minimum)
✅ Include administrators
```

---

## 4️⃣ Fazer Primeiro Commit com CI/CD

```bash
# Criar feature branch
git checkout -b feature/test-ci

# Fazer mudança
echo "# Test" >> README.md

# Testar localmente
make test
make lint

# Commit com convenção
git commit -m "feat: adicionar teste de CI"
git push origin feature/test-ci

# Criar PR
# (No GitHub: Compare & pull request)
```

**Resultado:**
- ✅ CI workflow roda testes
- ✅ Security workflow roda scans
- ✅ Lint workflow roda formatação
- ✅ Merge é bloqueado até tudo passar

---

## 5️⃣ Fazer Deploy para Staging

```bash
# Merge PR para main
git checkout main
git pull origin main

# Push para main
git push origin main

# Automáticamente:
# 1. Docker image é buildada
# 2. Deploy para staging
# 3. Health check realizado
# 4. Slack notificação (se configurado)
```

**Acesso:**
```
Staging: https://staging.seu-dominio.com
```

---

## 6️⃣ Fazer Release para Produção

```bash
# Criar tag (semver)
git tag v1.0.0

# Push tag
git push origin v1.0.0

# Automáticamente:
# 1. Docker image é buildada
# 2. Release criada no GitHub
# 3. Deploy para produção
# 4. Health check realizado
# 5. Slack notificação
```

**Acesso:**
```
Produção: https://seu-dominio.com
```

---

## 📋 Checklist Completo

### Setup
- [ ] Arquivos .github/ adicionados
- [ ] Arquivos de configuração adicionado
- [ ] Documentação adicionada

### GitHub Configuration
- [ ] Secrets configurados
- [ ] Branch protection ativada
- [ ] Environments criados (staging/production)

### Integrações (Opcional)
- [ ] Codecov integrado
- [ ] Slack notificações
- [ ] SonarCloud ativado

### Primeiros Testes
- [ ] Primeiro workflow rodou
- [ ] Testes passaram
- [ ] PR merge bem-sucedido

---

## 🎯 Comandos Úteis

```bash
# Desenvolvimento
make install-dev        # Instalar dependências
make test               # Rodar testes
make lint               # Verificar código
make format             # Formatar código
make run                # Rodar aplicação
make dev-run            # Rodar em desenvolvimento

# Docker
make docker-up          # Iniciar containers
make docker-down        # Parar containers
docker-compose -f docker-compose.dev.yml logs -f web

# Git
git checkout -b feature/nome   # Criar branch
git commit -m "feat: descrição" # Commit com tipo
git push origin feature/nome    # Push
git tag v1.0.0                 # Criar tag
git push origin v1.0.0         # Push tag
```

---

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| **Workflow não executa** | Verifique se YAML está correto: `yamllint .github/workflows/` |
| **Testes falham no CI** | Execute localmente: `make test` com mesma Python version |
| **Deploy falha** | Verificar secrets: `Settings > Secrets` |
| **GitHub Actions não encontra** | Aguarde 30s e refresh: `Actions > Re-run all jobs` |

---

## 📞 Suporte

- **Documentação:** `docs/DEVELOPMENT.md`
- **GitHub Actions:** `docs/GITHUB_ACTIONS_SETUP.md`
- **Commits:** `docs/COMMIT_CONVENTIONS.md`
- **Visão Geral:** `docs/CI_CD_PIPELINE_OVERVIEW.md`

---

## ✨ Próximo?

Parabéns! 🎉 Sua esteira de CI/CD está configurada!

**Recomendações:**
1. Faça seu primeiro commit de teste
2. Abra uma PR e veja os testes rodando
3. Faça merge e veja o deploy para staging
4. Crie uma tag e faça release para produção

Qualquer dúvida, consulte a documentação em `docs/`.

