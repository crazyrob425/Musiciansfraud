# Desktop Application Setup Guide

This guide will help you set up the AI Song Generator as a simple double-click desktop application.

## Windows Setup (Recommended Method)

### Quick Start (3 Easy Steps)

1. **Download or Clone the Repository**
   - Download the ZIP file and extract it to a folder (e.g., `C:\AIMusic`)
   - Or use Git: `git clone https://github.com/crazyrob425/Musiciansfraud.git`

2. **Run the Desktop Setup**
   - Double-click `start_desktop.bat`
   - The first time will take a few minutes to install dependencies
   - The app window will open automatically

3. **Create Desktop Shortcut (Optional)**
   - Double-click `create_desktop_shortcut.bat`
   - A shortcut will appear on your desktop
   - Double-click it anytime to launch the app

### What Gets Installed

- Python virtual environment (isolated from your system Python)
- Required Python packages (Flask, gTTS, mido, pywebview, etc.)
- Desktop shortcut (if you run the shortcut creator)

### Alternative Launch Methods

**Method 1: Silent Launch (No Console Window)**
- Double-click `AI_Song_Generator.vbs`
- App opens directly with no command window

**Method 2: With Console (See Status Messages)**
- Double-click `start_desktop.bat`
- Console window shows startup progress

**Method 3: Desktop Shortcut**
- Run `create_desktop_shortcut.bat` once
- Then double-click "AI Song Generator" on your desktop

## macOS Setup

### Installation

1. Open Terminal
2. Navigate to the app folder:
   ```bash
   cd ~/Downloads/Musiciansfraud
   ```

3. Make the launcher executable:
   ```bash
   chmod +x start_desktop.sh
   ```

4. Run the launcher:
   ```bash
   ./start_desktop.sh
   ```

### Create macOS App Bundle (Optional)

You can create a proper macOS application:

1. Open Automator
2. Create new "Application"
3. Add "Run Shell Script" action
4. Paste this script:
   ```bash
   cd /path/to/Musiciansfraud
   ./start_desktop.sh
   ```
5. Save as "AI Song Generator.app"
6. Move to Applications folder

## Linux Setup

### Ubuntu/Debian

1. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-venv python3-gi gir1.2-webkit2-4.0
   ```

2. Make launcher executable:
   ```bash
   chmod +x start_desktop.sh
   ```

3. Run:
   ```bash
   ./start_desktop.sh
   ```

### Create Desktop Entry

Create `~/.local/share/applications/ai-song-generator.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=AI Song Generator
Comment=Create AI-generated songs
Exec=/path/to/Musiciansfraud/start_desktop.sh
Icon=applications-multimedia
Terminal=false
Categories=Audio;Music;
```

## Troubleshooting

### Windows: "Python is not recognized"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try again

### Windows: Desktop mode doesn't work

**Solution 1:** The app automatically falls back to browser mode
- It will open in your default web browser instead
- All features work the same way

**Solution 2:** Install missing dependencies
```bash
pip install pywebview pywebview[winforms]
```

### macOS: Permission Denied

**Solution:**
```bash
chmod +x start_desktop.sh
./start_desktop.sh
```

### Linux: GTK/WebKit errors

**Solution:**
Install GTK and WebKit:
```bash
sudo apt-get install python3-gi gir1.2-webkit2-4.0
```

### Can't connect to localhost

**Problem:** ERR_CONNECTION_REFUSED when accessing http://localhost:5000

**Solution:**
1. Close any running instances of the app
2. Check if port 5000 is in use:
   - Windows: `netstat -ano | findstr :5000`
   - Mac/Linux: `lsof -i :5000`
3. Restart the application

### App won't start

**Check these:**
1. Python 3.8 or higher installed
2. Internet connection (for initial setup and TTS features)
3. Enough disk space (at least 500MB free)
4. Antivirus not blocking Python or the app

## How It Works

### Desktop Mode
- Creates a native application window using PyWebView
- Runs Flask server in the background
- Automatically opens when you start the app
- Closes server when you close the window
- No browser needed!

### Browser Mode (Fallback)
- Opens in your default web browser
- Same features as desktop mode
- Server stays running until you close the terminal/command window

## Features Available

All features work in both desktop and browser modes:
- ✅ Text-to-Speech vocals
- ✅ MIDI export
- ✅ Enhanced audio synthesis
- ✅ Full song generation
- ✅ Project save/load
- ✅ Genre selection
- ✅ Instrument configuration

## Uninstallation

### Windows
1. Delete the application folder
2. Delete desktop shortcut (if created)
3. Done! No system files modified

### macOS/Linux
1. Delete the application folder
2. Remove .desktop file (if created)
3. Done!

The app is completely self-contained in its folder.

## Advanced: Manual Installation

If you prefer to install manually:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run desktop mode
python desktop_app.py

# Or run web mode
python app.py
```

## Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review console output for error messages
3. Make sure Python 3.8+ is installed
4. Ensure you have internet connection
5. Open an issue on GitHub with error details

## Tips for Best Experience

1. **First Launch**: Takes longer due to dependency installation
2. **Subsequent Launches**: Much faster (1-2 seconds)
3. **Desktop Shortcut**: Most convenient for daily use
4. **Keep Updated**: Pull latest changes from Git regularly
5. **Internet**: Required for TTS vocals (gTTS)

## System Requirements

**Minimum:**
- Windows 7/10/11, macOS 10.12+, or Ubuntu 18.04+
- Python 3.8 or higher
- 2GB RAM
- 500MB free disk space
- Internet connection (for TTS features)

**Recommended:**
- Windows 10/11, macOS 12+, or Ubuntu 20.04+
- Python 3.10 or higher
- 4GB RAM
- 1GB free disk space
- Broadband internet connection

Enjoy creating music! 🎵
