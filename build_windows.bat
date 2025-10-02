@echo off
REM Script para gerar executável específico para Windows (.exe)
REM Execute este script no Windows com Python e PyInstaller instalados

echo === Gerando executável Windows (.exe) ===

REM Verificar se está no diretório correto
if not exist "main.py" (
    echo ❌ Erro: Execute este script no diretório raiz do projeto
    pause
    exit /b 1
)

REM Ativar ambiente virtual (se existir)
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Ambiente virtual não encontrado, usando Python global
)

REM Limpar builds anteriores
echo Limpando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo Gerando Sheetwise_v1.exe...

REM Gerar executável com configurações específicas para Windows
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
    --hidden-import PIL ^
    --hidden-import Pillow ^
    --hidden-import sqlite3 ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import _tkinter ^
    --collect-all ttkthemes ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --noconsole ^
    --noconfirm ^
    main.py

REM Verificar resultado
if %errorlevel% equ 0 (
    echo.
    echo === ✅ Build concluído! ===
    
    REM Verificar se o arquivo foi gerado
    if exist "dist\Sheetwise_v1.exe" (
        echo ✅ Arquivo .exe gerado: dist\Sheetwise_v1.exe
        for %%A in ("dist\Sheetwise_v1.exe") do echo Tamanho: %%~zA bytes
    ) else (
        echo ❌ Arquivo .exe não encontrado em dist\
    )
    
    echo.
    echo 📁 Conteúdo do diretório dist\:
    if exist "dist" (
        dir /b dist\
    ) else (
        echo Diretório dist\ não existe
    )
    
    echo.
    echo 🎉 Executável pronto para uso no Windows!
    echo 💡 Para testar, execute: dist\Sheetwise_v1.exe
    
) else (
    echo.
    echo === ❌ Erro na geração ===
    echo Verifique os logs acima para detalhes
    echo.
    echo 🔧 Possíveis soluções:
    echo - Instale o PyInstaller: pip install pyinstaller
    echo - Verifique se todas as dependências estão instaladas: pip install -r requirements.txt
    echo - Execute como administrador se necessário
    pause
    exit /b 1
)

echo.
echo Pressione qualquer tecla para continuar...
pause > nul