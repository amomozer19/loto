"""Pacote de autenticação."""

from app.auth.auth_handler import AuthHandler
from app.auth.email_service import EmailService
from app.auth.decorators import requer_autenticacao, requer_admin

__all__ = [
    'AuthHandler',
    'EmailService',
    'requer_autenticacao',
    'requer_admin',
]
