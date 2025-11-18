@echo off
REM SUTRA Publishing Script for Windows
REM This script automates the process of publishing to PyPI

echo ======================================
echo SUTRA Publishing Script
echo ======================================

REM Check and install dependencies
echo.
echo Checking dependencies...
pip show build >nul 2>&1 || pip install build
pip show twine >nul 2>&1 || pip install twine
echo [OK] Dependencies installed

REM Clean old builds
echo.
echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
echo [OK] Old builds removed

REM Build the package
echo.
echo Building package...
python -m build
if errorlevel 1 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)
echo [OK] Package built successfully

REM Check the distribution
echo.
echo Checking distribution...
python -m twine check dist/*
if errorlevel 1 (
    echo [ERROR] Distribution check failed
    pause
    exit /b 1
)
echo [OK] Distribution check passed

REM Upload to TestPyPI
echo.
echo ======================================
echo Uploading to TestPyPI...
echo ======================================
python -m twine upload --repository testpypi dist/*

echo.
echo [OK] Uploaded to TestPyPI successfully!
echo.
echo Test installation with:
echo pip install --index-url https://test.pypi.org/simple/ --no-deps sutra
echo.

REM Ask for confirmation before uploading to PyPI
set /p REPLY="Do you want to upload to PyPI? (y/n): "
if /i "%REPLY%"=="y" (
    echo.
    echo ======================================
    echo Uploading to PyPI...
    echo ======================================
    python -m twine upload dist/*
    
    echo.
    echo ======================================
    echo [OK] Successfully published to PyPI!
    echo ======================================
    echo.
    echo Install with: pip install sutra
    echo.
) else (
    echo.
    echo [OK] Skipped PyPI upload
    echo.
)

echo Done!
pause
