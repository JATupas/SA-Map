@echo off
:: Set environment variables
set PYTHONHOME=%cd%\python-embedded
set PYTHONPATH=%cd%;%PYTHONHOME%\Lib;%PYTHONHOME%\Lib\site-packages;%PYTHONHOME%\DLLs
set PATH=%PYTHONHOME%;%PYTHONHOME%\Scripts;%PATH%

:: Confirm Python home and version
echo Python Home: %PYTHONHOME%
%PYTHONHOME%\python.exe --version

:: Ensure Lib\site-packages is in python312._pth
echo Configuring python312._pth...
if not exist "%PYTHONHOME%\python312._pth" (
    echo Error: python312._pth file not found!
    pause
    exit /b
)
findstr /c:"Lib\site-packages" "%PYTHONHOME%\python312._pth" >nul || (
    echo Lib\site-packages>>"%PYTHONHOME%\python312._pth"
    echo Added Lib\site-packages to python312._pth
)

:: Install pip if not already installed
if not exist "%PYTHONHOME%\Scripts\pip.exe" (
    echo Installing pip...
    if not exist "get-pip.py" (
        echo Downloading get-pip.py...
        powershell -Command "& { (New-Object Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py') }"
    )
    %PYTHONHOME%\python.exe get-pip.py
    if %errorlevel% neq 0 (
        echo Failed to install pip. Exiting...
        pause
        exit /b
    )
)

:: Upgrade pip, setuptools, and wheel
echo Upgrading pip, setuptools, and wheel...
%PYTHONHOME%\python.exe -m pip install --upgrade pip setuptools wheel

:: Install required dependencies
echo Installing required dependencies from requirements.txt...
%PYTHONHOME%\python.exe -m pip install -r requirements.txt

:: Start the Django server
echo Starting Django server...
%PYTHONHOME%\python.exe manage.py runserver
pause
