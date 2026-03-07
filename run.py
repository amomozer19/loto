"""
Aplicação Loto - Arquivo Principal
Point de entrada da aplicação (wrapper)

Este arquivo importa de scripts/ e inicia a aplicação.
"""
import sys
from pathlib import Path

# Adicionar scripts ao path para importações
scripts_path = Path(__file__).parent / "scripts"
if str(scripts_path) not in sys.path:
    sys.path.insert(0, str(scripts_path))

# Importar do script de inicialização
from run_exe import setup_paths, abrir_navegador
from app import create_app
import threading

if __name__ == '__main__':
    # Setup paths
    setup_paths()
    
    print("=" * 60)
    print("  🎲 APLICAÇÃO LOTO - Iniciando...")
    print("=" * 60)
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
            debug=True,
            port=5000,
            host='0.0.0.0',
            use_reloader=False  # Desabilitar reloader para evitar múltiplas abas
        )
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        input("\nPressione ENTER para sair...")
