"""
Configuração do Keycloak para autenticação OAuth2/OIDC.

O Keycloak é um servidor de gerenciamento de identidade e acesso de código aberto.
Fornece:
- Autenticação OAuth2/OIDC
- Gerenciamento de usuários
- Multi-tenancy
- Roles e permissões
- Integração LDAP/AD
"""

import os
from typing import Dict, Optional

class KeycloakConfig:
    """Configuração para integração com Keycloak."""
    
    # URLs e configuração do servidor
    KEYCLOAK_SERVER_URL = os.getenv(
        'KEYCLOAK_SERVER_URL',
        'http://localhost:8080'  # Padrão local
    )
    KEYCLOAK_REALM = os.getenv(
        'KEYCLOAK_REALM',
        'loto-realm'  # Nome do realm (tenant)
    )
    KEYCLOAK_CLIENT_ID = os.getenv(
        'KEYCLOAK_CLIENT_ID',
        'loto-app'  # ID do cliente registrado
    )
    KEYCLOAK_CLIENT_SECRET = os.getenv(
        'KEYCLOAK_CLIENT_SECRET',
        'your-secret-key-here-change-in-production'
    )
    
    # Configurações da aplicação
    FLASK_SECRET_KEY = os.getenv(
        'FLASK_SECRET_KEY',
        'flask-secret-key-change-in-production'
    )
    
    # URLs de redirecionamento (Redirect URIs)
    KEYCLOAK_REDIRECT_URI = os.getenv(
        'KEYCLOAK_REDIRECT_URI',
        'http://localhost:5000/auth/callback'
    )
    
    KEYCLOAK_LOGOUT_REDIRECT_URI = os.getenv(
        'KEYCLOAK_LOGOUT_REDIRECT_URI',
        'http://localhost:5000'
    )
    
    # Configurações de token
    TOKEN_EXPIRY = int(os.getenv('TOKEN_EXPIRY', '3600'))  # 1 hora
    REFRESH_TOKEN_EXPIRY = int(os.getenv('REFRESH_TOKEN_EXPIRY', '86400'))  # 24 horas
    
    # Modo de autenticação (keycloak ou local)
    AUTH_MODE = os.getenv('AUTH_MODE', 'keycloak')  # 'keycloak' ou 'local'
    
    # Mapeamento de claims do Keycloak para aplicação
    USER_ATTRIBUTES = {
        'email': 'email',
        'preferred_username': 'username',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'name': 'full_name'
    }
    
    # Roles que a aplicação utiliza
    REQUIRED_ROLES = [
        'user',        # Usuário básico
        'admin',       # Administrador
        'analyst'      # Analista
    ]
    
    @staticmethod
    def get_keycloak_urls() -> Dict[str, str]:
        """
        Gera as URLs importantes do Keycloak.
        
        Returns:
            Dict com URLs do Keycloak
        """
        base_url = KeycloakConfig.KEYCLOAK_SERVER_URL
        realm = KeycloakConfig.KEYCLOAK_REALM
        
        return {
            'base': base_url,
            'realm': f"{base_url}/realms/{realm}",
            'auth': f"{base_url}/realms/{realm}/protocol/openid-connect/auth",
            'token': f"{base_url}/realms/{realm}/protocol/openid-connect/token",
            'userinfo': f"{base_url}/realms/{realm}/protocol/openid-connect/userinfo",
            'logout': f"{base_url}/realms/{realm}/protocol/openid-connect/logout",
            'jwks': f"{base_url}/realms/{realm}/protocol/openid-connect/certs",
            'admin': f"{base_url}/admin/realms/{realm}"
        }
    
    @staticmethod
    def get_oauth2_config() -> Dict:
        """
        Retorna configuração OAuth2/OIDC para o Authlib.
        
        Returns:
            Dict com configuração OAuth2
        """
        urls = KeycloakConfig.get_keycloak_urls()
        
        return {
            'client_id': KeycloakConfig.KEYCLOAK_CLIENT_ID,
            'client_secret': KeycloakConfig.KEYCLOAK_CLIENT_SECRET,
            'server_metadata_url': urls['realm'] + '/.well-known/openid-configuration',
            'authorize_url': urls['auth'],
            'token_url': urls['token'],
            'userinfo_url': urls['userinfo'],
            'client_kwargs': {
                'scope': 'openid profile email roles',
                'token_endpoint_auth_method': 'client_secret_basic'
            }
        }
    
    @staticmethod
    def validar_configuracao() -> tuple[bool, str]:
        """
        Valida se a configuração do Keycloak está correta.
        
        Returns:
            Tupla (válido: bool, mensagem: str)
        """
        if not KeycloakConfig.KEYCLOAK_SERVER_URL:
            return False, "KEYCLOAK_SERVER_URL não configurada"
        
        if not KeycloakConfig.KEYCLOAK_CLIENT_ID:
            return False, "KEYCLOAK_CLIENT_ID não configurada"
        
        if not KeycloakConfig.KEYCLOAK_CLIENT_SECRET:
            return False, "KEYCLOAK_CLIENT_SECRET não configurada"
        
        if KeycloakConfig.AUTH_MODE not in ['keycloak', 'local']:
            return False, "AUTH_MODE inválido (use 'keycloak' ou 'local')"
        
        return True, "Configuração válida"


# Variáveis de ambiente para produção
KEYCLOAK_ENV_VARS = {
    'KEYCLOAK_SERVER_URL': 'http://keycloak.exemplo.com:8080',  # Mudar em produção
    'KEYCLOAK_REALM': 'loto-realm',
    'KEYCLOAK_CLIENT_ID': 'loto-app',
    'KEYCLOAK_CLIENT_SECRET': 'generated-secret-from-keycloak',
    'KEYCLOAK_REDIRECT_URI': 'https://seu-dominio.com/auth/callback',
    'KEYCLOAK_LOGOUT_REDIRECT_URI': 'https://seu-dominio.com',
    'AUTH_MODE': 'keycloak',
    'FLASK_SECRET_KEY': 'mudar-em-producao'
}
