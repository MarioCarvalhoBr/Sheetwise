# Release Instructions

## How to create a new release

### 1. Via GitHub Web Interface (Recommended)

1. Go to the repository page on GitHub
2. Click on **"Releases"** in the right sidebar
3. Click on **"Draft a new release"**
4. Fill in:
   - **Tag version**: e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`
   - **Release title**: e.g., `Sheetwise v1.0.0`
   - **Description**: Describe the version changes
5. Click on **"Publish release"**

### 2. Via Git Command Line

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create the release on GitHub via web interface
```

## What happens automatically

When you create a release, the CD workflow will automatically:

1. ✅ Set up Windows environment on GitHub Actions
2. ✅ Install Python 3.12
3. ✅ Install Poetry and all dependencies
4. ✅ Install PyInstaller
5. ✅ Build the Windows executable
6. ✅ Verify that `Sheetwise_v1.exe` was generated
7. ✅ Upload the executable as artifact (available for 90 days)
8. ✅ Attach the executable to the release for public download

## Downloading the executable

After the release is created and the workflow completes (about 5-10 minutes):

1. Go to the release page on GitHub
2. In the **"Assets"** section, you'll see:
   - `Source code (zip)`
   - `Source code (tar.gz)`
   - **`Sheetwise_v1.exe`** ← Windows executable ready to download

## Check build status

1. Go to the **"Actions"** tab of the repository
2. Look for the **"CD - Build and Release"** workflow
3. Click on the workflow for your release to see the logs
4. Verify that all steps completed successfully ✅

## Semantic Versioning

We recommend using [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., `v1.2.3`)
- **MAJOR**: Incompatible API changes
- **MINOR**: New backwards-compatible functionality
- **PATCH**: Bug fixes

Examples:
- `v1.0.0` - First stable version
- `v1.1.0` - New feature added
- `v1.1.1` - Bug fix
- `v2.0.0` - Breaking change

## Troubleshooting

### Workflow didn't run
- Verify you created a **release**, not just a tag
- Check in Actions if the workflow is enabled

### Build failed
- Go to Actions → failed workflow → detailed logs
- Verify all dependencies are in `pyproject.toml`
- Check if `assets/icon.ico` file exists

### Executable doesn't appear in release
- Wait for workflow to complete (5-10 minutes)
- Reload the release page
- Check logs of "Upload to Release" step

## Test the workflow manually

You can test the workflow without creating a release:

1. Go to **Actions** on GitHub
2. Select **"CD - Build and Release"**
3. Click **"Run workflow"**
4. Select the `main` branch
5. Click **"Run workflow"**

The executable will be generated and available as an artifact (but not attached to any release).

---

**Portuguese version:** [RELEASE.md](RELEASE.md)
