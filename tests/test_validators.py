"""Testes para o módulo validators"""
import pytest
from app.utils.validators import SorteioValidator


class TestValidarNumeros:
    """Testes para validação de números"""
    
    def test_numeros_validos(self):
        """Testa validação com números válidos"""
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                   '11', '12', '13', '14', '15']
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is True
        assert msg == 'Válido'
    
    def test_numeros_fora_range(self):
        """Testa se números fora do range são rejeitados"""
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                   '11', '12', '13', '14', '26']  # 26 é inválido
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is False
        assert 'entre 1 e 25' in msg
    
    def test_numeros_repetidos(self):
        """Testa se números repetidos são rejeitados"""
        numeros = ['1', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                   '10', '11', '12', '13', '14']  # 1 repetido
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is False
        assert 'repetições' in msg
    
    def test_numeros_vazio(self):
        """Testa se campos vazios são rejeitados"""
        numeros = ['1', '', '3', '4', '5', '6', '7', '8', '9', '10',
                   '11', '12', '13', '14', '15']
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is False
        assert 'vazio' in msg
    
    def test_numeros_nao_inteiros(self):
        """Testa se valores não inteiros são rejeitados"""
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                   '11', 'abc', '13', '14', '15']
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is False
        assert 'inteiro' in msg
    
    def test_quantidade_incorreta(self):
        """Testa se quantidade incorreta de números é rejeitada"""
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # Apenas 10
        valido, msg = SorteioValidator.validar_numeros(numeros)
        assert valido is False
        assert '15' in msg


class TestValidarID:
    """Testes para validação de ID"""
    
    def test_id_valido(self):
        """Testa ID válido"""
        valido, msg = SorteioValidator.validar_id('2874')
        assert valido is True
        assert msg == 'Válido'
    
    def test_id_vazio(self):
        """Testa ID vazio"""
        valido, msg = SorteioValidator.validar_id('')
        assert valido is False
        assert 'vazio' in msg
    
    def test_id_spaces(self):
        """Testa ID com apenas espaços"""
        valido, msg = SorteioValidator.validar_id('   ')
        assert valido is False
        assert 'vazio' in msg


class TestValidarData:
    """Testes para validação de data"""
    
    def test_data_valida(self):
        """Testa data válida"""
        valido, msg = SorteioValidator.validar_data('03/03/2026')
        assert valido is True
        assert msg == 'Válido'
    
    def test_data_vazia(self):
        """Testa data vazia"""
        valido, msg = SorteioValidator.validar_data('')
        assert valido is False
        assert 'vazio' in msg
    
    def test_data_spaces(self):
        """Testa data com apenas espaços"""
        valido, msg = SorteioValidator.validar_data('   ')
        assert valido is False
        assert 'vazio' in msg


class TestValidacaoCompleta:
    """Testes de validação completa"""
    
    def test_dados_completamente_validos(self, sample_data):
        """Testa validação com todos os dados válidos"""
        validar_id = SorteioValidator.validar_id(sample_data['id'])
        validar_data = SorteioValidator.validar_data(sample_data['data'])
        validar_numeros = SorteioValidator.validar_numeros(sample_data['numeros'])
        
        assert validar_id[0] is True
        assert validar_data[0] is True
        assert validar_numeros[0] is True
    
    def test_dados_completamente_invalidos(self, invalid_data):
        """Testa validação com dados inválidos"""
        validar_id = SorteioValidator.validar_id(invalid_data['id'])
        validar_numeros = SorteioValidator.validar_numeros(invalid_data['numeros'])
        
        assert validar_id[0] is False
        assert validar_numeros[0] is False
