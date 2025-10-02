#!/bin/bash
# Script para configurar o ambiente de desenvolvimento no Ubuntu

echo "=== Configurando AnalisaPlanilhas - Ambiente de Desenvolvimento ==="

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv .venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências via poetry
echo "Instalando dependências..."
pip install poetry
poetry install

echo "=== Configuração concluída! ==="
echo "Para ativar o ambiente virtual: source .venv/bin/activate"
echo "Para executar o aplicativo: python main.py"