@echo off
REM Quick demo launcher for Windows
REM Double-click this file or run from command prompt

echo ========================================
echo Cognitive EW System - Demo Launcher
echo ========================================
echo.
echo Choose a demo to run:
echo.
echo 1. Setup Check (verify everything is ready)
echo 2. Data Pipeline Demo (IQ to Spectrogram)
echo 3. Classification Demo (Model Inference)
echo 4. Run All Demos
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running setup check...
    python demo_setup_check.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Running data pipeline demo...
    python demo_pipeline.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Running classification demo...
    python demo_classification.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo Running full demo sequence...
    python run_full_demo.py
    pause
) else if "%choice%"=="5" (
    exit
) else (
    echo Invalid choice!
    pause
)

