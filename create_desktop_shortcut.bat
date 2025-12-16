@echo off
REM Create Desktop Shortcut for AI Song Generator

echo Creating desktop shortcut...

set SCRIPT_DIR=%~dp0
set SHORTCUT_NAME=AI Song Generator.lnk
set TARGET_PATH=%SCRIPT_DIR%AI_Song_Generator.vbs
set DESKTOP=%USERPROFILE%\Desktop

REM Create shortcut using PowerShell
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%'); $s.TargetPath = '%TARGET_PATH%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.IconLocation = 'shell32.dll,221'; $s.Description = 'AI Song Generator - Musicians Fraud'; $s.Save()"

if errorlevel 1 (
    echo ❌ Error creating shortcut
    pause
    exit /b 1
)

echo.
echo ✅ Desktop shortcut created successfully!
echo.
echo You can now double-click "AI Song Generator" on your desktop to launch the app.
echo.
pause
