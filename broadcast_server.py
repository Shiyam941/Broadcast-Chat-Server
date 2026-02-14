#!/usr/bin/env python3
"""
Broadcast Server - A simple WebSocket-based broadcast server
that allows clients to connect and broadcast messages to all connected clients.
"""

import asyncio
import websockets
import argparse
import signal
import sys
from datetime import datetime
from typing import Set

# Default configuration
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8765

# Store all connected clients
connected_clients: Set[websockets.WebSocketServerProtocol] = set()


class BroadcastServer:
    """WebSocket broadcast server that forwards messages to all connected clients."""
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.server = None
        
    async def register(self, websocket: websockets.WebSocketServerProtocol):
        """Register a new client connection."""
        connected_clients.add(websocket)
        client_count = len(connected_clients)
        print(f"[{self._timestamp()}] New client connected. Total clients: {client_count}")
        
        # Notify all clients about the new connection
        if client_count > 1:
            await self.broadcast(f"[SERVER] A new client has joined. Total clients: {client_count}", websocket)
    
    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister a client connection."""
        connected_clients.discard(websocket)
        client_count = len(connected_clients)
        print(f"[{self._timestamp()}] Client disconnected. Total clients: {client_count}")
        
        # Notify remaining clients about the disconnection
        if client_count > 0:
            await self.broadcast(f"[SERVER] A client has left. Total clients: {client_count}")
    
    async def broadcast(self, message: str, exclude_client=None):
        """Broadcast a message to all connected clients except the excluded one."""
        if connected_clients:
            # Send to all clients except the one that sent the message (if specified)
            recipients = connected_clients - {exclude_client} if exclude_client else connected_clients
            
            # Create tasks for sending to all clients
            tasks = [client.send(message) for client in recipients]
            
            # Wait for all sends to complete, handling any errors
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle a client connection."""
        # Register the client
        await self.register(websocket)
        
        try:
            # Listen for messages from this client
            async for message in websocket:
                print(f"[{self._timestamp()}] Received: {message}")
                
                # Broadcast the message to all other clients
                broadcast_message = f"[CLIENT] {message}"
                await self.broadcast(broadcast_message, exclude_client=websocket)
                
        except websockets.exceptions.ConnectionClosed:
            print(f"[{self._timestamp()}] Client connection closed")
        except Exception as e:
            print(f"[{self._timestamp()}] Error handling client: {e}")
        finally:
            # Unregister the client
            await self.unregister(websocket)
    
    async def start(self):
        """Start the WebSocket server."""
        print(f"[{self._timestamp()}] Starting broadcast server on {self.host}:{self.port}")
        
        # Create and start the server
        self.server = await websockets.serve(self.handler, self.host, self.port)
        
        print(f"[{self._timestamp()}] Server is running. Waiting for clients to connect...")
        print(f"[{self._timestamp()}] Press Ctrl+C to stop the server")
        
        # Keep the server running
        await asyncio.Future()  # Run forever
    
    async def stop(self):
        """Stop the WebSocket server."""
        print(f"\n[{self._timestamp()}] Shutting down server...")
        
        # Close all client connections
        if connected_clients:
            await asyncio.gather(
                *[client.close() for client in connected_clients],
                return_exceptions=True
            )
        
        # Stop the server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        print(f"[{self._timestamp()}] Server stopped")
    
    @staticmethod
    def _timestamp():
        """Get current timestamp for logging."""
        return datetime.now().strftime("%H:%M:%S")


class BroadcastClient:
    """WebSocket client that can connect to the broadcast server."""
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.uri = f"ws://{host}:{port}"
        self.websocket = None
        self.running = False
    
    async def connect(self):
        """Connect to the broadcast server and handle sending/receiving messages."""
        print(f"[{self._timestamp()}] Connecting to server at {self.uri}...")
        
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                self.running = True
                
                print(f"[{self._timestamp()}] Connected to server!")
                print(f"[{self._timestamp()}] Type your messages and press Enter to send.")
                print(f"[{self._timestamp()}] Press Ctrl+C to disconnect.\n")
                
                # Create tasks for sending and receiving
                receive_task = asyncio.create_task(self.receive_messages())
                send_task = asyncio.create_task(self.send_messages())
                
                # Wait for either task to complete
                done, pending = await asyncio.wait(
                    [receive_task, send_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # Cancel pending tasks
                for task in pending:
                    task.cancel()
                    
        except websockets.exceptions.WebSocketException as e:
            print(f"[{self._timestamp()}] WebSocket error: {e}")
        except ConnectionRefusedError:
            print(f"[{self._timestamp()}] Could not connect to server. Make sure the server is running.")
        except Exception as e:
            print(f"[{self._timestamp()}] Error: {e}")
        finally:
            self.running = False
            print(f"\n[{self._timestamp()}] Disconnected from server")
    
    async def receive_messages(self):
        """Receive and display messages from the server."""
        try:
            async for message in self.websocket:
                print(f"\n{message}")
                print("> ", end="", flush=True)  # Re-display prompt
        except websockets.exceptions.ConnectionClosed:
            print(f"\n[{self._timestamp()}] Connection to server lost")
        except Exception as e:
            print(f"\n[{self._timestamp()}] Error receiving message: {e}")
    
    async def send_messages(self):
        """Send user input to the server."""
        loop = asyncio.get_event_loop()
        
        try:
            while self.running:
                # Read user input asynchronously
                message = await loop.run_in_executor(None, self._get_input)
                
                if message and self.running:
                    await self.websocket.send(message)
                    
        except Exception as e:
            print(f"\n[{self._timestamp()}] Error sending message: {e}")
    
    def _get_input(self):
        """Get input from user (blocking call)."""
        try:
            return input("> ")
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
    
    @staticmethod
    def _timestamp():
        """Get current timestamp for logging."""
        return datetime.now().strftime("%H:%M:%S")


def setup_signal_handlers(server_instance=None):
    """Setup signal handlers for graceful shutdown."""
    
    def signal_handler(sig, frame):
        print("\n\nReceived interrupt signal...")
        
        if server_instance:
            # Schedule server shutdown
            asyncio.create_task(server_instance.stop())
        
        # Exit
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)


async def start_server(host: str, port: int):
    """Start the broadcast server."""
    server = BroadcastServer(host, port)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.stop()
    except Exception as e:
        print(f"Server error: {e}")
        await server.stop()


async def connect_client(host: str, port: int):
    """Connect to the broadcast server as a client."""
    client = BroadcastClient(host, port)
    
    try:
        await client.connect()
    except KeyboardInterrupt:
        print("\nDisconnecting...")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Broadcast Server - Real-time WebSocket message broadcasting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s start                    Start server on default port (8765)
  %(prog)s start --port 9000        Start server on port 9000
  %(prog)s connect                  Connect to server on localhost:8765
  %(prog)s connect --host 192.168.1.100 --port 9000
        """
    )
    
    parser.add_argument(
        "command",
        choices=["start", "connect"],
        help="Command to execute: 'start' to run server, 'connect' to join as client"
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host address (default: {DEFAULT_HOST})"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port number (default: {DEFAULT_PORT})"
    )
    
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "start":
        asyncio.run(start_server(args.host, args.port))
    elif args.command == "connect":
        asyncio.run(connect_client(args.host, args.port))


if __name__ == "__main__":
    main()
