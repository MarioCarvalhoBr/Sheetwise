# Sheetwise

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/Package%20Manager-Poetry-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20PT-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[Português](docs/pt_BR/README.pt_BR.md) | **English**

## 📋 Description

Sheetwise is a desktop application developed in Python with a modern graphical interface using Tkinter. The system allows you to analyze CSV/XLSX spreadsheets containing customer and sales data, generating detailed reports with statistics and data integrity analysis.

### 🌍 Internationalization (i18n)

- **English** (default)
- **Português** (complete)
- Real-time language switching in settings

### 🚀 Key Features

- **Modern Graphical Interface**: Clean and intuitive design using ttk themes
- **Settings System**: Themes, languages, and dark mode
- **Internationalization**: Full support for English and Portuguese
- **Smart Window**: Initial size at 80% of screen (10% side padding) + maximize button
- **Keyboard Shortcuts**: F11, Ctrl+M to maximize/restore, ESC to restore
- **Multi-format Support**: Accepts CSV and XLSX files
- **User Registration**: Login/registration system with SQLite
- **Execution CRUD**: Complete management of analysis history
- **Data Validation**: Automatic file structure verification
- **Detailed Reports**: Report generation with complete statistics
- **Windows Executable**: Standalone .exe generation with all dependencies
- **Poetry Management**: Modern dependencies and virtual environments

## 📁 Project Structure

```bash
Sheetwise/
├── src/                         # Source code
│   ├── main.py                  # Application entry point
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── database.py          # SQLite Manager + Models
│   ├── views/                   # Graphical interfaces
│   │   ├── __init__.py
│   │   ├── login_view.py        # Login/registration screen
│   │   └── main_view.py         # Main screen
│   ├── controllers/             # Controllers
│   │   ├── __init__.py
│   │   └── app_controller.py    # Main controller
│   ├── utils/                   # Utilities
│   │   ├── __init__.py
│   │   ├── file_processor.py    # File processing
│   │   └── i18n_manager.py      # Translation manager
│   └── static/                  # Static resources
│       └── i18n/                # Translation files
│           ├── en.json          # English translations
│           └── pt.json          # Portuguese translations
├── 
├── scripts/                     # Build and setup scripts
│   ├── build_windows.bat        # Windows build script
│   ├── build_linux.sh           # Linux build script
│   └── setup.sh                 # Environment setup script
├── 
├── database/                    # SQLite database
├── assets/                      # Resources (icons, images)
├── tests/                       # Unit tests
├── docs/                        # Additional documentation
│   ├── GUIDE.md                 # Quick guide (English)
│   ├── exemplos/                # Example files
│   └── pt_BR/                   # Portuguese documentation
│       ├── README.pt_BR.md      # Portuguese README
│       └── GUIDE.pt_BR.md       # Portuguese guide
├── 
├── pyproject.toml               # Poetry configuration
├── poetry.lock                  # Dependencies lock file
├── .venv/                       # Poetry virtual environment
└── README.md                    # Project documentation
```

## 🔧 Installation and Setup

### 1. Prerequisites

