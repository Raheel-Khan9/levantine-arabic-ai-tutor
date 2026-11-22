@echo off
title Push Ahlan AI to GitHub
echo ===============================================================
echo  Pushing Ahlan AI to https://github.com/Raheel-Khan9/levantine-arabic-ai-tutor
echo ===============================================================
echo.
cd /d "%~dp0"
git push -u origin main
echo.
if %errorlevel% neq 0 (
    echo [!] If this is your first push, please make sure you created the empty repo at:
    echo     https://github.com/new?name=levantine-arabic-ai-tutor
) else (
    echo [OK] Successfully pushed to https://github.com/Raheel-Khan9/levantine-arabic-ai-tutor!
)
echo.
pause
