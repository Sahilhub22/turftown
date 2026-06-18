@echo off
echo ================================================
echo   TurfTown - Turf Booking Platform
echo   Starting server at http://localhost:5000
echo ================================================
echo.

cd /d "%~dp0"

:: Check if database exists, if not seed it
if not exist "instance\turftown.db" (
    echo First run detected - seeding database...
    python seed.py
    echo.
)

echo Starting Flask development server...
echo Open your browser: http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py
pause
