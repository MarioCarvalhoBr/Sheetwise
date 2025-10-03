# PDF Generation Implementation Guide

## 📋 Overview

This document describes the implementation of PDF generation functionality in Sheetwise using **pdfkit** and **wkhtmltopdf**.

## 🎯 Features Added

### 1. Triple Output Format
The application now generates **three report formats** for each analysis:
- **results.txt** - Plain text report
- **results.html** - Formatted HTML report (from external template)
- **results.pdf** - Professional PDF report (generated from HTML)

### 2. PDF Generation Method

Added new method `generate_report_pdf()` in `src/utils/file_processor.py`:

```python
def generate_report_pdf(self, html_path: str, pdf_path: str) -> bool:
    """Generate PDF report from HTML file using pdfkit
    
    Args:
        html_path: Path to the HTML file
        pdf_path: Path where PDF will be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
```

**Key Features:**
- Uses pdfkit library (wrapper for wkhtmltopdf)
- Auto-detects wkhtmltopdf path in bundled executables
- Configurable PDF options (A4 size, margins, encoding)
- Graceful error handling with logging
- Works in both development and production (executable) mode

### 3. Controller Integration

Updated `src/controllers/app_controller.py` to:
- Generate PDF after HTML creation
- Track PDF generation success/failure
- Update database records with all file formats
- Show user-friendly success messages indicating all generated files

## 🔧 Technical Implementation

### Dependencies Added

**Python Package:**
```bash
poetry add pdfkit
```

**System Dependency:**
- **wkhtmltopdf** - Binary executable for HTML to PDF conversion

### Build System Updates

#### Linux Build Script (`scripts/build_linux.sh`)
```bash
# Checks for wkhtmltopdf
WKHTMLTOPDF_PATH=$(which wkhtmltopdf 2>/dev/null)

# Creates temporary directory structure
mkdir -p wkhtmltopdf/bin
cp "$WKHTMLTOPDF_PATH" wkhtmltopdf/bin/

# Bundles with PyInstaller
--add-data=wkhtmltopdf:wkhtmltopdf
--hidden-import=pdfkit
```

#### Windows Build Script (`scripts/build_windows.bat`)
```batch
REM Checks for wkhtmltopdf
where wkhtmltopdf

REM Creates temporary directory
mkdir wkhtmltopdf\bin
copy wkhtmltopdf.exe wkhtmltopdf\bin\

REM Bundles with PyInstaller
--add-data wkhtmltopdf;wkhtmltopdf
--hidden-import pdfkit
```

### CI/CD Workflows Updated

#### Linux Workflow (`.github/workflows/cd_linux_workflow.yml`)
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y python3-tk python3-dev wkhtmltopdf

- name: Prepare wkhtmltopdf for bundling
  run: |
    mkdir -p wkhtmltopdf/bin
    cp $(which wkhtmltopdf) wkhtmltopdf/bin/
```

#### Windows Workflow (`.github/workflows/cd_windows_workflow.yml`)
```yaml
- name: Install wkhtmltopdf
  run: |
    choco install wkhtmltopdf -y

- name: Prepare wkhtmltopdf for bundling
  run: |
    mkdir -p wkhtmltopdf\bin
    $wkhtmlPath = (Get-Command wkhtmltopdf).Source
    Copy-Item $wkhtmlPath wkhtmltopdf\bin\wkhtmltopdf.exe
