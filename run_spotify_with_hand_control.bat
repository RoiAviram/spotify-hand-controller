@echo off

rem === activate spotify ===
start  spotify

rem == waiting few seconds to spotify work succesfuly ==
timeout /t 5 /nobreak >nul

rem === moving to project files ===
cd /d "C:\מסמכים שלי\ראיונות עבודה\projects\Spotify Hand Controller"

rem === activate main ===
py main.py
