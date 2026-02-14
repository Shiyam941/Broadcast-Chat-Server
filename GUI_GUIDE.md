# Broadcast Server - GUI Version

## Overview

The Broadcast Server now includes beautiful graphical user interfaces (GUI) for both server and client applications, making it even easier to use!

## 🚀 Quick Start - GUI Version

### Option 1: Use the Launcher (Recommended)

The easiest way to get started:

1. **Double-click** `start.bat` (Windows) or run:
   ```bash
   python launcher.py
   ```

2. The launcher will open with options to start:
   - **Server GUI** - Start the broadcast server with visual interface
   - **Client GUI** - Connect to server as a client with chat interface
   - **Server CLI** - Start the command-line server
   - **Client CLI** - Connect via command-line

3. Click **"Start Server GUI"** first

4. Then click **"Start Client GUI"** as many times as you want clients (each opens a new window)

### Option 2: Launch Directly

**Start the Server GUI:**
```bash
python gui_server.py
```
Or double-click `server-gui.bat` (Windows)

**Start the Client GUI:**
```bash
python gui_client.py
```
Or double-click `client-gui.bat` (Windows)

## 📱 GUI Features

### Server GUI Features

- ✅ **Visual Server Control** - Start/stop server with one click
- 📊 **Real-time Monitoring** - See all connected clients count
- 📝 **Message Log** - View all client messages and server events
- ⚙️ **Easy Configuration** - Set host and port in the interface
- 🎨 **Color-coded Logs** - Different colors for different event types
- 🔴 **Status Indicator** - Visual connection status

### Client GUI Features

- 💬 **Chat Interface** - Modern chat-like message display
- 👤 **Username Support** - Set your display name
- ⌨️ **Easy Messaging** - Type and press Enter to send
- 🎨 **Color-coded Messages** - Distinguish your messages from others
- 📊 **Connection Status** - Visual connection indicator
- ⚡ **Real-time Updates** - Instant message delivery
- 🧹 **Clear Chat** - Clear message history anytime

## 🖼️ Screenshots & Interface Guide

### Server GUI

