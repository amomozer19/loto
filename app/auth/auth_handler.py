"""
Manipulador de autenticação - Lógica central de autenticação.

Responsável por:
- Gerar tokens seguros
- Verificar tokens
- Gerenciar login/logout
"""

import secrets
from typing import Tuple, Optional
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from app.models.user import User, UserManager
from app.auth.email_service import EmailService


class AuthHandler:
    """Manipulador de autenticação com tokens seguros."""

    def __init__(self, secret_key: str = 'dev-secret-key-change-in-production'):
        """
        Inicializa o manipulador de autenticação.

        Args:
            secret_key: Chave secreta para gerar tokens (MUDAR EM PRODUÇÃO!)
        """
        self.secret_key = secret_key
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.user_manager = UserManager()

    def solicitar_token(self, email: str) -> Tuple[bool, str]:
        """
        Solicita um token de autenticação para um email.

        Args:
            email: Email do usuário

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if not email or '@' not in email:
            return False, "Email inválido"

        email = email.lower().strip()

        try:
            # Gerar token seguro
            token = self._gerar_token_seguro(email)

            # Criar ou atualizar usuário
            user = User(
                email=email,
                token=token,
                verified=False
            )
            
            # Salvar usuário
            if not self.user_manager.salvar_usuario(user):
                return False, "Erro ao salvar usuário"

            # Enviar token por email
            sucesso, mensagem = EmailService.enviar_token(email, token)
            
            if sucesso:
                return True, f"Token enviado para {email}. Verifique seu email."
            else:
                return False, mensagem

        except Exception as e:
            return False, f"Erro ao solicitar token: {str(e)}"

    def verificar_token(self, email: str,token_fornecido: str) -> Tuple[bool, str]:
        """
        Verifica se o token fornecido é válido.

        Args:
            email: Email do usuário
            token_fornecido: Token para verificar

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        email = email.lower().strip()

        if not email or not token_fornecido:
            return False, "Email e token são obrigatórios"

        try:
            # Buscar usuário
            user = self.user_manager.obter_usuario(email)
            
            if not user:
                return False, "Usuário não encontrado"

            # Verificar token
            if not user.token:
                return False, "Nenhum token solicitado para este email"

            # Comparar tokens (simples e seguro)
            if not secrets.compare_digest(user.token, token_fornecido.strip()):
                return False, "Token inválido"

            # Verificar expiração
            if user.created_at:
                from datetime import datetime, timedelta
                try:
                    created = datetime.fromisoformat(user.created_at)
                    agora = datetime.now()
                    diferenca = agora - created
                    if diferenca > timedelta(hours=24):
                        return False, "Token expirou. Solicite um novo."
                except:
                    pass

            # Token válido! Marcar como verificado
            user.verified = True
            user.token = None  # Limpar token após verificação
            self.user_manager.salvar_usuario(user)

            return True, "Email verificado com sucesso!"

        except Exception as e:
            return False, f"Erro ao verificar token: {str(e)}"

    def autenticar(self, email: str, token: str) -> Tuple[bool, str]:
        """
        Autentica um usuário com email e token.

        Alias para verificar_token com nomeação mais clara.

        Args:
            email: Email do usuário
            token: Token fornecido

        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        return self.verificar_token(email, token)

    def usuario_verificado(self, email: str) -> bool:
        """
        Verifica se um email está verificado.

        Args:
            email: Email para verificar

        Returns:
            True se verificado
        """
        user = self.user_manager.obter_usuario(email.lower().strip())
        return user is not None and user.verified

    def fazer_logout(self, email: str) -> bool:
        """
        Faz logout de um usuário (remove token).

        Args:
            email: Email do usuário

        Returns:
            True se sucesso
        """
        email = email.lower().strip()
        user = self.user_manager.obter_usuario(email)
        
        if user:
            user.token = None
            return self.user_manager.salvar_usuario(user)
        
        return False

    def deletar_usuario(self, email: str) -> bool:
        """
        Deleta um usuário da aplicação.

        Args:
            email: Email a deletar

        Returns:
            True se deletado
        """
        return self.user_manager.deletar_usuario(email.lower().strip())

    @staticmethod
    def _gerar_token_seguro(email: str, tamanho: int = 32) -> str:
        """
        Gera um token seguro e criptográfico.

        Args:
            email: Email (para referência)
            tamanho: Tamanho do token em caracteres

        Returns:
            Token seguro em hexadecimal
        """
        # Gerar bytes aleatórios seguros
        token_bytes = secrets.token_bytes(tamanho // 2)  # bytes -> hex duplica tamanho
        token_hex = token_bytes.hex()
        return token_hex[:tamanho]

    def obter_estatisticas(self) -> dict:
        """
        Obtém estatísticas de autenticação.

        Returns:
            Dicionário com estatísticas
        """
        return {
            'total_usuarios': self.user_manager.contar_usuarios(),
            'usuarios_verificados': self.user_manager.contar_usuarios_verificados(),
            'usuarios_pendentes': self.user_manager.contar_usuarios() - self.user_manager.contar_usuarios_verificados(),
        }
