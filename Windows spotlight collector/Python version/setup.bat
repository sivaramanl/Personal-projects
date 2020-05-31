@echo off
schtasks /query /TN "Windows_spotlight_collector" >NUL 2>&1
if %errorlevel% EQU 0 (
schtasks /DELETE /TN "Windows_spotlight_collector" /f
)
python "%~dp0\windows_spotlight_copier_installer.py"
if exist %~dp0\install_temp(
del "%~dp0\install_temp"
schtasks /CREATE /TN "Windows_spotlight_collector" /XML "%~dp0\windows_spotlight_copier.xml"
)
