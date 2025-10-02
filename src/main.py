#!/usr/bin/env python3
"""
Sheetwise - CSV/XLSX Spreadsheet Analysis Software
Main application file
"""

import sys
import os

# Add parent directory to path to allow relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.controllers.app_controller import AppController

def main():
    """Main application function"""
    try:
        app = AppController()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar o aplicativo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())