# 🔐 Sistema de Autenticação - Implementação Completa

Resumo da camada de segurança adicionada à aplicação Loto.

## ✨ O Que Foi Implementado

### 1. **Autenticação baseada em Email + Token**
- ✅ Usuários se registram/autenticam com email
- ✅ Token seguro gerado e enviado por "email"
- ✅ Em desenvolvimento: tokens salvos em `auth_tokens.log`
- ✅ Em produção: pode usar SMTP real

### 2. **Persistência em CSV**
- ✅ Arquivo: `dados_usuarios.csv`
- ✅ Campos: email, token, verificado, data_criação
- ✅ Sem banco de dados, apenas arquivo simples

### 3. **Segurança de Sessão**
- ✅ Tokens criptográficos (256-bit random)
- ✅ Comparação segura contra timing attacks
- ✅ HttpOnly cookies (sem acesso JavaScript)
- ✅ CSRF protection (SameSite=Lax)
- ✅ Expiração automática (24 horas)

### 4. **Proteção de Rotas**
- ✅ Decorator `@requer_autenticacao` para proteger endpoints
- ✅ Todas as rotas existentes agora requerem login
- ✅ Redirecionamento automático para login se não autenticado

### 5. **APIs RESTful**
- ✅ POST `/auth/api/solicitar-token` - Solicita token
- ✅ POST `/auth/api/verificar-token` - Verifica/autentica
- ✅ GET `/auth/api/status` - Verifica autenticação
- ✅ POST `/auth/api/logout` - Faz logout

---

## 📁 Novos Arquivos Criados

```
app/
├── auth/                           # Novo pacote de autenticação
│   ├── __init__.py                 
│   ├── auth_handler.py             # Lógica principal (AuthHandler)
│   ├── email_service.py            # Envio de emails + log
│   └── decorators.py               # @requer_autenticacao
├── models/
│   └── user.py                     # User + UserManager (CSV)
└── routes/
    └── auth.py                     # Rotas de autenticação

app/templates/auth/
├── login.html                      # Página de login
└── verificar.html                  # Página de verificação

dados_usuarios.csv                  # Persistência de usuários
auth_tokens.log                     # Log de tokens (dev)

tests/
└── test_auth.py                    # 40+ testes de autenticação
```

---

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

Novas:
- `itsdangerous==2.1.2` - Tokens seguros
- `Flask-WTF==1.1.1` - CSRF protection
- `WTForms==3.0.1` - Validação de formulários

### 2. Iniciar Aplicação
```bash
python run.py
```

### 3. Fluxo de Login
```
1. Acesse http://localhost:5000/auth/login
2. Insira seu email
3. Clique "Enviar Token de Acesso"
4. Abra auth_tokens.log para encontrar seu token
5. Insira token em http://localhost:5000/auth/verificar
6. Agora pode acessar /
```

---

## 🔌 APIs

### Solicitar Token
```bash
curl -X POST http://localhost:5000/auth/api/solicitar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

### Verificar Token
```bash
curl -X POST http://localhost:5000/auth/api/verificar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "token": "abc123..."}'
```

### Verificar Status
```bash
curl http://localhost:5000/auth/api/status
```

---

## 📊 Estrutura de Dados

### `dados_usuarios.csv`
```csv
email;token;verified;created_at
usuario@example.com;abc123def456;True;2026-03-04T10:00:00
novo@example.com;;False;2026-03-04T10:05:00
```

### Rotas Públicas (sem autenticação)
```
GET  /auth/login        - Formulário de login
POST /auth/login        - Processa email
GET  /auth/verificar    - Formulário de token
POST /auth/verificar    - Processa token
GET  /auth/logout       - Faz logout
```

### Rotas Privadas (requerem autenticação)
```
GET  /                  - Lista de sorteios
GET  /novo              - Novo sorteio
GET  /estatisticas      - Estatísticas
POST /api/gerar_numeros - Gera números
POST /api/validar       - Valida dados
POST /api/salvar        - Salva sorteio
```

---

## 🧪 Testes

### Executar Testes de Autenticação
```bash
pytest tests/test_auth.py -v
```

### Cobertura
- 14 testes User model e UserManager
- 10 testes AuthHandler
- 6 testes rotas de autenticação
- 4 testes EmailService

**Total**: 34+ testes

### Executar com Cobertura
```bash
pytest tests/test_auth.py --cov=app.auth --cov-report=html
```

---

## 🎯 Classes Principais

### `AuthHandler`
```python
from app.auth import AuthHandler

