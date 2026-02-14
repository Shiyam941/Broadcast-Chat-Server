# 🚀 Quick Git Push - 3 Simple Steps

## ✅ You Have Git Installed!

Git version detected: 2.52.0.windows.1

## 🎯 Easiest Method: Use the Helper Scripts

### Option 1: First Time Setup (Recommended)

**Double-click:** `git-setup.bat`

This wizard will:
1. Configure Git with your name/email
2. Initialize the repository
3. Create initial commit
4. Connect to GitHub
5. Push everything

### Option 2: Already Set Up? Quick Push

**Double-click:** `git-push.bat`

This script will:
1. Add all changes
2. Ask for commit message
3. Push to GitHub

## 📝 Manual Method (Copy & Paste)

Open **Git Bash** or **Command Prompt** in this folder and run:

### First Time Only:

```bash
# 1. Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Initialize repository
git init

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Broadcast Server"

# 5. Create repository on GitHub first, then connect
# Go to: https://github.com/new
# Create repo named: broadcast-server
# Then run (replace YOUR_USERNAME):

git remote add origin https://github.com/YOUR_USERNAME/broadcast-server.git
git branch -M main
git push -u origin main
```

### After First Time:

```bash
git add .
git commit -m "Your message here"
git push
```

## 🌐 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `broadcast-server`
3. Description: `Real-time WebSocket broadcast server with GUI and CLI`
4. Choose Public or Private
5. **Don't initialize** with README
6. Click "Create repository"
7. Copy the URL shown

## 🔑 Authentication

When asked for password, use a **Personal Access Token**:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `Broadcast Server`
4. Select: `repo` (full control)
5. Generate token
6. **Copy it** (you won't see it again!)
7. Use as password when pushing

## ⚡ Even Easier: GitHub Desktop

Don't want to use command line?

1. Download: https://desktop.github.com
2. Install and sign in
3. File → Add Local Repository
4. Select this folder
5. Click "Publish repository"
6. Done!

## 📁 What Gets Pushed?

All files in this folder EXCEPT:
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `.vscode/` (editor settings)
- `venv/` (virtual environments)
- `.log` files

See `.gitignore` for complete list.

## ✨ Current Project Structure

```
Project 2/
├── GUI Apps (gui_server.py, gui_client.py, launcher.py)
├── CLI App (broadcast_server.py)
├── Tests (test_server.py, demo.py)
├── Docs (README.md, GUI_GUIDE.md, etc.)
├── Batch Files (.bat helpers)
└── Config (requirements.txt, .gitignore)
```

Everything will be uploaded to GitHub!

## 🎯 Recommended Workflow

**First time:**
1. Run `git-setup.bat` (easiest)
2. OR follow manual method above

**Future updates:**
1. Make your changes
2. Run `git-push.bat`
3. Enter commit message
4. Done!

## 🆘 Need Help?

Check the detailed guide: **GIT_GUIDE.md**

---

## Quick Commands Cheat Sheet

```bash
git status          # See what changed
git add .           # Stage everything
git commit -m "msg" # Commit with message
git push            # Upload to GitHub
git pull            # Download updates
git log             # See history
```

**Ready to push?** Use `git-setup.bat` or follow the manual method above!
