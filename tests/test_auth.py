"""
Testes do sistema de autenticação.

Cobertura:
- User model
- UserManager
- AuthHandler
- Routes de autenticação
"""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from app.models.user import User, UserManager
from app.auth.auth_handler import AuthHandler
from app.auth.email_service import EmailService


class TestUserModel:
    """Testes da classe User."""

    def test_criar_usuario(self):
        """Testa criação básica de usuário."""
        user = User(email='test@example.com')
        assert user.email == 'test@example.com'
        assert user.verified is False

    def test_usuario_com_token(self):
        """Testa usuário com token."""
        user = User(email='test@example.com', token='abc123', verified=True)
        assert user.token == 'abc123'
        assert user.verified is True

    def test_usuario_to_dict(self):
        """Testa conversão para dicionário."""
        user = User(email='test@example.com', token='abc123', verified=True)
        resultado = user.to_dict()
        assert resultado['email'] == 'test@example.com'
        assert resultado['token'] == 'abc123'
        assert resultado['verified'] == 'True'

    def test_usuario_to_csv_row(self):
        """Testa conversão para linha CSV."""
        user = User(email='test@example.com', token='abc123', verified=True)
        linha = user.to_csv_row()
        assert len(linha) == 4
        assert linha[0] == 'test@example.com'
        assert linha[1] == 'abc123'

    def test_usuario_from_csv_row(self):
        """Testa criação a partir de linha CSV."""
        linha = ['test@example.com', 'abc123', 'True', '2026-03-04T10:00:00']
        user = User.from_csv_row(linha)
        assert user.email == 'test@example.com'
        assert user.token == 'abc123'
        assert user.verified is True


class TestUserManager:
    """Testes do responsável por usuários."""

    @pytest.fixture
    def csv_temp(self):
        """Cria arquivo CSV temporário para testes."""
        fd, path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    def test_criar_csv(self, csv_temp):
        """Testa criação de arquivo CSV."""
        manager = UserManager(csv_temp)
        assert os.path.exists(csv_temp)

    def test_salvar_usuario(self, csv_temp):
        """Testa salvamento de usuário."""
        manager = UserManager(csv_temp)
        user = User(email='test@example.com', token='abc123')
        resultado = manager.salvar_usuario(user)
        assert resultado is True

    def test_obter_usuario(self, csv_temp):
        """Testa recuperação de usuário."""
        manager = UserManager(csv_temp)
        user = User(email='test@example.com')
        manager.salvar_usuario(user)
        
        recuperado = manager.obter_usuario('test@example.com')
        assert recuperado is not None
        assert recuperado.email == 'test@example.com'

    def test_obter_usuario_inexistente(self, csv_temp):
        """Testa obtenção de usuário inexistente."""
        manager = UserManager(csv_temp)
        resultado = manager.obter_usuario('inexistente@example.com')
        assert resultado is None

    def test_deletar_usuario(self, csv_temp):
        """Testa deleção de usuário."""
        manager = UserManager(csv_temp)
        user = User(email='test@example.com')
        manager.salvar_usuario(user)
        
        resultado = manager.deletar_usuario('test@example.com')
        assert resultado is True
        
        recuperado = manager.obter_usuario('test@example.com')
        assert recuperado is None

    def test_contar_usuarios(self, csv_temp):
        """Testa contagem de usuários."""
        manager = UserManager(csv_temp)
        assert manager.contar_usuarios() == 0
        
        manager.salvar_usuario(User(email='user1@example.com'))
        assert manager.contar_usuarios() == 1
        
        manager.salvar_usuario(User(email='user2@example.com'))
        assert manager.contar_usuarios() == 2

    def test_usuarios_verificados(self, csv_temp):
        """Testa filtro de usuários verificados."""
        manager = UserManager(csv_temp)
        manager.salvar_usuario(User(email='user1@example.com', verified=False))
        manager.salvar_usuario(User(email='user2@example.com', verified=True))
        
        verificados = manager.listar_usuarios_verificados()
        assert len(verificados) == 1
        assert verificados[0].email == 'user2@example.com'


