"""
Modelo de usuário para autenticação.

Responsvel por representar um usuário da aplicação com:
- Email único
- Tokens de acesso temporários
- Estado de verificação
"""

import csv
import os
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.paths import get_users_csv


class User:
    """Representa um usuário da aplicação."""

    def __init__(self, email: str, token: str = None, verified: bool = False, created_at: str = None,
                 keycloak_id: str = None, username: str = None, first_name: str = None,
                 last_name: str = None, full_name: str = None, roles: list = None,
                 auth_provider: str = 'local'):
        """
        Inicializa um usuário.

        Args:
            email: Email do usuário (identificador único)
            token: Token de autenticação temporário (para modo local)
            verified: Se o usuário verificou seu email
            created_at: Data de criação (ISO format)
            keycloak_id: ID do usuário no Keycloak (para OIDC)
            username: Nome de usuário
            first_name: Primeiro nome
            last_name: Sobrenome
            full_name: Nome completo
            roles: Roles do usuário [user, admin, analyst]
            auth_provider: Provedor de autenticação ('local' ou 'keycloak')
        """
        self.email = email
        self.token = token  # Para autenticação local
        self.verified = verified
        self.created_at = created_at or datetime.now().isoformat()
        
        # Campos Keycloak
        self.keycloak_id = keycloak_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.roles = roles or ['user']
        self.auth_provider = auth_provider  # 'local' ou 'keycloak'

    def to_dict(self) -> dict:
        """Converte usuário para dicionário."""
        return {
            'email': self.email,
            'token': self.token,
            'verified': self.verified,
            'created_at': self.created_at,
            'keycloak_id': self.keycloak_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'roles': self.roles,
            'auth_provider': self.auth_provider
        }

    def to_csv_row(self) -> List[str]:
        """Converte para linha CSV."""
        return [
            self.email,
            self.token or '',
            str(self.verified),
            self.created_at,
            self.keycloak_id or '',
            self.username or '',
            self.first_name or '',
            self.last_name or '',
            self.full_name or '',
            '|'.join(self.roles) if self.roles else 'user',
            self.auth_provider
        ]

    @staticmethod
    def from_csv_row(row: List[str]) -> 'User':
        """Cria User a partir de linha CSV."""
        # Backward compatibility: se linha tem apenas 4 elementos (formato antigo)
        if len(row) == 4:
            email, token, verified, created_at = row
            return User(
                email=email,
                token=token if token else None,
                verified=verified.lower() == 'true',
                created_at=created_at,
                auth_provider='local'
            )
        
        # Novo formato com Keycloak (11 elementos)
        if len(row) >= 11:
            email, token, verified, created_at, keycloak_id, username, first_name, last_name, full_name, roles_str, auth_provider = row[:11]
            
            roles = roles_str.split('|') if roles_str else ['user']
            
            return User(
                email=email,
                token=token if token else None,
                verified=verified.lower() == 'true',
                created_at=created_at,
                keycloak_id=keycloak_id if keycloak_id else None,
                username=username if username else None,
                first_name=first_name if first_name else None,
                last_name=last_name if last_name else None,
                full_name=full_name if full_name else None,
                roles=roles,
                auth_provider=auth_provider or 'local'
            )
        
        # Fallback para formato desconhecido
        return User(email=row[0] if row else 'unknown_user')


