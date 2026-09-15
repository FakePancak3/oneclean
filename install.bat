@echo off
setlocal

set "SRC=%~dp0oneclean.exe"
set "DEST=%LOCALAPPDATA%\OneClean"

if not exist "%SRC%" (
    echo Could not find oneclean.exe next to this installer.
    echo Make sure install.bat is in the same folder as oneclean.exe.
    pause
    exit /b 1
)

if not exist "%DEST%" mkdir "%DEST%"
copy /Y "%SRC%" "%DEST%\oneclean.exe" >nul

powershell -NoProfile -Command ^
    "$p = [Environment]::GetEnvironmentVariable('Path','User');" ^
    "if ($p -notlike '*%DEST%*') {" ^
    "    [Environment]::SetEnvironmentVariable('Path', $p + ';%DEST%', 'User');" ^
    "    Write-Host 'Added OneClean to PATH.'" ^
    "} else {" ^
    "    Write-Host 'OneClean is already in PATH.'" ^
    "}"

echo.
echo Installed to %DEST%
echo Close and reopen Command Prompt, then just type: oneclean
pause
