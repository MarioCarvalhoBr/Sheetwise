# Sheetwise - Quick Guide

[Português](docs/pt_BR/GUIDE.pt_BR.md) | **English**

## Quick Installation

1. **Setup Environment:**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

2. **Run Application:**
   ```bash
   source .venv/bin/activate
   python src/main.py
   ```

## New Features v1.1

- **🖥️ Smart Window**: Starts at 80% of screen (10% padding)
- **🗖 Maximize Button**: In the upper right corner
- **⌨️ Shortcuts**: F11, Ctrl+M to maximize, ESC to restore
- **💡 Tooltips**: Hints when hovering the mouse

## Generate Windows Executable

```bash
chmod +x scripts/build_windows.bat
./scripts/build_windows.bat
```

The `Sheetwise_v1.exe` file will be created in `dist/`

## Generate Linux Executable

```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

The `Sheetwise_v1` file will be created in `dist/`

## Example Files

In the `docs/exemplos/` folder you'll find test files:
- `clientes.csv` - Customer data
- `vendas.csv` - Sales data  
- `enderecos.csv` - Addresses (optional)

## Data Structure

### clients.csv/xlsx
- `id`: Unique customer ID
- `name`: Customer full name

### sales.csv/xlsx  
- `client_id`: Reference to customer ID
- `product`: Product name
- `quantity`: Quantity sold
- `unit_price`: Price per unit
- `final_price`: Total sale value

### addresses.csv/xlsx (optional)
- `client_id`: Reference to customer ID
- `street`: Full address
- `neighborhood`: Neighborhood
- `city`: City

## User Interface

### Login Screen
- **Login**: Enter email of existing user
- **Register**: Enter username and email for new user
- Default test user: `test@example.com`

### Main Screen

#### 1. Folder Tab
- Select source folder containing CSV/XLSX files
- Automatic file detection (clients, sales, addresses)
- Real-time validation

#### 2. Files Tab
- View detected files
- Validate file structure
- Check required columns

#### 3. Analysis Tab
- Enter protocol number
- Enter department name
- Select output file location
- Click "Analyze" to generate report

#### 4. Executions Tab
- View analysis history
- Filter by date
- Delete old executions
- Refresh list

#### 5. Settings Tab
- **Theme**: Choose interface theme
- **Language**: Switch between English and Portuguese
- **Dark Mode**: Enable/disable dark mode
- Changes are saved automatically

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F11` | Toggle maximize/restore window |
| `Ctrl+M` | Toggle maximize/restore window |
| `ESC` | Restore window to normal size |
| `Enter` | Submit form (login screen) |

## Generated Report

The analysis generates a `.txt` file with:

### Execution Information
- Protocol number
- Department
- Execution date
- Source folder path
- Result file path

### General Statistics
- Total customers
- Total sales
- Total addresses
- Total revenue
- Average ticket
- Total product quantity

### Top 5 Best-Selling Products
- Product name
- Quantity sold
- Total revenue

### Top 5 Customers (by revenue)
- Customer ID
- Total revenue
- Total items purchased

### Data Integrity Analysis
- Customers without sales
- Sales with non-existent customer
- Customers without address
- Address coverage percentage

## Troubleshooting

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

### Problem: Files not recognized
**Solution:** Verify file names are correct:
- `clientes.csv` or `clientes.xlsx` (Portuguese names still work)
- `vendas.csv` or `vendas.xlsx`
- `enderecos.csv` or `enderecos.xlsx` (optional)

### Problem: Invalid columns
**Solution:** Check if files have required columns:

**clients:**
- `id` and `nome` OR `name`

**sales:**
- `cliente_id`, `produto`, `quantidade`, `preco_unitario`, `preco_final`

**addresses:**
- `cliente_id`, `rua`, `bairro`, `cidade`

### Problem: Database error
**Solution:** Delete database and restart
```bash
rm -rf database/sheetwise.db
python src/main.py
```

### Problem: Executable not working
**Solution:** Rebuild with clean environment
```bash
rm -rf build/ dist/ *.spec
./scripts/build_linux.sh  # or build_windows.bat on Windows
```

## Development Tips

### Adding New Translations

Edit `src/static/i18n/en.json` or `pt.json`:

```json
{
  "your_key": {
    "subkey": "Your translated text"
  }
}
```

Use in code:
```python
from utils.i18n_manager import _
text = _('your_key.subkey')
```

### Changing Default Theme

Edit `src/models/database.py`:
```python
# In ConfigurationManager.get_configuration_or_create()
config = {
    'theme': 'equilux',  # Change here
    'language': 'en',
    'dark_mode': True
}
```

### Adding New Themes

Edit `src/models/database.py`:
```python
def get_available_themes(self) -> Dict[str, str]:
    return {
        'arc': 'Arc',
        'equilux': 'Equilux (Dark)',
        'your_theme': 'Your Theme Name'  # Add here
    }
```

## Performance Tips

- Close unused tabs in main screen
- Delete old executions regularly
- Use CSV format for faster processing
- Keep file sizes under 100MB for best performance

## Data Privacy

- All data is stored locally in SQLite database
- No data is sent to external servers
- Database file: `database/sheetwise.db`
- To reset all data: delete database file

## Backup Recommendations

Regularly backup:
1. `database/sheetwise.db` - User data and configurations
2. Generated report files
3. Source CSV/XLSX files

## Support

- GitHub Issues: Report bugs or request features
- Documentation: Check README.md for detailed information
- Portuguese Guide: See [GUIDE.pt_BR.md](docs/pt_BR/GUIDE.pt_BR.md)

---

For more detailed information, see the [full documentation](README.md).
