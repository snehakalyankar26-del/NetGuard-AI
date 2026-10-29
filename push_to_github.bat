@echo off
echo ======================================================================
echo NETGUARD AI - GitHub Push Helper
echo ======================================================================
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g., https://github.com/username/NETGUARD_AI.git): "
if "%REPO_URL%"=="" (
    echo [ERROR] No URL entered. Exiting.
    pause
    exit /b
)

git init
git add .
git commit -m "Initial commit: NETGUARD AI threat console & ML model"
git branch -M main
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ======================================================================
echo Successfully pushed to GitHub!
echo Repository Description to copy (< 350 chars):
echo.
type REPO_DESCRIPTION.txt
echo ======================================================================
pause

