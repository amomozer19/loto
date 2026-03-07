"""Gerenciador de apostas e histórico de previsões"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from app.utils.paths import get_project_root

class ApostaManager:
    """Gerencia leitura, escrita e análise de apostas em JSON"""
    
    def __init__(self):
        self.project_root = get_project_root()
        self.dados_dir = os.path.join(self.project_root, 'data')
        self.aposta_file = os.path.join(self.dados_dir, 'aposta.json')
        self._garantir_arquivo()
    
    def _garantir_arquivo(self):
        """Garante que o arquivo existe com estrutura inicial"""
        if not os.path.exists(self.aposta_file):
            estrutura_inicial = {
                'apostas': [],
                'ultima_atualizacao': datetime.now().isoformat()
            }
            self._salvar_json(estrutura_inicial)
    
    def _carregar_json(self) -> Dict:
        """Carrega dados do arquivo JSON"""
        try:
            if os.path.exists(self.aposta_file):
                with open(self.aposta_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar aposta.json: {e}")
        
        return {'apostas': [], 'ultima_atualizacao': datetime.now().isoformat()}
    
    def _salvar_json(self, dados: Dict):
        """Salva dados no arquivo JSON"""
        try:
            with open(self.aposta_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar aposta.json: {e}")
    
    def salvar_apostas_dia(self, apostas: List[Dict], data: datetime = None) -> bool:
        """
        Salva as apostas do dia atual
        
        Args:
            apostas: Lista de apostas geradas
            data: Data das apostas (padrão: hoje)
        
        Returns:
            bool: True se salvo com sucesso
        """
        try:
            if data is None:
                data = datetime.now()
            
            data_str = data.strftime('%Y-%m-%d')
            
            dados = self._carregar_json()
            
            # Remove apostas do mesmo dia se existirem
            dados['apostas'] = [
                a for a in dados['apostas'] 
                if a.get('data') != data_str
            ]
            
            # Prepara aposta do dia
            aposta_dia = {
                'data': data_str,
                'dia_semana': self._obter_dia_semana(data),
                'mes': data.month,
                'ano': data.year,
                'timestamp': data.isoformat(),
                'apostas': [
                    {
                        'nome': a.get('nome'),
                        'criterio': a.get('criterio'),
                        'numeros': a.get('numeros'),
                        'raciocinio': a.get('raciocinio', ''),
                        'tuplas': a.get('tuplas', []),
                        'tripletas': a.get('tripletas', [])
                    }
                    for a in apostas
                ],
                'resultado_sorteio': None,  # Será preenchido depois
                'acertos': None,
                'analise': None
            }
            
            dados['apostas'].append(aposta_dia)
            dados['ultima_atualizacao'] = datetime.now().isoformat()
            
            self._salvar_json(dados)
            return True
        except Exception as e:
            print(f"Erro ao salvar apostas do dia: {e}")
            return False
    
    def registrar_resultado(self, data: datetime, numeros_sorteio: List[int]) -> bool:
        """
        Registra o resultado do sorteio para uma data específica
        
        Args:
            data: Data do sorteio
            numeros_sorteio: Lista dos 15 números sorteados
        
        Returns:
            bool: True se registrado com sucesso
        """
        try:
            data_str = data.strftime('%Y-%m-%d')
            dados = self._carregar_json()
            
            # Encontra aposta do dia
            for aposta_dia in dados['apostas']:
                if aposta_dia.get('data') == data_str:
                    aposta_dia['resultado_sorteio'] = numeros_sorteio
                    aposta_dia['data_resultado'] = datetime.now().isoformat()
                    dados['ultima_atualizacao'] = datetime.now().isoformat()
                    self._salvar_json(dados)
                    return True
            
            return False
        except Exception as e:
            print(f"Erro ao registrar resultado: {e}")
            return False
    
    def obter_apostas_dia(self, data: datetime = None) -> Optional[Dict]:
        """
        Obtém as apostas de um dia específico
        
        Args:
            data: Data desejada (padrão: hoje)
        
        Returns:
            Dict com as apostas do dia ou None
        """
        if data is None:
            data = datetime.now()
        
        data_str = data.strftime('%Y-%m-%d')
        dados = self._carregar_json()
        
        for aposta_dia in dados['apostas']:
            if aposta_dia.get('data') == data_str:
                return aposta_dia
        
        return None
    
    def obter_historico(self, dias: int = 30) -> List[Dict]:
        """
        Obtém histórico de apostas dos últimos N dias
        
        Args:
            dias: Número de dias do histórico
        
        Returns:
            Lista de apostas com resultados
        """
        dados = self._carregar_json()
        return dados.get('apostas', [])[-dias:]
    
    def obter_todas_apostas(self) -> List[Dict]:
        """Retorna todas as apostas registradas"""
        dados = self._carregar_json()
        return dados.get('apostas', [])
    
    @staticmethod
    def _obter_dia_semana(data: datetime) -> str:
        """Retorna o nome do dia da semana em português"""
        dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        return dias[(data.weekday() + 1) % 7]
