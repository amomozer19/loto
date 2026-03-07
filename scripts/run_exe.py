"""
Aplicação Loto - Executável
Script otimizado para gerar executável funcional com PyInstaller
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

# Garantir que os caminhos funcionam corretamente
def setup_paths():
    """Configurar caminhos corretamente para o executável."""
    if getattr(sys, 'frozen', False):
        # Executado como .exe
        application_path = Path(sys.executable).parent
    else:
        # Executado como script Python
        application_path = Path(__file__).parent
    
    # Adicionar ao sys.path se necessário
    if str(application_path) not in sys.path:
        sys.path.insert(0, str(application_path))
    
    return application_path

# Setup paths antes de tudo
app_path = setup_paths()

# Agora importar a aplicação
from app import create_app

def abrir_navegador():
    """Abre automaticamente o navegador após servidor iniciar."""
    time.sleep(3)  # Aguardar 3 segundos para servidor iniciar
    try:
        webbrowser.open('http://localhost:5000/auth/login')
    except:
        pass

if __name__ == '__main__':
    print("=" * 60)
    print("  🎲 APLICAÇÃO LOTO - Iniciando...")
    print("=" * 60)
    print()
    print("📍 Caminho da aplicação:", app_path)
    print()
    print("⏳ Iniciando servidor Flask...")
    print("   Abra no navegador: http://localhost:5000")
    print()
    print("💡 Dica: Clique em '🔌 Encerrar' para parar a aplicação")
    print()
    print("-" * 60)
    print()
    
    # Criar app
    app = create_app()
    
    # Thread para abrir navegador
    thread = threading.Thread(target=abrir_navegador, daemon=True)
    thread.start()
    
    # Executar servidor
    try:
        app.run(
            debug=False,  # debug=False em exe
            port=5000,
            host='127.0.0.1',
            use_reloader=False  # Não usar reloader em exe
        )
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        input("\nPressione ENTER para sair...")
