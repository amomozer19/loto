"""
Script para gerar executável da aplicação Loto com PyInstaller
Execute este script uma única vez para criar o .exe
"""
import subprocess
import sys
import os
from pathlib import Path

def criar_executavel():
    """Criar executável com PyInstaller."""
    
    print("=" * 70)
    print(" 🔨 GERADOR DE EXECUTÁVEL - Aplicação Loto")
    print("=" * 70)
    print()
    
    # Caminho do projeto
    projeto_dir = Path(__file__).parent
    output_dir = Path("C:\\Users\\SAMSUNG\\Desktop")
    
    print(f"📁 Diretório do projeto: {projeto_dir}")
    print(f"📁 Saída (Desktop): {output_dir}")
    print()
    
    # Verificar se PyInstaller está instalado
    print("⏳ Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("⏳ Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado")
    
    print()
    
    # Comando PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=LOTO",
        "--onefile",  # Executável único
        "--windowed",  # Sem console (opcional, remover se quiser ver logs)
        "--icon=LOTO.ico" if Path("LOTO.ico").exists() else "",  # Ícone se existir
        f"--distpath={output_dir}",  # Saída no Desktop
        "--workpath=build",  # Pasta temporária
        "--specpath=.",  # Spec file aqui
        "--hidden-import=flask",
        "--hidden-import=flask_cors",
        "--hidden-import=csv",
        "--hidden-import=secrets",
        "--hidden-import=itsdangerous",
        f"{projeto_dir}/run_exe.py"
    ]
    
    # Remover strings vazias
    cmd = [item for item in cmd if item]
    
    print("🔨 Executando PyInstaller...")
    print()
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 70)
        print(" ✅ SUCESSO!")
        print("=" * 70)
        print()
        print(f"📦 Executável criado: {output_dir}\\LOTO.exe")
        print()
        print("Para usar:")
        print(f"  1. Abra: {output_dir}\\LOTO.exe")
        print("  2. Espere o navegador abrir automaticamente")
        print("  3. Se não abrir, acesse: http://localhost:5000")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print(" ❌ ERRO AO CREATE EXECUTÁVEL")
        print("=" * 70)
        print(f"Erro: {e}")
        print()
        return False
    
    return True

if __name__ == "__main__":
    try:
        sucesso = criar_executavel()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
