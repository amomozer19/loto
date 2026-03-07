# 📧 Guia: Envio Real de Emails com SMTP

## 🎯 Situação Atual

✅ **Em Desenvolvimento (AGORA)**:
- Tokens são gerados corretamente
- Salvos em `auth_tokens.log`
- Não há envio de email real
- Perfeito para testes locais

📧 **Para Produção (Próximo)**:
- Implementar SMTP real
- Enviar emails verdadeiros
- Usar SendGrid, AWS SES, Gmail, etc

---

## 🔧 Como Configurar SMTP Real

### Opção 1: Gmail (Mais Fácil)

**Passo 1: Criar App Password**

1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione: Mail + Windows Computer
3. Copie a senha gerada (16 caracteres)

**Passo 2: Configurar `.env`**

```env
FLASK_ENV=production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_EMAIL=seu-email@gmail.com
```

### Opção 2: SendGrid (Recomendado para Produção)

**Passo 1: Criar Conta**

1. Registre em: https://sendgrid.com
2. Crie API key em Settings → API Keys
3. Copie a chave

**Passo 2: Configurar `.env`**

```env
FLASK_ENV=production
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.sua-api-key-aqui
FROM_EMAIL=seu-email@suaempresa.com
```

### Opção 3: AWS SES

**Passo 1: Configurar AWS**

1. Acesse AWS Console → SES
2. Verifique seu email
3. Crie SMTP credentials
4. Copie Access Key e Secret Key

**Passo 2: Configurar `.env`**

```env
FLASK_ENV=production
SMTP_SERVER=email-smtp.region.amazonaws.com
SMTP_PORT=587
SMTP_USER=seu-access-key
SMTP_PASSWORD=sua-secret-key
FROM_EMAIL=seu-email@verified.com
```

### Opção 4: Seu Próprio Email

**Passo 1: Obter Credenciais SMTP**

Para ProtonMail, Outlook, Yahoo, etc., procure por "SMTP settings" na documentação.

**Passo 2: Configurar `.env`**

```env
FLASK_ENV=production
SMTP_SERVER=smtp.seu-provedor.com
SMTP_PORT=587
SMTP_USER=seu-email@provedor.com
SMTP_PASSWORD=sua-senha
FROM_EMAIL=seu-email@provedor.com
```

---

## 🔄 Alternando Entre Desenvolvimento e Produção

### Em Desenvolvimento (AGORA)

```env
FLASK_ENV=development
# Não é necessário configurar SMTP
# Tokens são salvos em auth_tokens.log
```

**Teste**:
```bash
python run.py
# Acesse http://localhost:5000/auth/login
# Token aparecerá em auth_tokens.log
```

### Em Produção (Com Email Real)

```env
FLASK_ENV=production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_EMAIL=seu-email@gmail.com
```

**O que muda**:
```python
# Antes: Token salvo em arquivo
[2026-03-04 18:35:22] Email: user@example.com | Token: c648...

# Depois: Email real enviado para user@example.com
```

---

## 📝 Implementação

### Passo 1: Backup do Arquivo Atual

```bash
cp app/auth/email_service.py app/auth/email_service.bak
```

### Passo 2: Usar Versão com SMTP

```bash
cp app/auth/email_service_smtp.py app/auth/email_service.py
```

### Passo 3: Instalar Dependências (Se Necessário)

```bash
pip install python-dotenv  # Para ler .env
```

### Passo 4: Configurar `.env`

Criar arquivo `.env` na raiz do projeto:

```env
# Flask
FLASK_ENV=development

# Secret Key (mudar em produção!)
SECRET_KEY=sua-chave-super-secreta

# SMTP (deixar vazio em desenvolvimento)
SMTP_SERVER=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
FROM_EMAIL=noreply@seudominio.com

# Session
SESSION_LIFETIME=2592000
```

### Passo 5: Carregar `.env` em `run.py`

```python
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Depois criar app
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
```

---

## 🧪 Testar Envio de Email

### Teste 1: Verificar Status