- Python 3.8+ installed on the system
- Poetry installed ([instructions](https://python-poetry.org/docs/#installation))
- Ubuntu 24.04 or compatible Linux system
- 4GB RAM minimum
- 1GB disk space

### 2. Installation with Poetry (Recommended)

```bash
# Clone the repository (or extract ZIP)
cd Sheetwise

# Configure and install dependencies automatically
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
- Create a Python virtual environment (`.venv`)
- Install Poetry
- Install all project dependencies
- Configure the development environment

### 3. Alternative: Manual Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Poetry
pip install poetry

# Install dependencies
poetry install
```

## 🚀 Running the Application

### Quick Start (Windows Users)

Download the latest Windows executable from the [Releases page](../../releases/latest):
1. Go to **Releases** → Download `Sheetwise_v1.exe`
2. Double-click the `.exe` file to run
3. No installation required! ✨

### Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run application
python src/main.py
```

### Production Mode (Build Executable)

#### Linux:
```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

#### Windows:
```bat
scripts\build_windows.bat
```

The executable will be created in the `dist/` directory.

### Automated Releases

Every release automatically builds and publishes the Windows executable:
- Create a new release on GitHub
- GitHub Actions builds `Sheetwise_v1.exe` on Windows
- Executable is automatically attached to the release
- See [Release Instructions](.github/RELEASE_EN.md) for details

## 📊 Database Schema

The application uses SQLite with the following structure:

### Users Table
```sql
users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date TIMESTAMP
)
```

### Executions Table
```sql
executions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    protocol TEXT,
    department TEXT,
    filename TEXT,
    source_folder_path TEXT,
    result_file_path TEXT,
    execution_date TIMESTAMP,
    status TEXT,
    notes TEXT
)
```

### Configurations Table
```sql
configurations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    theme TEXT DEFAULT 'arc',
    language TEXT DEFAULT 'en',
    dark_mode INTEGER DEFAULT 0,
    last_updated TIMESTAMP
)
```

## 📄 Expected File Formats

### clients.csv/xlsx
Required columns:
- `id`: Unique customer ID
- `name`: Customer full name

### sales.csv/xlsx
Required columns:
- `client_id`: Reference to customer ID
- `product`: Product name
- `quantity`: Quantity sold
- `unit_price`: Price per unit
- `final_price`: Total sale value

### addresses.csv/xlsx (optional)
Optional columns:
- `client_id`: Reference to customer ID
- `street`: Full address
- `neighborhood`: Neighborhood
- `city`: City

## 🎨 Themes and Customization

Available themes:
- **Arc** (default)
- **Equilux** (dark)
- **Adapta**
- **Breeze**
- **Yaru**

Dark mode can be enabled in settings for any theme.

## 🌐 Internationalization

The system supports:
- **English** (en) - Default
- **Portuguese** (pt)

Language can be changed in real-time through Settings tab.

Translation files are located in `src/static/i18n/`:
- `en.json` - English translations
- `pt.json` - Portuguese translations

## 🔑 Keyboard Shortcuts

- **F11**: Toggle maximize/restore window
- **Ctrl+M**: Toggle maximize/restore window
- **ESC**: Restore window to normal size
- **Enter**: Submit form (login screen)

## 🧪 Testing

Example files are provided in `docs/exemplos/`:
- `clientes.csv` - Sample customer data
- `vendas.csv` - Sample sales data
- `enderecos.csv` - Sample address data (optional)

## 📝 Generated Reports

Reports include:
- **General Statistics**: Total customers, sales, revenue
- **Top Products**: Best-selling products by quantity
- **Top Customers**: Customers by revenue
- **Data Integrity**: Missing relationships, coverage analysis

Reports are saved as `.txt` files in the location specified by the user.

## 🛠️ Development

### Project Architecture

The project follows the **MVC (Model-View-Controller)** pattern:

- **Models** (`src/models/`): Database management and business entities
- **Views** (`src/views/`): Tkinter graphical interfaces
- **Controllers** (`src/controllers/`): Business logic and coordination

### Adding New Features

1. **Database Changes**: Edit `src/models/database.py`
2. **Interface Changes**: Edit views in `src/views/`
3. **Business Logic**: Edit `src/controllers/app_controller.py`
4. **Translations**: Update `src/static/i18n/en.json` and `pt.json`

### Code Style

- Follow PEP 8 conventions
- Use type hints where possible
- Document functions with docstrings
- Keep code in English (comments, variables, functions)

## 🐛 Troubleshooting

### Problem: Error running application
**Solution:** Check if virtual environment is active
```bash
source .venv/bin/activate
```

### Problem: Module not found
**Solution:** Reinstall dependencies
```bash
poetry install
```

### Problem: Files not found
**Solution:** Check if file names are correct:
- clients.csv or clients.xlsx
- sales.csv or sales.xlsx
- addresses.csv or addresses.xlsx (optional)

### Problem: Database error
**Solution:** Delete database and restart application
```bash
rm -rf database/sheetwise.db
python src/main.py
```

## 📦 Dependencies

Main dependencies:
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file support
- **ttkthemes**: Modern Tkinter themes
- **Pillow**: Image processing
- **PyInstaller**: Executable generation

See `pyproject.toml` for complete dependency list.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Mario Carvalho

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the [Quick Guide](GUIDE.md)
- Review the [Portuguese documentation](docs/pt_BR/README.pt_BR.md)

---

**Note:** For Portuguese documentation, see [README.pt_BR.md](docs/pt_BR/README.pt_BR.md)
