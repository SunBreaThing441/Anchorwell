@echo off
title AnchorWell - UNESCO Mental Support Grid
echo =========================================================================
echo  ANCHORWELL: UNESCO MENTAL SUPPORT GRID
echo  Starting Persistence Tier (MySQL) and Presentation Gateway (Port 8000)
echo =========================================================================
echo.

:: 1. Check & Start MySQL if not running on port 3306
netstat -ano | findstr :3306 >nul
if %errorlevel% neq 0 (
    echo [1/3] Initializing MySQL persistence tier on port 3306...
    if exist "C:\xampp\mysql\bin\mysqld.exe" (
        start "" /b "C:\xampp\mysql\bin\mysqld.exe" --defaults-file="C:\xampp\mysql\bin\my.ini" --standalone
        timeout /t 2 /nobreak >nul
    ) else (
        echo [WARNING] MySQL not found at C:\xampp\mysql\bin\mysqld.exe. Please ensure MySQL is running.
    )
) else (
    echo [1/3] MySQL persistence service is already active on port 3306.
)

:: 2. Set Python Interpreter Path
set PYTHON_EXE=C:\Users\somnathsinha\AppData\Roaming\uv\python\cpython-3.10-windows-x86_64-none\python.exe
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)

echo [2/3] Launching Django WSGI Server on http://127.0.0.1:8000/ ...
echo.
echo =========================================================================
echo  AnchorWell Console is now live!
echo  Access URL: http://127.0.0.1:8000/
echo  Press Ctrl+C to terminate the server.
echo =========================================================================
echo.

:: 3. Launch browser and start Django server
start http://127.0.0.1:8000/
cd /d "D:\PROJECT_S\PsychBuddy\Psychbuddy"
"%PYTHON_EXE%" manage.py runserver 127.0.0.1:8000