```
┌─────────────────────────────────────────────────┐
│ Broadcast Server                          [×]    │
├─────────────────────────────────────────────────┤
│ Server Configuration                             │
│ Host: localhost        Port: 8765                │
│                                                   │
│ [Start Server]  [Clear Log]  ● Server Running   │
│                              Connected Clients: 3│
│                                                   │
│ Server Log                                        │
│ ┌─────────────────────────────────────────────┐ │
│ │ [14:30:45] Server started on localhost:8765 │ │
│ │ [14:30:52] Client connected: 192.168.1.100 │ │
│ │ [14:31:10] From 192.168.1.100: Hello!      │ │
│ │                                             │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Client GUI

```
┌─────────────────────────────────────────────────┐
│ Broadcast Client                          [×]    │
├─────────────────────────────────────────────────┤
│ Connection                                        │
│ Username: Alice  Host: localhost  Port: 8765     │
│                                   [Disconnect]    │
│                                                   │
│ ● Connected              [Clear Chat]            │
│                                                   │
│ Chat                                              │
│ ┌─────────────────────────────────────────────┐ │
│ │ [14:30:52] Connected to server!             │ │
│ │ [14:31:10] You: Hello everyone!             │ │
│ │ [14:31:12] Bob: Hi Alice!                   │ │
│ │ [14:31:15] Charlie: Hey there!              │ │
│ │                                             │ │
│ └─────────────────────────────────────────────┘ │
│                                                   │
│ Type your message...           [Send]            │
└─────────────────────────────────────────────────┘
```

## 📖 How to Use

### Server Setup

1. **Launch the Server GUI**
   - Run `python gui_server.py` or use the launcher

2. **Configure Settings** (optional)
   - Default: `localhost:8765`
   - To accept remote connections, change host to `0.0.0.0`
   - To use a different port, change the port number

3. **Start the Server**
   - Click the **"Start Server"** button
   - Status indicator will turn green
   - Server log will show "Server started successfully"

4. **Monitor Activity**
   - Watch the log for client connections
   - See message count update in real-time
   - View all messages being sent between clients

5. **Stop the Server**
   - Click **"Stop Server"** button
   - All clients will be disconnected gracefully

### Client Setup

1. **Launch the Client GUI**
   - Run `python gui_client.py` or use the launcher
   - You can launch multiple clients!

2. **Enter Your Details**
   - Set your **Username** (displayed with your messages)
   - Enter **Host** (where server is running)
   - Enter **Port** (server's port number)

3. **Connect to Server**
   - Click **"Connect"** button
   - Status indicator will turn green when connected
   - You'll see a "Connected to server!" message

4. **Send Messages**
   - Type your message in the input box
   - Press **Enter** or click **"Send"**
   - Your message appears in green
   - Others' messages appear in blue
   - Server notifications appear in gray

5. **Disconnect**
   - Click **"Disconnect"** button
   - Or simply close the window

## 💡 Tips & Tricks

### For Server

- **Monitor Activity**: Keep the server window open to monitor all connections and messages
- **Clear Log**: Click "Clear Log" if the log gets too long
- **Remote Access**: Set host to `0.0.0.0` to allow connections from other computers
- **Port in Use**: If you get an error, try a different port number

### For Client

- **Unique Usernames**: Use different usernames for each client to identify who's talking
- **Press Enter**: You can press Enter to send messages instead of clicking Send
- **Clear Chat**: Use "Clear Chat" to start fresh
- **Multiple Clients**: Open multiple client windows to test multi-user chat
- **Reconnect**: If disconnected, just change settings and click Connect again

## 🎨 Color Coding

### Server Log Colors

- 🔵 **Blue** - Informational messages
- 🟢 **Green** - Success messages (connections, server start)
- 🟠 **Orange** - Warnings (disconnections)
- 🔴 **Red** - Errors

### Client Chat Colors

- 🟢 **Green Bold** - Your own messages
- 🔵 **Blue** - Other clients' messages
- ⚫ **Gray** - Server notifications
- 🟠 **Orange** - System messages

## 🔧 Advanced Configuration

### Custom Server Settings

Edit the default values in `gui_server.py`:
```python
DEFAULT_HOST = "localhost"  # Change to "0.0.0.0" for all interfaces
DEFAULT_PORT = 8765         # Change to your preferred port
```

### Custom Client Settings

Edit the default values in `gui_client.py`:
```python
self.host = tk.StringVar(value="localhost")
self.port = tk.StringVar(value="8765")
self.username = tk.StringVar(value="User")
```

## 🐛 Troubleshooting

### Server Issues

**"Address already in use"**
- The port is being used by another application
- Change the port number in the Server Configuration

**Can't start server**
- Check if you have permission to bind to that port
- Ports below 1024 may require administrator privileges

### Client Issues

**"Could not connect to server"**
- Make sure the server is running first
- Verify host and port match the server
- Check firewall settings

**Messages not sending**
- Check if you're still connected (green status)
- Try disconnecting and reconnecting

**Can't type messages**
- Make sure you're connected to the server
- Input field is disabled when not connected

## 🚀 Running Multiple Instances

### Test with Multiple Clients

1. Start ONE server (only one needed)
2. Start MULTIPLE clients:
   - Each client needs its own window
   - Use different usernames for each
   - All connect to the same server

**Example Setup:**
- 1 Server GUI window
- 3+ Client GUI windows (representing different users)
- All clients can chat in real-time!

## 📝 Keyboard Shortcuts

### Client GUI

- **Enter** - Send current message
- **Ctrl+A** - Select all in message box
- **Alt+F4 / Cmd+Q** - Close window (prompts if connected)

## 🔐 Security Notes

⚠️ **Important**: This is a basic implementation for learning purposes.

For production use, consider adding:
- SSL/TLS encryption (wss:// instead of ws://)
- User authentication
- Message encryption
- Rate limiting
- Input validation

## 🎯 Next Steps

After mastering the GUI:

1. **Test Multi-Client Chat**
   - Open 3-4 client windows
   - Send messages from each
   - Watch real-time broadcasting

2. **Try Remote Connections**
   - Set server host to `0.0.0.0`
   - Connect from another device on your network

3. **Explore the Code**
   - Check out `gui_server.py` and `gui_client.py`
   - See how asyncio works with tkinter
   - Learn about threading in GUI applications

4. **Extend the Application**
   - Add emoji support
   - Implement message timestamps
   - Add chat rooms/channels
   - Create user lists
   - Add file sharing

## 📚 Related Documentation

- [README.md](README.md) - Complete project documentation
- [QUICKSTART.md](QUICKSTART.md) - CLI quick start guide
- [examples.py](examples.py) - Programmatic usage examples

## 🤝 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review the server log for error messages
3. Ensure Python and dependencies are installed correctly
4. Try the CLI version to isolate GUI-specific issues

---

**Enjoy your new GUI broadcast server! 🎉**
