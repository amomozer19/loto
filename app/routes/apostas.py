"""Rotas para função de apostas do usuário"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from app.utils.csv_handler import CSVHandler
from app.utils.aposta_manager import ApostaManager
from app.utils.betting_analyzer import BettingAnalyzer
from app.auth.decorators import requer_autenticacao
import json

apostas_bp = Blueprint('apostas', __name__)

csv_handler = CSVHandler()
aposta_mgr = ApostaManager()
betting_analyzer = BettingAnalyzer()


@apostas_bp.route('/apostas')
@requer_autenticacao
def registrar_apostas():
    """Página para registrar apostas realizadas"""
    return render_template('apostas_registro.html')


@apostas_bp.route('/apostas/analisar', methods=['POST'])
@requer_autenticacao
def analisar_apostas():
    """Recebe als apostas, valida vs resultado e fornece análise"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Extração de dados básicos
        data_aposta = data.get('data_aposta')
        concurso = data.get('concurso')
        quantidade_apostas = int(data.get('quantidade_apostas', 1))
        
        # Resultado do sorteio
        resultado_ids = data.getlist('resultado_sorteio[]')
        numeros_sorteio = sorted([int(n) for n in resultado_ids if n])
        
        # Validação básica
        if len(numeros_sorteio) != 15:
            return jsonify({
                'sucesso': False,
                'erro': 'O resultado deve conter exatamente 15 números'
            }), 400
        
        # Extrair apostas do usuário
        apostas_usuario = []
        for i in range(quantidade_apostas):
            nome = data.get(f'apostasnome_aposta_{i}') or data.get(f'nome_aposta_{i}') or f'Aposta {i+1}'
            numeros_ids = data.getlist(f'numeros_{i}[]')
            numeros = sorted([int(n) for n in numeros_ids if n])
            raciocinio = data.get(f'raciocinio_aposta_{i}', '').strip()
            
            if len(numeros) >= 7 and len(numeros) <= 15:
                apostas_usuario.append({
                    'nome': nome,
                    'numeros': numeros,
                    'raciocinio': raciocinio
                })
        
        if not apostas_usuario:
            return jsonify({
                'sucesso': False,
                'erro': 'Nenhuma aposta válida foi fornecida'
            }), 400
        
        # Analisar apostas vs resultado
        resultado_analise = analisar_apostas_vs_resultado(
            apostas_usuario,
            numeros_sorteio,
            data_aposta,
            concurso
        )
        
        # Se não ganhou, chamar agente de análise
        if not resultado_analise['ganhou']:
            dados_csv = csv_handler.carregar_dados()
            analise_agente = gerar_recomendacoes_agente(
                apostas_usuario,
                numeros_sorteio,
                dados_csv,
                resultado_analise
            )
            resultado_analise['analise_agente'] = analise_agente
        
        # Salvar resultado em análise do usuário (session)
        if 'apostas_analisadas' not in session:
            session['apostas_analisadas'] = []
        
        session['apostas_analisadas'].append({
            'data': data_aposta,
            'concurso': concurso,
            'resultado': resultado_analise
        })
        session.modified = True
        
        return jsonify({
            'sucesso': True,
            'resultado': resultado_analise,
            'redirect': '/analise-resultado'
        })
        
    except Exception as e:
        print(f"Erro ao analisar apostas: {e}")
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@apostas_bp.route('/analise-resultado')
@requer_autenticacao
def ver_analise_resultado():
    """Exibe análise do último conjunto de apostas"""
    resultado = None
    
    # Pega a última análise da session
    if 'apostas_analisadas' in session and session['apostas_analisadas']:
        resultado = session['apostas_analisadas'][-1]
    
    return render_template('analise_resultado.html', resultado=resultado)


def analisar_apostas_vs_resultado(apostas, numeros_sorteio, data_str, concurso):
    """
    Analisa apostas contra o resultado real
    
    Args:
        apostas: Lista de apostas do usuário
        numeros_sorteio: Números que saíram (15)
        data_str: Data em formato YYYY-MM-DD
        concurso: Número do concurso
    
    Returns:
        Dict com análise completa
    """
    resultado_sorteio = set(numeros_sorteio)
    analise_apostas = []
    maior_acerto = 0
    melhor_aposta = "N/A"
    scores = []
    ganhou = False
    
    for aposta in apostas:
        numeros = set(aposta['numeros'])
        acertos = numeros & resultado_sorteio
        nao_acertos = numeros - resultado_sorteio
        
        qtd_acertos = len(acertos)
        qtd_apostados = len(numeros)
        
        # Calcular tuplas e triplas acertadas
        tuplas_acertadas = _contar_padroes(numeros_sorteio, list(numeros), 2)
        tripletas_acertadas = _contar_padroes(numeros_sorteio, list(numeros), 3)
        
        # Score: baseia-se em acertos, tuplas e triplas
        score = min(
            100,
            (qtd_acertos * 12) + (tuplas_acertadas * 3) + (tripletas_acertadas * 5)
        )
        
        # Verificar se ganhou (consideramos comme "ganho" se acertou 5+ números)
        if qtd_acertos >= 5:
            ganhou = True
        
        if score > maior_acerto:
            maior_acerto = score
            melhor_aposta = aposta['nome']
        
        scores.append(score)
        
        analise_apostas.append({
            'nome': aposta['nome'],
            'numeros': sorted(list(numeros)),
            'acertos': sorted(list(acertos)),
            'nao_acertos': sorted(list(nao_acertos)),
            'qtd_acertos': qtd_acertos,
            'qtd_apostados': qtd_apostados,
            'raciocinio': aposta.get('raciocinio', ''),
            'score': score,
            'tuplas_acertadas': tuplas_acertadas,
            'tripletas_acertadas': tripletas_acertadas
        })
    
    return {
        'data': data_str,
        'concurso': concurso,
        'numeros_sorteio': numeros_sorteio,
        'analise_apostas': analise_apostas,
        'ganhou': ganhou,
        'maior_acerto': maior_acerto,
        'melhor_aposta': melhor_aposta,
        'score_medio': round(sum(scores) / len(scores)) if scores else 0
    }


