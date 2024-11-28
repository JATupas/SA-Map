@echo off

:: Set the current working directory to the script's location
cd /d %~dp0

:: Set environment variables for Python embedded runtime
set PYTHONHOME=%cd%\python-embedded
set PYTHONPATH=%PYTHONHOME%;%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs
set PATH=%PYTHONHOME%;%PATH%

echo Python home: %PYTHONHOME%
echo Python paths: %PYTHONPATH%

%PYTHONHOME%\python.exe --version

:: Install dependencies (only run this if you haven't installed them yet)
if not exist "%PYTHONHOME%\Scripts\pip.exe" (
    echo Installing pip...
    "%PYTHONHOME%\python.exe" get-pip.py
)
echo Installing required dependencies...
"%PYTHONHOME%\Scripts\pip.exe" install -r requirements.txt

:: Start the Django development server
echo Starting Django server...
"%PYTHONHOME%\python.exe" manage.py runserver

:: Pause the command window to see any errors (optional)
pause