"""Rotas de geração de apostas"""
from flask import Blueprint, render_template
from datetime import datetime
from app.utils.csv_handler import CSVHandler
from app.utils.stats_calculator import StatsCalculator
from app.utils.aposta_manager import ApostaManager
from app.utils.betting_analyzer import BettingAnalyzer
from app.auth.decorators import requer_autenticacao

aposta_bp = Blueprint('aposta', __name__)
csv_handler = CSVHandler()
stats_calc = StatsCalculator()
aposta_mgr = ApostaManager()
betting_analyzer = BettingAnalyzer()

@aposta_bp.route('/aposta')
@requer_autenticacao
def gerar_aposta():
    """Página de geração de apostas recomendadas"""
    # Obter data atual
    agora = datetime.now()
    dia_semana = (agora.weekday() + 1) % 7  # 0=domingo, 6=sábado
    mes = agora.month
    ano = agora.year
    
    # Carregar dados
    dados = csv_handler.carregar_dados()
    
    # Gerar apostas recomendadas
    apostas = stats_calc.gerar_apostas_recomendadas(dados, dia_semana, mes, ano)
    
    # Adicionar análise de tuplas e tripletas para cada aposta
    for aposta in apostas:
        numeros_aposta = aposta['numeros']
        
        # Extrair tuplas e tripletas apenas com os números da aposta
        tuplas_todas = []
        tripletas_todas = []
        
        for dado in dados:
            try:
                numeros_sorteio = []
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        numeros_sorteio.append(int(dado[chave]))
                
                # Verificar tuples e tripletas nos números da aposta
                for i in range(len(numeros_sorteio)):
                    for j in range(i + 1, len(numeros_sorteio)):
                        tupla = tuple(sorted([numeros_sorteio[i], numeros_sorteio[j]]))
                        if all(n in numeros_aposta for n in tupla):
                            tuplas_todas.append(tupla)
                
                for i in range(len(numeros_sorteio)):
                    for j in range(i + 1, len(numeros_sorteio)):
                        for k in range(j + 1, len(numeros_sorteio)):
                            trip = tuple(sorted([numeros_sorteio[i], numeros_sorteio[j], numeros_sorteio[k]]))
                            if all(n in numeros_aposta for n in trip):
                                tripletas_todas.append(trip)
                
            except:
                continue
        
        # Contar frequências
        from collections import Counter
        aposta['tuplas'] = Counter(tuplas_todas).most_common(5) if tuplas_todas else []
        aposta['tripletas'] = Counter(tripletas_todas).most_common(5) if tripletas_todas else []
    
    # Salvar apostas do dia em JSON
    aposta_mgr.salvar_apostas_dia(apostas, agora)
    
    # Sincronizar resultados (compara com histórico do CSV)
    analise_stats = betting_analyzer.sincronizar_resultados(dados)
    
    # Gerar feedback para melhorar futuras apostas
    feedback = betting_analyzer.gerar_feedback_para_futuras_apostas()
    
    # Obter estatísticas globais
    stats_globais = stats_calc.calcular_estatisticas_globais(dados)
    
    contexto = {
        'apostas': apostas,
        'data_atual': agora.strftime('%d/%m/%Y'),
        'dia_semana_nome': stats_calc._obter_nome_dia(dia_semana),
        'mes_nome': stats_calc._obter_nome_mes(mes),
        'ano': ano,
        'stats_globais': stats_globais,
        'analise_stats': analise_stats,
        'feedback': feedback
    }
    
    return render_template('aposta.html', **contexto)


@aposta_bp.route('/analise-apostas')
@requer_autenticacao
def analise_apostas():
    """Página de análise detalhada das apostas vs resultados reais"""
    # Carregar dados históricos
    dados = csv_handler.carregar_dados()
    
    # Sincronizar e analisar resultados
    analise_stats = betting_analyzer.sincronizar_resultados(dados)
    feedback = betting_analyzer.gerar_feedback_para_futuras_apostas()
    
    # Obter histórico de apostas
    historico = aposta_mgr.obter_historico(dias=90)
    
    contexto = {
        'analise_stats': analise_stats,
        'feedback': feedback,
        'historico_apostas': historico,
        'total_apostas': len(historico),
        'apostas_analisadas': feedback.get('apostas_analisadas', 0)
    }
    
    return render_template('analise_apostas.html', **contexto)

