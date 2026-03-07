"""Utilidades para manipulação de arquivos CSV"""
import csv
import os
from typing import List, Dict, Tuple
from app.utils.paths import get_sorteios_csv

class CSVHandler:
    """Gerencia leitura e escrita de dados em CSV"""
    
    def __init__(self, filepath: str = None):
        self.filepath = filepath or get_sorteios_csv()
    
    def carregar_dados(self) -> List[Dict]:
        """Carrega todos os dados do CSV"""
        dados = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    leitor = csv.DictReader(f, delimiter=';')
                    for linha in leitor:
                        if linha:
                            dados.append(linha)
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
        return dados
    
    def salvar_dados(self, id_val: str, data_val: str, numeros: List[str]) -> bool:
        """Salva dados no arquivo CSV"""
        try:
            arquivo_existe = os.path.exists(self.filepath)
            
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f, delimiter=';')
                
                if not arquivo_existe:
                    cabecalho = ['ID', 'Data'] + [f'Bola{i+1}' for i in range(15)]
                    escritor.writerow(cabecalho)
                
                linha = [id_val, data_val] + numeros
                escritor.writerow(linha)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def obter_proximo_id(self) -> int:
        """Obtém o próximo ID disponível"""
        dados = self.carregar_dados()
        if dados:
            ids = [int(d['ID']) for d in dados]
            return max(ids) + 1
        return 1
    
    def obter_ultima_data(self) -> str:
        """Obtém a data do último sorteio"""
        dados = self.carregar_dados()
        if dados:
            return dados[-1]['Data']
        return ''
