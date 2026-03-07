"""Rotas de estatísticas"""
from flask import Blueprint, render_template
from app.utils.csv_handler import CSVHandler
from app.utils.stats_calculator import StatsCalculator
from app.auth.decorators import requer_autenticacao

stats_bp = Blueprint('stats', __name__)
csv_handler = CSVHandler()
stats_calc = StatsCalculator()

@stats_bp.route('/estatisticas')
@requer_autenticacao
def estatisticas():
    """Página de estatísticas"""
    dados = csv_handler.carregar_dados()
    stats_por_dia = stats_calc.calcular_estatisticas_por_dia(dados)
    stats_por_mes = stats_calc.calcular_estatisticas_por_mes(dados)
    stats_por_ano = stats_calc.calcular_estatisticas_por_ano(dados)
    stats_globais = stats_calc.calcular_estatisticas_globais(dados)
    return render_template('estatisticas.html', 
                           stats_por_dia=stats_por_dia, 
                           stats_por_mes=stats_por_mes,
                           stats_por_ano=stats_por_ano,
                           stats_globais=stats_globais)
