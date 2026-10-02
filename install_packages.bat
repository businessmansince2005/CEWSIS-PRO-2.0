@echo off
REM Simple package installer for Cognitive EW System
REM This installs all required packages

echo ========================================
echo Installing Required Packages
echo ========================================
echo.
echo This will install:
echo - numpy, scipy, scikit-learn
echo - matplotlib, torch, pandas
echo - pyyaml, jupyter
echo.
echo This may take 2-3 minutes...
echo.

python -m pip install --upgrade pip
python -m pip install numpy scipy scikit-learn matplotlib torch pandas pyyaml jupyter

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now run: python demo_setup_check.py
echo.
pause




