@echo off

:: Set variables
set EMBEDDED_PYTHON_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip
set ZIP_FILE=python-embedded-3.12.zip
set TARGET_DIR=%cd%\python-embedded

:: Check if Python embedded is already set up
if not exist "%TARGET_DIR%" (
    echo Python embedded not found. Setting it up...

    :: Download the zip file
    echo Downloading Python embedded...
    powershell -Command "Invoke-WebRequest -Uri '%EMBEDDED_PYTHON_URL%' -OutFile '%ZIP_FILE%'"

    :: Check if download was successful
    if not exist "%ZIP_FILE%" (
        echo Error: Failed to download Python embedded zip file!
        pause
        exit /b 1
    )

    :: Extract the zip file
    echo Extracting files...
    powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%TARGET_DIR%'"

    :: Clean up the zip file
    echo Cleaning up...
    del "%ZIP_FILE%"
)

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

      :: Check if pip.exe exists to confirm installation
    if not exist "%PYTHONHOME%\Scripts\pip.exe" (
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
