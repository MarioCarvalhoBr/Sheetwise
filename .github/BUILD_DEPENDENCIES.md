# 📦 Dependências Atualizadas nos Scripts de Build

## ✅ Mudanças Realizadas

Todos os arquivos de build foram atualizados para incluir **todas** as dependências especificadas em `pyproject.toml`.

### 📋 Dependências do pyproject.toml

```toml
dependencies = [
    "pandas (>=2.2.3,<3.0.0)",
    "openpyxl (>=3.1.5,<4.0.0)",
    "pandas-stubs (>=2.2.3.250527,<3.0.0)",  # Type hints
    "ttkthemes (>=3.2.2,<4.0.0)",
    "pillow (>=10,<11)",
    "pyinstaller (>=6.16.0,<7.0.0)",
    "ttkbootstrap (>=1.14.2,<2.0.0)",        # ← NOVA!
]
```

### 🔧 Arquivos Atualizados

#### 1. **scripts/build_windows.bat**
```bat
Adicionado:
--hidden-import ttkbootstrap
--collect-all ttkbootstrap
```

#### 2. **scripts/build_linux.sh**
```bash
Adicionado:
--hidden-import="ttkbootstrap"
--collect-all="ttkbootstrap"
```

#### 3. **.github/workflows/cd_windows_workflow.yml**
```yaml
Adicionado:
--hidden-import ttkbootstrap
--collect-all ttkbootstrap
```

## 📊 Lista Completa de Imports Incluídos

### Hidden Imports (bibliotecas principais)
- ✅ `pandas` - Manipulação de dados
- ✅ `openpyxl` - Suporte a Excel
- ✅ `ttkthemes` - Temas Tkinter modernos
- ✅ `ttkbootstrap` - **Temas Bootstrap para Tkinter** (NOVO!)
- ✅ `PIL` / `Pillow` - Processamento de imagens
- ✅ `sqlite3` - Banco de dados
- ✅ `tkinter` - GUI framework
- ✅ `tkinter.ttk` - Widgets themed
- ✅ `tkinter.messagebox` - Caixas de mensagem
- ✅ `tkinter.filedialog` - Diálogos de arquivo
- ✅ `_tkinter` - Backend do Tkinter (Windows)

### Collect-All (coletar todos os recursos)
- ✅ `ttkthemes` - Todos os temas
- ✅ `ttkbootstrap` - **Todos os recursos Bootstrap** (NOVO!)
- ✅ `pandas` - Todos os módulos pandas
- ✅ `openpyxl` - Todos os recursos openpyxl

## ⚠️ Nota sobre pandas-stubs

`pandas-stubs` é uma dependência **apenas para desenvolvimento** (type hints/linting).

**Não precisa** ser incluída no executável porque:
- Só fornece arquivos `.pyi` (type stubs)
- Usado apenas durante desenvolvimento para autocomplete/validação
- Não afeta o runtime da aplicação

## 🎯 O que isso melhora?

### Antes:
- ❌ `ttkbootstrap` não era incluído
- ⚠️ Executável poderia falhar se o código usasse ttkbootstrap

### Depois:
- ✅ `ttkbootstrap` incluído
- ✅ Todos os temas e recursos empacotados
- ✅ Executável funciona mesmo usando ttkbootstrap

## 🧪 Como Testar

### Windows:
```bat
scripts\build_windows.bat
dist\Sheetwise_v1.exe
```

### Linux:
```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
./dist/Sheetwise_v1
```

### GitHub Actions:
```
Criar release → Workflow executará automaticamente
```

## 📈 Impacto no Tamanho do Executável

| Biblioteca | Tamanho Estimado |
|------------|------------------|
| pandas | ~50-60 MB |
| openpyxl | ~5-10 MB |
| ttkthemes | ~2-5 MB |
| ttkbootstrap | ~5-10 MB |
| Pillow | ~10-15 MB |
| Python runtime | ~20-30 MB |
| **Total esperado** | **~100-150 MB** |

## ✅ Checklist de Validação

- [x] `ttkbootstrap` adicionado em build_windows.bat
- [x] `ttkbootstrap` adicionado em build_linux.sh
- [x] `ttkbootstrap` adicionado em cd_windows_workflow.yml
- [x] Todas as dependências do pyproject.toml cobertas
- [x] `pandas-stubs` corretamente excluído (dev-only)

## 🔍 Verificação Rápida

Para verificar se todas as dependências estão nos scripts:

```bash
# Windows
grep -i "ttkbootstrap" scripts/build_windows.bat

# Linux
grep -i "ttkbootstrap" scripts/build_linux.sh

# Workflow
grep -i "ttkbootstrap" .github/workflows/cd_windows_workflow.yml
```

Todos devem retornar matches! ✅

## 📚 Recursos

- [PyInstaller Docs](https://pyinstaller.org/en/stable/)
- [ttkbootstrap Docs](https://ttkbootstrap.readthedocs.io/)
- [Hidden Imports Guide](https://pyinstaller.org/en/stable/when-things-go-wrong.html#listing-hidden-imports)

---

**Atualizado em:** 02/10/2025  
**Status:** ✅ Todos os arquivos sincronizados com pyproject.toml
