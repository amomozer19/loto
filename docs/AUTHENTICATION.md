# 🔐 Autenticação - Documentação

Sistema de autenticação robusto baseado em email e tokens seguros para a aplicação Loto.

## 📋 Visão Geral

### Fluxo de Autenticação

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuário acessa /auth/login                       │
│    └─> Adiciona email                               │
└──────────┬──────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 2. Token seguro gerado e enviado para email        │
│    └─> Salvo em auth_tokens.log (desenvolvimento)  │
└──────────┬──────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 3. Usuário vai para /auth/verificar                │
│    └─> Insere código do email                       │
└──────────┬──────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ 4. Token verificado, sessão criada                 │
│    └─> Redirecionado para /                         │
└─────────────────────────────────────────────────────┘
```

### Características

✅ **Tokens Seguros**
- Gerados com `secrets.token_bytes()` (criptográfico)
- 32 caracteres em hexadecimal
- Únicos por requisição

✅ **Persistência em CSV**
- `dados_usuarios.csv` armazena usuários
- Email, token, status verificado, data de criação
- Carregado/salvo a cada operação

✅ **Expiração de Token**
- Tokens expiram após 24 horas
- Verificação automática ao fazer login

✅ **Proteção de Sessão**
- HttpOnly cookies (sem acesso JavaScript)
- SameSite Lax para CSRF protection
- 30 dias de duração padrão

✅ **Desenvolvimento Fácil**
- Tokens salvos em `auth_tokens.log`
- Fácil visualizar tokens gerados
- `EmailService.obter_ultimo_token()` para testes

---

## 🏗️ Estrutura de Arquivos

```
app/
├── auth/
│   ├── __init__.py              # Exports públicos
│   ├── auth_handler.py          # Lógica principal
│   ├── email_service.py         # Envio de emails
│   └── decorators.py            # Proteção de rotas
├── models/
│   └── user.py                  # User + UserManager
└── routes/
    └── auth.py                  # Rotas de autenticação

dados_usuarios.csv              # Persistência de usuários
auth_tokens.log                 # Log de tokens (desenvolvimento)
```

---

## 🔐 Fluxo Detalhado

### 1. Solicitar Token

**Rota**: `POST /auth/login`

```python
from app.auth import AuthHandler

auth = AuthHandler()
sucesso, mensagem = auth.solicitar_token('user@example.com')
# sucesso: True
# mensagem: "Token enviado para user@example.com..."
```

**O que acontece**:
1. Email validado
2. Token seguro gerado
3. User criado/atualizado em CSV
4. Token enviado por "email" (log no dev)

**Token salvo em**: `auth_tokens.log`
```
[2026-03-04 10:00:00] Email: user@example.com | Token: a1b2c3d4e5f6g7h8...
```

### 2. Verificar Token

**Rota**: `POST /auth/verificar`

```python
auth = AuthHandler()
sucesso, mensagem = auth.verificar_token('user@example.com', 'abc123...')
# sucesso: True
# mensagem: "Email verificado com sucesso!"
```

**O que acontece**:
1. Usuário encontrado
2. Token comparado (seguro com `secrets.compare_digest`)
3. Expiração verificada
4. User marcado como verificado
5. Token limpo
6. Sessão criada

### 3. Acessar Aplicação

**Decorador**: `@requer_autenticacao`

```python
@app.route('/dados')
@requer_autenticacao
def meus_dados():
    # Usuário só chega aqui se autenticado
    email = session.get('email')
    return f"Bem-vindo {email}"
```

**Verificações**:
- ✅ Email em `session['email']`
- ✅ `session['verificado'] == True`
- ❌ Senão redireciona para login

### 4. Fazer Logout

**Rota**: `GET /auth/logout`

```python
auth = AuthHandler()
auth.fazer_logout('user@example.com')
# Sessão limpada
# Token removido do CSV
```

---

## 📊 Modelo de Dados

### User (CSV)

```csv
email;token;verified;created_at
user@example.com;abc123def456;True;2026-03-04T10:00:00
```

**Campos**:
- `email`: Identificador único
- `token`: Token temporário (null se não pendente)
- `verified`: Bool se email foi verificado
- `created_at`: Timestamp ISO para expiração

### UserManager

```python
from app.models.user import UserManager

manager = UserManager('dados_usuarios.csv')

# Operações CRUD
usuarios = manager.carregar_usuarios()              # List[User]
user = manager.obter_usuario('test@example.com')  # User | None
encontrado = manager.salvar_usuario(user)          # bool
deletado = manager.deletar_usuario('test@example.com') # bool

# Queries
verificados = manager.listar_usuarios_verificados()  # List[User]
pendentes = manager.listar_usuarios_pendentes()      # List[User]
total = manager.contar_usuarios()                    # int
verificados = manager.contar_usuarios_verificados()  # int
```

---

## 🔑 AuthHandler API

```python
from app.auth import AuthHandler

auth = AuthHandler(secret_key='sua-chave-secreta')

# Login
sucesso, msg = auth.solicitar_token(email)       # (bool, str)
sucesso, msg = auth.verificar_token(email, token) # (bool, str)
sucesso, msg = auth.autenticar(email, token)     # alias

# Gerenciamento
verificado = auth.usuario_verificado(email)      # bool
sucesso = auth.fazer_logout(email)                # bool
sucesso = auth.deletar_usuario(email)             # bool

