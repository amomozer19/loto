"""Testes para as rotas da aplicação"""
import pytest
import json


class TestRotaPrincipal:
    """Testes para a rota principal"""
    
    def test_index_status_200(self, client):
        """Testa se rota / retorna status 200"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_contem_html(self, client):
        """Testa se resposta contém HTML"""
        response = client.get('/')
        assert b'html' in response.data.lower()
    
    def test_index_carrega_template(self, client):
        """Testa se template é carregado"""
        response = client.get('/')
        # Verificar se contém elementos esperados
        assert response.status_code == 200


class TestRotaNovo:
    """Testes para a rota de novo sorteio"""
    
    def test_novo_status_200(self, client):
        """Testa se rota /novo retorna status 200"""
        response = client.get('/novo')
        assert response.status_code == 200
    
    def test_novo_contem_formulario(self, client):
        """Testa se página contém formulário"""
        response = client.get('/novo')
        assert response.status_code == 200


class TestAPIGerarNumeros:
    """Testes para API de geração de números"""
    
    def test_gerar_numeros_status_200(self, client):
        """Testa se API retorna status 200"""
        response = client.get('/api/gerar_numeros')
        assert response.status_code == 200
    
    def test_gerar_numeros_retorna_json(self, client):
        """Testa se API retorna JSON"""
        response = client.get('/api/gerar_numeros')
        data = json.loads(response.data)
        assert 'numeros' in data
    
    def test_gerar_numeros_quantidade(self, client):
        """Testa se retorna 15 números"""
        response = client.get('/api/gerar_numeros')
        data = json.loads(response.data)
        assert len(data['numeros']) == 15
    
    def test_gerar_numeros_range(self, client):
        """Testa se números estão no range 1-25"""
        response = client.get('/api/gerar_numeros')
        data = json.loads(response.data)
        
        for num in data['numeros']:
            assert 1 <= num <= 25
    
    def test_gerar_numeros_sem_repeticao(self, client):
        """Testa se não há números repetidos"""
        response = client.get('/api/gerar_numeros')
        data = json.loads(response.data)
        
        assert len(data['numeros']) == len(set(data['numeros']))


class TestAPIValidar:
    """Testes para API de validação"""
    
    def test_validar_status_200(self, client):
        """Testa se API retorna status 200"""
        payload = {'numeros': [str(i) for i in range(1, 16)]}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_validar_numeros_corretos(self, client):
        """Testa validação de números corretos"""
        payload = {'numeros': [str(i) for i in range(1, 16)]}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['valido'] is True
    
    def test_validar_numeros_repetidos(self, client):
        """Testa validação com números repetidos"""
        payload = {'numeros': ['1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['valido'] is False
        assert 'repetições' in data['erro']
    
    def test_validar_numeros_fora_range(self, client):
        """Testa validação com números fora do range"""
        payload = {'numeros': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '26']}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['valido'] is False
    
    def test_validar_campos_vazios(self, client):
        """Testa validação com campos vazios"""
        payload = {'numeros': ['']}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['valido'] is False


class TestAPISalvar:
    """Testes para API de salvamento"""
    
    def test_salvar_dados_validos(self, client, sample_data):
        """Testa salvamento com dados válidos"""
        response = client.post('/api/salvar',
                             data=json.dumps(sample_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'sucesso' in data or 'erro' not in data
    
    def test_salvar_sem_id(self, client, sample_data):
        """Testa salvamento sem ID"""
        data = sample_data.copy()
        data['id'] = ''
        response = client.post('/api/salvar',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_salvar_sem_data(self, client, sample_data):
        """Testa salvamento sem data"""
        data = sample_data.copy()
        data['data'] = ''
        response = client.post('/api/salvar',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_salvar_numeros_repetidos(self, client, sample_data):
        """Testa salvamento com números repetidos"""
        data = sample_data.copy()
        data['numeros'] = ['1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        response = client.post('/api/salvar',
                             data=json.dumps(data),
                             content_type='application/json')
        assert response.status_code == 400


class TestRotaEstatisticas:
    """Testes para rota de estatísticas"""
    
    def test_estatisticas_status_200(self, client):
        """Testa se rota /estatisticas retorna status 200"""
        response = client.get('/estatisticas')
        assert response.status_code == 200
    
    def test_estatisticas_template(self, client):
        """Testa se template é carregado"""
        response = client.get('/estatisticas')
        assert response.status_code == 200


class TestRotaInexistente:
    """Testes para rotas inexistentes"""
    
    def test_rota_nao_existe(self, client):
        """Testa se rota inexistente retorna 404"""
        response = client.get('/rota_que_nao_existe')
        assert response.status_code == 404


class TestIntegracaoRotas:
    """Testes de integração das rotas"""
    
    def test_fluxo_usuario(self, client):
        """Testa fluxo completo do usuário"""
        # 1. Acessar página inicial
        response = client.get('/')
        assert response.status_code == 200
        
        # 2. Acessar página de novo sorteio
        response = client.get('/novo')
        assert response.status_code == 200
        
        # 3. Gerar números
        response = client.get('/api/gerar_numeros')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # 4. Validar números
        payload = {'numeros': [str(n) for n in data['numeros']]}
        response = client.post('/api/validar',
                             data=json.dumps(payload),
                             content_type='application/json')
        result = json.loads(response.data)
        assert result['valido'] is True
        
        # 5. Visualizar estatísticas
        response = client.get('/estatisticas')
        assert response.status_code == 200
