@echo off
echo Setting up Veeresh AI Bot...

:: Create required directories
mkdir config
mkdir logs
mkdir user_memories

:: Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

:: Create virtual environment
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

:: Activate and install dependencies
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Setup completed successfully!
echo Run the bot using: python src\main.py
pause