# Stats
stats = auth.obter_estatisticas()                 # dict
# {
#   'total_usuarios': 5,
#   'usuarios_verificados': 3,
#   'usuarios_pendentes': 2
# }
```

---

## 📧 EmailService API

```python
from app.auth import EmailService

# Enviar token (dev: salva em arquivo)
sucesso, msg = EmailService.enviar_token('test@example.com', 'abc123')

# Obter token do log (apenas desenvolvimento)
token = EmailService.obter_ultimo_token('test@example.com')

# Limpar logs
EmailService.limpar_logs()
```

---

## 🔗 Rotas HTTP

### Rotas Públicas (sem autenticação)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/auth/login` | Formulário de login |
| POST | `/auth/login` | Solicita token |
| GET | `/auth/verificar` | Formulário de verificação |
| POST | `/auth/verificar` | Verifica token |
| GET | `/auth/logout` | Faz logout |

### APIs

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/auth/api/status` | Status de autenticação |
| POST | `/auth/api/solicitar-token` | Solicita token (JSON) |
| POST | `/auth/api/verificar-token` | Verifica token (JSON) |
| POST | `/auth/api/logout` | Logout (JSON) |
| GET | `/auth/api/estatisticas` | Stats (requer auth) |

### Exemplo: POST /auth/api/solicitar-token

```bash
curl -X POST http://localhost:5000/auth/api/solicitar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'

# Resposta:
{
  "sucesso": true,
  "mensagem": "Token enviado para user@example.com",
  "email": "user@example.com"
}
```

### Exemplo: POST /auth/api/verificar-token

```bash
curl -X POST http://localhost:5000/auth/api/verificar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "token": "abc123..."}'

# Resposta:
{
  "sucesso": true,
  "mensagem": "Email verificado com sucesso!",
  "email": "user@example.com"
}
```

---

## 🛡️ Segurança

### Proteções Implementadas

✅ **Tokens Criptográficos**
```python
token = secrets.token_bytes(16).hex()  # 32 chars, cryptographically random
```

✅ **Comparação Segura**
```python
secrets.compare_digest(token1, token2)  # Protege contra timing attacks
```

✅ **Sessão Segura**
```python
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Sem acesso JS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # CSRF protection
app.config['SESSION_COOKIE_SECURE'] = True     # HTTPS only (produção)
```

✅ **Expiração de Token**
```python
# Tokens expiram após 24 horas
EXPIRATION = timedelta(hours=24)
```

### Boas Práticas

⚠️ **IMPORTANTE**: Em produção:

1. **Mudar `SECRET_KEY`**
   ```python
   app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
   ```

2. **Usar SMTP Real**
   ```python
   # Implementar sendgrid, AWS SES, etc
   EmailService.enviar_com_smtp(email, token)
   ```

3. **Usar HTTPS**
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True
   ```

4. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter.limit("5 per hour")(auth.solicitar_token)
   ```

5. **Logging de Segurança**
   ```python
   import logging
   logger.warning(f"Tentativa de login falhada: {email}")
   ```

---

## 🧪 Testes

### Executar Testes de Autenticação

```bash
pytest tests/test_auth.py -v
```

### Cobertura

```bash
pytest tests/test_auth.py --cov=app.auth --cov-report=html
```

### Testes Inclusos

- ✅ User model (CRUD)
- ✅ UserManager (persistência)
- ✅ AuthHandler (geração/verificação tokens)
- ✅ Rotas de autenticação
- ✅ EmailService
- ✅ Decorators de proteção

---

## 🔧 Configuração

### Environment Variables

```bash
# .env
SECRET_KEY=sua-chave-super-secreta
FLASK_ENV=production
SESSION_LIFETIME=2592000  # 30 dias
TOKEN_VALIDITY=86400      # 24 horas
```

### settings.py

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 2592000))
```

---

## 📝 Exemplos

### Exemplo: Login via HTML Form

```html
<form action="{{ url_for('auth.login') }}" method="POST">
    <input type="email" name="email" required>
    <button type="submit">Login</button>
</form>
```

### Exemplo: Verificar Token via JS

```javascript
async function verificarToken(email, token) {
    const response = await fetch('/auth/api/verificar-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, token })
    });
    
    const data = await response.json();
    if (data.sucesso) {
        window.location.href = '/';
    }
}
```

### Exemplo: Proteger Rota

```python
from flask import Flask
from app.auth.decorators import requer_autenticacao

@app.route('/dashboard')
@requer_autenticacao
def dashboard():
    return "Dados confidenciais"
```

---

## 🚀 Próximos Passos

1. **Integração com SMTP Real**
   - Usar SendGrid, AWS SES, ou similar
   - Enviar emails de verdade

2. **Rate Limiting**
   - Limitar tentativas de login
   - Proteger contra brute force

3. **2FA (Two-Factor Authentication)**
   - SMS ou TOTP adicional
   - Maior segurança

4. **OAuth2**
   - Login com Google, GitHub, etc
   - Autenticação federada

5. **Admin Panel**
   - Interface para gerenciar usuários
   - Visualizar logs

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs em `auth_tokens.log`
2. Debugging em modo desenvolvimento
3. Consultar testes em `tests/test_auth.py`

---

**Versão**: 1.0  
**Status**: Production Ready  
**Atualizado**: 2026-03-04
