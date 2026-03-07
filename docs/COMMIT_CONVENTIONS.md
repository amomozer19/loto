# Convenção de Commits - Semantic Versioning

## Formato Padrão

```
<tipo>[escopo opcional]: <descrição curta>

[corpo opcional]

[rodapé(s) opcional(is)]
```

## Tipos de Commits

### ✨ feat
Adiciona uma nova funcionalidade (compatível com MINOR no semver)

```bash
git commit -m "feat(auth): adicionar autenticação com Google OAuth"
git commit -m "feat: implementar validação de apostas"
```

### 🐛 fix
Corrige um bug (compatível com PATCH no semver)

```bash
git commit -m "fix(api): corrigir erro 500 em /statistics"
git commit -m "fix(db): resolver problema de conexão"
```

### 📝 docs
Mudanças em documentação apenas

```bash
git commit -m "docs: atualizar README com instruções de setup"
git commit -m "docs(api): adicionar exemplos de endpoints"
```

### 🎨 style
Mudanças que não afetam funcionalidade (formatting, indentação, etc)

```bash
git commit -m "style: formatar código com black"
git commit -m "style(css): atualizar cores do tema"
```

### ♻️ refactor
Refatoração sem mudança de funcionalidade ou correção de bug

```bash
git commit -m "refactor(utils): extrair lógica de validação"
git commit -m "refactor(models): reorganizar imports"
```

### ⚡ perf
Melhoria de performance

```bash
git commit -m "perf(cache): adicionar cache em queries SQL"
git commit -m "perf(api): otimizar algoritmo de recomendação"
```

### 🧪 test
Adição ou atualização de testes

```bash
git commit -m "test: adicionar testes para validador"
git commit -m "test(auth): aumentar cobertura de OAuth"
```

### 🔧 chore
Mudanças em build, CI/CD, dependências, etc

```bash
git commit -m "chore: atualizar dependências"
git commit -m "chore(ci): melhorar configuração do GitHub Actions"
```

### 🚀 ci
Mudanças em configuração de CI/CD

```bash
git commit -m "ci: adicionar workflow de security checks"
git commit -m "ci(deploy): configurar deploy automático"
```

### 🔒 security
Correções de vulnerabilidades ou segurança

```bash
git commit -m "security: não expor variáveis sensíveis em logs"
git commit -m "security(auth): validar CSRF tokens"
```

## Escopo (Opcional)

Indique a área do código afetada:

```
feat(auth)      - Autenticação
feat(api)       - API REST
feat(models)    - Modelos de dados
feat(ui)        - Interface de usuário
feat(db)        - Banco de dados
feat(cache)     - Cache
feat(utils)     - Utilitários
feat(docs)      - Documentação
feat(ci)        - CI/CD
```

## Descrição

- Use imperativo: "adicionar" não "adiciona" ou "adicionado"
- Não comece com letra maiúscula
- Sem ponto (.) no final
- Máximo 50 caracteres
- Seja específico e descritivo

### ✅ Bom
```
feat(auth): adicionar suporte OAuth2 via Keycloak
fix(api): corrigir validação de CPF em endpoints
docs: atualizar guia de desenvolvimento
```

### ❌ Ruim
```
feat: mudanças
fix: corrigido um problema
atualizaria algo no sistema
```

## Corpo (Opcional)

Explicar o QUÊ e o POR QUÊ, não o COMO:

```
fix(auth): corrigir autenticação dupla

A validação de token estava sendo feita duas vezes,
causando timeout em requisições. Removida a segunda
validação redundante na middleware.

Fixes #123
```

## Rodapé (Opcional)

### Referências de Issues
```
Fixes #123
Closes #123, #456
Related to #789
```

### Breaking Changes
```
BREAKING CHANGE: removida rota /api/v1/users

A rota foi descontinuada. Use /api/v2/users no lugar.
```

## Exemplos Completos

### Simples
```
feat(betting): implementar análise preditiva de apostas
```

### Com escopo e corpo
```
feat(api): adicionar endpoint de exportação CSV

Implementar novo endpoint POST /api/exports que permite
aos usuários exportar suas apostas no formato CSV.

- Validar formato de data
- Comprimir arquivos grande
- Limpar exports após 24h

Closes #456
```

### Breaking change
```
refactor(models)!: reorganizar estrutura de dados

BREAKING CHANGE: campo 'user_id' renomeado para 'userId'

A nova estrutura segue padrão camelCase.
Migração: UPDATE users SET ... 

Closes #789
```

## Dicas

1. **Commit frequente**: Faça commits pequenos e atômicos
2. **Revise antes de fazer push**: `git log --oneline -5`
3. **Squash if needed**: Se fez muitos commits, faça squash
4. **Use templates**: Configure git com template de commit

```bash
# Configurar template global
git config --global commit.template ~/.gitmessage

# Ou por repositório
git config commit.template .gitmessage
```

## Formato de Versão Semântica

Seus commits determinam a versão:

```
v1.2.3
│ │ │
│ │ └─ PATCH: fix (bug fixes)
│ └─── MINOR: feat (new features)
└───── MAJOR: BREAKING CHANGE
```

Exemplo de histórico:
```
v1.0.0 - Release inicial
  feat: sistema de apostas
  feat: autenticação
  
v1.1.0 - Novas features
  feat: análise estatística
  feat: export CSV
  
v1.1.1 - Bug fix
  fix: erro com datas
  
v2.0.0 - Email refactoring
  refactor!: estrutura de banco dados
```

## Integração com GitHub Actions

Seus commits acionam workflows automaticamente:

- **feat**: Aumenta versão MINOR
- **fix**: Aumenta versão PATCH
- **BREAKING CHANGE**: Aumenta versão MAJOR

Configurado no `.github/workflows/release.yml` (use ferramentas como `semantic-release`)

---

**Convenção baseada em:** [Conventional Commits](https://www.conventionalcommits.org/)
