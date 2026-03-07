"""
Handler de autenticação com Keycloak.

Integração OAuth2/OIDC com Keycloak para:
- Login seguro
- Gerenciamento de tokens
- Validação de permissões
- Gerenciamento de sessões
"""

import requests
import json
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta
import jwt
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakAuthorizationConfigError
from keycloak.exceptions import KeycloakClientError, KeycloakAuthorizationConfigError
from app.auth.keycloak_config import KeycloakConfig
from app.models.user import User, UserManager


class KeycloakHandler:
    """Handler para autenticação com Keycloak."""
    
    def __init__(self):
        """Inicializa o cliente Keycloak."""
        self.config = KeycloakConfig()
        self.user_manager = UserManager()
        self.keycloak_openid = None
        self.keycloak_admin = None
        
        try:
            self._inicializar_clientes()
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível inicializar Keycloak: {e}")
            print("   Executando em modo fallback (autenticação local)")
    
    def _inicializar_clientes(self):
        """Inicializa clientes OpenID e Admin do Keycloak."""
        try:
            # Cliente OpenID para autenticação e tokens
            self.keycloak_openid = KeycloakOpenID(
                server_url=self.config.KEYCLOAK_SERVER_URL,
                client_id=self.config.KEYCLOAK_CLIENT_ID,
                realm_name=self.config.KEYCLOAK_REALM,
                client_secret_key=self.config.KEYCLOAK_CLIENT_SECRET,
                verify_certs=False  # Apenas para desenvolvimento
            )
            
            print("✅ Cliente Keycloak OpenID inicializado")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Keycloak OpenID: {e}")
            raise
    
    def obter_urls_autenticacao(self) -> Dict[str, str]:
        """
        Retorna URLs para autenticação OAuth2.
        
        Returns:
            Dict com authorization_url, token_url, etc
        """
        urls = self.config.get_keycloak_urls()
        
        return {
            'authorization_url': urls['auth'],
            'token_url': urls['token'],
            'redirect_uri': self.config.KEYCLOAK_REDIRECT_URI,
            'client_id': self.config.KEYCLOAK_CLIENT_ID,
            'realm': self.config.KEYCLOAK_REALM
        }
    
    def gerar_authorization_url(self, state: str) -> str:
        """
        Gera URL de autorização para redirecionar o usuário.
        
        Args:
            state: Token CSRF para segurança
        
        Returns:
            URL para redirecionar usuário ao Keycloak
        """
        urls = self.obter_urls_autenticacao()
        
        params = {
            'client_id': urls['client_id'],
            'redirect_uri': urls['redirect_uri'],
            'response_type': 'code',
            'scope': 'openid profile email',
            'state': state
        }
        
        url = urls['authorization_url'] + '?'
        url += '&'.join([f"{k}={v}" for k, v in params.items()])
        
        return url
    
    def trocar_codigo_por_token(self, code: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Troca o código de autorização por access token.
        
        Args:
            code: Código retornado pelo Keycloak
        
        Returns:
            Tupla (sucesso, token_response, mensagem)
        """
        if not self.keycloak_openid:
            return False, None, "Keycloak não inicializado"
        
        try:
            token = self.keycloak_openid.token(
                code=code,
                grant_type='authorization_code',
                redirect_uri=self.config.KEYCLOAK_REDIRECT_URI
            )
            
            return True, token, "Token obtido com sucesso"
            
        except Exception as e:
            return False, None, f"Erro ao obter token: {str(e)}"
    
    def validar_access_token(self, access_token: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Valida um access token e retorna as claims.
        
        Args:
            access_token: Token para validar
        
        Returns:
            Tupla (válido, claims, mensagem)
        """
        if not self.keycloak_openid:
            return False, None, "Keycloak não inicializado"
        
        try:
            # Decodificar e validar JWT
            userinfo = self.keycloak_openid.userinfo(access_token)
            
            claims = {
                'sub': userinfo.get('sub'),
                'email': userinfo.get('email'),
                'username': userinfo.get('preferred_username'),
                'name': userinfo.get('name'),
                'roles': userinfo.get('realm_access', {}).get('roles', []),
                'exp': userinfo.get('exp'),
                'iat': userinfo.get('iat')
            }
            
            return True, claims, "Token válido"
            
        except Exception as e:
            return False, None, f"Erro ao validar token: {str(e)}"
    
    def obter_usuario_info(self, access_token: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Obtém informações do usuário do Keycloak.
        
        Args:
            access_token: Access token do usuário
        
        Returns:
            Tupla (sucesso, user_info, mensagem)
        """
        if not self.keycloak_openid:
            return False, None, "Keycloak não inicializado"
        
        try:
            userinfo = self.keycloak_openid.userinfo(access_token)
            
            user_info = {
                'id': userinfo.get('sub'),
                'email': userinfo.get('email'),
                'username': userinfo.get('preferred_username'),
                'first_name': userinfo.get('given_name'),
                'last_name': userinfo.get('family_name'),
                'full_name': userinfo.get('name'),
                'email_verified': userinfo.get('email_verified', False),
                'roles': userinfo.get('realm_access', {}).get('roles', [])
            }
            
            return True, user_info, "Informações obtidas com sucesso"
            
        except Exception as e:
            return False, None, f"Erro ao obter informações: {str(e)}"
    
    def refresh_token(self, refresh_token: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Refresh um access token expirado.
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            Tupla (sucesso, novo_token, mensagem)
        """
        if not self.keycloak_openid:
            return False, None, "Keycloak não inicializado"
        
        try:
            token = self.keycloak_openid.token(
                grant_type='refresh_token',
                refresh_token=refresh_token
            )
            
            return True, token, "Token atualizado com sucesso"
            
        except Exception as e:
            return False, None, f"Erro ao atualizar token: {str(e)}"
    
    def fazer_logout(self, refresh_token: str) -> Tuple[bool, str]:
        """
        Faz logout do usuário.
        
        Args:
            refresh_token: Refresh token do usuário
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.keycloak_openid:
            return False, "Keycloak não inicializado"
        
        try:
            self.keycloak_openid.logout(refresh_token)
            return True, "Logout realizado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao fazer logout: {str(e)}"
    
    def sincronizar_usuario(self, user_info: Dict) -> Tuple[bool, User, str]:
        """
        Sincroniza usuário do Keycloak com banco de dados local.
        
        Args:
            user_info: Informações do usuário do Keycloak
        
        Returns:
            Tupla (sucesso, user, mensagem)
        """
        try:
            email = user_info.get('email', '')
            
            if not email:
                return False, None, "Email não fornecido"
            
            # Buscar usuário existente
            user = self.user_manager.obter_usuario(email)
            
            if not user:
                # Criar novo usuário
                user = User(
                    email=email,
                    keycloak_id=user_info.get('id'),
                    username=user_info.get('username'),
                    first_name=user_info.get('first_name'),
                    last_name=user_info.get('last_name'),
                    full_name=user_info.get('full_name'),
                    verified=user_info.get('email_verified', False),
                    roles=user_info.get('roles', ['user']),
                    auth_provider='keycloak'
                )
            else:
                # Atualizar usuário existente
                user.keycloak_id = user_info.get('id')
                user.username = user_info.get('username')
                user.first_name = user_info.get('first_name')
                user.last_name = user_info.get('last_name')
                user.full_name = user_info.get('full_name')
                user.verified = user_info.get('email_verified', False)
                user.roles = user_info.get('roles', ['user'])
                user.auth_provider = 'keycloak'
            
            # Salvar usuário
            if self.user_manager.salvar_usuario(user):
                return True, user, "Usuário sincronizado com sucesso"
            else:
                return False, None, "Erro ao salvar usuário"
            
        except Exception as e:
            return False, None, f"Erro ao sincronizar usuário: {str(e)}"
    
    def verificar_permissao(self, user_roles: list, role_obrigatoria: str) -> bool:
        """
        Verifica se usuário tem uma role necessária.
        
        Args:
            user_roles: Roles do usuário
            role_obrigatoria: Role requerida
        
        Returns:
            True se usuário tem a role, False caso contrário
        """
        return role_obrigatoria in user_roles
    
    def verificar_permissoes(self, user_roles: list, roles_obrigatorias: list) -> bool:
        """
        Verifica se usuário tem todas as roles necessárias.
        
        Args:
            user_roles: Roles do usuário
            roles_obrigatorias: Roles requeridas
        
        Returns:
            True se usuário tem todas as roles, False caso contrário
        """
        return all(role in user_roles for role in roles_obrigatorias)
    
    @staticmethod
    def validar_configuracao() -> Tuple[bool, str]:
        """Valida se o Keycloak está configurado corretamente."""
        config = KeycloakConfig()
        return config.validar_configuracao()
