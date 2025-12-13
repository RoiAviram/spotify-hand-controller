@echo off

rem === מפעיל את ספוטיפיי ===
start  spotify

rem מחכים כמה שניות שיסתדר
timeout /t 5 /nobreak >nul

rem === עוברים לתיקיית הפרויקט ===
cd /d "C:\מסמכים שלי\ראיונות עבודה\projects\Spotify Hand Controller"

rem === מפעילים את הסקריפט שלך ===
py main.py
