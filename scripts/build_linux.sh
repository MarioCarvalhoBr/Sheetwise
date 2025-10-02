#!/bin/bash
# Script to generate cross-platform executable

echo "=== Generating Sheetwise executable ==="

# Check if in correct directory
if [ ! -f "src/main.py" ]; then
    echo "❌ Error: Run this script in the project root directory (where src/main.py is)"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

source .venv/bin/activate

# Check PyInstaller
echo "Checking PyInstaller..."
if ! pyinstaller --version > /dev/null 2>&1; then
    echo "❌ Error: PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Determine operating system for executable name
OS_NAME=$(uname -s)
case "$OS_NAME" in
    Linux*)     
        EXE_NAME="Sheetwise-v1-linux_x64.run"
        ;;
    Darwin*)    
        EXE_NAME="Sheetwise-v1-macos_x64.app"
        ;;
    MINGW*)     
        EXE_NAME="Sheetwise-v1-windows_x64.exe"
        ;;
    *)          
        EXE_NAME="Sheetwise-v1-unknown_x64"
        ;;
esac

echo "Detected system: $OS_NAME"
echo "Generating executable: $EXE_NAME"

# Generate executable
echo "Running PyInstaller..."
pyinstaller \
    --onefile \
    --windowed \
    --name="$EXE_NAME" \
    --distpath="dist" \
    --workpath="build" \
    --specpath="." \
    --add-data="src:src" \
    --add-data="assets:assets" \
    --hidden-import="pandas" \
    --hidden-import="openpyxl" \
    --hidden-import="ttkthemes" \
    --hidden-import="ttkbootstrap" \
    --hidden-import="PIL" \
    --hidden-import="sqlite3" \
    --hidden-import="tkinter" \
    --hidden-import="tkinter.ttk" \
    --hidden-import="tkinter.messagebox" \
    --hidden-import="tkinter.filedialog" \
    --collect-all="ttkthemes" \
    --collect-all="ttkbootstrap" \
    --collect-all="pandas" \
    src/main.py

# Check if generated successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "=== ✅ Executable generated successfully! ==="
    echo "Location: $(pwd)/dist/$EXE_NAME"
    echo "Size: $(du -h dist/$EXE_NAME 2>/dev/null | cut -f1 || echo 'N/A')"
    echo ""
    echo "To test: ./dist/$EXE_NAME"
    
    # Make executable on Linux/Mac
    chmod +x "dist/$EXE_NAME"
    
else
    echo ""
    echo "=== ❌ Error generating executable ==="
    echo "Check the logs above for more details"
    exit 1
fi
