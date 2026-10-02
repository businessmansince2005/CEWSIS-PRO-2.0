@echo off
REM ========================================
REM COGNITIVE EW SYSTEM - QUICK START
REM ========================================
REM Run this file to set up and test everything

echo.
echo ========================================
echo Cognitive EW System - Quick Start
echo ========================================
echo.
echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Step 2: Checking if packages are installed...
python -c "import numpy" 2>nul
if errorlevel 1 (
    echo Packages not installed. Installing now...
    echo This will take 2-3 minutes...
    call install_packages.bat
) else (
    echo Packages already installed!
)

echo.
echo Step 3: Running setup check...
python demo_setup_check.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python demo_pipeline.py
echo 2. Run: python demo_classification.py
echo.
echo Or double-click: run_demo.bat
echo.
pause




