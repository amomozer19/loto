"""
Serviço de email para envio de tokens de autenticação.

Versão local: Salva tokens em arquivo de log para desenvolvimento.
Pode ser expandido para usar SMTP real.
"""

import os
from datetime import datetime
from typing import Tuple
from app.utils.paths import get_tokens_log


class EmailService:
    """Serviço de envio de emails."""

    LOG_FILE = None  # Será inicializado dinamicamente na primeira utilização

    @staticmethod
    def _get_log_file() -> str:
        """
        Resolve dinamicamente o caminho do arquivo de log.
        
        Returns:
            Caminho para o arquivo de log de tokens
        """
        if EmailService.LOG_FILE is None:
            EmailService.LOG_FILE = get_tokens_log()
        return EmailService.LOG_FILE

    @staticmethod
    def enviar_token(email: str, token: str) -> Tuple[bool, str]:
        """
        Envia token de autenticação para email.

        Em desenvolvimento, salva em arquivo local.
        Em produção, pode usar SMTP real.

        Args:
            email: Email do usuário
            token: Token de autenticação

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        try:
            # Em desenvolvimento: salvar em arquivo log
            EmailService._salvar_token_log(email, token)
            
            mensagem = f"Token enviado para {email}"
            return True, mensagem
        except Exception as e:
            return False, f"Erro ao enviar token: {str(e)}"

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
        
        log_file = EmailService._get_log_file()
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    @staticmethod
    def obter_ultimo_token(email: str) -> str:
        """
        Obtém o último token enviado para um email (para desenvolvimento).

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
        except:
            return ''

    @staticmethod
    def limpar_logs() -> None:
        """Limpa o arquivo de log (para testes)."""
        log_file = EmailService._get_log_file()
        if os.path.exists(log_file):
            open(log_file, 'w').close()
