@echo off
REM First-time Git setup script

echo.
echo ============================================
echo   GIT SETUP WIZARD
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo Step 1: Configure Git
echo ----------------------
echo.
set /p username="Enter your name: "
set /p email="Enter your email: "

git config --global user.name "%username%"
git config --global user.email "%email%"

echo.
echo ✓ Git configured!
echo.

echo Step 2: Initialize Repository
echo ------------------------------
echo.

if exist ".git" (
    echo Repository already initialized.
) else (
    git init
    echo ✓ Repository initialized!
)

echo.
echo Step 3: Add Files
echo ------------------
echo.
git add .
echo ✓ Files added!

echo.
echo Step 4: Create Initial Commit
echo ------------------------------
echo.
git commit -m "Initial commit: Broadcast Server with GUI and CLI"
echo ✓ Initial commit created!

echo.
echo Step 5: Connect to GitHub
echo -------------------------
echo.
echo Now you need to:
echo 1. Go to https://github.com/new
echo 2. Create a new repository named: broadcast-server
echo 3. Do NOT initialize with README or .gitignore
echo 4. Copy the repository URL
echo.
set /p repo_url="Paste your repository URL (https://github.com/username/repo.git): "

git remote add origin %repo_url%

echo.
echo Step 6: Push to GitHub
echo ----------------------
echo.
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo Push failed. You may need to authenticate.
    echo.
    echo Create a Personal Access Token:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Generate new token (classic)
    echo 3. Select 'repo' scope
    echo 4. Copy the token
    echo 5. Use it as password when prompted
    echo.
    pause
    git push -u origin main
)

echo.
echo ============================================
echo   SETUP COMPLETE!
echo ============================================
echo.
echo Your repository is now on GitHub!
echo URL: %repo_url%
echo.
echo Future pushes: Use git-push.bat
echo.
pause
