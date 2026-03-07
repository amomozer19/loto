"""
Decorators para proteção de rotas.

Uso:
    @requer_autenticacao
    def minhaRota():
        pass
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from typing import Callable


def requer_autenticacao(f: Callable) -> Callable:
    """
    Decorator que requer autenticação para acessar a rota.

    Redireciona para login se não autenticado.

    Uso:
        @app.route('/protegido')
        @requer_autenticacao
        def rota_protegida():
            return "Acesso garantido"
    """
    @wraps(f)
    def decorator_funcao(*args, **kwargs):
        # Verificar se existe email na sessão
        if 'email' not in session:
            flash('Por favor, faça login primeiro', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar se usuário está verificado
        if not session.get('verificado', False):
            flash('Por favor, verifique seu email', 'warning')
            return redirect(url_for('auth.verificar'))

        # Usuário autenticado, executar função
        return f(*args, **kwargs)
    
    return decorator_funcao


def requer_admin(f: Callable) -> Callable:
    """
    Decorator que requer privilégios de administrador.

    Nota: Atualmente igual a requer_autenticacao.
    Pode ser expandido para roles de usuário.
    """
    @wraps(f)
    def decorator_funcao(*args, **kwargs):
        # Por enquanto, mesma verificação de autenticação
        if 'email' not in session:
            flash('Acesso negado', 'danger')
            return redirect(url_for('auth.login'))
        
        # Em produção, adicionar verificação de role/admin
        # if not session.get('is_admin', False):
        #     flash('Acesso restrito a administradores', 'danger')
        #     return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    
    return decorator_funcao
