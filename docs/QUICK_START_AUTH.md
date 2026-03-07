# 🚀 Como Usar a Autenticação - Guia Rápido

Guia passo-a-passo para usar o sistema de autenticação da aplicação Loto.

## 🎯 Começando

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

Novas dependências adicionadas:
- `itsdangerous==2.1.2` - Geração de tokens
- `Flask-WTF==1.1.1` - CSRF protection
- `WTForms==3.0.1` - Validação de formulários

### 2. Iniciar a Aplicação

```bash
python run.py
```

Acesse: `http://localhost:5000/auth/login`

---

## 📱 Fluxo de Login (User Perspective)

### Passo 1: Inserir Email

```
Página: http://localhost:5000/auth/login
👉 Insira seu email
👉 Clique "Enviar Token de Acesso"
```

✅ **Resultado esperado**: Página de verificação, mensagem "Token enviado"

### Passo 2: Copiar Token do Email

```
Email recebido:
📧 Verificar Email - Código de Acesso

Abra em desenvolvimento: auth_tokens.log
[2026-03-04 10:00:00] Email: seu@email.com | Token: a1b2c3d4e5f6...
```

### Passo 3: Inserir Token

```
Página: http://localhost:5000/auth/verificar
👉 Cole o código da email
👉 Clique "Verificar e Acessar"
```

✅ **Resultado esperado**: Redirecionado para `/` (lista de sorteios)

### Passo 4: Usar Sistema

```
Agora você pode:
- Visualizar sorteios em /
- Adicionar novo em /novo
- Ver estatísticas em /estatisticas
```

### Passo 5: Logout

```
Clique em "Logout" ou acesse:
http://localhost:5000/auth/logout
```

---

## 🔍 Encontrar Seu Token (Desenvolvimento)

Como a aplicação não envia email real, os tokens são salvos em Um arquivo local.

### Opção 1: Abrir arquivo de log

```
Arquivo: auth_tokens.log
Localização: c:\Users\SAMSUNG\OneDrive\Meus Documentos\Python Projects\Loto\auth_tokens.log
```

**Formato**:
```
[2026-03-04 10:00:00] Email: seu@email.com | Token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### Opção 2: Usar Python

```python
from app.auth.email_service import EmailService

email = 'seu@email.com'
token = EmailService.obter_ultimo_token(email)
print(f"Token: {token}")
```

### Opção 3: Consultar banco de dados

```python
from app.models.user import UserManager

manager = UserManager()
user = manager.obter_usuario('seu@email.com')
if user:
    print(f"Token: {user.token}")
    print(f"Verificado: {user.verified}")
```

---

## 🔌 APIs de Autenticação

### 1. Solicitar Token (JSON)

```bash
curl -X POST http://localhost:5000/auth/api/solicitar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com"}'
```

**Resposta**:
```json
{
  "sucesso": true,
  "mensagem": "Token enviado para seu@email.com",
  "email": "seu@email.com"
}
```

### 2. Verificar Token (JSON)

```bash
curl -X POST http://localhost:5000/auth/api/verificar-token \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu@email.com",
    "token": "a1b2c3d4e5f6..."
  }'
```

**Resposta**:
```json
{
  "sucesso": true,
  "mensagem": "Email verificado com sucesso!",
  "email": "seu@email.com"
}
```

### 3. Verificar Status (JSON)

```bash
curl http://localhost:5000/auth/api/status
```

**Resposta (não autenticado)**:
```json
{
  "autenticado": false,
  "email": null,
  "verificado": false
}
```

**Resposta (autenticado)**:
```json
{
  "autenticado": true,
  "email": "seu@email.com",
  "verificado": true
}
```

### 4. Fazer Logout (JSON)

```bash
curl -X POST http://localhost:5000/auth/api/logout
```

**Resposta**:
```json
{
  "sucesso": true,
  "mensagem": "Logout realizado"
}
```

---

## 💾 Verificar Usuários Salvos

### Arquivo CSV

```csv
email;token;verified;created_at
user1@example.com;abc123def456;True;2026-03-04T10:00:00
user2@example.com;;False;2026-03-04T10:05:00
```

Localização: `dados_usuarios.csv`

### Python

```python
from app.models.user import UserManager

manager = UserManager('dados_usuarios.csv')

# Listar todos
usuarios = manager.carregar_usuarios()
for user in usuarios:
    print(f"{user.email}: {'✓' if user.verified else '✗'}")

