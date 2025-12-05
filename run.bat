@echo off
setlocal

REM Try to find Python 3.12 or 3.11
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.12
    goto :FOUND
)

py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.11
    goto :FOUND
)

echo.
echo [ERROR] Could not find Python 3.12 or 3.11.
pause
exit /b 1

:FOUND
echo Starting Paper2Podcast with %PYTHON_CMD%...
%PYTHON_CMD% -m streamlit run app.py
pause
