@echo off
REM JKWI Cloud System Setup and Start Script
echo ==============================================
echo JK Winners Investment - Cloud System Setup
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Navigate to cloud config directory
cd /d "%~dp0..\information-management-system\cloud-config"

if not exist "app.py" (
    echo ❌ Cloud system files not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

echo 📦 Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    echo Please check your internet connection and Python setup
    pause
    exit /b 1
)

echo ✅ Packages installed successfully
echo.

REM Create environment file if it doesn't exist
if not exist ".env" (
    echo 🔧 Creating environment configuration...
    echo SECRET_KEY=jkwi-secret-key-change-in-production > .env
    echo FLASK_ENV=development >> .env
    echo DATABASE_URL=sqlite:///jkwi_local.db >> .env
    echo JWT_SECRET_KEY=jkwi-jwt-secret-change-in-production >> .env
    echo ✅ Environment file created
)

echo.
echo 🚀 Starting JKWI Cloud System...
echo.
echo The system will be available at: http://localhost:5000
echo Health check: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop the server
echo ==============================================
echo.

REM Start the Flask application
python app.py

pause
