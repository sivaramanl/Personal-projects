@echo off
schtasks /query /TN "Windows_spotlight_collector" >NUL 2>&1
if %errorlevel% EQU 0 (
schtasks /DELETE /TN "Windows_spotlight_collector" /f
schtasks /CREATE /TN "Windows_spotlight_collector" /XML "%~dp0\windows_spotlight_copier.xml"
) else (
schtasks /CREATE /TN "Windows_spotlight_collector" /XML "%~dp0\windows_spotlight_copier.xml"
)
exit
