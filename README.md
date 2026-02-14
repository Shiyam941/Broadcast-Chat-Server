# Broadcast Server

A WebSocket broadcast server with both **GUI and CLI interfaces** that allows multiple clients to connect and broadcast messages in real-time. This project demonstrates how to work with WebSockets and implement real-time communication between clients and servers.

## 🎨 New! GUI Version Available
Project URL : https://roadmap.sh/projects/broadcast-server
This project now includes beautiful graphical user interfaces! Choose between:

- **🖼️ GUI Mode** - Easy-to-use graphical interface (Recommended for beginners)
- **⌨️ CLI Mode** - Command-line interface (Great for automation and servers)

**Quick Start with GUI:**
```bash
python launcher.py        # Opens launcher with all options
python gui_server.py      # Or start server GUI directly
python gui_client.py      # Or start client GUI directly
```

👉 **See [GUI_GUIDE.md](GUI_GUIDE.md) for complete GUI documentation**

## Features

✨ **Real-time Broadcasting**: Messages sent by any client are instantly broadcasted to all connected clients  
🔌 **Multiple Clients**: Supports multiple simultaneous client connections  
🛡️ **Graceful Handling**: Properly handles client connections and disconnections  
⚡ **Async Architecture**: Built with Python's asyncio for efficient concurrent operations  
🖥️ **Dual Interfaces**: Choose between GUI and CLI modes  
📊 **Connection Notifications**: Clients are notified when other clients join or leave  
🔧 **Configurable**: Customizable host and port settings  
🎨 **Visual Monitoring**: GUI includes real-time logs and status indicators  

## Requirements

- Python 3.7 or higher
- websockets library

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install websockets
   ```

## Usage

### 🖼️ GUI Mode (Recommended for Beginners)

#### Using the Launcher

The easiest way to get started:

```bash
python launcher.py
```

Or on Windows, double-click `start.bat`

This opens a launcher with buttons to:
- Start Server GUI
- Start Client GUI  
- Start Server CLI
- Start Client CLI

#### Direct Launch

**Start Server GUI:**
```bash
python gui_server.py
```

**Start Client GUI:**
```bash
python gui_client.py
```

**Windows users:** Double-click `server-gui.bat` or `client-gui.bat`

📖 **Full GUI documentation:** [GUI_GUIDE.md](GUI_GUIDE.md)

---

### ⌨️ CLI Mode

#### Starting the Server

To start the broadcast server on the default port (8765):

```bash
python broadcast_server.py start
```

To start the server on a custom host and port:

```bash
python broadcast_server.py start --host 0.0.0.0 --port 9000
```

**Using the batch file (Windows):**
```bash
broadcast-server.bat start
broadcast-server.bat start --port 9000
```

### Connecting as a Client

To connect to the server running on localhost:

```bash
python broadcast_server.py connect
```

To connect to a remote server:

```bash
python broadcast_server.py connect --host 192.168.1.100 --port 9000
```

**Using the batch file (Windows):**
```bash
broadcast-server.bat connect
broadcast-server.bat connect --host 192.168.1.100
```

## How It Works

### Server Mode

When you start the server:
1. The server listens for incoming WebSocket connections on the specified port
2. When a client connects, it's added to the list of active connections
3. When a client sends a message, the server broadcasts it to all other connected clients
4. When a client disconnects, it's removed from the active connections list
5. All clients are notified when someone joins or leaves

### Client Mode

When you connect as a client:
1. The client establishes a WebSocket connection to the server
2. You can type messages and press Enter to send them
3. Messages from other clients appear in your terminal
4. Press Ctrl+C to disconnect gracefully

## Example Session

**Terminal 1 - Start Server:**
```
$ python broadcast_server.py start
[14:30:45] Starting broadcast server on localhost:8765
[14:30:45] Server is running. Waiting for clients to connect...
[14:30:45] Press Ctrl+C to stop the server
[14:30:52] New client connected. Total clients: 1
[14:31:05] New client connected. Total clients: 2
[14:31:10] Received: Hello from Client 1!
[14:31:15] Received: Hi there from Client 2!
```

**Terminal 2 - Client 1:**
```
$ python broadcast_server.py connect
[14:30:52] Connecting to server at ws://localhost:8765...
[14:30:52] Connected to server!
[14:30:52] Type your messages and press Enter to send.
[14:30:52] Press Ctrl+C to disconnect.

