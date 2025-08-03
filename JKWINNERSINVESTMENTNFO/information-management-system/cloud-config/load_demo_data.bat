@echo off
REM JKWI Demo Data Loader for Windows
REM This script loads demo members into the JKWI cloud system

echo ==========================================
echo    JKWI Demo Data Loader
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if demo data file exists
if not exist "jkwi_demo_data.json" (
    echo ERROR: Demo data file not found!
    echo Expected: jkwi_demo_data.json
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

REM Check if JKWI system is running
echo Checking if JKWI system is running...
python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=5)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: JKWI system doesn't seem to be running
    echo Please start the system first with: python app.py
    echo.
    set /p choice="Continue anyway? (y/N): "
    if /i not "%choice%"=="y" (
        echo Cancelled by user
        pause
        exit /b 1
    )
)

echo.
echo Loading demo data into JKWI system...
echo Please wait...
echo.

REM Load the demo data
python load_demo_data.py

REM Check result
if errorlevel 1 (
    echo.
    echo ERROR: Demo data loading failed!
    echo Check the output above for details
) else (
    echo.
    echo SUCCESS: Demo data loaded successfully!
    echo.
    echo You can now access the system at: http://localhost:5000
    echo.
    echo Demo Login Credentials:
    echo   Username: jkwi_admin
    echo   Password: Admin123!
    echo.
    echo Or try any demo member:
    echo   Username: sipho.mthembu123
    echo   Password: password123
)

echo.
echo Press any key to exit...
pause >nul