# Contar
print(f"Total: {manager.contar_usuarios()}")
print(f"Verificados: {manager.contar_usuarios_verificados()}")
```

---

## 🧪 Testar com Postman

### 1. Criar Collection

```
Name: Loto Auth
```

### 2. Adicionar Requests

#### Request 1: Login

```
Method: POST
URL: http://localhost:5000/auth/api/solicitar-token
Headers: Content-Type: application/json

Body (raw):
{
  "email": "test@example.com"
}
```

#### Request 2: Verificar

```
Method: POST
URL: http://localhost:5000/auth/api/verificar-token
Headers: Content-Type: application/json

Body (raw):
{
  "email": "test@example.com",
  "token": "{{ token_aqui }}"
}
```

---

## 🐛 Troubleshooting

### Problema: "Email inválido"
- ✅ Certifique-se que tem @ e domínio
- ✅ Exemplo correto: `usuario@example.com`

### Problema: "Token não encontrado"
- ✅ Verificar arquivo `auth_tokens.log`
- ✅ Certifique-se que email está correto
- ✅ Token pode estar expirado (24 horas)

### Problema: "Token expirou"
- ✅ Gere um novo token
- ✅ Solicitação antiga de mais de 24 horas

### Problema: "Acesso negado para rota"
- ✅ Você precisa estar autenticado
- ✅ Faça login em `/auth/login`
- ✅ Erros redirecionam para login automaticamente

### Problema: "Email já existe"
- ✅ Você pode reutilizar o mesmo email
- ✅ Se não conseguir verificar, delete em código

---

## 🔐 Gerenciamento de Usuários (Admin)

### Listar Usuários

```python
from app.models.user import UserManager
from app.auth.auth_handler import AuthHandler

manager = UserManager()
usuarios = manager.carregar_usuarios()

for user in usuarios:
    status = "✓ Verificado" if user.verified else "✗ Pendente"
    print(f"{user.email}: {status}")
```

### Deletar Usuário

```python
manager = UserManager()
manager.deletar_usuario('usuario@example.com')
```

### Ver Estatísticas

```python
auth = AuthHandler()
stats = auth.obter_estatisticas()

print(f"Total de usuários: {stats['total_usuarios']}")
print(f"Verificados: {stats['usuarios_verificados']}")
print(f"Pendentes: {stats['usuarios_pendentes']}")
```

---

## 🧬 Integração com Código

### Proteger Rota

```python
from flask import Blueprint
from app.auth.decorators import requer_autenticacao

bp = Blueprint('exemplo', __name__)

@bp.route('/dados-privados')
@requer_autenticacao
def dados_privados():
    return "Dados confidenciais"
```

### Verificar Sessão

```python
from flask import session

def minhaFunction():
    if 'email' in session:
        email = session['email']
        print(f"Usuário autenticado: {email}")
    else:
        print("Não autenticado")
```

### Usar AuthHandler

```python
from app.auth import AuthHandler

auth = AuthHandler()

# Solicitar token
sucesso, msg = auth.solicitar_token('usuario@example.com')
if sucesso:
    print(msg)

# Verificar token
token = "abc123..."
sucesso, msg = auth.verificar_token('usuario@example.com', token)
if sucesso:
    print("Usuário autenticado!")
```

---

## 📊 Workflow Completo (Teste Manual)

### Step-by-step

```bash
# 1. Iniciar servidor
python run.py

# 2. Em outro terminal, solicitar token
curl -X POST http://localhost:5000/auth/api/solicitar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com"}'

# 3. Verificar auth_tokens.log
cat auth_tokens.log

# 4. Usar token para autenticar
# Copie token de auth_tokens.log
curl -X POST http://localhost:5000/auth/api/verificar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "token": "TOKEN_AQUI"}'

# 5. Verificar status
curl http://localhost:5000/auth/api/status
# Deve retornar autenticado: true
```

---

## 🚀 Próximos Passos

1. **Migrar para SMTP Real**
   - Implementar envio de emails
   - Usar SendGrid, AWS SES, etc

2. **Adicionar 2FA**
   - SMS ou TOTP
   - Maior segurança

3. **Integrar com OAuth**
   - Login com Google
   - Login com GitHub

4. **Rate Limiting**
   - Proteger contra brute force
   - Limitar requisições

5. **Admin Panel**
   - Interface para gerenciar usuários
   - Ver logs de login

---

**Dica**: Para desenvolvimento, sempre cheque `auth_tokens.log` para encontrar tokens gerados! 💡
