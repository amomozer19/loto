"""Analisador de sorte - Analisa 7 números fornecidos pelo usuário"""
from typing import List, Dict, Tuple
from collections import Counter
from itertools import combinations
from app.utils.csv_handler import CSVHandler
from app.utils.stats_calculator import StatsCalculator


class SorteAnalyzer:
    """Analisa combinações e potencial de 7 números fornecidos pelo usuário"""
    
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.stats_calc = StatsCalculator()
        self.dados = self.csv_handler.carregar_dados()
    
    def analisar_numeros(self, numeros: List[int]) -> Dict:
        """
        Análise completa dos 7 números fornecidos pelo usuário
        
        Args:
            numeros: Lista com 7 números (1-25)
        
        Returns:
            Dict com análise detalhada
        """
        if not numeros or len(numeros) != 7:
            return {'erro': 'Forneça exatamente 7 números'}
        
        # Extrai estatísticas históricas
        frequencias = self._extrair_frequencias()
        
        analise = {
            'numeros_entrada': numeros,
            'analise_numeros': self._analisar_cada_numero(numeros, frequencias),
            'score_geral': 0,
            'numeros_mais_jogados': self._identificar_padroes(numeros, frequencias, 'mais'),
            'numeros_azaroes': self._identificar_padroes(numeros, frequencias, 'menos'),
            'tuplas_recomendadas': self._analisar_duplas(numeros, frequencias),
            'tripletas_recomendadas': self._analisar_tripletas(numeros, frequencias),
            'recomendacoes': []
        }
        
        # Calcula score geral
        analise['score_geral'] = self._calcular_score_geral(analise)
        
        # Gera recomendações
        analise['recomendacoes'] = self._gerar_recomendacoes(analise, frequencias)
        
        return analise
    
    def _extrair_frequencias(self) -> Dict[int, int]:
        """
        Extrai frequência de cada número do histórico
        
        Returns:
            Dict com {numero: frequencia}
        """
        todas_numeros = []
        
        for dado in self.dados:
            for i in range(1, 16):
                chave = f'Bola{i}'
                if chave in dado:
                    todas_numeros.append(int(dado[chave]))
        
        return dict(Counter(todas_numeros))
    
    def _analisar_cada_numero(self, numeros: List[int], frequencias: Dict[int, int]) -> List[Dict]:
        """
        Analisa cada número individualmente
        
        Args:
            numeros: Lista de 7 números
            frequencias: Dicionário de frequências
        
        Returns:
            Lista com análise de cada número
        """
        analise_nums = []
        freq_max = max(frequencias.values()) if frequencias else 1
        
        for num in sorted(numeros):
            freq = frequencias.get(num, 0)
            percentual = (freq / len(self.dados) / 15 * 100) if self.dados else 0
            
            analise_nums.append({
                'numero': num,
                'frequencia': freq,
                'percentual': round(percentual, 2),
                'tendencia': 'Alta' if freq > freq_max * 0.7 else 'Média' if freq > freq_max * 0.4 else 'Baixa',
                'chance_relativa': round((freq / freq_max * 100), 1) if freq_max > 0 else 0
            })
        
        return sorted(analise_nums, key=lambda x: x['frequencia'], reverse=True)
    
    def _identificar_padroes(self, numeros: List[int], frequencias: Dict[int, int], tipo: str) -> List[Dict]:
        """
        Identifica se os números estão entre os mais ou menos jogados
        
        Args:
            numeros: Lista de 7 números
            frequencias: Dicionário de frequências
            tipo: 'mais' ou 'menos'
        
        Returns:
            Lista com análise de padrões
        """
        # Top 8 números mais jogados
        top_8 = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)[:8]
        top_8_nums = [num for num, _ in top_8]
        
        # Bottom 8 números menos jogados
        bottom_8 = sorted(frequencias.items(), key=lambda x: x[1])[:8]
        bottom_8_nums = [num for num, _ in bottom_8]
        
        if tipo == 'mais':
            resultado = []
            for num in numeros:
                if num in top_8_nums:
                    freq = frequencias[num]
                    resultado.append({
                        'numero': num,
                        'frequencia': freq,
                        'em_top_8': True,
                        'posicao_top': top_8_nums.index(num) + 1
                    })
            return sorted(resultado, key=lambda x: x['frequencia'], reverse=True)
        
        else:  # menos
            resultado = []
            for num in numeros:
                if num in bottom_8_nums:
                    freq = frequencias[num]
                    resultado.append({
                        'numero': num,
                        'frequencia': freq,
                        'em_bottom_8': True,
                        'posicao_bottom': bottom_8_nums.index(num) + 1
                    })
            return sorted(resultado, key=lambda x: x['frequencia'])
    
    def _analisar_duplas(self, numeros: List[int], frequencias: Dict[int, int]) -> List[Dict]:
        """
        Analisa as melhores duplas (tuplas) entre os 7 números
        
        Args:
            numeros: Lista de 7 números
            frequencias: Dicionário de frequências
        
        Returns:
            Lista com análise de duplas
        """
        duplas_historicas = self._extrair_duplas_historicas()
        duplas_usuario = list(combinations(numeros, 2))
        
        duplas_analise = []
        
        for dupla in duplas_usuario:
            freq_historica = duplas_historicas.get(dupla, 0)
            freq_num1 = frequencias.get(dupla[0], 0)
            freq_num2 = frequencias.get(dupla[1], 0)
            
            # Score da dupla baseado na frequência histórica e frequência individual
            score = (freq_historica * 1.5) + (freq_num1 * 0.25) + (freq_num2 * 0.25)
            
            duplas_analise.append({
                'numeros': list(dupla),
                'frequencia_historica': freq_historica,
                'freq_num1': freq_num1,
                'freq_num2': freq_num2,
                'score': round(score, 2),
                'potencial': 'Alto' if score > 20 else 'Médio' if score > 10 else 'Baixo'
            })
        
        return sorted(duplas_analise, key=lambda x: x['score'], reverse=True)[:5]
    
    def _analisar_tripletas(self, numeros: List[int], frequencias: Dict[int, int]) -> List[Dict]:
        """
        Analisa as melhores tripletas entre os 7 números
        
        Args:
            numeros: Lista de 7 números
            frequencias: Dicionário de frequências
        
        Returns:
            Lista com análise de tripletas
        """
        tripletas_historicas = self._extrair_tripletas_historicas()
        tripletas_usuario = list(combinations(numeros, 3))
        
        tripletas_analise = []
        
        for tripleta in tripletas_usuario:
            freq_historica = tripletas_historicas.get(tripleta, 0)
            freq_nums = sum(frequencias.get(num, 0) for num in tripleta) / 3
            
            # Score da tripleta
            score = (freq_historica * 2) + (freq_nums * 0.3)
            
            tripletas_analise.append({
                'numeros': list(tripleta),
                'frequencia_historica': freq_historica,
                'freq_media': round(freq_nums, 2),
                'score': round(score, 2),
                'potencial': 'Alto' if score > 25 else 'Médio' if score > 12 else 'Baixo'
            })
        
        return sorted(tripletas_analise, key=lambda x: x['score'], reverse=True)[:5]
    
    def _extrair_duplas_historicas(self) -> Dict[Tuple, int]:
        """
        Extrai frequência de todas as duplas que saíram historicamente
        
        Returns:
            Dict com {(num1, num2): frequencia}
        """
        duplas_contador = Counter()
        
        for dado in self.dados:
            numeros = []
            for i in range(1, 16):
                chave = f'Bola{i}'
                if chave in dado:
                    numeros.append(int(dado[chave]))
            
            # Extrai todas as duplas deste sorteio
            duplas = list(combinations(sorted(numeros), 2))
            duplas_contador.update(duplas)
        
        return dict(duplas_contador)
    
    def _extrair_tripletas_historicas(self) -> Dict[Tuple, int]:
        """
        Extrai frequência de todas as tripletas que saíram historicamente
        
        Returns:
            Dict com {(num1, num2, num3): frequencia}
        """
        tripletas_contador = Counter()
        
        for dado in self.dados:
            numeros = []
            for i in range(1, 16):
                chave = f'Bola{i}'
                if chave in dado:
                    numeros.append(int(dado[chave]))
            
            # Extrai todas as tripletas deste sorteio
            tripletas = list(combinations(sorted(numeros), 3))
            tripletas_contador.update(tripletas)
        
        return dict(tripletas_contador)
    
    def _calcular_score_geral(self, analise: Dict) -> float:
        """
        Calcula um score geral baseado na análise
        
        Args:
            analise: Dict com análise completa
        
        Returns:
            Score geral (0-100)
        """
        score = 50  # Base
        
        # Bônus por números mais jogados
        score += len(analise['numeros_mais_jogados']) * 5
        
        # Penalidade por números azarões
        score -= len(analise['numeros_azaroes']) * 2
        
        # Bônus por tuplas de alto potencial
        tuplas_altos = [t for t in analise['tuplas_recomendadas'] if t['potencial'] == 'Alto']
        score += len(tuplas_altos) * 3
        
        # Bônus por tripletas de alto potencial
        tripletas_altos = [t for t in analise['tripletas_recomendadas'] if t['potencial'] == 'Alto']
        score += len(tripletas_altos) * 5
        
        return round(min(100, max(0, score)), 2)
    
    def _gerar_recomendacoes(self, analise: Dict, frequencias: Dict[int, int]) -> List[str]:
        """
        Gera recomendações baseado na análise
        
        Args:
            analise: Dict com análise completa
            frequencias: Dicionário de frequências
        
        Returns:
            Lista com recomendações em texto
        """
        recomendacoes = []
        
        # Recomendação sobre números mais jogados
        nums_mais = analise['numeros_mais_jogados']
        if len(nums_mais) >= 5:
            recomendacoes.append(f"✨ Excelente! Você tem {len(nums_mais)} números entre os TOP 8 mais sorteados. Muito prometedor!")
        elif len(nums_mais) >= 3:
            recomendacoes.append(f"👍 Bom! Você tem {len(nums_mais)} números entre os mais sorteados historicamente.")
        else:
            recomendacoes.append(f"⚠️  Cuidado: Apenas {len(nums_mais)} números estão entre os top sorteados.")
        
        # Recomendação sobre números azarões
        nums_azaroes = analise['numeros_azaroes']
        if nums_azaroes:
            recomendacoes.append(f"🎲 Você incluiu {len(nums_azaroes)} números azarões (menos sorteados). Isto pode ser arriscado!")
        else:
            recomendacoes.append("✅ Nenhum número muito improvável na sua seleção.")
        
        # Recomendação sobre tuplas
        tuplas = analise['tuplas_recomendadas']
        tupla_top = tuplas[0] if tuplas else None
        if tupla_top and tupla_top['score'] > 20:
            recomendacoes.append(f"🔥 A dupla {tupla_top['numeros']} tem excelente potencial (score: {tupla_top['score']})")
        
        # Recomendação sobre tripletas
        tripletas = analise['tripletas_recomendadas']
        tripleta_top = tripletas[0] if tripletas else None
        if tripleta_top and tripleta_top['score'] > 25:
            recomendacoes.append(f"🌟 A tripleta {tripleta_top['numeros']} tem altíssimo potencial (score: {tripleta_top['score']})")
        
        # Score geral
        score = analise['score_geral']
        if score >= 75:
            recomendacoes.append(f"🎯 SCORE GERAL: {score}/100 - Combinação MUITO PROMISSORA!")
        elif score >= 60:
            recomendacoes.append(f"👉 SCORE GERAL: {score}/100 - Combinação PROMISSORA!")
        elif score >= 40:
            recomendacoes.append(f"🎪 SCORE GERAL: {score}/100 - Combinação EQUILIBRADA!")
        else:
            recomendacoes.append(f"⚡ SCORE GERAL: {score}/100 - Combinação COM RISCO! Considere revisar.")
        
        return recomendacoes
