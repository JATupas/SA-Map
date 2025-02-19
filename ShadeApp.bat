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

:: Set paths
set WKHTMLTOPDF_DIR="C:\Program Files\wkhtmltopdf\bin"
set WKHTMLTOPDF_EXEC=%WKHTMLTOPDF_DIR%\wkhtmltopdf.exe
set INSTALLER=wkhtmltox-0.12.6-1.msvc2015-win64.exe
set INSTALL_DIR=%cd%\wkhtmltopdf
set TARGET_PATH=%cd%\%INSTALLER%

:: Check if wkhtmltopdf is installed
echo Checking if wkhtmltopdf is already installed...
if exist %WKHTMLTOPDF_EXEC% (
    echo wkhtmltopdf is already installed.
) else (
    echo wkhtmltopdf not found. Installing...

    :: Check if installer is present
    if not exist %TARGET_PATH% (
        echo Error: %INSTALLER% not found in the current directory!
        echo Please place %INSTALLER% in the same folder as this script.
        pause
        exit /b 1
    )
    :: Run the installer
    echo Running the wkhtmltopdf installer...
    "%TARGET_PATH%" /quiet /norestart
    if %errorlevel%==0 (
        echo wkhtmltopdf installation successful!
    ) else (
        echo Error: Installation failed!
        pause
        exit /b 1
    )
)

:: Confirm that wkhtmltopdf is now recognized
echo Verifying wkhtmltopdf version...
wkhtmltopdf --version

set GTK_PATH="C:\Program Files\GTK3-Runtime Win64"
set GTK_EXE="gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe"

REM Check if GTK is installed by verifying the existence of the GTK folder
if not exist %GTK_PATH%\* (
    echo GTK3 runtime not found. Installing...
    start /wait %~dp0%GTK_EXE
) else (
    echo GTK3 runtime is already installed.
)

:: Start the Django server
echo Starting Django server...
start http://127.0.0.1:8000
%PYTHONHOME%\python.exe manage.py migrate
%PYTHONHOME%\python.exe manage.py runserver
pause