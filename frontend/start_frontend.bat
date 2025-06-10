@echo off
chcp 65001
echo Installing frontend dependencies...
call npm install

echo Starting frontend development server...
call npm start

pause 