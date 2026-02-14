@echo off
REM Git Quick Push Script for Windows

echo.
echo ============================================
echo   GIT PUSH HELPER
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Download Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo Git is installed. Good!
echo.

REM Check if this is a git repository
if not exist ".git" (
    echo This is not a Git repository yet.
    echo.
    choice /C YN /M "Do you want to initialize Git now"
    if errorlevel 2 goto :end
    if errorlevel 1 goto :init_repo
)

:check_status
echo.
echo Current status:
git status
echo.

choice /C YN /M "Do you want to commit and push changes"
if errorlevel 2 goto :end
if errorlevel 1 goto :commit_push

:commit_push
echo.
set /p commit_msg="Enter commit message: "
if "%commit_msg%"=="" set commit_msg=Update files

echo.
echo Adding files...
git add .

echo Committing with message: "%commit_msg%"
git commit -m "%commit_msg%"

echo.
echo Pushing to GitHub...
git push

if errorlevel 1 (
    echo.
    echo Push failed! This might be the first push.
    echo.
    choice /C YN /M "Try: git push -u origin main"
    if errorlevel 2 goto :end
    git push -u origin main
)

echo.
echo ============================================
echo   PUSH COMPLETED!
echo ============================================
goto :end

:init_repo
echo.
echo Initializing Git repository...
git init

echo.
set /p username="Enter your name for Git: "
set /p email="Enter your email for Git: "

git config user.name "%username%"
git config user.email "%email%"

echo.
echo Adding all files...
git add .

echo.
echo Creating initial commit...
git commit -m "Initial commit: Broadcast Server with GUI and CLI"

echo.
echo ============================================
echo   REPOSITORY INITIALIZED!
echo ============================================
echo.
echo Next steps:
echo 1. Create a repository on GitHub
echo 2. Run this command (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/broadcast-server.git
echo    git push -u origin main
echo.
echo OR run: git-setup.bat
echo ============================================

:end
echo.
pause
