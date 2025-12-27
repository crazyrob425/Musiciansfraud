# Building Windows Executable and Installer

This guide explains how to build a standalone Windows executable and installer for the Musicians Fraud AI Song Generator.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Manual Build Process](#manual-build-process)
4. [Creating the Installer](#creating-the-installer)
5. [Testing](#testing)
6. [Alternative Tools](#alternative-tools)
7. [Troubleshooting](#troubleshooting)
8. [Distribution](#distribution)

## Prerequisites

Before building the executable, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Inno Setup (for creating installer)**
   - Download from [jrsoftware.org](https://jrsoftware.org/isdl.php)
   - Install the free Inno Setup Compiler
   - Version 6.0 or higher recommended

3. **FFmpeg (for audio processing)**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract and add to system PATH
   - Required for the application to function properly

### Optional Software

- **Icon editor** (e.g., GIMP, Paint.NET) for creating custom `icon.ico`
- **UPX** (Ultimate Packer for eXecutables) for better compression (included with PyInstaller)

## Quick Start

The easiest way to build the executable is using the provided `build.bat` script:

1. **Open Command Prompt** in the project directory

2. **Run the build script:**
   ```batch
   build.bat
   ```

3. **Wait for completion** (may take 2-5 minutes)

4. **Find your executable** in `dist\MusiciansFraud.exe`

5. **Create installer** (optional):
   - Open Inno Setup Compiler
   - Open `installer.iss`
   - Click "Compile"
   - Find installer in `installer_output\`

## Manual Build Process

If you prefer to build manually or need more control:

### Step 1: Install Build Dependencies

```batch
pip install -r requirements-build.txt
```

This installs all runtime dependencies plus:
- `eel==0.16.0` - Desktop GUI wrapper
- `pyinstaller==6.3.0` - Executable builder

### Step 2: Create Application Icon (Optional)

Create or obtain an `icon.ico` file:

**Using Python PIL/Pillow:**
```python
from PIL import Image

# Create a simple icon (or use your own image)
img = Image.new('RGB', (256, 256), color='#1e3a8a')
img.save('icon.ico', format='ICO')
```

**Or download a free icon:**
- [Icons8](https://icons8.com/)
- [Flaticon](https://www.flaticon.com/)

Place the `icon.ico` file in the project root directory.

### Step 3: Build Executable with PyInstaller

Run PyInstaller with the provided spec file:

```batch
pyinstaller musiciansfraud.spec --clean
```

**Build Options:**
- `--clean` - Clean PyInstaller cache before building
- `--log-level=DEBUG` - Show detailed build information
- `--noconfirm` - Replace output directory without confirmation

**What happens:**
- PyInstaller analyzes `gui_app.py` and dependencies
- Bundles all Python modules, libraries, and data files
- Creates single executable in `dist\MusiciansFraud.exe`
- Includes templates folder and output directory
- Hides console window (windowed application)

### Step 4: Test the Executable

Before creating an installer, test the executable:

```batch
cd dist
MusiciansFraud.exe
```

The application should:
- Launch without errors
- Open a desktop window (1200x800)
- Display the web interface
- Allow you to generate lyrics and songs
- Save files to the output directory

## Creating the Installer

### Using Inno Setup (Recommended)

1. **Open Inno Setup Compiler**

2. **Load the script:**
   - File → Open
   - Select `installer.iss`

3. **Review configuration:**
   - Application name: Musicians Fraud AI Song Generator
   - Version: 1.0.0
   - Output: `installer_output\MusiciansFraud_Setup_v1.0.0.exe`

4. **Compile:**
   - Build → Compile (or press Ctrl+F9)
   - Wait for compilation (30-60 seconds)

5. **Find your installer:**
   - Located in `installer_output\` directory
   - Filename: `MusiciansFraud_Setup_v1.0.0.exe`

### Installer Features

The created installer includes:

- **Modern wizard interface** with branding
- **License agreement** (GPL v2)
- **Custom install location** (default: Program Files)
- **Desktop shortcut** (optional, unchecked by default)
- **Quick launch icon** (optional, for Windows 7)
- **Start Menu entries** (application and uninstaller)
- **Uninstaller** for clean removal
- **Documentation** (README.md, LICENSE, QUICKSTART.md)
- **LZMA2 compression** for smaller file size

## Testing

### Testing the Executable

1. **Initial Launch:**
   ```batch
   dist\MusiciansFraud.exe
   ```
   - Should open desktop window
   - No console window should appear
   - Interface should be responsive

2. **Functionality Test:**
   - Select a genre
   - Enter a topic
   - Generate lyrics
   - Generate song structure
   - Generate audio
   - Download MP3 file

3. **File Output:**
   - Check `output\` directory for generated files
   - Verify MP3 files play correctly

### Testing the Installer

1. **Run the installer:**
   ```batch
   installer_output\MusiciansFraud_Setup_v1.0.0.exe
   ```

2. **Follow installation wizard:**
   - Accept license
   - Choose install location
   - Select optional shortcuts
   - Complete installation

3. **Launch from Start Menu:**
   - Check Start Menu for "Musicians Fraud AI Song Generator"
   - Launch the application
   - Test functionality

4. **Test Uninstaller:**
   - Start Menu → Uninstall
   - Or Control Panel → Programs and Features
   - Verify clean removal

## Alternative Tools

### NSIS (Nullsoft Scriptable Install System)

Alternative to Inno Setup for creating installers.

**Example NSIS script:**

```nsis
!define APP_NAME "Musicians Fraud AI Song Generator"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "crazyrob425"
!define APP_EXE "MusiciansFraud.exe"

Name "${APP_NAME}"
OutFile "MusiciansFraud_Setup_v${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"

Page directory
Page instfiles

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\${APP_EXE}"
    File "README.md"
    File "LICENSE"
    File "QUICKSTART.md"
    
    CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\${APP_EXE}"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\QUICKSTART.md"
    Delete "$INSTDIR\Uninstall.exe"
    Delete "$SMPROGRAMS\${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir "$INSTDIR"
SectionEnd
```

**To use:**
1. Install NSIS from [nsis.sourceforge.io](https://nsis.sourceforge.io/)
2. Save script as `installer.nsi`
3. Right-click → Compile NSIS Script

### auto-py-to-exe (GUI Tool)

A graphical alternative to command-line PyInstaller.

**Installation:**
```batch
pip install auto-py-to-exe
```

**Usage:**
1. Run `auto-py-to-exe`
2. Select `gui_app.py` as script
3. Choose "One File" mode
4. Select "Window Based" (no console)
5. Add icon file
6. Add data files (templates, output)
7. Add hidden imports
8. Click "Convert .py to .exe"

## Troubleshooting

### Common Issues

#### 1. Missing DLL Errors

**Problem:** Application fails to start with missing DLL message.

**Solutions:**
- Install Microsoft Visual C++ Redistributable
- Add `--collect-all <package>` to PyInstaller command
- Check hidden imports in `musiciansfraud.spec`

#### 2. Module Not Found

**Problem:** `ModuleNotFoundError` when running executable.

**Solutions:**
- Add missing module to `hiddenimports` in `musiciansfraud.spec`
- Example: `'flask.ext.cors'`, `'numpy.core._methods'`
- Rebuild with `--clean` flag

#### 3. Large File Size

**Problem:** Executable is very large (>100MB).

**Solutions:**
- Enable UPX compression: `upx=True` (already enabled)
- Exclude unnecessary packages in spec file
- Use `--exclude-module <module>` for unneeded imports
- Consider two-file mode instead of one-file

**Example exclusions:**
```python
excludes=['matplotlib', 'tkinter', 'unittest', 'test'],
```

#### 4. Antivirus False Positives

**Problem:** Antivirus flags the executable as malware.

**Solutions:**
- Sign the executable with a code signing certificate
- Submit false positive report to antivirus vendor
- Build with `--debug=all` to help diagnosis
- Use VirusTotal to verify it's a false positive

#### 5. Templates Not Found

**Problem:** Application can't find HTML templates.

**Solutions:**
- Verify `datas` includes templates in spec file
- Check template paths use `os.path.join()`
- Test with `--onedir` mode first
- Add print statements to debug file paths

#### 6. Eel Chrome Mode Not Working

**Problem:** Eel fails to open in Chrome mode.

**Solutions:**
- Install Chrome or Edge browser
- Modify `gui_app.py` to use fallback:
  ```python
  eel.start('index.html', 
            mode='chrome',  # Will fallback to Edge or default browser
            ...
  ```
- Or explicitly set mode to `'edge'` or `'default'`

### Build Environment Issues

#### Virtual Environment

If builds fail, try in a clean virtual environment:

```batch
python -m venv build_env
build_env\Scripts\activate
pip install -r requirements-build.txt
pyinstaller musiciansfraud.spec --clean
```

#### Python Version

PyInstaller works best with:
- Python 3.8 to 3.11
- Avoid Python 3.12 (may have compatibility issues)

#### Clean Build

Force a completely clean build:

```batch
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__
pyinstaller musiciansfraud.spec --clean --noconfirm
```

## Distribution

### Distribution Checklist

Before distributing your installer:

- [ ] Test on clean Windows installation
- [ ] Test on different Windows versions (10, 11)
- [ ] Verify all features work
- [ ] Check file size is reasonable
- [ ] Include README in installer
- [ ] Include license information
- [ ] Test uninstaller completely removes files
- [ ] Scan with antivirus (VirusTotal)
- [ ] Create release notes
- [ ] Update version number

### File Size Optimization

Expected sizes:
- Executable: 40-80 MB (compressed with UPX)
- Installer: 30-60 MB (compressed with LZMA2)

### Code Signing (Optional but Recommended)

For production distribution:

1. Obtain code signing certificate
2. Sign executable:
   ```batch
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\MusiciansFraud.exe
   ```
3. Sign installer:
   ```batch
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com installer_output\MusiciansFraud_Setup_v1.0.0.exe
   ```

### Release Platforms

Consider distributing on:
- **GitHub Releases** - Free hosting for your releases
- **SourceForge** - Traditional open-source distribution
- **Microsoft Store** - Requires app signing and conversion to MSIX
- **Your website** - Direct download

### GitHub Release Example

```batch
# Create release with GitHub CLI
gh release create v1.0.0 ^
  installer_output\MusiciansFraud_Setup_v1.0.0.exe ^
  --title "Musicians Fraud v1.0.0" ^
  --notes "Initial Windows release"
```

## Additional Resources

### Documentation
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [Eel Documentation](https://github.com/python-eel/Eel)

### Tools
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) - ★11k GitHub stars
- [Eel](https://github.com/python-eel/Eel) - ★6k GitHub stars
- [Inno Setup](https://jrsoftware.org/isinfo.php) - ★4k GitHub stars
- [NSIS](https://nsis.sourceforge.io/) - Alternative installer
- [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) - GUI for PyInstaller

### Community
- [PyInstaller Issues](https://github.com/pyinstaller/pyinstaller/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/pyinstaller)
- [r/Python](https://www.reddit.com/r/Python/)

## Version History

### Version 1.0.0
- Initial Windows executable build support
- Eel-based desktop GUI wrapper
- PyInstaller single-file executable
- Inno Setup installer wizard
- Comprehensive build documentation

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review PyInstaller documentation
3. Open an issue on GitHub
4. Check existing issues for solutions

---

**Happy Building! 🚀**
