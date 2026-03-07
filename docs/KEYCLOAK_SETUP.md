# 🔐 Implementação do Keycloak - Guia Completo

## 📋 Resumo da Implementação

O sistema de autenticação foi migrado de um sistema baseado em tokens por email para **Keycloak**, um servidor de gerenciamento de identidade robusto baseado em OAuth2/OpenID Connect.

---

## 🎯 Mudanças Implementadas

### 1. **Arquivos Criados**

#### `app/auth/keycloak_config.py`
- Configuração centralizada do Keycloak
- Variáveis de ambiente
- Geração de URLs OAuth2
- Validação de configurações

#### `app/auth/keycloak_handler.py`
- Handler para comunicação com Keycloak
- Gerenciamento de tokens OAuth2
- Sincronização de usuários
- Validação de roles e permissões

#### `app/routes/auth_keycloak.py`
- Rotas atualizadas com suporte a Keycloak
- Login via OAuth2
- Callback do Keycloak
- Logout integrado
- Suporte a modo local como fallback

#### `docker-compose.yml`
- Ambiente Docker para Keycloak
- PostgreSQL para persistência
- Redis para sessões (opcional)
- Networking adequado

### 2. **Arquivos Modificados**

#### `app/models/user.py`
- Adicionados campos Keycloak:
  - `keycloak_id`: ID do usuário no Keycloak
  - `username`: Nome de usuário
  - `first_name`, `last_name`, `full_name`
  - `roles`: Lista de roles do usuário
  - `auth_provider`: 'local' ou 'keycloak'
- Migração automática de formato antigo
- Backward compatibility mantida

#### `config/requirements.txt`
- python-keycloak==3.8.0
- authlib==1.2.1
- PyJWT==2.8.1
- Outras dependências de segurança

---

## 🚀 Instalação e Setup

### Pré-requisitos

```bash
# 1. Docker e Docker Compose instalados
docker --version
docker-compose --version

# 2. Python 3.8+
python --version

# 3. Atualizar requirements
pip install -r config/requirements.txt
```

### Passo 1: Iniciar Keycloak com Docker

```bash
# No diretório raiz do projeto
docker-compose up -d

# Aguardar alguns segundos para Keycloak inicializar
# Verificar logs:
docker-compose logs -f keycloak
```

Keycloak estará disponível em: **http://localhost:8080**

### Passo 2: Configurar Keycloak

#### Acessar Console Admin

1. Abrir: `http://localhost:8080/admin`
2. Login:
   - Username: `admin`
   - Password: `admin_password_change_me`

#### Criar Realm

1. Ir para "Realms" (canto superior esquerdo)
2. Clique em "Create"
3. Name: `loto-realm`
4. Create

#### Criar Cliente (aplicação)

1. Ir para "Clients" no menu esquerdo
2. Clique em "Create client"
3. Configurar:
   - **Client type**: OpenID Connect
   - **Client ID**: `loto-app`
   - **Name**: Loto App
4. Next
5. Configurar "Access settings":
   - **Root URL**: http://localhost:5000
   - **Home URL**: http://localhost:5000
   - **Valid redirect URIs**: http://localhost:5000/auth/callback
   - **Valid post logout redirect URIs**: http://localhost:5000
   - **Web origins**: http://localhost:5000
6. Save

#### Obter Cliente Secret

1. Ir para a aba "Credentials"
2. Copiar o "Client secret"
3. Salvar em variável de ambiente (veja abaixo)

#### Configurar Roles (Opcional)

1. Ir para "Realm roles"
2. Criar roles:
   - `user` (padrão)
   - `admin`
   - `analyst`
3. Atribuir roles aos usuários

---

## 🔧 Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```bash
# Keycloak Configuration
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=loto-realm
KEYCLOAK_CLIENT_ID=loto-app
KEYCLOAK_CLIENT_SECRET=<copiar-de-keycloak-console>
KEYCLOAK_REDIRECT_URI=http://localhost:5000/auth/callback
KEYCLOAK_LOGOUT_REDIRECT_URI=http://localhost:5000

# Flask
FLASK_SECRET_KEY=seu-secret-key-aleatorio-aqui

# Modo de autenticação
AUTH_MODE=keycloak  # ou 'local' para usar autenticação local