def gerar_recomendacoes_agente(apostas, numeros_sorteio, dados_csv, resultado_analise):
    """
    Agente inteligente que analisa por que apostas perderam
    e faz recomendações baseadas em padrões históricos
    
    Args:
        apostas: Apostas do usuário
        numeros_sorteio: Números que saíram
        dados_csv: Dados históricos
        resultado_analise: Análise prévia
    
    Returns:
        Dict com análise inteligente e recomendações
    """
    resultado_sorteio = set(numeros_sorteio)
    
    # Extração de padrões não identificados
    padroes_nao_identificados = []
    
    # Padrão 1: Números sucessivos (1,2,3)
    tuplas_sucessivas = _encontrar_padroes_sucessivos(numeros_sorteio, 2)
    if tuplas_sucessivas and len(tuplas_sucessivas) >= 3:
        padroes_nao_identificados.append({
            'tipo': 'Duplas Sucessivas',
            'descricao': f'Encontramos {len(tuplas_sucessivas)} duplas de números consecutivos',
            'frequencia': 35
        })
    
    # Padrão 2: Distribuição par/ímpar
    pares_sorteio = [n for n in numeros_sorteio if n % 2 == 0]
    frequencia_pares = (len(pares_sorteio) / 15) * 100
    padroes_nao_identificados.append({
        'tipo': 'Distribuição Par/Ímpar',
        'descricao': f'Proporção de números pares: {frequencia_pares:.0f}%',
        'frequencia': frequencia_pares
    })
    
    # Recomendações baseadas em padrões
    recomendacoes = [
        'Varie mais entre números altos (13-25) e baixos (1-12)',
        'Considere a proporção par/ímpar na próxima aposta',
        'Observe padrões de números consecutivos',
        'Analise a frequência de cada número nos últimos 30 sorteios',
        'Considere agrupar números por década (1-5, 6-10, etc.)'
    ]
    
    # Números recomendados (os mais frequentes nos dados históricos)
    numeros_recomendados = _extrair_numeros_mais_frequentes(dados_csv, 10)
    
    # Adicionar frequência relativa ao sorteio atual
    for num_rec in numeros_recomendados:
        # Quantas vezes esse número apareceu com os números que saíram
        aparicoes = 0
        for dado in dados_csv:
            try:
                sorteio_nums = set()
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        sorteio_nums.add(int(dado[chave]))
                
                if num_rec['numero'] in sorteio_nums:
                    # Verifica quantos do sorteio atual estão nesse histórico
                    intersecao = len(sorteio_nums & resultado_sorteio)
                    if intersecao >= 3:
                        aparicoes += 1
            except:
                continue
        
        num_rec['compatibilidade'] = min(aparicoes // 10, 100) if aparicoes else 0
    
    return {
        'padroes_nao_identificados': padroes_nao_identificados[:3],
        'recomendacoes': recomendacoes,
        'numeros_recomendados': numeros_recomendados[:8],
        'registros_analisados': len(dados_csv)
    }


def _contar_padroes(numeros_sorteio, numeros_aposta, tamanho):
    """Contar tuplas ou triplas que acertaram"""
    contagem = 0
    numerosaposta_set = set(numeros_aposta)
    sorteio_set = set(numeros_sorteio)
    
    sorteio_list = sorted(sorteio_set)
    
    if tamanho == 2:
        for i in range(len(sorteio_list)):
            for j in range(i + 1, len(sorteio_list)):
                if sorteio_list[i] in numerosaposta_set and sorteio_list[j] in numerosaposta_set:
                    contagem += 1
    elif tamanho == 3:
        for i in range(len(sorteio_list)):
            for j in range(i + 1, len(sorteio_list)):
                for k in range(j + 1, len(sorteio_list)):
                    if (sorteio_list[i] in numerosaposta_set and
                        sorteio_list[j] in numerosaposta_set and
                        sorteio_list[k] in numerosaposta_set):
                        contagem += 1
    
    return contagem


def _encontrar_padroes_sucessivos(numeros, tamanho=2):
    """Encontra números sucessivos (ex: 5,6,7)"""
    numeros_sort = sorted(numeros)
    padroes = []
    
    for i in range(len(numeros_sort) - tamanho + 1):
        eh_sucessivo = True
        for j in range(tamanho - 1):
            if numeros_sort[i + j + 1] - numeros_sort[i + j] != 1:
                eh_sucessivo = False
                break
        
        if eh_sucessivo:
            padroes.append(tuple(numeros_sort[i:i+tamanho]))
    
    return padroes


def _extrair_numeros_mais_frequentes(dados_csv, quantidade=10):
    """
    Extrai os números mais frequentes do histórico
    
    Returns:
        Lista de dicts com 'numero' e 'frequencia'
    """
    from collections import Counter
    
    contador = Counter()
    
    for linha in dados_csv:
        try:
            for i in range(1, 16):
                chave = f'Bola{i}'
                if chave in linha:
                    contador[int(linha[chave])] += 1
        except:
            continue
    
    total = sum(contador.values())
    resultado = []
    
    for numero, freq in contador.most_common(quantidade):
        resultado.append({
            'numero': numero,
            'frequencia': round((freq / total) * 100, 1) if total > 0 else 0,
            'ocorrencias': freq
        })
    
    return resultado
