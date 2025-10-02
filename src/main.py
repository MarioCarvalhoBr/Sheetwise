#!/usr/bin/env python3
"""
Sheetwise - Software para análise de planilhas CSV/XLSX
Aplicativo principal
"""

import sys
import os

# Adicionar o diretório pai ao path para permitir imports relativos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.controllers.app_controller import AppController

def main():
    """Função principal do aplicativo"""
    try:
        app = AppController()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar o aplicativo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())