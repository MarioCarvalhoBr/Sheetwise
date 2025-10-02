#!/usr/bin/env python3
"""
AnalisaPlanilhas - Software para análise de planilhas CSV/XLSX
Aplicativo principal
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

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