```python
from app.auth.email_service import EmailService

status = EmailService.obter_status()
print(status)

# Resultado:
# {
#   'modo': 'desenvolvimento (log local)',
#   'arquivo_log': 'auth_tokens.log',
#   'smtp_configurado': False,
#   'email_remetente': 'noreply@loto-app.com'
# }
```

### Teste 2: Solicitação de Token

```bash
curl -X POST http://localhost:5000/auth/api/solicitar-token \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com"}'

# Resultado (desenvolvimento):
# {
#   "sucesso": true,
#   "mensagem": "Token salvo em auth_tokens.log"
# }

# Resultado (produção com SMTP):
# {
#   "sucesso": true,
#   "mensagem": "Token enviado para seu@email.com"
# }
```

### Teste 3: Verificar Email Recebido

Após configurar SMTP:
```bash
1. Insira email em /auth/login
2. Clique "Enviar Token"
3. Verifique sua caixa de entrada
4. Copie o código do email
5. Insira em /auth/verificar
```

---

## 🐛 Troubleshooting

### "SMTPAuthenticationError"
→ Verifique user/password
→ Se for Gmail, verifique App Password
→ Se for SendGrid, certifique-se que é "apikey"

### "SMTPServerDisconnected"
→ Verifique SMTP_SERVER e SMTP_PORT
→ Certifique-se que a porta está correta (geralmente 587)

### "Connection refused"
→ Verifique firewall/proxy
→ Tente com VPN desativada
→ Verifique se precisa de TLS

### Email não chega
→ Verifique pasta de spam
→ Configure SPF/DKIM no seu domínio
→ Verifique se remetente está verificado

### "SMTP port 465 vs 587"
- **587**: TLS (recomendado) - Use `starttls()`
- **465**: SSL - Use `smtplib.SMTP_SSL()`

---

## 📧 Template de Email

O email enviado com SMTP real será assim:

```html
┌─────────────────────────────┐
│                             │
│   🔐 Loto - Token Acesso   │
│                             │
│ Olá,                        │
│                             │
│ Seu token é:                │
│ ┌───────────────────────┐   │
│ │ c6481e4e17157b85... │   │
│ └───────────────────────┘   │
│                             │
│ Válido por: 24 horas        │
│                             │
│ ⚠️ Nunca compartilhe!       │
│                             │
└─────────────────────────────┘
```

---

## 🔐 Boas Práticas

✅ **Nunca commit `.env` no git**
```bash
echo ".env" >> .gitignore
```

✅ **Usar variáveis de ambiente em produção**
```bash
export SMTP_PASSWORD="sua-senha"
# Não colocar em arquivo!
```

✅ **Testar antes de produção**
```bash
FLASK_ENV=production python -c "from app.auth.email_service import EmailService; print(EmailService.obter_status())"
```

✅ **Monitora tentativas falhadas**
```python
# Adicionar logging
import logging
logger = logging.getLogger(__name__)
logger.error(f"Email falhou para {email}: {erro}")
```

---

## 🚀 Próximos Passos

### Agora (Desenvolvimento)
1. ✅ Você já tem tudo funcionando
2. Use `auth_tokens.log` para testar
3. Rotas protegidas estão ativas

### Depois (Produção)
1. Escolha provedor de email
2. Configure variáveis de ambiente
3. Substitua `email_service.py`
4. Teste solicitação e recebimento
5. Deploy!

### Futuro (Melhorias)
1. Rastreamento de emails (abertos, clicados)
2. Templates customizados
3. Reenvio automático
4. Suporte a múltiplos provedores
5. Webhooks para confirmação

---

## 📞 Referências

- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [SendGrid Documentation](https://docs.sendgrid.com/for-developers/sending-email/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [Python smtplib](https://docs.python.org/3/library/smtplib.html)
- [Email MIME types](https://docs.python.org/3/library/email.mime.html)

---

**Status Atual**: ✅ Funcionando em desenvolvimento com `auth_tokens.log`  
**Próximo Passo**: Configurar SMTP real para produção  
**Tempo Estimado**: 15 minutos