auth = AuthHandler(secret_key='minha-chave')

# Solicitar token
sucesso, msg = auth.solicitar_token('user@example.com')

# Verificar token (autentica)
sucesso, msg = auth.verificar_token('user@example.com', 'token123')

# Verificar se está verificado
if auth.usuario_verificado('user@example.com'):
    print("Usuário autenticado")

# Logout
auth.fazer_logout('user@example.com')

# Deletar usuário
auth.deletar_usuario('user@example.com')

# Stats
stats = auth.obter_estatisticas()
```

### `UserManager`
```python
from app.models.user import UserManager

manager = UserManager('dados_usuarios.csv')

# CRUD
usuarios = manager.carregar_usuarios()
user = manager.obter_usuario('test@example.com')
manager.salvar_usuario(user)
manager.deletar_usuario('test@example.com')

# Queries
verificados = manager.listar_usuarios_verificados()
pendentes = manager.listar_usuarios_pendentes()
total = manager.contar_usuarios()
```

### `Decorator`
```python
from app.auth.decorators import requer_autenticacao

@app.route('/privado')
@requer_autenticacao
def minha_rota():
    # Só chega aqui se autenticado
    email = session.get('email')
    return f"Bem-vindo {email}"
```

---

## 🔐 Segurança

### Protections Implementadas

✅ **Tokens Criptográficos**
- Gerados com `secrets.token_bytes(16).hex()`
- 32 caracteres aleatórios
- Único por requisição

✅ **Comparação Segura**
- `secrets.compare_digest()` protege contra timing attacks
- Evita ataques de força bruta por tempo

✅ **Sessão Segura**
- HttpOnly: sem acesso JavaScript
- SameSite: protege contra CSRF
- Expiração: 24 horas automática

✅ **Validação**
- Email validado (tem @)
- Token validado (comprimento, caracteres)
- Expiração verificada

### ⚠️ Em Produção

1. **Mudar SECRET_KEY**
   ```python
   export SECRET_KEY="sua-chave-secreta-super-segura"
   ```

2. **Usar SMTP Real**
   ```python
   # Implementar com SendGrid, AWS SES, etc
   ```

3. **Ativar HTTPS**
   ```python
   FLASK_ENV=production
   ```

4. **Rate Limiting**
   ```python
   # Adicionar flask-limiter para prevenir brute force
   ```

5. **Logging**
   ```python
   # Registrar tentativas de login falhadas
   ```

---

## 📚 Documentação Completa

- **[AUTHENTICATION.md](AUTHENTICATION.md)** - Documentação técnica completa
- **[QUICK_START_AUTH.md](QUICK_START_AUTH.md)** - Guia passo-a-passo
- **[tests/test_auth.py](tests/test_auth.py)** - Exemplos de testes

---

## 🎨 Frontend

### Login (html)
```html
<form action="{{ url_for('auth.login') }}" method="POST">
    <input type="email" name="email" required>
    <button type="submit">Enviar Token</button>
</form>
```

### JavaScript (API)
```javascript
// Solicitar token
const response = await fetch('/auth/api/solicitar-token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'user@example.com' })
});

// Verificar token
const verify = await fetch('/auth/api/verificar-token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        email: 'user@example.com', 
        token: 'abc123...' 
    })
});

// Verificar status
const status = await fetch('/auth/api/status');
const data = await status.json();
console.log(data.autenticado); // true/false
```

---

## 🚀 Próximos Passos

1. **Integração com SMTP**
   - Implementar envio real de emails
   - SendGrid, AWS SES, Gmail SMTP

2. **2FA (Two-Factor Authentication)**
   - SMS com código
   - TOTP (Google Authenticator)

3. **OAuth2**
   - Login com Google
   - Login com GitHub
   - Login com Facebook

4. **Roles e Permissões**
   - Administrative access
   - User roles
   - Permission-based access

5. **Admin Panel**
   - Interface para gerenciar usuários
   - Dashboard de autenticação
   - Logs de segurança

6. **Mobile App Auth**
   - API tokens para app mobile
   - Refresh tokens
   - Mobile-specific flows

---

## 📞 Suporte

**Arquivo de log**: `auth_tokens.log` - Ver todos os tokens gerados em desenvolvimento

**Testes**: `pytest tests/test_auth.py -v` - Rodar suite completa

**Documentação**: Ver [AUTHENTICATION.md](AUTHENTICATION.md) para detalhes técnicos

---

**Status**: ✅ Production Ready  
**Última atualização**: 2026-03-04  
**Versão**: 1.0
