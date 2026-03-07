"""Analisador de apostas com retroalimentação para melhorar futuras previsões"""
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import Counter
from app.utils.aposta_manager import ApostaManager
from app.utils.csv_handler import CSVHandler

class BettingAnalyzer:
    """Analisa apostas vs resultados reais e fornece retroalimentação"""
    
    def __init__(self):
        self.aposta_mgr = ApostaManager()
        self.csv_handler = CSVHandler()
    
    def sincronizar_resultados(self, dados_csv: List[Dict]) -> Dict:
        """
        Sincroniza resultados reais (CSV) com apostas predichas (JSON)
        Confronta as apostas com os sorteios realizados
        
        Args:
            dados_csv: Dados históricos do CSV
        
        Returns:
            Dict com estatísticas de acertos
        """
        stats = {
            'apostas_processadas': 0,
            'apostas_com_resultado': 0,
            'acertos_por_tipo': {},
            'apostas_detalhes': []
        }
        
        apostas_historico = self.aposta_mgr.obter_todas_apostas()
        
        for aposta_dia in apostas_historico:
            data_aposta = aposta_dia.get('data')
            if not data_aposta or aposta_dia.get('resultado_sorteio'):
                continue
            
            # Busca resultado no CSV
            resultado = self._buscar_sorteio_por_data(dados_csv, data_aposta)
            
            if resultado:
                numeros_sorteio = resultado
                self.aposta_mgr.registrar_resultado(
                    datetime.fromisoformat(data_aposta),
                    numeros_sorteio
                )
                
                # Analisa acertos
                analise = self._analisar_acertos(
                    aposta_dia['apostas'],
                    numeros_sorteio,
                    data_aposta
                )
                
                aposta_dia['analise'] = analise
                stats['apostas_com_resultado'] += 1
                stats['apostas_detalhes'].append({
                    'data': data_aposta,
                    'analise': analise
                })
                
                # Atualiza estatísticas por tipo
                for tipo, acertos in analise['acertos_por_aposta'].items():
                    if tipo not in stats['acertos_por_tipo']:
                        stats['acertos_por_tipo'][tipo] = []
                    stats['acertos_por_tipo'][tipo].append(acertos)
            
            stats['apostas_processadas'] += 1
        
        return stats
    
    def _buscar_sorteio_por_data(self, dados_csv: List[Dict], data_str: str) -> List[int]:
        """
        Busca o sorteio em um arquivo CSV pela data
        
        Args:
            dados_csv: Dados do CSV
            data_str: Data em formato YYYY-MM-DD
        
        Returns:
            Lista com 15 números or None
        """
        try:
            # Converte data_str (YYYY-MM-DD) para comparação
            for linha in dados_csv:
                data_csv = linha.get('Data', '')
                
                # Tenta diferentes formatos de data no CSV
                try:
                    if data_csv.replace('/', '-') == data_str or data_csv == data_str:
                        numeros = []
                        for i in range(1, 16):
                            chave = f'Bola{i}'
                            if chave in linha:
                                numeros.append(int(linha[chave]))
                        
                        if len(numeros) == 15:
                            return numeros
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Erro ao buscar sorteio: {e}")
            return None
    
    def _analisar_acertos(self, apostas: List[Dict], numeros_sorteio: List[int], 
                          data: str) -> Dict:
        """
        Analisa quanto cada aposta acertou
        
        Args:
            apostas: Lista de apostas do dia
            numeros_sorteio: Números que saíram
            data: Data do sorteio
        
        Returns:
            Dict com estatísticas de acertos
        """
        analise = {
            'data': data,
            'numeros_sorteio': numeros_sorteio,
            'acertos_por_aposta': {},
            'melhor_aposta': None,
            'pior_aposta': None,
            'media_acertos': 0
        }
        
        melhor_score = -1
        pior_score = float('inf')
        scores = []
        
        for aposta in apostas:
            nome = aposta.get('nome', 'Desconhecida')
            numeros_aposta = aposta.get('numeros', [])
            
            # Calcula acertos
            acertos = set(numeros_aposta) & set(numeros_sorteio)
            qtd_acertos = len(acertos)
            
            # Calcula tuplas e tripletas acertadas
            tuplas_acertadas = self._contar_padroes(numeros_sorteio, numeros_aposta, 2)
            tripletas_acertadas = self._contar_padroes(numeros_sorteio, numeros_aposta, 3)
            
            score = (qtd_acertos * 10) + (tuplas_acertadas * 5) + (tripletas_acertadas * 15)
            
            analise['acertos_por_aposta'][nome] = {
                'numeros_acertos': qtd_acertos,
                'numeros_sorteados': list(acertos),
                'tuplas_acertadas': tuplas_acertadas,
                'tripletas_acertadas': tripletas_acertadas,
                'score': score
            }
            
            scores.append(score)
            
            if score > melhor_score:
                melhor_score = score
                analise['melhor_aposta'] = nome
            
            if score < pior_score:
                pior_score = score
                analise['pior_aposta'] = nome
        
        analise['media_acertos'] = sum(scores) / len(scores) if scores else 0
        
        return analise
    
    def _contar_padroes(self, numeros_sorteio: List[int], numeros_aposta: List[int], 
                        tamanho: int) -> int:
        """
        Conta quantos padrões de N números aparecem em ambos
        
        Args:
            numeros_sorteio: Números que saíram
            numeros_aposta: Números da aposta
            tamanho: Tamanho do padrão (2 para duplas, 3 para tripletas)
        
        Returns:
            Quantidade de padrões acertados
        """
        from itertools import combinations
        
        padroes_sorteio = set(combinations(sorted(numeros_sorteio), tamanho))
        padroes_aposta = set(combinations(sorted(numeros_aposta), tamanho))
        
        return len(padroes_sorteio & padroes_aposta)
    
    def gerar_feedback_para_futuras_apostas(self) -> Dict:
        """
        Analisa histórico de acertos e gera feedback para melhorar futuras apostas
        
        Returns:
            Dict com insights e recomendações
        """
        apostas_historico = self.aposta_mgr.obter_historico(dias=90)
        
        feedback = {
            'periodo_analise': '90 dias',
            'apostas_analisadas': 0,
            'numeros_mais_acertados': [],
            'numeros_menos_acertados': [],
            'tipos_aposta_performance': {},
            'tuplas_mais_frequentes': [],
            'tripletas_mais_frequentes': [],
            'recomendacoes': []
        }
        
        contador_numeros_acertados = Counter()
        contador_numeros_nao_acertados = Counter()
        contador_tuplas_acertadas = Counter()
        contador_tripletas_acertadas = Counter()
        performance_tipo = {}
        
        for aposta_dia in apostas_historico:
            if not aposta_dia.get('analise'):
                continue
            
            feedback['apostas_analisadas'] += 1
            analise = aposta_dia['analise']
            
            # Coleta números acertados
            for nome_aposta, stats in analise['acertos_por_aposta'].items():
                for num in stats.get('numeros_sorteados', []):
                    contador_numeros_acertados[num] += 1
                
                # Coleta performance por tipo
                if nome_aposta not in performance_tipo:
                    performance_tipo[nome_aposta] = []
                performance_tipo[nome_aposta].append(stats['score'])
        
        # Top 10 números mais acertados
        feedback['numeros_mais_acertados'] = [
            {'numero': num, 'frequencia': freq}
            for num, freq in contador_numeros_acertados.most_common(10)
        ]
        
        # Top 10 números menos acertados (que aparecem nas apostas mas não saem)
        todos_numeros = set(range(1, 26))
        numeros_sorteados = {num for num in contador_numeros_acertados.keys()}
        numeros_raros = todos_numeros - numeros_sorteados
        
        # Performance média por tipo de aposta
        for tipo, scores in performance_tipo.items():
            if scores:
                feedback['tipos_aposta_performance'][tipo] = {
                    'score_medio': sum(scores) / len(scores),
                    'melhor_score': max(scores),
                    'pior_score': min(scores),
                    'consistencia': self._calcular_consistencia(scores)
                }
        
        # Gera recomendações
        feedback['recomendacoes'] = self._gerar_recomendacoes(feedback, performance_tipo)
        
        return feedback
    
    def _calcular_consistencia(self, scores: List[float]) -> str:
        """Calcula a consistência de uma estratégia baseada nos scores"""
        if not scores:
            return 'N/A'
        
        media = sum(scores) / len(scores)
        variancia = sum((x - media) ** 2 for x in scores) / len(scores)
        
        if variancia < 10:
            return 'Muito consistente'
        elif variancia < 50:
            return 'Consistente'
        elif variancia < 100:
            return 'Moderadamente consistente'
        else:
            return 'Pouco consistente'
    
    def _gerar_recomendacoes(self, feedback: Dict, performance_tipo: Dict) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recomendacoes = []
        
        if not feedback['apostas_analisadas']:
            return ['Dados insuficientes para análise']
        
        # Melhor tipo de aposta
        if performance_tipo:
            melhor_tipo = max(performance_tipo.items(), 
                            key=lambda x: x[1].get('score_medio', 0))
            recomendacoes.append(
                f"Foco maior em '{melhor_tipo[0]}' (melhor performance)"
            )
        
        # Números mais frequentes
        if feedback['numeros_mais_acertados']:
            top_3 = [n['numero'] for n in feedback['numeros_mais_acertados'][:3]]
            recomendacoes.append(
                f"Números com maior histórico de saída: {', '.join(map(str, top_3))}"
            )
        
        # Análise de padrões
        recomendacoes.append(
            "Continue monitorando padrões de duplas e tripletas para identificar tendências"
        )
        
        recomendacoes.append(
            "Atualize o modelo periodicamente com novos dados de sorteios"
        )
        
        return recomendacoes
