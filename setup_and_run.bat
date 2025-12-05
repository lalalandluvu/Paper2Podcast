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
echo You are currently running Python 3.14 which is too new for these libraries.
echo.
echo Please download and install Python 3.12 from:
echo https://www.python.org/downloads/release/python-3120/
echo.
pause
exit /b 1

:FOUND
echo Using %PYTHON_CMD%
echo Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b %errorlevel%
)

echo Starting Paper2Podcast...
%PYTHON_CMD% -m streamlit run app.py
pause
