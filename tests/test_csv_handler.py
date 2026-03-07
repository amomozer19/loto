"""Testes para o módulo csv_handler"""
import pytest
import os
import tempfile
import csv
from app.utils.csv_handler import CSVHandler


class TestCSVHandlerBasico:
    """Testes básicos do CSVHandler"""
    
    def test_inicializacao(self):
        """Testa inicialização do CSVHandler"""
        handler = CSVHandler('dados.csv')
        assert handler.filepath == 'dados.csv'
    
    def test_arquivo_nao_existe(self):
        """Testa carregamento quando arquivo não existe"""
        handler = CSVHandler('/tmp/nao_existe_12345.csv')
        dados = handler.carregar_dados()
        assert dados == []
        assert isinstance(dados, list)


class TestCarregarDados:
    """Testes para carregamento de dados"""
    
    def test_carregar_dados_validos(self, csv_test_file):
        """Testa carregamento de dados válidos"""
        handler = CSVHandler(str(csv_test_file))
        dados = handler.carregar_dados()
        
        assert len(dados) == 2
        assert dados[0]['ID'] == '1'
        assert dados[0]['Data'] == '01/01/2026'
        assert dados[1]['ID'] == '2'
    
    def test_dados_estrutura(self, csv_test_file):
        """Testa estrutura dos dados carregados"""
        handler = CSVHandler(str(csv_test_file))
        dados = handler.carregar_dados()
        
        # Verificar campos principais
        assert 'ID' in dados[0]
        assert 'Data' in dados[0]
        assert 'Bola1' in dados[0]
        assert 'Bola15' in dados[0]
    
    def test_carregar_arquivo_vazio(self):
        """Testa carregamento de arquivo vazio"""
        # Criar arquivo CSV vazio
        _, temp_file = tempfile.mkstemp(suffix='.csv')
        
        try:
            with open(temp_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['ID', 'Data'])
            
            handler = CSVHandler(temp_file)
            dados = handler.carregar_dados()
            assert len(dados) == 0
        finally:
            os.unlink(temp_file)


class TestSalvarDados:
    """Testes para salvamento de dados"""
    
    def test_salvar_novo_arquivo(self):
        """Testa salvamento em arquivo novo"""
        _, temp_file = tempfile.mkstemp(suffix='.csv')
        os.unlink(temp_file)  # Remover arquivo antes do teste
        
        handler = CSVHandler(temp_file)
        numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
                   '11', '12', '13', '14', '15']
        
        resultado = handler.salvar_dados('1', '03/03/2026', numeros)
        
        assert resultado is True
        assert os.path.exists(temp_file)
        
        # Verificar conteúdo
        with open(temp_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            dados = list(reader)
            assert len(dados) == 1
            assert dados[0]['ID'] == '1'
            assert dados[0]['Data'] == '03/03/2026'
        
        os.unlink(temp_file)
    
    def test_salvar_arquivo_existente(self):
        """Testa salvamento em arquivo existente"""
        _, temp_file = tempfile.mkstemp(suffix='.csv')
        
        try:
            # Criar arquivo com dados iniciais
            with open(temp_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['ID', 'Data'] + [f'Bola{i}' for i in range(1, 16)])
                writer.writerow(['1', '01/01/2026'] + list(range(1, 16)))
            
            # Salvar novo dado
            handler = CSVHandler(temp_file)
            numeros = [str(i) for i in range(11, 26)]
            resultado = handler.salvar_dados('2', '02/02/2026', numeros)
            
            assert resultado is True
            
            # Verificar conteúdo
            dados = handler.carregar_dados()
            assert len(dados) == 2
            assert dados[1]['ID'] == '2'
        finally:
            os.unlink(temp_file)
    
    def test_salvar_com_erro(self):
        """Testa salvamento com caminho inválido"""
        handler = CSVHandler('/caminho/invalido/nao_existe/dados.csv')
        numeros = [str(i) for i in range(1, 16)]
        
        resultado = handler.salvar_dados('1', '03/03/2026', numeros)
        assert resultado is False


class TestProximoID:
    """Testes para cálculo do próximo ID"""
    
    def test_proximo_id_vazio(self):
        """Testa próximo ID em arquivo vazio"""
        handle = CSVHandler('/tmp/nao_existe_proximo_id.csv')
        proximo = handle.obter_proximo_id()
        assert proximo == 1
    
    def test_proximo_id_com_dados(self, csv_test_file):
        """Testa próximo ID com dados existentes"""
        handler = CSVHandler(str(csv_test_file))
        proximo = handler.obter_proximo_id()
        assert proximo == 3  # Dados vão até ID 2
    
    def test_proximo_id_sequencial(self):
        """Testa se próximo ID é sempre maior"""
        _, temp_file = tempfile.mkstemp(suffix='.csv')
        
        try:
            handler = CSVHandler(temp_file)
            
            # Salvar vários dados
            for i in range(1, 5):
                numeros = [str(j) for j in range(1, 16)]
                handler.salvar_dados(str(i), '01/01/2026', numeros)
            
            # Verificar próximo ID
            proximo = handler.obter_proximo_id()
            assert proximo == 5
        finally:
            os.unlink(temp_file)


class TestUltimaData:
    """Testes para obtenção da última data"""
    
    def test_ultima_data_vazio(self):
        """Testa última data em arquivo vazio"""
        handler = CSVHandler('/tmp/nao_existe_ultima_data.csv')
        data = handler.obter_ultima_data()
        assert data == ''
    
    def test_ultima_data_com_dados(self, csv_test_file):
        """Testa última data com dados"""
        handler = CSVHandler(str(csv_test_file))
        data = handler.obter_ultima_data()
        assert data == '02/01/2026'


class TestIntegracao:
    """Testes de integração do CSVHandler"""
    
    def test_fluxo_completo(self):
        """Testa fluxo completo: criar, salvar, carregar"""
        _, temp_file = tempfile.mkstemp(suffix='.csv')
        os.unlink(temp_file)
        
        try:
            handler = CSVHandler(temp_file)
            
            # Obter próximo ID
            id1 = handler.obter_proximo_id()
            assert id1 == 1
            
            # Salvar primeiro dado
            numeros1 = [str(i) for i in range(1, 16)]
            handler.salvar_dados(str(id1), '01/03/2026', numeros1)
            
            # Obter próximo ID
            id2 = handler.obter_proximo_id()
            assert id2 == 2
            
            # Salvar segundo dado
            numeros2 = [str(i) for i in range(11, 26)]
            handler.salvar_dados(str(id2), '02/03/2026', numeros2)
            
            # Carregar e verificar
            dados = handler.carregar_dados()
            assert len(dados) == 2
            assert dados[0]['ID'] == '1'
            assert dados[1]['ID'] == '2'
            assert handler.obter_ultima_data() == '02/03/2026'
        finally:
            os.unlink(temp_file)
