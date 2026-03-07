"""Rotas principais da aplicação"""
from flask import Blueprint, render_template, request, jsonify
import random
from app.utils.csv_handler import CSVHandler
from app.utils.validators import SorteioValidator
from app.utils.sorte_analyzer import SorteAnalyzer
from app.auth.decorators import requer_autenticacao

main_bp = Blueprint('main', __name__)
csv_handler = CSVHandler()
sorte_analyzer = SorteAnalyzer()

@main_bp.route('/')
@requer_autenticacao
def index():
    """Página inicial"""
    dados = csv_handler.carregar_dados()
    proximo_id = csv_handler.obter_proximo_id()
    return render_template('index.html', dados=dados, proximo_id=proximo_id, total=len(dados))

@main_bp.route('/novo')
@requer_autenticacao
def novo():
    """Página para adicionar novo sorteio"""
    proximo_id = csv_handler.obter_proximo_id()
    return render_template('novo.html', proximo_id=proximo_id)

@main_bp.route('/api/gerar_numeros')
@requer_autenticacao
def gerar_numeros():
    """API para gerar números aleatórios"""
    numeros = sorted(random.sample(range(1, 26), 15))
    return jsonify({'numeros': numeros})

@main_bp.route('/api/validar', methods=['POST'])
@requer_autenticacao
def api_validar():
    """API para validar dados"""
    try:
        dados = request.json
        numeros = dados.get('numeros', [])
        
        valido, mensagem = SorteioValidator.validar_numeros(numeros)
        
        if not valido:
            return jsonify({'valido': False, 'erro': mensagem})
        
        return jsonify({'valido': True})
    
    except Exception as e:
        return jsonify({'valido': False, 'erro': str(e)})


@main_bp.route('/sorte')
@requer_autenticacao
def sorte():
    """Página de análise de sorte com 7 números"""
    return render_template('sorte.html')


@main_bp.route('/api/analisar-sorte', methods=['POST'])
@requer_autenticacao
def api_analisar_sorte():
    """API para analisar os 7 números fornecidos"""
    try:
        dados = request.json
        numeros = dados.get('numeros', [])
        
        # Validação básica
        if not numeros or len(numeros) != 7:
            return jsonify({'erro': 'Forneça exatamente 7 números'})
        
        # Validar se são números entre 1-25
        if not all(isinstance(n, int) and 1 <= n <= 25 for n in numeros):
            return jsonify({'erro': 'Todos os números devem estar entre 1 e 25'})
        
        # Validar se não há duplicatas
        if len(set(numeros)) != 7:
            return jsonify({'erro': 'Não pode haver números repetidos'})
        
        # Realizar análise
        analise = sorte_analyzer.analisar_numeros(numeros)
        
        return jsonify(analise)
    
    except Exception as e:
        return jsonify({'erro': str(e)})


@main_bp.route('/api/salvar', methods=['POST'])
@requer_autenticacao
def api_salvar():
    """API para salvar dados"""
    try:
        dados = request.json
        id_val = dados.get('id')
        data_val = dados.get('data')
        numeros = dados.get('numeros', [])
        
        # Validações
        valido_id, msg_id = SorteioValidator.validar_id(id_val)
        if not valido_id:
            return jsonify({'erro': msg_id}), 400
        
        valido_data, msg_data = SorteioValidator.validar_data(data_val)
        if not valido_data:
            return jsonify({'erro': msg_data}), 400
        
        valido_numeros, msg_numeros = SorteioValidator.validar_numeros(numeros)
        if not valido_numeros:
            return jsonify({'erro': msg_numeros}), 400
        
        if csv_handler.salvar_dados(id_val, data_val, numeros):
            return jsonify({'sucesso': True, 'mensagem': 'Dados salvos com sucesso!'})
        else:
            return jsonify({'erro': 'Erro ao salvar dados'}), 500
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
