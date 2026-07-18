@echo off
echo ===================================================
echo   🔮 MoneyLens - Starting Local Development Servers
echo ===================================================

:: 1. Initialize and Seed SQLite database if it doesn't exist yet
if not exist backend\moneylens.db (
    echo [System] Database not found. Initializing and seeding database...
    cd backend
    call .\venv\Scripts\python database\seed.py
    cd ..
)

:: 2. Launch the backend Flask server in a new command window
echo [System] Starting Backend API Server on port 5000...
start "MoneyLens Backend API" cmd /k "cd backend && call .\venv\Scripts\python app.py"

:: 3. Launch the frontend HTTP server in a new command window
echo [System] Starting Frontend Web Server on port 8000...
start "MoneyLens Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

:: 4. Pause briefly to allow servers to bind, then launch browser
timeout /t 2 /nobreak >nul
echo [System] Opening MoneyLens in your web browser...
start http://localhost:8000

echo ===================================================
echo   Active! Keep the spawned cmd windows open.
echo   Press any key to close this setup helper.
echo ===================================================
pause >nul
