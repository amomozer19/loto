from flask import Flask
from app.routes import main_bp, stats_bp
from app.routes.auth import auth_bp
from app.routes.aposta import aposta_bp
from app.routes.apostas import apostas_bp
import os

def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__, instance_relative_config=False)
    
    # Configurações de segurança e sessão
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'loto-secret-key-change-in-production')
    
    # Em desenvolvimento, permitir HTTP; em produção exigir HTTPS
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_SECURE'] = is_production  # HTTPS only em produção
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Sem acesso JS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 dias
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)  # Autenticação (primeira para interceptar /auth/login)
    app.register_blueprint(main_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(aposta_bp)
    app.register_blueprint(apostas_bp)
    
    return app
