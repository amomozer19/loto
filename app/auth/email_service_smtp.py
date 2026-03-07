"""
EmailService com suporte a SMTP real.

Em desenvolvimento: salva em arquivo local
Em produção: pode usar SMTP real
"""

import os
import smtplib
from datetime import datetime
from typing import Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.paths import get_tokens_log


class EmailService:
    """Serviço de envio de emails com suporte a SMTP."""

    LOG_FILE = None  # Será definido dinamicamente

    # Configurações de SMTP (para produção)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', '')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@loto-app.com')

    @staticmethod
    def _get_log_file() -> str:
        """Obtém o caminho do arquivo de log, inicializando se necessário."""
        if EmailService.LOG_FILE is None:
            EmailService.LOG_FILE = get_tokens_log()
        return EmailService.LOG_FILE

    @staticmethod
    def enviar_token(email: str, token: str) -> Tuple[bool, str]:
        """
        Envia token de autenticação para email.

        Em desenvolvimento: salva em arquivo local
        Em produção: usa SMTP real se configurado

        Args:
            email: Email do usuário
            token: Token de autenticação

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            # Verificar se está em produção e SMTP está configurado
            if EmailService._usar_smtp_real():
                return EmailService._enviar_via_smtp(email, token)
            else:
                # Modo desenvolvimento: salvar em arquivo log
                EmailService._salvar_token_log(email, token)
                return True, f"Token salvo em auth_tokens.log"

        except Exception as e:
            return False, f"Erro ao enviar token: {str(e)}"

    @staticmethod
    def _usar_smtp_real() -> bool:
        """Verifica se deve usar SMTP real."""
        # Usar SMTP real apenas se:
        # 1. Está em modo produção
        # 2. Credenciais SMTP estão configuradas
        if os.environ.get('FLASK_ENV') != 'production':
            return False

        return bool(EmailService.SMTP_USER and EmailService.SMTP_PASSWORD)

    @staticmethod
    def _enviar_via_smtp(email: str, token: str) -> Tuple[bool, str]:
        """
        Envia email real via SMTP.

        Args:
            email: Email do usuário
            token: Token de autenticação

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            # Criar mensagem
            mensagem = MIMEMultipart('alternative')
            mensagem['Subject'] = '🔐 Seu Token de Acesso - Loto'
            mensagem['From'] = EmailService.FROM_EMAIL
            mensagem['To'] = email

            # Versão texto puro
            texto = f"""
Olá,

Seu token de acesso para a aplicação Loto é:

{token}

Este token expira em 24 horas.

Nunca compartilhe seu token com outra pessoa.

---
Aplicação Loto
            """

            # Versão HTML
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
                  <h1 style="color: #667eea;">🔐 Loto - Token de Acesso</h1>
                  
                  <p>Olá,</p>
                  
                  <p>Seu token de acesso para a aplicação Loto é:</p>
                  
                  <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <code style="font-size: 18px; font-weight: bold;">
                      {token}
                    </code>
                  </div>
                  
                  <p><strong>Válido por:</strong> 24 horas</p>
                  
                  <p style="color: #d32f2f;">
                    <strong>⚠️ IMPORTANTE:</strong> Nunca compartilhe seu token com outra pessoa.
                  </p>
                  
                  <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                  
                  <p style="color: #999; font-size: 12px;">
                    Se você não solicitou este token, ignore este email.
                  </p>
                </div>
              </body>
            </html>
            """

            # Anexar partes
            part1 = MIMEText(texto, 'plain')
            part2 = MIMEText(html, 'html')
            mensagem.attach(part1)
            mensagem.attach(part2)

            # Conectar e enviar
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT) as servidor:
                servidor.starttls()
                servidor.login(EmailService.SMTP_USER, EmailService.SMTP_PASSWORD)
                servidor.send_message(mensagem)

            return True, f"Token enviado para {email}"

        except smtplib.SMTPAuthenticationError:
            return False, "Erro: Credenciais SMTP inválidas"
        except smtplib.SMTPException as e:
            return False, f"Erro ao enviar email: {str(e)}"
        except Exception as e:
            return False, f"Erro desconhecido: {str(e)}"

    @staticmethod
    def _salvar_token_log(email: str, token: str) -> None:
        """
        Salva token em arquivo log para desenvolvimento.

        Args:
            email: Email do usuário
            token: Token enviado
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Email: {email} | Token: {token}\n"

        try:
            log_file = EmailService._get_log_file()
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Erro ao salvar token em log: {e}")

    @staticmethod
    def obter_ultimo_token(email: str) -> str:
        """
        Obtém o último token enviado para um email.

        Args:
            email: Email para buscar

        Returns:
            Token encontrado ou string vazia
        """
        log_file = EmailService._get_log_file()
        if not os.path.exists(log_file):
            return ''

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            # Procurar pela última ocorrência do email
            for linha in reversed(linhas):
                if f"Email: {email}" in linha:
                    # Extrair token da linha
                    # Formato: [timestamp] Email: email | Token: token
                    partes = linha.split('Token: ')
                    if len(partes) > 1:
                        return partes[1].strip()

            return ''
        except Exception as e:
            print(f"Erro ao obter token: {e}")
            return ''

    @staticmethod
    def limpar_logs() -> None:
        """Limpa o arquivo de log (para testes)."""
        try:
            log_file = EmailService._get_log_file()
            if os.path.exists(log_file):
                open(log_file, 'w').close()
        except Exception as e:
            print(f"Erro ao limpar logs: {e}")

    @staticmethod
    def obter_status() -> dict:
        """
        Retorna status do serviço de email.

        Returns:
            Dicionário com informações de status
        """
        return {
            'modo': 'produção (SMTP real)' if EmailService._usar_smtp_real() else 'desenvolvimento (log local)',
            'arquivo_log': EmailService._get_log_file(),
            'smtp_configurado': bool(EmailService.SMTP_USER and EmailService.SMTP_PASSWORD),
            'email_remetente': EmailService.FROM_EMAIL,
            'smtp_server': EmailService.SMTP_SERVER if EmailService._usar_smtp_real() else None,
        }
