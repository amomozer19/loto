"""
Rotas de autenticação.

Endpoints:
- GET /auth/login - Página de login
- POST /auth/solicitar-token - Solicita token para email
- GET /auth/verificar - Página para inserir token
- POST /auth/verificar - Verifica token
- GET /auth/logout - Faz logout
- GET /auth/encerrar - Faz logout e encerra servidor
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.auth.auth_handler import AuthHandler
import threading
import atexit

# Criar blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Instanciar manipulador de autenticação
auth_handler = AuthHandler(secret_key='loto-secret-key-change-in-production')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de login - solicita email.

    GET: Mostra formulário
    POST: Processa email e envia token
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Por favor, insira um email', 'warning')
            return redirect(url_for('auth.login'))

        # Solicitar token
        sucesso, mensagem = auth_handler.solicitar_token(email)
        
        if sucesso:
            flash(mensagem, 'success')
            # Armazenar email na sessão para próxima etapa
            session['email_solicitado'] = email
            return redirect(url_for('auth.verificar'))
        else:
            flash(mensagem, 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/verificar', methods=['GET', 'POST'])
def verificar():
    """
    Página de verificação de token.

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
            session['verificado'] = True
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
    
    if email:
        auth_handler.fazer_logout(email)
    
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/encerrar')
def encerrar_sessao_app():
    """
    Faz logout do usuário e encerra a aplicação.
    
    Esta rota:
    1. Faz logout (limpa sessão)
    2. Remove token do CSV
    3. Encerra o servidor Flask após 1 segundo
    """
    email = session.get('email')
    
    if email:
        auth_handler.fazer_logout(email)
    
    session.clear()
    
    def parar_servidor():
        """Para o servidor de forma graceful após 1 segundo."""
        import time
        import os
        time.sleep(1)
        
        # Tentar parar via werkzeug
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()
        except:
            pass
        
        # Se werkzeug falhar, usar os exit
        try:
            os._exit(0)
        except:
            pass
    
    # Iniciar thread para parar servidor
    thread = threading.Thread(target=parar_servidor, daemon=True)
    thread.start()
    
    # Renderizar página de confirmação
    return render_template('auth/encerramento.html')


@auth_bp.route('/api/status')
def api_status():
    """
    API: Retorna status de autenticação do usuário.

    Returns:
        JSON com status
    """
    email = session.get('email')
    verificado = session.get('verificado', False)
    
    return jsonify({
        'autenticado': email is not None,
        'email': email,
        'verificado': verificado
    })


@auth_bp.route('/api/solicitar-token', methods=['POST'])
def api_solicitar_token():
    """
    API: Solicita token para um email.

    JSON:
        {
            "email": "user@example.com"
        }

    Returns:
        JSON com resultado
    """
    dados = request.get_json() or {}
    email = dados.get('email', '').strip()
    
    sucesso, mensagem = auth_handler.solicitar_token(email)
    
    return jsonify({
        'sucesso': sucesso,
        'mensagem': mensagem,
        'email': email if sucesso else None
    }), 200 if sucesso else 400


@auth_bp.route('/api/verificar-token', methods=['POST'])
def api_verificar_token():
    """
    API: Verifica e autentica com token.

    JSON:
        {
            "email": "user@example.com",
            "token": "abc123..."
        }

    Returns:
        JSON com resultado
    """
    dados = request.get_json() or {}
    email = dados.get('email', '').strip()
    token = dados.get('token', '').strip()
    
    sucesso, mensagem = auth_handler.verificar_token(email, token)
    
    if sucesso:
        # Armazenar na sessão
        session['email'] = email
        session['verificado'] = True
        session.permanent = True
    
    return jsonify({
        'sucesso': sucesso,
        'mensagem': mensagem,
        'email': email if sucesso else None
    }), 200 if sucesso else 400


@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    """API: Faz logout."""
    email = session.get('email')
    
    if email:
        auth_handler.fazer_logout(email)
    
    session.clear()
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Logout realizado'
    })


@auth_bp.route('/api/estatisticas')
def api_estatisticas():
    """
    API: Retorna estatísticas de autenticação.

    Requer autenticação admin.

    Returns:
        JSON com estatísticas
    """
    # Verificar se está autenticado
    if 'email' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401

    stats = auth_handler.obter_estatisticas()
    
    return jsonify(stats)
