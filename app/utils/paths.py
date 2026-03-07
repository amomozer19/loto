"""
Utilitário para resolver paths de forma dinâmica

Mantém compatibilidade com arquivos movidos para pastas específicas
"""
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Obtém o diretório raiz do projeto.
    
    Procura por markers como app/, scripts/, config/ etc
    """
    current = Path(__file__).parent.parent.parent  # app/utils/ -> raiz
    
    # Verificar se é o diretório raiz comparando com indicadores
    while current != current.parent:
        if (current / 'app').exists() and (current / 'config').exists():
            return current
        current = current.parent
    
    # Fallback: usar current working directory
    return Path.cwd()


def get_data_path(filename: str) -> str:
    """
    Resolve caminho para arquivos de dados.
    
    Procura em:
    1. data/filename
    2. filename (fallback para compatibilidade)
    """
    root = get_project_root()
    
    # Primeiro tenta em data/
    data_path = root / "data" / filename
    if data_path.exists():
        return str(data_path)
    
    # Fallback para raiz
    root_path = root / filename
    if root_path.exists():
        return str(root_path)
    
    # Se não existir, retorna o caminho esperado (será criado)
    return str(data_path)


def get_config_path(filename: str) -> str:
    """
    Resolve caminho para arquivos de configuração.
    
    Procura em:
    1. config/filename
    2. filename (fallback para compatibilidade)
    """
    root = get_project_root()
    
    # Primeiro tenta em config/
    config_path = root / "config" / filename
    if config_path.exists():
        return str(config_path)
    
    # Fallback para raiz
    root_path = root / filename
    if root_path.exists():
        return str(root_path)
    
    # Se não existir, retorna o caminho esperado (será criado)
    return str(config_path)


def get_docs_path(filename: str) -> str:
    """
    Resolve caminho para arquivos de documentação.
    
    Procura em: docs/filename
    """
    root = get_project_root()
    docs_path = root / "docs" / filename
    return str(docs_path)


def get_users_csv() -> str:
    """Resolve caminho para dados_usuarios.csv"""
    return get_data_path("dados_usuarios.csv")


def get_sorteios_csv() -> str:
    """Resolve caminho para dados_loto.csv"""
    return get_data_path("dados_loto.csv")


def get_tokens_log() -> str:
    """Resolve caminho para auth_tokens.log"""
    return get_config_path("auth_tokens.log")


def get_requirements_txt() -> str:
    """Resolve caminho para requirements.txt"""
    return get_config_path("requirements.txt")


# Aliases para compatibilidade
def resolve_path(filename: str, folder_type: str = 'data') -> str:
    """
    Resolve arquivo em qualquer pasta.
    
    Args:
        filename: Nome do arquivo
        folder_type: Tipo de pasta ('data', 'config', 'docs')
    """
    if folder_type == 'data':
        return get_data_path(filename)
    elif folder_type == 'config':
        return get_config_path(filename)
    elif folder_type == 'docs':
        return get_docs_path(filename)
    else:
        return str(get_project_root() / filename)


__all__ = [
    'get_project_root',
    'get_data_path',
    'get_config_path',
    'get_docs_path',
    'get_users_csv',
    'get_sorteios_csv',
    'get_tokens_log',
    'get_requirements_txt',
    'resolve_path',
]
