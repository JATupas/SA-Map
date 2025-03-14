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

set "GTK_PATH=C:\Program Files\GTK3-Runtime Win64\gtk3_runtime_uninst.exe"
set "GTK_FOLDER=C:\Program Files\GTK3-Runtime Win64\"
set "GTK_EXE=gtk3.exe"

:check_installation
REM Check if GTK is installed by verifying the existence of the GTK folder
if not exist "%GTK_PATH%*" (
    echo GTK3 runtime not found in "%GTK_FOLDER%". Installing...
    start /wait "" "%~dp0%GTK_EXE%"
    
    REM Check again after installation
    echo.
    echo Verifying installation...
    if not exist "%GTK_PATH%*" (
        echo Installation failed or incomplete. Retrying...
        goto check_installation
    ) else (
        echo GTK3 runtime successfully installed.
    )
) else (
    echo GTK3 runtime is already installed.
)

:: Check if TileServer-GL is installed
where tileserver-gl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing TileServer-GL...
    npm install -g tileserver-gl
    
    :: Ensure npm is available
    where npm >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: npm not found. Ensure Node.js installed correctly.
        pause
        exit /b 1
    )

    :: Run npm install with elevated privileges
    powershell Start-Process npm -ArgumentList 'install -g tileserver-gl' -Verb RunAs -Wait
)

:: Verify TileServer-GL installation
where tileserver-gl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: TileServer-GL installation failed.
    pause
    exit /b 1
)

:: Start TileServer-GL
echo Starting TileServer-GL...
start "" cmd /k "tileserver-gl --mbtiles "%CD%\myapp\static\maps\osm-2020-02-10-v3.11_asia_philippines.mbtiles" --port 8080"
timeout /t 5

:: Start Django server
echo Starting Django server...
start http://127.0.0.1:8000
%PYTHONHOME%\python.exe manage.py migrate
%PYTHONHOME%\python.exe manage.py runserver
pause