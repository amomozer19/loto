"""Validadores de dados"""
from typing import List, Tuple

class SorteioValidator:
    """Valida dados de sorteio"""
    
    @staticmethod
    def validar_numeros(numeros: List[str]) -> Tuple[bool, str]:
        """Valida lista de números"""
        
        if len(numeros) != 15:
            return False, 'Deve haver 15 números'
        
        numeros_int = []
        
        for i, num_str in enumerate(numeros):
            if not num_str or num_str.strip() == '':
                return False, f'Número {i+1} está vazio'
            
            try:
                num = int(num_str)
                if num < 1 or num > 25:
                    return False, f'Números devem estar entre 1 e 25'
                numeros_int.append(num)
            except ValueError:
                return False, f'Número {i+1} deve ser um inteiro'
        
        if len(numeros_int) != len(set(numeros_int)):
            return False, 'Não são permitidas repetições'
        
        return True, 'Válido'
    
    @staticmethod
    def validar_id(id_val: str) -> Tuple[bool, str]:
        """Valida ID"""
        if not id_val or not id_val.strip():
            return False, 'ID não pode estar vazio'
        return True, 'Válido'
    
    @staticmethod
    def validar_data(data_val: str) -> Tuple[bool, str]:
        """Valida data"""
        if not data_val or not data_val.strip():
            return False, 'Data não pode estar vazia'
        return True, 'Válido'
