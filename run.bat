@echo off
title Honda Atlas Autonomous Neural Concierge & Voice Intelligence System
cls
echo ===============================================================================
echo   HONDA ATLAS AUTONOMOUS NEURAL CONCIERGE ^& VOICE INTELLIGENCE SYSTEM
echo   Honda Atlas Cars (Pakistan) Limited - Executive AI Engine
echo   Engineered by Engr. Muhaiman Awan
echo ===============================================================================
echo.

cd /d "%~dp0"

IF EXIST "venv\Scripts\python.exe" (
    echo [*] Utilizing dedicated virtual environment...
    set PYTHON_EXEC=venv\Scripts\python.exe
) ELSE (
    echo [*] Virtual environment not detected. Checking system Python...
    where py >nul 2>nul
    IF %ERRORLEVEL% EQU 0 (
        set PYTHON_EXEC=py
    ) ELSE (
        set PYTHON_EXEC=python
    )
)

echo [*] Initializing SQLite database and verifying Honda Atlas inventory...
%PYTHON_EXEC% -c "import database; print('Inventory verified. Loaded models:', len(database.get_all_cars()))"

echo.
echo [*] Launching Enterprise FastAPI Server on http://127.0.0.1:8000
echo [*] Public Showroom:    http://127.0.0.1:8000
echo [*] Admin Dashboard:    http://127.0.0.1:8000/admin (Default credentials: admin / honda_admin_2025)
echo.
echo Press CTRL+C to terminate server at any time.
echo.

%PYTHON_EXEC% -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pause
