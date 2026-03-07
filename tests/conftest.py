"""Configuração e fixtures compartilhadas para testes"""
import pytest
import os
import tempfile
from app import create_app


@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes"""
    
    # Criar arquivo CSV temporário para testes
    db_fd, db_path = tempfile.mkstemp(suffix='.csv')
    usuario_fd, usuario_path = tempfile.mkstemp(suffix='.csv')
    
    app = create_app()
    
    # Usar CSV temporário para testes
    app.config['TESTING'] = True
    app.config['CSV_PATH'] = db_path
    app.config['USUARIOS_CSV_PATH'] = usuario_path
    
    yield app
    
    # Limpar arquivos temporais
    os.close(db_fd)
    os.unlink(db_path)
    os.close(usuario_fd)
    os.unlink(usuario_path)


@pytest.fixture
def client(app):
    """Cliente de teste da aplicação"""
    # Usar contexto de aplicação para sessões
    with app.app_context():
        yield app.test_client()


@pytest.fixture
def runner(app):
    """CLI test runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_data():
    """Dados de exemplo para testes"""
    return {
        'id': '2874',
        'data': '03/03/2026',
        'numeros': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    }


@pytest.fixture
def invalid_data():
    """Dados inválidos para testes"""
    return {
        'id': '',
        'data': '03/03/2026',
        'numeros': ['1', '1', '2', '2', '3', '3', '4', '4', '5', '5']  # Repetidos e poucos
    }


@pytest.fixture
def csv_test_file():
    """Cria arquivo CSV temporário com dados de teste"""
    import csv
    from pathlib import Path
    
    # Criar diretório temporário
    test_dir = Path(tempfile.gettempdir()) / "loto_tests"
    test_dir.mkdir(exist_ok=True)
    
    csv_path = test_dir / "test_dados.csv"
    
    # Criar arquivo CSV com dados de teste
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['ID', 'Data'] + [f'Bola{i}' for i in range(1, 16)])
        writer.writerow(['1', '01/01/2026'] + list(range(1, 16)))
        writer.writerow(['2', '02/01/2026'] + list(range(11, 26)))
    
    yield csv_path
    
    # Limpar
    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def usuarios_csv_temp():
    """Cria arquivo CSV temporário com usuários de teste"""
    import tempfile
    import csv
    
    fd, path = tempfile.mkstemp(suffix='.csv')
    
    # Criar arquivo vazio com headers
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['email', 'token', 'verified', 'created_at'])
    
    yield path
    
    # Limpar
    os.close(fd)
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture(autouse=True)
def limpar_auth_logs():
    """Limpa arquivo de logs de autenticação antes de cada teste"""
    from app.auth.email_service import EmailService
    EmailService.limpar_logs()
    yield
    EmailService.limpar_logs()