class UserManager:
    """Gerencia persistência de usuários em CSV."""

    CSV_HEADERS = ['email', 'token', 'verified', 'created_at', 'keycloak_id', 'username', 
                   'first_name', 'last_name', 'full_name', 'roles', 'auth_provider']
    TOKEN_EXPIRATION_HOURS = 24

    def __init__(self, csv_path: str = None):
        """
        Inicializa o gerenciador de usuários.

        Args:
            csv_path: Caminho para arquivo CSV de usuários (padrão: data/dados_usuarios.csv)
        """
        self.csv_path = csv_path or get_users_csv()
        self._ensure_csv_exists()
        self._migrate_csv_if_needed()  # Migrar de formato antigo se necessário

    def _ensure_csv_exists(self) -> None:
        """Cria arquivo CSV se não existir."""
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(self.CSV_HEADERS)

    def _migrate_csv_if_needed(self) -> None:
        """Migra CSV do formato antigo para novo (com suporte Keycloak)."""
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader, None)
                
                # Se header é antigo (4 colunas), fazer migração
                if header and len(header) == 4:
                    print("🔄 Migrando arquivo de usuários para novo formato...")
                    
                    usuarios = []
                    for row in reader:
                        if row:
                            usuarios.append(User.from_csv_row(row))
                    
                    # Resalvar com novo header
                    with open(self.csv_path, 'w', newline='', encoding='utf-8') as fw:
                        writer = csv.writer(fw, delimiter=';')
                        writer.writerow(self.CSV_HEADERS)
                        for u in usuarios:
                            writer.writerow(u.to_csv_row())
                    
                    print("✅ Migração concluída com sucesso!")
        except Exception as e:
            print(f"⚠️  Erro na migração: {e}")

    def carregar_usuarios(self) -> List[User]:
        """Carrega todos os usuários do CSV."""
        usuarios = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                next(reader)  # Pular header
                for row in reader:
                    if row:  # Ignorar linhas vazias
                        usuarios.append(User.from_csv_row(row))
        except FileNotFoundError:
            self._ensure_csv_exists()
        return usuarios

    def salvar_usuario(self, user: User) -> bool:
        """
        Salva ou atualiza um usuário no CSV.

        Args:
            user: Usuário a salvar

        Returns:
            True se sucesso, False caso contrário
        """
        usuarios = self.carregar_usuarios()
        
        # Verificar se usuário já existe
        user_index = None
        for i, u in enumerate(usuarios):
            if u.email == user.email:
                user_index = i
                break

        if user_index is not None:
            # Atualizar
            usuarios[user_index] = user
        else:
            # Adicionar novo
            usuarios.append(user)

        # Salvar todos
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(self.CSV_HEADERS)
                for u in usuarios:
                    writer.writerow(u.to_csv_row())
            return True
        except Exception as e:
            print(f"Erro ao salvar usuário: {e}")
            return False

    def obter_usuario(self, email: str) -> Optional[User]:
        """
        Obtém um usuário pelo email.

        Args:
            email: Email do usuário

        Returns:
            Usuário ou None se não encontrado
        """
        usuarios = self.carregar_usuarios()
        for user in usuarios:
            if user.email.lower() == email.lower():
                return user
        return None

    def obter_usuario_por_token(self, token: str) -> Optional[User]:
        """
        Obtém um usuário pelo token.

        Args:
            token: Token de autenticação

        Returns:
            Usuário ou None se não encontrado/expirado
        """
        usuarios = self.carregar_usuarios()
        for user in usuarios:
            if user.token == token and not self._token_expirou(user):
                return user
        return None

    def _token_expirou(self, user: User) -> bool:
        """Verifica se token do usuário expirou."""
        if not user.created_at:
            return True
        
        try:
            created = datetime.fromisoformat(user.created_at)
            agora = datetime.now()
            diferenca = agora - created
            return diferenca > timedelta(hours=self.TOKEN_EXPIRATION_HOURS)
        except:
            return True

    def deletar_usuario(self, email: str) -> bool:
        """
        Deleta um usuário.

        Args:
            email: Email do usuário

        Returns:
            True se deletado, False caso contrário
        """
        usuarios = self.carregar_usuarios()
        usuarios_filtrados = [u for u in usuarios if u.email.lower() != email.lower()]
        
        if len(usuarios_filtrados) == len(usuarios):
            return False  # Não encontrado

        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(self.CSV_HEADERS)
                for u in usuarios_filtrados:
                    writer.writerow(u.to_csv_row())
            return True
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return False

    def listar_usuarios_verificados(self) -> List[User]:
        """Lista todos os usuários verificados."""
        usuarios = self.carregar_usuarios()
        return [u for u in usuarios if u.verified]

    def listar_usuarios_pendentes(self) -> List[User]:
        """Lista usuários aguardando verificação."""
        usuarios = self.carregar_usuarios()
        return [u for u in usuarios if not u.verified]

    def contar_usuarios(self) -> int:
        """Retorna total de usuários."""
        return len(self.carregar_usuarios())

    def contar_usuarios_verificados(self) -> int:
        """Retorna total de usuários verificados."""
        return len(self.listar_usuarios_verificados())
