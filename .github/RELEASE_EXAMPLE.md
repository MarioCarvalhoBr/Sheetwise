# Example: Creating Release v1.0.0

This is a step-by-step example of creating your first release.

## Step 1: Prepare your code

```bash
# Make sure you're on main branch
git checkout main
git pull origin main

# Verify everything is working
source .venv/bin/activate
python src/main.py
```

## Step 2: Update version references (optional)

You may want to update version in:
- `pyproject.toml` (version field)
- Any changelog files
- Documentation

## Step 3: Create the release on GitHub

### Via Web Interface:

1. Go to: `https://github.com/MarioCarvalhoBr/Sheetwise/releases/new`

2. Fill in the form:
   ```
   Tag version: v1.0.0
   Target: main
   Release title: Sheetwise v1.0.0 - Initial Stable Release
   
   Description:
   ## 🎉 What's New in v1.0.0
   
   This is the first stable release of Sheetwise!
   
   ### ✨ Features
   - CSV/XLSX spreadsheet analysis
   - Customer and sales data processing
   - Detailed report generation
   - Multi-language support (EN/PT)
   - Dark mode theme
   - User authentication system
   - Execution history management
   
   ### 📦 Downloads
   
   **Windows Users:**
   - Download `Sheetwise_v1.exe` below
   - No installation needed!
   
   **Linux/macOS:**
   - Download source code
   - Follow [installation guide](../README.md#-installation-and-setup)
   
   ### 📚 Documentation
   - [README](../README.md)
   - [Quick Guide](../GUIDE.md)
   - [Portuguese Docs](../docs/pt_BR/)
   ```

3. Click **"Publish release"**

## Step 4: Monitor the build

1. Go to **Actions** tab
2. Wait for **"CD - Build and Release"** workflow to complete (~5-10 min)
3. Check for green checkmark ✅

## Step 5: Verify the executable

1. Go back to the release page
2. Refresh the page
3. In **Assets** section, you should see:
   - `Source code (zip)`
   - `Source code (tar.gz)`
   - **`Sheetwise_v1.exe`** ✨

## Step 6: Test the executable (if on Windows)

1. Download `Sheetwise_v1.exe`
2. Double-click to run
3. Verify the application works correctly

## Example GitHub CLI method:

```bash
# Install GitHub CLI if not installed
# https://cli.github.com/

# Create release
gh release create v1.0.0 \
  --title "Sheetwise v1.0.0 - Initial Stable Release" \
  --notes "First stable release with full feature set" \
  --target main

# The workflow will automatically build and attach the .exe
```

## What the workflow does automatically:

```yaml
1. Triggers on release creation
2. Spins up Windows runner
3. Installs Python 3.12
4. Installs Poetry + dependencies
5. Installs PyInstaller
6. Runs: pyinstaller [options] src\main.py
7. Verifies dist\Sheetwise_v1.exe exists
8. Uploads as artifact (90-day retention)
9. Attaches to release as downloadable asset
```

## Expected timeline:

- **0-1 min**: Workflow starts, sets up environment
- **1-3 min**: Installs Poetry and dependencies
- **3-5 min**: Builds executable with PyInstaller
- **5-7 min**: Uploads and attaches to release
- **Total**: ~5-10 minutes

## Success indicators:

✅ Green checkmark in Actions
✅ Workflow shows "success" status
✅ Release page shows `Sheetwise_v1.exe` in Assets
✅ Download works and file size is reasonable (~80-150 MB)
✅ Executable runs on Windows without errors

## Troubleshooting common issues:

### Issue: Workflow not triggered
**Solution:** Make sure you created a **release**, not just a git tag

### Issue: PyInstaller fails
**Solution:** Check all dependencies are in `pyproject.toml`

### Issue: Missing assets/icon.ico
**Solution:** Verify `assets/icon.ico` exists in repository

### Issue: Upload failed
**Solution:** Check GitHub token permissions (should be automatic)

## Next releases:

For subsequent releases, use semantic versioning:
- `v1.0.1` - Bug fix
- `v1.1.0` - New feature
- `v2.0.0` - Breaking change

The process is exactly the same, just change the version number!

---

**That's it!** Your automated release system is now set up and ready to use. 🚀