# Token Expiry
TOKEN_EXPIRY=3600  # 1 hora em segundos
REFRESH_TOKEN_EXPIRY=86400  # 24 horas
```

### Carregando .env na aplicação

Adicionar antes de `from app import create_app`:

```python
from dotenv import load_dotenv
load_dotenv()
```

Instalar: `pip install python-dotenv`

---

## 🔄 Fluxo de Autenticação

### Antes (Sistema Local)
```
User → Login Form → Email → Token via Email → Token Verification → Session
```

### Depois (Keycloak OAuth2/OIDC)
```
User → Login Form → Keycloak Authorization → Keycloak Login 
→ Authorization Code → Token Exchange → User Info → Session
```

### Modo Híbrido (Local Fallback)
```
User → AUTH_MODE=keycloak? 
├─ YES → Keycloak Flow
└─ NO → Local Token Flow
```

---

## 📊 Estrutura de Usuário Sincronizada

```python
{
    'email': 'usuario@exemplo.com',
    'username': 'usuario_keycloak',
    'first_name': 'João',
    'last_name': 'Silva',
    'full_name': 'João Silva',
    'roles': ['user', 'analyst'],
    'verified': True,
    'auth_provider': 'keycloak',
    'keycloak_id': 'uuid-do-keycloak'
}
```

---

## 🔐 Segurança

### Benefícios do Keycloak

✅ **OAuth2/OIDC**: Padrão de segurança industrial  
✅ **JWT**: Tokens seguros e validáveis  
✅ **Roles e Permissões**: Controle de aceso granular  
✅ **Integração LDAP/AD**: Autenticação corporativa  
✅ **MFA/2FA**: Autenticação multi-fator  
✅ **Auditoria**: Logs de segurança completos  
✅ **Isolamento**: Dados separados por realm  

### Boas Práticas

1. **Em Produção**:
   ```bash
   # Usar HTTPS
   KC_HOSTNAME=seu-dominio.com
   KC_PROXY=xforwarded
   
   # Usar banco de dados externo robusto
   KC_DB=postgres (ou MySQL)
   
   # Configurar backup
   backup do postgresql/mysql
   ```

2. **Senhas**:
   - Alterar `KEYCLOAK_ADMIN_PASSWORD`
   - Alterar `POSTGRES_PASSWORD`
   - Alterar `FLASK_SECRET_KEY`

3. **HTTPS**:
   - Obter certificado SSL
   - Configurar nas variáveis de ambiente

---

## 🧪 Testes

### Teste Rápido Localmente

```bash
# 1. Iniciar Docker
docker-compose up -d

# 2. Aguardar ~30 segundos

# 3. Instalar dependências
pip install -r config/requirements.txt

# 4. Iniciar aplicação
python run.py

# 5. Acessar navegador
# http://localhost:5000

# 6. Clique em "Login com Keycloak"
```

### Teste via cURL

```bash
# 1. Obter authorization code
curl -L "http://localhost:8080/realms/loto-realm/protocol/openid-connect/auth?\
client_id=loto-app&\
redirect_uri=http://localhost:5000/auth/callback&\
response_type=code&\
scope=openid profile email"

# 2. Trocar código por token
curl -X POST \
  http://localhost:8080/realms/loto-realm/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=loto-app" \
  -d "client_secret=<seu-secret>" \
  -d "code=<authorization-code>" \
  -d "redirect_uri=http://localhost:5000/auth/callback"

# 3. Obter informações do usuário
curl -H "Authorization: Bearer <access-token>" \
  http://localhost:8080/realms/loto-realm/protocol/openid-connect/userinfo
```

---

## 🔄 Migração de Usuários Existentes

A migração ocorre automaticamente:

1. **Primeira Execução**: `user.py` detecta formato antigo
2. **Migração Automática**: Converte para novo formato
3. **Backward Compatibility**: Usuários locais continuam funcionando

Dados antigos são preservados, novos campos são preenchidos automaticamente.

---

## 🛠️ Troubleshooting

### Keycloak não inicia

```bash
# Verificar logs
docker-compose logs keycloak

# Deletar e reiniciar
docker-compose down -v
docker-compose up -d
```

### Connection refused em http://localhost:8080

```bash
# Aguardar mais tempo (até 60 segundos)
# O Keycloak leva tempo para inicializar

# Ou verificar status
docker ps | grep keycloak
```

### Client secret inválido

```bash
# Voltar ao Keycloak Console
# Admin → Realm → Clients → loto-app → Credentials
# Regenerar novo secret
```

### Token inválido

```bash
# Verificar:
# 1. Realm está correto
# 2. Client ID está correto
# 3. Redirect URI está correto
# 4. Variáveis de ambiente estão setadas
```

### Usuário não sincroniza

```bash
# Verificar arquivo de log
tail -f config/auth_tokens.log

# Ou verificar userData
cat data/dados_usuarios.csv
```

---

## 📈 Próximos Passos

- [ ] Implementar MFA/2FA
- [ ] Integração com LDAP/Active Directory
- [ ] Configurar backup automático
- [ ] Implementar SSO para múltiplos domínios
- [ ] Dashboard de segurança
- [ ] Rate limiting para login
- [ ] Session management avançado

---

## 📚 Referências

- [Documentação oficial Keycloak](https://www.keycloak.org/documentation)
- [OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect](https://openid.net/connect/)
- [Python Keycloak Client](https://github.com/marcospereirampj/python-keycloak)

---

## ⚡ Resumo de Comandos

```bash
# Iniciar Keycloak
docker-compose up -d

# Parar Keycloak
docker-compose down

# Ver logs
docker-compose logs -f keycloak

# Resetar tudo (limpar volumes)
docker-compose down -v

# Acessar Keycloak Admin
# http://localhost:8080/admin
# admin / admin_password_change_me

# Acessar Aplicação
# http://localhost:5000
```

---

**Status**: ✅ Implementação Completa  
**Versão**: 1.0  
**Data**: Março 2026  
**Suporte**: Tanto Keycloak quanto modo local (fallback)
