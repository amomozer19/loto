"""Testes para o módulo stats_calculator"""
import pytest
from app.utils.stats_calculator import StatsCalculator


class TestCalcularEstatisticasGlobais:
    """Testes para estatísticas globais"""
    
    def test_dados_vazios(self):
        """Testa cálculo com dados vazios"""
        stats = StatsCalculator.calcular_estatisticas_globais([])
        
        assert stats['total_sorteios'] == 0
        assert stats['data_primeira'] == 'N/A'
        assert stats['data_ultima'] == 'N/A'
        assert stats['numero_mais_frequente'] == 0
        assert stats['numero_menos_frequente'] == 0
    
    def test_um_sorteio(self):
        """Testa cálculo com um sorteio"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_globais(dados)
        
        assert stats['total_sorteios'] == 1
        assert stats['data_primeira'] == '01/01/2026'
        assert stats['data_ultima'] == '01/01/2026'
        assert stats['total_numeros_unicos'] == 15
    
    def test_multiplos_sorteios(self):
        """Testa cálculo com múltiplos sorteios"""
        dados = [
            {
                'ID': '1',
                'Data': '01/01/2026',
                **{f'Bola{i}': str(i) for i in range(1, 16)}
            },
            {
                'ID': '2',
                'Data': '02/01/2026',
                **{f'Bola{i}': str(i + 5) for i in range(1, 16)}
            }
        ]
        
        stats = StatsCalculator.calcular_estatisticas_globais(dados)
        
        assert stats['total_sorteios'] == 2
        assert stats['data_primeira'] == '01/01/2026'
        assert stats['data_ultima'] == '02/01/2026'
    
    def test_numeros_mais_jogados(self):
        """Testa se números mais frequentes são identificados"""
        dados = [
            {
                'ID': '1',
                'Data': '01/01/2026',
                'Bola1': '1', 'Bola2': '1', 'Bola3': '1', 'Bola4': '2', 'Bola5': '2',
                'Bola6': '3', 'Bola7': '4', 'Bola8': '5', 'Bola9': '6',
                'Bola10': '7', 'Bola11': '8', 'Bola12': '9', 'Bola13': '10',
                'Bola14': '11', 'Bola15': '12'
            }
        ]
        
        stats = StatsCalculator.calcular_estatisticas_globais(dados)
        
        assert len(stats['numeros_mais_jogados']) > 0
        # O número 1 deve estar entre os tops (aparece 3 vezes)
        numeros_top = [num for num, freq in stats['numeros_mais_jogados']]
        assert 1 in numeros_top


class TestCalcularEstatisticasPorDia:
    """Testes para estatísticas por dia da semana"""
    
    def test_dados_vazios(self):
        """Testa cálculo com dados vazios"""
        stats =StatsCalculator.calcular_estatisticas_por_dia([])
        
        assert len(stats) == 7  # 7 dias da semana
        for dia_stat in stats:
            assert dia_stat['sorteios'] == 0
            assert dia_stat['numeros_mais_jogados'] == []
    
    def test_um_sorteio(self):
        """Testa cálculo com um sorteio"""
        dados = [{
            'ID': '1',
            'Data': '03/03/2026',  # Segunda-feira
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        
        # Verificar se pelo menos um dia tem dados
        dias_com_sorteios = [s for s in stats if s['sorteios'] > 0]
        assert len(dias_com_sorteios) >= 1
    
    def test_estrutura_stats(self):
        """Testa estrutura das estatísticas de um dia"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        
        # Dia com dados
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        assert 'id' in dia_com_dados
        assert 'nome' in dia_com_dados
        assert 'sorteios' in dia_com_dados
        assert 'media' in dia_com_dados
        assert 'mediana' in dia_com_dados
        assert 'desvio_padrao' in dia_com_dados
        assert 'minimo' in dia_com_dados
        assert 'maximo' in dia_com_dados
        assert 'media_ponderada' in dia_com_dados
        assert 'numeros_mais_jogados' in dia_com_dados
        assert 'probabilidades' in dia_com_dados
        assert 'numeros_nao_sorteados' in dia_com_dados
    
    def test_numeros_nao_sorteados(self):
        """Testa identificação de números não sorteados"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}  # 1-15
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        # Números 16-25 não foram sorteados
        assert set(dia_com_dados['numeros_nao_sorteados']) == set(range(16, 26))
    
    def test_probabilidades(self):
        """Testa cálculo de probabilidades"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        probs = dia_com_dados['probabilidades']
        
        # Números 1-15 têm probabilidade > 0
        for num in range(1, 16):
            assert probs[num] > 0
        
        # Números 16-25 têm probabilidade = 0
        for num in range(16, 26):
            assert probs[num] == 0
    
    def test_media_minimo_maximo(self):
        """Testa cálculo de média, mínimo e máximo"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}  # 1-15
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        assert dia_com_dados['minimo'] == 1
        assert dia_com_dados['maximo'] == 15
        assert dia_com_dados['media'] == 8  # Média de 1-15 é 8


class TestStatisticsCorretness:
    """Testes para validar corretude das estatísticas"""
    
    def test_media_ponderada_valida(self):
        """Testa se média ponderada é um valor válido"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        # Média ponderada deve estar entre 1 e 25
        assert 1 <= dia_com_dados['media_ponderada'] <= 25
    
    def test_desvio_padrao_valido(self):
        """Testa se desvio padrão é válido"""
        dados = [{
            'ID': '1',
            'Data': '01/01/2026',
            **{f'Bola{i}': str(i) for i in range(1, 16)}
        }]
        
        stats = StatsCalculator.calcular_estatisticas_por_dia(dados)
        dia_com_dados = next(s for s in stats if s['sorteios'] > 0)
        
        # Desvio padrão deve ser >= 0
        assert dia_com_dados['desvio_padrao'] >= 0


class TestIntegracaoEstatisticas:
    """Testes de integração das estatísticas"""
    
    def test_consistencia_global_vs_dias(self):
        """Testa consistência entre estadísticas globais e por dia"""
        dados = [
            {
                'ID': '1',
                'Data': '01/01/2026',
                **{f'Bola{i}': str(i) for i in range(1, 16)}
            },
            {
                'ID': '2',
                'Data': '02/01/2026',
                **{f'Bola{i}': str(i + 5) for i in range(1, 16)}
            }
        ]
        
        stats_globais = StatsCalculator.calcular_estatisticas_globais(dados)
        stats_dias = StatsCalculator.calcular_estatisticas_por_dia(dados)
        
        # Total de sorteios deve ser 2
        assert stats_globais['total_sorteios'] == 2
        
        # Sum de sorteios por dia deve ser 2
        total_dias = sum(s['sorteios'] for s in stats_dias)
        assert total_dias == 2