```

## 📦 Executable Distribution

### How wkhtmltopdf is Bundled

**Development Mode:**
- Developers must install wkhtmltopdf system-wide
- Application detects it automatically from PATH

**Production Mode (Executables):**
- wkhtmltopdf binary is bundled inside the executable
- Extracted to `sys._MEIPASS/wkhtmltopdf/bin/` at runtime
- No end-user installation required! ✨

### Path Resolution Logic

```python
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    if sys.platform.startswith('win'):
        wkhtmltopdf_path = os.path.join(sys._MEIPASS, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')
    else:
        wkhtmltopdf_path = os.path.join(sys._MEIPASS, 'wkhtmltopdf', 'bin', 'wkhtmltopdf')
    
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
```

## 📚 Developer Guide

### Installing wkhtmltopdf for Development

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install wkhtmltopdf -y
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install wkhtmltopdf -y
```

**macOS (Homebrew):**
```bash
brew install wkhtmltopdf
```

**Windows (Chocolatey):**
```bash
choco install wkhtmltopdf -y
```

**Windows (Manual):**
1. Download from [wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
2. Install the `.exe` installer
3. Add installation directory to PATH environment variable

### Verifying Installation

```bash
# Check if wkhtmltopdf is installed
which wkhtmltopdf  # Linux/macOS
where wkhtmltopdf  # Windows

# Check version
wkhtmltopdf --version
```

### Building Executables

**Linux:**
```bash
# Install wkhtmltopdf first!
sudo apt install wkhtmltopdf -y

# Build executable
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

**Windows:**
```bash
# Install wkhtmltopdf first!
choco install wkhtmltopdf -y

# Build executable
.\scripts\build_windows.bat
```

## 🧪 Testing PDF Generation

### Test Workflow
1. Run the application
2. Login or register a user
3. Select source folder with CSV/XLSX files
4. Select output folder for results
5. Click "Analyze"
6. Check output folder for:
   - ✅ `results.txt`
   - ✅ `results.html`
   - ✅ `results.pdf`

### Troubleshooting

**PDF Not Generated:**
- Check if wkhtmltopdf is installed: `which wkhtmltopdf` (Linux) or `where wkhtmltopdf` (Windows)
- Check application logs in `sheetwise.log`
- Verify HTML file was created successfully

**Build Fails:**
- Ensure wkhtmltopdf is installed before building
- Check PyInstaller includes `--hidden-import pdfkit`
- Verify `--add-data` includes wkhtmltopdf directory

**Permission Errors (Linux):**
- Make wkhtmltopdf executable: `chmod +x wkhtmltopdf/bin/wkhtmltopdf`
- Check file permissions in output folder

## 📝 Files Modified

### Source Code
- ✅ `src/utils/file_processor.py` - Added `generate_report_pdf()` method
- ✅ `src/controllers/app_controller.py` - Integrated PDF generation in analysis flow

### Build Scripts
- ✅ `scripts/build_linux.sh` - Added wkhtmltopdf bundling logic
- ✅ `scripts/build_windows.bat` - Added wkhtmltopdf bundling logic

### CI/CD Workflows
- ✅ `.github/workflows/cd_linux_workflow.yml` - Install and bundle wkhtmltopdf
- ✅ `.github/workflows/cd_windows_workflow.yml` - Install and bundle wkhtmltopdf
- ✅ `.github/workflows/ci_linux_workflow.yml` - Install wkhtmltopdf for testing

### Documentation
- ✅ `README.md` - Added developer installation instructions for wkhtmltopdf
- ✅ `pyproject.toml` - Added pdfkit dependency (via Poetry)

## 🎉 Benefits

### For End Users
- 📄 Professional PDF reports ready to share
- 🚀 No additional software installation needed (bundled executable)
- 📊 Three output formats for different use cases

### For Developers
- 🛠️ Clean implementation with external template system
- 📦 Automated bundling of system dependencies
- 🔄 CI/CD ready with GitHub workflows
- 📝 Well-documented codebase

## 🔗 References

- [pdfkit Documentation](https://pypi.org/project/pdfkit/)
- [wkhtmltopdf Official Site](https://wkhtmltopdf.org/)
- [PyInstaller Data Files](https://pyinstaller.org/en/stable/spec-files.html#adding-data-files)
- [Sheetwise Repository](https://github.com/MarioCarvalhoBr/Sheetwise)

---

**Implementation Date:** October 2, 2025  
**Version:** Sheetwise v1.0  
**Status:** ✅ Complete and Tested
