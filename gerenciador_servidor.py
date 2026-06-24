#!/usr/bin/env python3
"""
Gerenciador de servidor para SOS 102
Mantém o servidor rodando 24/7 com reinicialização automática
"""
import subprocess
import sys
import os
import time
from pathlib import Path

os.chdir(Path(__file__).parent)

print("=" * 70)
print("SOS 102 - GERENCIADOR DE SERVIDOR (24/7)")
print("=" * 70)
print("\nEste script vai manter o servidor rodando continuamente.")
print("Pressione Ctrl+C para encerrar completamente.\n")

tentativas = 0
max_tentativas = 5

while True:
    try:
        tentativas = 0
        print("\n[INFO] Iniciando servidor...")
        print("[INFO] Acesse: http://localhost:8000")
        print("[INFO] Pressione Ctrl+C no gerenciador para desligar\n")
        
        # Inicia o servidor
        processo = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Lê a saída do servidor em tempo real
        try:
            for linha in processo.stdout:
                print(f"[SERVER] {linha.rstrip()}")
        except KeyboardInterrupt:
            print("\n[INFO] Encerrando servidor...")
            processo.terminate()
            try:
                processo.wait(timeout=5)
            except subprocess.TimeoutExpired:
                processo.kill()
                processo.wait()
            print("[INFO] Servidor encerrado. Encerrando gerenciador.\n")
            sys.exit(0)
        
        # Se chegou aqui, o servidor foi encerrado
        print("\n[AVISO] Servidor desconectou!")
        
    except FileNotFoundError:
        print("[ERRO] Arquivo server.py não encontrado!")
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO] {e}")
    
    tentativas += 1
    if tentativas >= max_tentativas:
        print(f"[ERRO] Número máximo de tentativas ({max_tentativas}) atingido.")
        print("[INFO] Verifique os logs acima para mais detalhes.")
        sys.exit(1)
    
    aguarda = 3
    print(f"[INFO] Reiniciando em {aguarda} segundos (Tentativa {tentativas}/{max_tentativas})...")
    time.sleep(aguarda)
