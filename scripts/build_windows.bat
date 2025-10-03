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

echo Generating Sheetwise-v1-windows_x64.exe...

REM Check for wkhtmltopdf
echo Checking wkhtmltopdf...
where wkhtmltopdf >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ wkhtmltopdf found
    REM Create temporary wkhtmltopdf directory structure (force create if exists)
    if not exist "wkhtmltopdf" mkdir wkhtmltopdf
    if not exist "wkhtmltopdf\bin" mkdir wkhtmltopdf\bin
    for /f "delims=" %%i in ('where wkhtmltopdf') do copy "%%i" wkhtmltopdf\bin\wkhtmltopdf.exe >nul 2>&1
    set WKHTMLTOPDF_DATA=--add-data wkhtmltopdf;wkhtmltopdf
) else (
    echo ⚠️  Warning: wkhtmltopdf not found. PDF generation will not work.
    echo    Install wkhtmltopdf: choco install wkhtmltopdf
    set WKHTMLTOPDF_DATA=
)

REM Generate executable with Windows-specific settings
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Sheetwise-v1-windows_x64" ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --icon assets\icon.ico ^
    --add-data src;src ^
    --add-data assets;assets ^
    %WKHTMLTOPDF_DATA% ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import ttkbootstrap ^
    --hidden-import PIL ^
    --hidden-import PIL._tkinter_finder ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageTk ^
    --hidden-import Pillow ^
    --hidden-import pdfkit ^
    --hidden-import sqlite3 ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import _tkinter ^
    --collect-all ttkbootstrap ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --collect-all PIL ^
    --noconsole ^
    --noconfirm ^
    src\main.py

REM Clean up temporary wkhtmltopdf directory
if exist "wkhtmltopdf" rmdir /s /q wkhtmltopdf

REM Check result
if %errorlevel% equ 0 (
    echo.
    echo === ✅ Build complete! ===
    
    REM Check if file was generated
    if exist "dist\Sheetwise-v1-windows_x64.exe" (
        echo ✅ .exe file generated: dist\Sheetwise-v1-windows_x64.exe
        for %%A in ("dist\Sheetwise-v1-windows_x64.exe") do echo Size: %%~zA bytes
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
    echo 💡 To test, run: dist\Sheetwise-v1-windows_x64.exe
    
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
