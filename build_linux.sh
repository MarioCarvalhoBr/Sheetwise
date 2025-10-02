#!/bin/bash
# Script para gerar executável multiplataforma

echo "=== Gerando executável AnalisaPlanilhas ==="

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto (onde está o main.py)"
    exit 1
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado. Execute ./setup.sh primeiro"
    exit 1
fi

source venv/bin/activate

# Verificar PyInstaller
echo "Verificando PyInstaller..."
if ! pyinstaller --version > /dev/null 2>&1; then
    echo "❌ Erro: PyInstaller não encontrado. Instalando..."
    pip install pyinstaller
fi

# Limpar builds anteriores
echo "Limpando builds anteriores..."
rm -rf build/ dist/ *.spec

# Determinar sistema operacional para nome do executável
OS_NAME=$(uname -s)
case "$OS_NAME" in
    Linux*)     EXE_NAME="AnalisaPlanilhas_v1";;
    Darwin*)    EXE_NAME="AnalisaPlanilhas_v1";;
    MINGW*)     EXE_NAME="AnalisaPlanilhas_v1.exe";;
    *)          EXE_NAME="AnalisaPlanilhas_v1";;
esac

echo "Sistema detectado: $OS_NAME"
echo "Gerando executável: $EXE_NAME"

# Gerar executável
echo "Executando PyInstaller..."
pyinstaller \
    --onefile \
    --windowed \
    --name="AnalisaPlanilhas_v1" \
    --distpath="dist" \
    --workpath="build" \
    --specpath="." \
    --add-data="src:src" \
    --add-data="assets:assets" \
    --hidden-import="pandas" \
    --hidden-import="openpyxl" \
    --hidden-import="ttkthemes" \
    --hidden-import="PIL" \
    --hidden-import="sqlite3" \
    --hidden-import="tkinter" \
    --hidden-import="tkinter.ttk" \
    --hidden-import="tkinter.messagebox" \
    --hidden-import="tkinter.filedialog" \
    --collect-all="ttkthemes" \
    --collect-all="pandas" \
    main.py

# Verificar se foi gerado com sucesso
if [ $? -eq 0 ]; then
    echo ""
    echo "=== ✅ Executável gerado com sucesso! ==="
    echo "Localização: $(pwd)/dist/$EXE_NAME"
    echo "Tamanho: $(du -h dist/$EXE_NAME 2>/dev/null | cut -f1 || echo 'N/A')"
    echo ""
    echo "Para testar: ./dist/$EXE_NAME"
    
    # Tornar executável no Linux/Mac
    chmod +x "dist/$EXE_NAME"
    
else
    echo ""
    echo "=== ❌ Erro na geração do executável ==="
    echo "Verifique os logs acima para mais detalhes"
    exit 1
fi