Set WshShell = CreateObject("WScript.Shell")
' Get the directory where this script is located
ScriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' Run the batch file silently (hidden window)
WshShell.Run """" & ScriptDir & "\start_desktop.bat""", 0, False
Set WshShell = Nothing