> Hello from Client 1!

[SERVER] A new client has joined. Total clients: 2

[CLIENT] Hi there from Client 2!
> 
```

**Terminal 3 - Client 2:**
```
$ python broadcast_server.py connect
[14:31:05] Connecting to server at ws://localhost:8765...
[14:31:05] Connected to server!
[14:31:05] Type your messages and press Enter to send.
[14:31:05] Press Ctrl+C to disconnect.

> 
[CLIENT] Hello from Client 1!
> Hi there from Client 2!
> 
```

## Command-Line Options

### Common Options

- `--host HOST`: Specify the host address (default: localhost)
- `--port PORT`: Specify the port number (default: 8765)

### Commands

- `start`: Start the broadcast server
- `connect`: Connect to the server as a client

### Examples

```bash
# Start server on all interfaces, port 9000
python broadcast_server.py start --host 0.0.0.0 --port 9000

# Connect to a specific server
python broadcast_server.py connect --host 192.168.1.100 --port 9000

# Get help
python broadcast_server.py --help
```

## Project Structure

```
Project 2/
├── gui_server.py          # GUI server application
├── gui_client.py          # GUI client application
├── launcher.py            # Main launcher for all modes
├── broadcast_server.py    # CLI server and client
├── test_server.py         # Automated tests
├── examples.py            # Usage examples
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── GUI_GUIDE.md          # GUI documentation
├── QUICKSTART.md         # Quick start guide
├── start.bat             # Windows launcher
├── server-gui.bat        # Windows GUI server
├── client-gui.bat        # Windows GUI client
└── broadcast-server.bat  # Windows CLI wrapper
```

## Architecture

The project includes both CLI and GUI implementations:

### CLI Components

**BroadcastServer Class**
- Manages WebSocket server lifecycle
- Maintains a set of connected clients
- Handles client registration/unregistration
- Broadcasts messages to all connected clients
- Implements graceful shutdown

**BroadcastClient Class**
- Manages WebSocket client connection
- Handles sending user input to the server
- Receives and displays broadcasted messages
- Concurrent send/receive using asyncio tasks

### GUI Components

**BroadcastServerGUI Class**
- Tkinter-based graphical server interface
- Real-time log display with color coding
- Visual connection status and client count
- Threaded asyncio event loop integration

**BroadcastClientGUI Class**
- Tkinter-based chat client interface
- Username support and message formatting
- Color-coded message display
- Real-time message updates

## Error Handling

The application includes robust error handling:

- **Connection Errors**: Gracefully handles failed connections
- **Network Errors**: Catches and reports WebSocket exceptions
- **Client Disconnections**: Properly cleans up when clients disconnect
- **Server Shutdown**: Cleanly closes all connections when stopping
- **Keyboard Interrupts**: Handles Ctrl+C for graceful shutdown

## Technical Details

- **Protocol**: WebSocket (RFC 6455)
- **Async Framework**: Python asyncio
- **WebSocket Library**: websockets 12.0
- **Message Format**: UTF-8 text messages
- **Connection**: Persistent bidirectional connections

## Extending the Project

Here are some ideas to extend this project:

1. **Authentication**: Add user authentication and login
2. **Message History**: Store and replay message history to new clients
3. **Private Messages**: Implement direct messaging between specific clients
4. **Usernames**: Allow clients to set custom usernames
5. **Rooms/Channels**: Create multiple chat rooms
6. **File Transfer**: Support sending files between clients
7. **Encryption**: Add message encryption for security
8. **Web Interface**: Create a browser-based client
9. **Logging**: Add comprehensive logging to files
10. **Rate Limiting**: Prevent message spam

## Troubleshooting

### "Could not connect to server"
- Make sure the server is running
- Check that you're using the correct host and port
- Verify firewall settings allow the connection

### "Address already in use"
- The port is already being used by another application
- Try a different port using `--port` option
- On Linux/Mac, you can find and kill the process using the port

### Messages not appearing
- Check your network connection
- Ensure both client and server are using the same host/port
- Verify no firewall is blocking the WebSocket connection

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and add your own features! Some ideas:
- Add unit tests
- Improve error messages
- Add message encryption
- Create a GUI client
- Add configuration file support

## Author

Created as a learning project to understand WebSocket communication and real-time messaging systems.
