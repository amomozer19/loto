"""Calculadora de estatísticas"""
from typing import List, Dict
from collections import Counter
import statistics
from datetime import datetime

class StatsCalculator:
    """Calcula estatísticas de sorteios"""
    
    @staticmethod
    def calcular_estatisticas_por_dia(dados: List[Dict]) -> List[Dict]:
        """Calcula estatísticas por dia da semana"""
        
        dias_semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        
        stats_por_dia = {
            0: {'nome': 'Domingo', 'numeros': [], 'datas': [], 'sorteios': 0},
            1: {'nome': 'Segunda', 'numeros': [], 'datas': [], 'sorteios': 0},
            2: {'nome': 'Terça', 'numeros': [], 'datas': [], 'sorteios': 0},
            3: {'nome': 'Quarta', 'numeros': [], 'datas': [], 'sorteios': 0},
            4: {'nome': 'Quinta', 'numeros': [], 'datas': [], 'sorteios': 0},
            5: {'nome': 'Sexta', 'numeros': [], 'datas': [], 'sorteios': 0},
            6: {'nome': 'Sábado', 'numeros': [], 'datas': [], 'sorteios': 0}
        }
        
        for dado in dados:
            try:
                data_str = dado['Data']
                dia, mes, ano = map(int, data_str.split('/'))
                data_obj = datetime(ano, mes, dia)
                
                dia_semana = (data_obj.weekday() + 1) % 7
                
                numeros = []
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        numeros.append(int(dado[chave]))
                
                stats_por_dia[dia_semana]['numeros'].extend(numeros)
                stats_por_dia[dia_semana]['datas'].append(data_str)
                stats_por_dia[dia_semana]['sorteios'] += 1
            
            except Exception as e:
                print(f"Erro processando linha: {e}")
                continue
        
        resultado = []
        
        for idx in range(7):
            dia_info = stats_por_dia[idx]
            numeros = dia_info['numeros']
            
            stats_dia = {
                'id': idx,
                'nome': dia_info['nome'],
                'sorteios': dia_info['sorteios'],
                'datas': dia_info['datas'],
            }
            
            if numeros:
                contador = Counter(numeros)
                top_10 = contador.most_common(10)
                
                stats_dia['numeros_mais_jogados'] = [
                    {'numero': num, 'frequencia': freq} 
                    for num, freq in top_10
                ]
                
                stats_dia['media'] = round(statistics.mean(numeros), 2)
                stats_dia['mediana'] = statistics.median(numeros)
                stats_dia['desvio_padrao'] = round(statistics.stdev(numeros) if len(numeros) > 1 else 0, 2)
                stats_dia['minimo'] = min(numeros)
                stats_dia['maximo'] = max(numeros)
                
                media_ponderada = sum(num * contador[num] for num in set(numeros)) / (stats_dia['sorteios'] * 15)
                stats_dia['media_ponderada'] = round(media_ponderada * 25, 2)
                
                probabilidades = {}
                for n in range(1, 26):
                    freq = contador.get(n, 0)
                    prob = (freq / len(numeros) * 100) if numeros else 0
                    probabilidades[n] = round(prob, 2)
                
                stats_dia['probabilidades'] = probabilidades
                stats_dia['numeros_nao_sorteados'] = [n for n in range(1, 26) if n not in set(numeros)]
            else:
                stats_dia['numeros_mais_jogados'] = []
                stats_dia['media'] = 0
                stats_dia['mediana'] = 0
                stats_dia['desvio_padrao'] = 0
                stats_dia['minimo'] = 0
                stats_dia['maximo'] = 0
                stats_dia['media_ponderada'] = 0
                stats_dia['probabilidades'] = {n: 0 for n in range(1, 26)}
                stats_dia['numeros_nao_sorteados'] = list(range(1, 26))
            
            resultado.append(stats_dia)
        
        return resultado
    
    @staticmethod
    def calcular_estatisticas_globais(dados: List[Dict]) -> Dict:
        """Calcula estatísticas globais"""
        
        if not dados:
            return {
                'total_sorteios': 0,
                'data_primeira': 'N/A',
                'data_ultima': 'N/A',
                'numeros_mais_jogados': [],
                'numeros_menos_jogados': [],
                'numero_mais_frequente': 0,
                'numero_menos_frequente': 0
            }
        
        todos_numeros = []
        for dado in dados:
            for i in range(1, 16):
                chave = f'Bola{i}'
                if chave in dado:
                    todos_numeros.append(int(dado[chave]))
        
        contador_global = Counter(todos_numeros)
        
        return {
            'total_sorteios': len(dados),
            'data_primeira': dados[0]['Data'],
            'data_ultima': dados[-1]['Data'],
            'numeros_mais_jogados': contador_global.most_common(5),
            'numeros_menos_jogados': contador_global.most_common()[-5:],
            'numero_mais_frequente': contador_global.most_common(1)[0][0] if contador_global else 0,
            'numero_menos_frequente': contador_global.most_common()[-1][0] if contador_global else 0,
            'total_numeros_unicos': len(contador_global)
        }

    @staticmethod
    def calcular_estatisticas_por_mes(dados: List[Dict]) -> List[Dict]:
        """Calcula estatísticas por mês (agregando todos os anos)"""
        
        meses_nomes = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        stats_por_mes = {}
        
        for dado in dados:
            try:
                data_str = dado['Data']
                dia, mes, ano = map(int, data_str.split('/'))
                
                # Agrupar apenas por mês, independente do ano
                chave_mes = mes
                
                if chave_mes not in stats_por_mes:
                    stats_por_mes[chave_mes] = {
                        'mes': mes,
                        'nome': meses_nomes[mes],
                        'numeros': [],
                        'sorteios': 0
                    }
                
                numeros = []
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        numeros.append(int(dado[chave]))
                
                stats_por_mes[chave_mes]['numeros'].extend(numeros)
                stats_por_mes[chave_mes]['sorteios'] += 1
                
            except Exception as e:
                print(f"Erro processando linha: {e}")
                continue
        
        resultado = []
        
        for mes_num in sorted(stats_por_mes.keys()):
            mes_info = stats_por_mes[mes_num]
            numeros = mes_info['numeros']
            
            stats_mes = {
                'mes': mes_info['mes'],
                'nome': mes_info['nome'],
                'sorteios': mes_info['sorteios'],
            }
            
            if numeros:
                contador = Counter(numeros)
                top_10 = contador.most_common(10)
                
                stats_mes['numeros_mais_jogados'] = [
                    {'numero': num, 'frequencia': freq} 
                    for num, freq in top_10
                ]
                
                stats_mes['numeros_menos_jogados'] = [
                    {'numero': num, 'frequencia': freq} 
                    for num, freq in contador.most_common()[-10:][::-1]
                ]
                
                stats_mes['numero_mais_frequente'] = top_10[0][0] if top_10 else 0
                stats_mes['numero_menos_frequente'] = contador.most_common()[-1][0] if contador else 0
                stats_mes['numeros_nao_sorteados'] = [n for n in range(1, 26) if n not in set(numeros)]
            else:
                stats_mes['numeros_mais_jogados'] = []
                stats_mes['numeros_menos_jogados'] = []
                stats_mes['numero_mais_frequente'] = 0
                stats_mes['numero_menos_frequente'] = 0
                stats_mes['numeros_nao_sorteados'] = list(range(1, 26))
            
            resultado.append(stats_mes)
        
        return resultado

    @staticmethod
    def calcular_estatisticas_por_ano(dados: List[Dict]) -> List[Dict]:
        """Calcula estatísticas por ano"""
        
        stats_por_ano = {}
        
        for dado in dados:
            try:
                data_str = dado['Data']
                dia, mes, ano = map(int, data_str.split('/'))
                
                if ano not in stats_por_ano:
                    stats_por_ano[ano] = {
                        'ano': ano,
                        'nome': f"{ano}",
                        'numeros': [],
                        'sorteios': 0
                    }
                
                numeros = []
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        numeros.append(int(dado[chave]))
                
                stats_por_ano[ano]['numeros'].extend(numeros)
                stats_por_ano[ano]['sorteios'] += 1
                
            except Exception as e:
                print(f"Erro processando linha: {e}")
                continue
        
        resultado = []
        
        for ano in sorted(stats_por_ano.keys(), reverse=True):
            ano_info = stats_por_ano[ano]
            numeros = ano_info['numeros']
            
            stats_ano = {
                'ano': ano_info['ano'],
                'nome': ano_info['nome'],
                'sorteios': ano_info['sorteios'],
            }
            
            if numeros:
                contador = Counter(numeros)
                top_10 = contador.most_common(10)
                
                stats_ano['numeros_mais_jogados'] = [
                    {'numero': num, 'frequencia': freq} 
                    for num, freq in top_10
                ]
                
                stats_ano['numeros_menos_jogados'] = [
                    {'numero': num, 'frequencia': freq} 
                    for num, freq in contador.most_common()[-10:][::-1]
                ]
                
                stats_ano['numero_mais_frequente'] = top_10[0][0] if top_10 else 0
                stats_ano['numero_menos_frequente'] = contador.most_common()[-1][0] if contador else 0
                stats_ano['numeros_nao_sorteados'] = [n for n in range(1, 26) if n not in set(numeros)]
            else:
                stats_ano['numeros_mais_jogados'] = []
                stats_ano['numeros_menos_jogados'] = []
                stats_ano['numero_mais_frequente'] = 0
                stats_ano['numero_menos_frequente'] = 0
                stats_ano['numeros_nao_sorteados'] = list(range(1, 26))
            
            resultado.append(stats_ano)
        
        return resultado

    @staticmethod
    def extrair_pares(numeros: List[int]) -> List[tuple]:
        """Extrai pares de números que frequentemente aparecem juntos"""
        pares_frequencia = {}
        
        # Contar frequência de pares
        for i in range(len(numeros)):
            for j in range(i + 1, len(numeros)):
                par = tuple(sorted([numeros[i], numeros[j]]))
                pares_frequencia[par] = pares_frequencia.get(par, 0) + 1
        
        # Retornar top 10 pares
        return sorted(pares_frequencia.items(), key=lambda x: x[1], reverse=True)[:10]

    @staticmethod
    def extrair_tripletas(numeros: List[int]) -> List[tuple]:
        """Extrai tripletas de números que frequentemente aparecem juntas"""
        tripletas_frequencia = {}
        
        # Contar frequência de tripletas
        for i in range(len(numeros)):
            for j in range(i + 1, len(numeros)):
                for k in range(j + 1, len(numeros)):
                    trip = tuple(sorted([numeros[i], numeros[j], numeros[k]]))
                    tripletas_frequencia[trip] = tripletas_frequencia.get(trip, 0) + 1
        
        # Retornar top 10 tripletas
        return sorted(tripletas_frequencia.items(), key=lambda x: x[1], reverse=True)[:10]

    @staticmethod
    def gerar_apostas_recomendadas(dados: List[Dict], dia_semana: int, mes: int, ano: int) -> List[Dict]:
        """
        Gera 5 melhores apostas combinando análise de dia/mês/ano
        
        Args:
            dados: Lista de dados de sorteios
            dia_semana: Dia da semana (0=domingo, 6=sábado)
            mes: Mês (1-12)
            ano: Ano
            
        Returns:
            Lista com até 5 apostas recomendadas
        """
        # Extrair números para cada contexto
        numeros_dia = []
        numeros_mes = []
        numeros_ano = []
        todos_numeros = []
        
        for dado in dados:
            try:
                data_str = dado['Data']
                dia, m, a = map(int, data_str.split('/'))
                data_obj = datetime(a, m, dia)
                dia_semana_dado = (data_obj.weekday() + 1) % 7
                
                numeros = []
                for i in range(1, 16):
                    chave = f'Bola{i}'
                    if chave in dado:
                        numeros.append(int(dado[chave]))
                
                todos_numeros.extend(numeros)
                
                if dia_semana_dado == dia_semana:
                    numeros_dia.extend(numeros)
                
                if m == mes:
                    numeros_mes.extend(numeros)
                    
                if a == ano:
                    numeros_ano.extend(numeros)
                    
            except:
                continue
        
        # Calcular frequências para cada contexto
        def calcular_score_numeros(numeros_contexto, todos_numeros_list):
            if not numeros_contexto:
                return []
            
            contador_contexto = Counter(numeros_contexto)
            contador_global = Counter(todos_numeros_list)
            
            scores = {}
            for num in range(1, 26):
                freq_contexto = contador_contexto.get(num, 0)
                freq_global = contador_global.get(num, 0)
                # Score combina frequência no contexto com frequência global
                score = (freq_contexto * 3) + (freq_global * 0.5) if freq_contexto > 0 else 0
                scores[num] = score
            
            return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Gerar apostas recomendadas
        apostas = []
        
        # Aposta 1: Baseada no dia da semana
        if numeros_dia:
            aposta1 = {
                'nome': 'Aposta do Dia da Semana',
                'criterio': StatsCalculator._obter_nome_dia(dia_semana),
                'numeros': [],
                'raciocinio': []
            }
            scores_dia = calcular_score_numeros(numeros_dia, todos_numeros)
            numeros_selecionados = [num for num, score in scores_dia[:15]]
            aposta1['numeros'] = sorted(numeros_selecionados)
            aposta1['raciocinio'] = f"Selecionados números mais frequentes em {StatsCalculator._obter_nome_dia(dia_semana)}"
            apostas.append(aposta1)
        
        # Aposta 2: Baseada no mês
        if numeros_mes:
            aposta2 = {
                'nome': 'Aposta do Mês',
                'criterio': StatsCalculator._obter_nome_mes(mes),
                'numeros': [],
                'raciocinio': []
            }
            scores_mes = calcular_score_numeros(numeros_mes, todos_numeros)
            numeros_selecionados = [num for num, score in scores_mes[:15]]
            aposta2['numeros'] = sorted(numeros_selecionados)
            aposta2['raciocinio'] = f"Selecionados números mais frequentes em {StatsCalculator._obter_nome_mes(mes)}"
            apostas.append(aposta2)
        
        # Aposta 3: Baseada no ano
        if numeros_ano:
            aposta3 = {
                'nome': 'Aposta do Ano',
                'criterio': str(ano),
                'numeros': [],
                'raciocinio': []
            }
            scores_ano = calcular_score_numeros(numeros_ano, todos_numeros)
            numeros_selecionados = [num for num, score in scores_ano[:15]]
            aposta3['numeros'] = sorted(numeros_selecionados)
            aposta3['raciocinio'] = f"Selecionados números mais frequentes em {ano}"
            apostas.append(aposta3)
        
        # Aposta 4: Combinação Dia + Mês
        if numeros_dia and numeros_mes:
            numeros_combinados = numeros_dia + numeros_mes
            aposta4 = {
                'nome': 'Aposta Dia + Mês',
                'criterio': f"{StatsCalculator._obter_nome_dia(dia_semana)} em {StatsCalculator._obter_nome_mes(mes)}",
                'numeros': [],
                'raciocinio': []
            }
            scores_comb = calcular_score_numeros(numeros_combinados, todos_numeros)
            numeros_selecionados = [num for num, score in scores_comb[:15]]
            aposta4['numeros'] = sorted(numeros_selecionados)
            aposta4['raciocinio'] = f"Combinação análise de {StatsCalculator._obter_nome_dia(dia_semana)} com {StatsCalculator._obter_nome_mes(mes)}"
            apostas.append(aposta4)
        
        # Aposta 5: Combinação Dia + Ano
        if numeros_dia and numeros_ano:
            numeros_combinados = numeros_dia + numeros_ano
            aposta5 = {
                'nome': 'Aposta Dia + Ano',
                'criterio': f"{StatsCalculator._obter_nome_dia(dia_semana)} em {ano}",
                'numeros': [],
                'raciocinio': []
            }
            scores_comb = calcular_score_numeros(numeros_combinados, todos_numeros)
            numeros_selecionados = [num for num, score in scores_comb[:15]]
            aposta5['numeros'] = sorted(numeros_selecionados)
            aposta5['raciocinio'] = f"Combinação análise de {StatsCalculator._obter_nome_dia(dia_semana)} com {ano}"
            apostas.append(aposta5)
        
        # Retornar até 5 apostas
        return apostas[:5]

    @staticmethod
    def _obter_nome_dia(dia_semana: int) -> str:
        """Obtém nome do dia da semana"""
        dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        return dias[dia_semana]

    @staticmethod
    def _obter_nome_mes(mes: int) -> str:
        """Obtém nome do mês"""
        meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return meses[mes]