class TestAuthHandler:
    """Testes do manipulador de autenticação."""

    @pytest.fixture
    def auth_handler(self, tmp_path):
        """Cria manipulador de autenticação com arquivo temp."""
        csv_path = tmp_path / 'usuarios.csv'
        handler = AuthHandler(secret_key='test-secret')
        handler.user_manager.csv_path = str(csv_path)
        handler.user_manager._ensure_csv_exists()
        return handler

    def test_gerar_token_seguro(self):
        """Testa geração de token seguro."""
        token1 = AuthHandler._gerar_token_seguro('test@example.com')
        token2 = AuthHandler._gerar_token_seguro('test@example.com')
        
        assert len(token1) == 32
        assert token1 != token2  # Cada token deve ser único

    def test_solicitar_token(self, auth_handler):
        """Testa solicitação de token."""
        sucesso, mensagem = auth_handler.solicitar_token('test@example.com')
        assert sucesso is True
        assert 'teste' in mensagem.lower() or 'sucesso' in mensagem.lower()

    def test_solicitar_token_email_invalido(self, auth_handler):
        """Testa com email inválido."""
        sucesso, mensagem = auth_handler.solicitar_token('invalid-email')
        assert sucesso is False

    def test_solicitar_token_vazio(self, auth_handler):
        """Testa com email vazio."""
        sucesso, mensagem = auth_handler.solicitar_token('')
        assert sucesso is False

    def test_verificar_token_valido(self, auth_handler):
        """Testa verificação de token válido."""
        # Solicitar token
        auth_handler.solicitar_token('test@example.com')
        
        # Obter token do arquivo de log
        token = EmailService.obter_ultimo_token('test@example.com')
        
        # Verificar token
        sucesso, mensagem = auth_handler.verificar_token('test@example.com', token)
        assert sucesso is True

    def test_verificar_token_invalido(self, auth_handler):
        """Testa com token inválido."""
        auth_handler.solicitar_token('test@example.com')
        
        sucesso, mensagem = auth_handler.verificar_token('test@example.com', 'token-errado')
        assert sucesso is False

    def test_usuario_nao_encontrado(self, auth_handler):
        """Testa verificação de usuário inexistente."""
        sucesso, mensagem = auth_handler.verificar_token('inexistente@example.com', 'token')
        assert sucesso is False

    def test_usuario_verificado(self, auth_handler):
        """Testa se usuário está verificado após autenticação."""
        email = 'test@example.com'
        
        # Solicitar e verificar token
        auth_handler.solicitar_token(email)
        token = EmailService.obter_ultimo_token(email)
        auth_handler.verificar_token(email, token)
        
        # Verificar status
        assert auth_handler.usuario_verificado(email) is True

    def test_fazer_logout(self, auth_handler):
        """Testa logout de usuário."""
        email = 'test@example.com'
        auth_handler.solicitar_token(email)
        
        resultado = auth_handler.fazer_logout(email)
        assert resultado is True

    def test_deletar_usuario(self, auth_handler):
        """Testa deleção de usuário."""
        email = 'test@example.com'
        auth_handler.solicitar_token(email)
        
        resultado = auth_handler.deletar_usuario(email)
        assert resultado is True

    def test_obter_estatisticas(self, auth_handler):
        """Testa obtenção de estatísticas."""
        auth_handler.solicitar_token('user1@example.com')
        auth_handler.solicitar_token('user2@example.com')
        
        stats = auth_handler.obter_estatisticas()
        assert stats['total_usuarios'] == 2
        assert stats['usuarios_pendentes'] == 2


class TestRotasAutenticacao:
    """Testes das rotas de autenticação."""

    def test_login_get(self, client):
        """Testa GET /auth/login."""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Email' in response.data

    def test_login_post_email_valido(self, client):
        """Testa POST /auth/login com email válido."""
        response = client.post('/auth/login', data={
            'email': 'test@example.com'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'verificar' in response.data.lower() or b'code' in response.data.lower()

    def test_login_post_email_vazio(self, client):
        """Testa POST /auth/login com email vazio."""
        response = client.post('/auth/login', data={
            'email': ''
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_verificar_get(self, client):
        """Testa GET /auth/verificar."""
        # Primeiro fazer login
        client.post('/auth/login', data={'email': 'test@example.com'})
        
        response = client.get('/auth/verificar')
        assert response.status_code == 200

    def test_api_status_nao_autenticado(self, client):
        """Testa /auth/api/status sem autenticação."""
        response = client.get('/auth/api/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['autenticado'] is False

    def test_api_solicitar_token(self, client):
        """Testa /auth/api/solicitar-token."""
        response = client.post('/auth/api/solicitar-token',
            json={'email': 'test@example.com'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['sucesso'] is True

    def test_logout(self, client):
        """Testa logout."""
        # Fazer login
        client.post('/auth/login', data={'email': 'test@example.com'})
        
        # Depois fazer logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200


class TestEmailService:
    """Testes do serviço de email."""

    def teardown_method(self):
        """Limpar arquivo de log após cada teste."""
        EmailService.limpar_logs()

    def test_enviar_token(self):
        """Testa envio de token."""
        sucesso, mensagem = EmailService.enviar_token('test@example.com', 'abc123')
        assert sucesso is True

    def test_obter_ultimo_token(self):
        """Testa obtenção do último token."""
        email = 'test@example.com'
        token = 'abc123'
        
        EmailService.enviar_token(email, token)
        recuperado = EmailService.obter_ultimo_token(email)
        
        assert recuperado == token

    def test_limpar_logs(self):
        """Testa limpeza de logs."""
        EmailService.enviar_token('test@example.com', 'abc123')
        EmailService.limpar_logs()
        
        recuperado = EmailService.obter_ultimo_token('test@example.com')
        assert recuperado == ''
