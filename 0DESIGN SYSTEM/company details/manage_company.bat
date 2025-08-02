@echo off
REM Company Details Manager - Windows Batch File
REM This script provides easy access to company details management

set COMPANY_DIR=C:\Users\jacob\Documents\0 company info\company details
cd /d "%COMPANY_DIR%"

echo.
echo ===================================
echo    JK WINNERS INVESTMENT
echo    Company Details Manager
echo ===================================
echo.

:MENU
echo Choose an option:
echo.
echo 1. View company details
echo 2. Edit company details
echo 3. Update all file formats
echo 4. Validate all files
echo 5. Open company folder
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto VIEW
if "%choice%"=="2" goto EDIT
if "%choice%"=="3" goto UPDATE
if "%choice%"=="4" goto VALIDATE
if "%choice%"=="5" goto OPEN_FOLDER
if "%choice%"=="6" goto EXIT
goto INVALID

:VIEW
echo.
echo Current Company Details:
echo ========================
python company_manager.py
echo.
pause
goto MENU

:EDIT
echo.
echo Starting interactive editor...
python company_manager.py --edit
echo.
pause
goto MENU

:UPDATE
echo.
echo Updating all file formats...
python company_manager.py --update-all
echo.
pause
goto MENU

:VALIDATE
echo.
echo Validating all files...
python company_manager.py --validate
echo.
pause
goto MENU

:OPEN_FOLDER
echo.
echo Opening company details folder...
explorer "%COMPANY_DIR%"
goto MENU

:INVALID
echo.
echo Invalid choice. Please try again.
echo.
goto MENU

:EXIT
echo.
echo Goodbye!
exit /b 0
