@echo off
REM Script to generate Windows-specific executable (.exe)
REM Run this script on Windows with Python and PyInstaller installed

echo === Generating Windows executable (.exe) ===

REM Check if in correct directory
if not exist "src\main.py" (
    echo ❌ Error: Run this script in the project root directory
    pause
    exit /b 1
)

REM Activate virtual environment (if exists)
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found, using global Python
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo Generating Sheetwise_v1.exe...

REM Generate executable with Windows-specific settings
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Sheetwise_v1" ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --icon assets\icon.ico ^
    --add-data src;src ^
    --add-data assets;assets ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import ttkthemes ^
    --hidden-import ttkbootstrap ^
    --hidden-import PIL ^
    --hidden-import Pillow ^
    --hidden-import sqlite3 ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import _tkinter ^
    --collect-all ttkthemes ^
    --collect-all ttkbootstrap ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --noconsole ^
    --noconfirm ^
    src\main.py

REM Check result
if %errorlevel% equ 0 (
    echo.
    echo === ✅ Build complete! ===
    
    REM Check if file was generated
    if exist "dist\Sheetwise_v1.exe" (
        echo ✅ .exe file generated: dist\Sheetwise_v1.exe
        for %%A in ("dist\Sheetwise_v1.exe") do echo Size: %%~zA bytes
    ) else (
        echo ❌ .exe file not found in dist\
    )
    
    echo.
    echo 📁 Contents of dist\ directory:
    if exist "dist" (
        dir /b dist\
    ) else (
        echo dist\ directory does not exist
    )
    
    echo.
    echo 🎉 Executable ready for use on Windows!
    echo 💡 To test, run: dist\Sheetwise_v1.exe
    
) else (
    echo.
    echo === ❌ Generation error ===
    echo Check the logs above for details
    echo.
    echo 🔧 Possible solutions:
    echo - Install PyInstaller: pip install pyinstaller
    echo - Check if all dependencies are installed: pip install -r requirements.txt
    echo - Run as administrator if necessary
    pause
    exit /b 1
)

echo.
echo Press any key to continue...
pause > nul
