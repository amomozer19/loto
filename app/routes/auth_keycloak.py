"""
Rotas de autenticação com suporte a Keycloak.

Endpoints:
- GET /auth/login - Página de login
- GET /auth/login-keycloak - Redireciona para Keycloak
- GET /auth/callback - Callback do Keycloak (OAuth2)
- POST /auth/solicitar-token - Solicita token (modo local)
- GET /auth/verificar - Página para inserir token (modo local)
- POST /auth/verificar - Verifica token (modo local)
- GET /auth/logout - Faz logout
- GET /auth/encerrar - Faz logout e encerra servidor
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.auth.auth_handler import AuthHandler
from app.auth.keycloak_handler import KeycloakHandler
from app.auth.keycloak_config import KeycloakConfig
import threading
import atexit
import secrets

# Criar blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Instanciar manipuladores
auth_handler = AuthHandler(secret_key='loto-secret-key-change-in-production')
keycloak_handler = KeycloakHandler()
keycloak_config = KeycloakConfig()

# Verificar configuração
valid, msg = keycloak_config.validar_configuracao()
if not valid:
    print(f"⚠️ Aviso: Keycloak não configurado corretamente: {msg}")
    print("   Usando autenticação local por padrão")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de login - suporta local e Keycloak.
    
    GET: Mostra formulário
    POST: Processa email e envia token (local)
    """
    auth_mode = keycloak_config.AUTH_MODE
    
    # Se modo é Keycloak, redirecionar para login Keycloak
    if auth_mode == 'keycloak' and request.method == 'GET':
        return redirect(url_for('auth.login_keycloak'))
    
    # Modo local
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        use_keycloak = request.form.get('use_keycloak', '').lower() == 'true'
        
        if not email:
            flash('Por favor, insira um email', 'warning')
            return redirect(url_for('auth.login'))
        
        # Se usuário quer Keycloak
        if use_keycloak:
            # Armazenar email na sessão e redirecionar
            session['email_para_keycloak'] = email
            return redirect(url_for('auth.login_keycloak'))
        
        # Solicitar token (modo local)
        sucesso, mensagem = auth_handler.solicitar_token(email)
        
        if sucesso:
            flash(mensagem, 'success')
            session['email_solicitado'] = email
            return redirect(url_for('auth.verificar'))
        else:
            flash(mensagem, 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', keycloak_enabled=(keycloak_config.AUTH_MODE == 'keycloak'))


@auth_bp.route('/login-keycloak')
def login_keycloak():
    """Redireciona para login do Keycloak (OAuth2)."""
    # Gerar state para CSRF
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Gerar URL de autorização
    auth_url = keycloak_handler.gerar_authorization_url(state)
    
    return redirect(auth_url)


@auth_bp.route('/callback')
def callback():
    """Callback do Keycloak após autenticação OAuth2."""
    # Validar state
    state = request.args.get('state')
    if not state or state != session.get('oauth_state'):
        flash('Erro de segurança: State inválido', 'danger')
        return redirect(url_for('auth.login'))
    
    # Obter código
    code = request.args.get('code')
    if not code:
        flash('Erro: Código de autorização não recebido', 'danger')
        return redirect(url_for('auth.login'))
    
    # Trocar código por token
    sucesso, token_response, mensagem = keycloak_handler.trocar_codigo_por_token(code)
    
    if not sucesso:
        flash(f'Erro na autenticação: {mensagem}', 'danger')
        return redirect(url_for('auth.login'))
    
    access_token = token_response.get('access_token')
    refresh_token = token_response.get('refresh_token')
    
    # Validar token e obter informações do usuário
    sucesso, user_info, mensagem = keycloak_handler.obter_usuario_info(access_token)
    
    if not sucesso:
        flash(f'Erro ao obter informações: {mensagem}', 'danger')
        return redirect(url_for('auth.login'))
    
    # Sincronizar usuário com banco de dados local
    sucesso, user, mensagem = keycloak_handler.sincronizar_usuario(user_info)
    
    if not sucesso:
        flash(f'Erro ao sincronizar usuário: {mensagem}', 'danger')
        return redirect(url_for('auth.login'))
    
    # Armazenar tokens na sessão
    session['email'] = user_info['email']
    session['username'] = user_info.get('username', user_info['email'])
    session['full_name'] = user_info.get('full_name', '')
    session['roles'] = user_info.get('roles', ['user'])
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['verified'] = True
    session['auth_provider'] = 'keycloak'
    session.permanent = True
    
    flash(f'Bem-vindo {user_info.get("full_name", user_info["email"])}!', 'success')
    
    return redirect(url_for('main.index'))


@auth_bp.route('/verificar', methods=['GET', 'POST'])
def verificar():
    """
    Página de verificação de token (modo local).
    
    GET: Mostra formulário
    POST: Processa e verifica token
    """
    # Se não tem email solicitado, redirecionar para login
    email = session.get('email_solicitado')
    if not email:
        flash('Por favor, faça login primeiro', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        
        if not token:
            flash('Por favor, insira o token', 'warning')
            return redirect(url_for('auth.verificar'))

        # Verificar token
        sucesso, mensagem = auth_handler.verificar_token(email, token)
        
        if sucesso:
            flash(mensagem, 'success')
            # Armazenar dados de autenticação na sessão
            session['email'] = email
            session['verified'] = True
            session['auth_provider'] = 'local'
            session.permanent = True  # Persistir sessão
            
            # Limpar dados temporários
            session.pop('email_solicitado', None)
            
            return redirect(url_for('main.index'))
        else:
            flash(mensagem, 'danger')
            return redirect(url_for('auth.verificar'))

    return render_template('auth/verificar.html', email=email)


@auth_bp.route('/logout')
def logout():
    """Faz logout do usuário."""
    email = session.get('email')
    auth_provider = session.get('auth_provider', 'local')
    
    # Se Keycloak, fazer logout lá também
    if auth_provider == 'keycloak':
        refresh_token = session.get('refresh_token')
        if refresh_token:
            keycloak_handler.fazer_logout(refresh_token)
    
    # Limpar sessão
    session.clear()
    
    flash('Você foi desconectado com sucesso', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/encerramento')
def encerramento():
    """Página de encerramento (logout + encerra servidor)."""
    auth_provider = session.get('auth_provider', 'local')
    
    # Se Keycloak, fazer logout
    if auth_provider == 'keycloak':
        refresh_token = session.get('refresh_token')
        if refresh_token:
            keycloak_handler.fazer_logout(refresh_token)
    
    # Limpar sessão
    session.clear()
    
    # Renderizar página de encerramento
    return render_template('auth/encerramento.html')


@auth_bp.route('/encerrar')
def encerrar():
    """Encerra o servidor (apenas em desenvolvimento)."""
    email = session.get('email')
    
    # Log
    print(f"\n{'='*60}")
    print(f"  🔌 Servidor encerrado pelo usuário: {email}")
    print(f"{'='*60}\n")
    
    # Limpar sessão
    session.clear()
    
    # Encerrar servidor em thread separada
    def shutdown_server():
        import time
        time.sleep(1)
        import os
        os._exit(0)
    
    thread = threading.Thread(target=shutdown_server, daemon=True)
    thread.start()
    
    flash('Servidor será encerrado...', 'info')
    return redirect(url_for('auth.encerramento'))


@auth_bp.route('/status')
def status():
    """Retorna status de autenticação (JSON)."""
    return jsonify({
        'authenticated': bool(session.get('email')),
        'email': session.get('email'),
        'username': session.get('username'),
        'full_name': session.get('full_name'),
        'roles': session.get('roles', []),
        'auth_provider': session.get('auth_provider', 'unknown')
    })
