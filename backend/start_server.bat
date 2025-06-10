@echo off
chcp 65001
echo Checking Python environment...

set PYTHON_PATH=C:\Python\Python312\python.exe
if not exist "%PYTHON_PATH%" (
    echo Error: Python interpreter not found at C:\Python\Python312\python.exe
    pause
    exit /b 1
)

echo Installing dependencies...
"%PYTHON_PATH%" -m pip install -r requirements.txt

echo Starting server...
"%PYTHON_PATH%" -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

pause 