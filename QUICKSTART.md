# Quick Start Guide

## Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

Open a terminal and run:

```bash
python broadcast_server.py start
```

You should see:
```
[HH:MM:SS] Starting broadcast server on localhost:8765
[HH:MM:SS] Server is running. Waiting for clients to connect...
[HH:MM:SS] Press Ctrl+C to stop the server
```

### Step 3: Connect Clients

Open **additional terminals** (one for each client) and run:

```bash
python broadcast_server.py connect
```

You should see:
```
[HH:MM:SS] Connecting to server at ws://localhost:8765...
[HH:MM:SS] Connected to server!
[HH:MM:SS] Type your messages and press Enter to send.
[HH:MM:SS] Press Ctrl+C to disconnect.

> 
```

Now type messages in any client terminal and watch them appear in all other connected clients!

## Testing

To run automated tests (requires server to be running):

1. Start the server in one terminal:
   ```bash
   python broadcast_server.py start
   ```

2. Run tests in another terminal:
   ```bash
   python test_server.py
   ```

## Common Commands

### Server Commands
```bash
# Start server (default: localhost:8765)
python broadcast_server.py start

# Start on custom port
python broadcast_server.py start --port 9000

# Start on all interfaces (accessible from other machines)
python broadcast_server.py start --host 0.0.0.0 --port 8765
```

### Client Commands
```bash
# Connect to local server
python broadcast_server.py connect

# Connect to remote server
python broadcast_server.py connect --host 192.168.1.100 --port 9000
```

### Windows Batch File
```bash
# Using the batch file wrapper
broadcast-server.bat start
broadcast-server.bat connect
broadcast-server.bat start --port 9000
```

## What's Next?

- Try connecting multiple clients from different terminals
- Test what happens when clients disconnect
- Try running the server on a different port
- Check out the README.md for advanced features and extension ideas

## Troubleshooting

**Can't connect to server?**
- Make sure the server is running first
- Check you're using the same port number
- Try `localhost` instead of `127.0.0.1` or vice versa

**Port already in use?**
- Use a different port: `--port 9000`
- Stop any other programs using that port

**Need help?**
- Run: `python broadcast_server.py --help`
- Check the full README.md file
