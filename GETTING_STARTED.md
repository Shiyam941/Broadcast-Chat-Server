# 🚀 Getting Started - Broadcast Server

## Welcome!

This guide will help you get up and running with the Broadcast Server in just a few minutes!

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.7 or higher installed
- ✅ pip (Python package installer)

**Check your Python version:**
```bash
python --version
```

## 🔧 Installation

### Step 1: Install Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs the `websockets` library needed for the application.

### Step 2: Verify Installation

Run this command to check if everything is installed:

```bash
python -c "import websockets; print('✓ Ready to go!')"
```

If you see "✓ Ready to go!" you're all set!

## 🎯 Choose Your Interface

You have two options:

### Option 1: GUI Mode (Easiest!)

Perfect if you want a visual, point-and-click interface.

**Launch the GUI Launcher:**

```bash
python launcher.py
```

**Or on Windows, simply double-click:**
- `start.bat` - Opens the launcher

Then click the buttons to start what you need!

### Option 2: CLI Mode (For Automation)

Perfect for headless servers or automation.

**Start the server:**
```bash
python broadcast_server.py start
```

**Connect a client (in a new terminal):**
```bash
python broadcast_server.py connect
```

## 🎮 Your First Chat Session

Let's test everything with a quick chat session:

### Using GUI (Recommended for First-Time)

1. **Start the launcher:**
   ```bash
   python launcher.py
   ```

2. **Click "Start Server GUI"**
   - A new window opens
   - Click the "Start Server" button
   - Wait for "Server is running" message

3. **Click "Start Client GUI" (do this 2-3 times)**
   - Each click opens a new client window
   - In each window:
     - Enter a different username (Alice, Bob, Charlie)
     - Click "Connect"

4. **Start chatting!**
   - Type a message in any client
   - Press Enter
   - See it appear in all other clients!

### Using CLI

1. **Terminal 1 - Start Server:**
   ```bash
   python broadcast_server.py start
   ```
   Leave this running.

2. **Terminal 2 - First Client:**
   ```bash
   python broadcast_server.py connect
   ```
   Type messages and press Enter.

3. **Terminal 3 - Second Client:**
   ```bash
   python broadcast_server.py connect
   ```
   Do the same here.

4. **Watch messages appear in both clients!**

## 📁 Quick Reference - Main Files

| File | Purpose | How to Use |
|------|---------|------------|
| `launcher.py` | Main launcher | `python launcher.py` |
| `gui_server.py` | GUI Server | `python gui_server.py` |
| `gui_client.py` | GUI Client | `python gui_client.py` |
| `broadcast_server.py` | CLI Server/Client | See CLI commands above |
| `start.bat` | Windows launcher | Double-click it |

## 🎨 Interface Comparison

### GUI Benefits
- ✅ Visual interface
- ✅ Easy for beginners
- ✅ Real-time visual feedback
- ✅ Color-coded messages
- ✅ No commands to remember

### CLI Benefits
- ✅ Lightweight
- ✅ Great for servers
- ✅ Easy to automate
- ✅ Works over SSH
- ✅ Scriptable

**Tip:** Start with GUI to learn, then use CLI for production!

## 🌐 Connecting from Another Computer

Want to chat with someone on another computer on your network?

### On the Server Computer:

1. **Find your IP address:**
   
   **Windows:**
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address"

   **Mac/Linux:**
   ```bash
   ifconfig
   ```
   or
   ```bash
   ip addr show
   ```

2. **Start server on all interfaces:**
   ```bash
   python broadcast_server.py start --host 0.0.0.0
   ```
   
   Or in GUI: Change host to `0.0.0.0`

3. **Allow through firewall** (if needed)
   - Windows: Allow Python through Windows Firewall
   - Mac: System Preferences → Security → Firewall
   - Linux: `sudo ufw allow 8765`

### On the Client Computer:

1. **Connect to server's IP:**
   ```bash
   python broadcast_server.py connect --host 192.168.1.XXX
   ```
   
   Or in GUI: Enter the server's IP in the Host field

2. **Start chatting!**

## 🔥 Common Issues & Solutions

### "Could not connect to server"

**Problem:** Client can't reach server

**Solutions:**
- ✅ Make sure server is running first
- ✅ Check host and port match
- ✅ Try `localhost` instead of `127.0.0.1` or vice versa
- ✅ Check firewall settings

### "Address already in use"

**Problem:** Port 8765 is being used

**Solutions:**
- ✅ Stop any other programs using that port
- ✅ Use a different port: `--port 9000`
- **Windows:** Check Task Manager for Python processes
- **Mac/Linux:** `lsof -i :8765` to find process

### "Module not found: websockets"

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install websockets
```

### GUI window doesn't open

**Problem:** Tkinter not installed

**Solutions:**
- **Windows:** Usually included with Python
- **Mac:** `brew install python-tk`
- **Linux:** `sudo apt-get install python3-tk`

### Messages not sending

**Problem:** Connection issue

**Solutions:**
- ✅ Check if still connected (green status in GUI)
- ✅ Disconnect and reconnect
- ✅ Restart server and client

## 📚 Next Steps

Now that you're set up:

1. **📖 Read the docs:**
   - [README.md](README.md) - Full documentation
   - [GUI_GUIDE.md](GUI_GUIDE.md) - GUI features and tips
   - [QUICKSTART.md](QUICKSTART.md) - CLI quick reference

2. **🧪 Run the tests:**
   ```bash
   python test_server.py
   ```

3. **💡 Check examples:**
   ```bash
   python examples.py
   ```

4. **🚀 Extend it:**
   - Add emoji support
   - Implement chat rooms
   - Add user authentication
   - Create a web interface
   - Build a mobile app

## 🎓 Learning Resources

**Understanding the Code:**

- **Server:** See how WebSocket servers work in `broadcast_server.py`
- **Client:** Learn about async message handling
- **GUI:** Explore tkinter and threading in `gui_server.py`

**Key Concepts:**

- **WebSockets:** Real-time bidirectional communication
- **Asyncio:** Concurrent programming in Python
- **Broadcasting:** One-to-many messaging pattern
- **Event Loops:** How async code executes

## 💬 Testing Tips

### Test with Multiple Clients

1. Open 4-5 client windows
2. Give each a unique username
3. Send messages from different clients
4. Watch real-time broadcasting in action!

### Test Disconnections

1. Connect multiple clients
2. Close one client window
3. See server notify others
4. Test that remaining clients still work

### Test Network Issues

1. Start on localhost
2. Move to LAN (same network)
3. Try from different devices (phone, tablet, laptop)

## 🎉 You're Ready!

You now know how to:
- ✅ Install and run the broadcast server
- ✅ Use both GUI and CLI modes
- ✅ Connect multiple clients
- ✅ Chat in real-time
- ✅ Troubleshoot common issues

**Have fun experimenting with real-time communication! 🚀**

---

## Quick Command Reference

```bash
# GUI Mode
python launcher.py          # Main launcher
python gui_server.py        # Direct server GUI
python gui_client.py        # Direct client GUI

# CLI Mode
python broadcast_server.py start                    # Start server
python broadcast_server.py connect                  # Connect client
python broadcast_server.py start --port 9000       # Custom port
python broadcast_server.py connect --host SERVER_IP # Remote connect

# Testing
python test_server.py       # Run automated tests
python examples.py          # See usage examples

# Windows Shortcuts
start.bat                   # Launcher
server-gui.bat             # Server GUI
client-gui.bat             # Client GUI
broadcast-server.bat start # Server CLI
```

**Need more help?** Check the full documentation in [README.md](README.md)!
