@echo off
echo ================================================
echo Musicians Fraud - Build Script
echo ================================================

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt
pip install eel pyinstaller

echo.
echo Step 2: Building executable with PyInstaller...
pyinstaller musiciansfraud.spec --clean

echo.
echo Step 3: Build complete!
echo Executable location: dist\MusiciansFraud.exe

echo.
echo Step 4: To create installer, run Inno Setup Compiler
echo and compile the installer.iss file

pause
