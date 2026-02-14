#!/usr/bin/env python3
"""
GUI Broadcast Server - Graphical interface for the broadcast server
"""

import asyncio
import websockets
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from typing import Set
import threading


class BroadcastServerGUI:
    """GUI for the broadcast server."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Broadcast Server")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Server state
        self.connected_clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.is_running = False
        self.loop = None
        self.server_thread = None
        
        # Default settings
        self.host = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="8765")
        
        # Create UI
        self.create_widgets()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Server configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Server Configuration", padding="10")
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Host
        ttk.Label(config_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        host_entry = ttk.Entry(config_frame, textvariable=self.host, width=20)
        host_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Port
        ttk.Label(config_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        port_entry = ttk.Entry(config_frame, textvariable=self.port, width=10)
        port_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.start_button = ttk.Button(
            control_frame, 
            text="Start Server", 
            command=self.toggle_server,
            width=15
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        # Clear button
        ttk.Button(
            control_frame,
            text="Clear Log",
            command=self.clear_log,
            width=15
        ).grid(row=0, column=1)
        
        # Status label
        self.status_label = ttk.Label(
            control_frame,
            text="● Server Stopped",
            foreground="red",
            font=("", 10, "bold")
        )
        self.status_label.grid(row=0, column=2, padx=(20, 0))
        
        # Client count label
        self.client_count_label = ttk.Label(
            control_frame,
            text="Connected Clients: 0",
            font=("", 10)
        )
        self.client_count_label.grid(row=0, column=3, padx=(20, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Server Log", padding="5")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.log_text.tag_config("info", foreground="#0066cc")
        self.log_text.tag_config("success", foreground="#00aa00")
        self.log_text.tag_config("warning", foreground="#ff8800")
        self.log_text.tag_config("error", foreground="#cc0000")
        self.log_text.tag_config("message", foreground="#333333")
    
    def log(self, message, level="info"):
        """Add a log entry to the text area."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry, level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the log text area."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def toggle_server(self):
        """Start or stop the server."""
        if self.is_running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        """Start the WebSocket server."""
        try:
            host = self.host.get()
            port = int(self.port.get())
            
            # Validate port
            if port < 1 or port > 65535:
                messagebox.showerror("Error", "Port must be between 1 and 65535")
                return
            
            # Update UI
            self.is_running = True
            self.start_button.config(text="Stop Server")
            self.status_label.config(text="● Server Running", foreground="green")
            
            # Log
            self.log(f"Starting server on {host}:{port}...", "info")
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self.run_server, args=(host, port), daemon=True)
            self.server_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")
            self.is_running = False
            self.start_button.config(text="Start Server")
            self.status_label.config(text="● Server Stopped", foreground="red")
    
    def run_server(self, host, port):
        """Run the asyncio server loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self.start_websocket_server(host, port))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Server error: {e}", "error"))
            self.root.after(0, self.stop_server)
    
    async def start_websocket_server(self, host, port):
        """Start the WebSocket server."""
        try:
            self.server = await websockets.serve(self.handle_client, host, port)
            self.root.after(0, lambda: self.log(f"Server started successfully on {host}:{port}", "success"))
            self.root.after(0, lambda: self.log("Waiting for clients to connect...", "info"))
            
            await asyncio.Future()  # Run forever
            
        except OSError as e:
            self.root.after(0, lambda: self.log(f"Failed to start server: {e}", "error"))
            self.root.after(0, lambda: messagebox.showerror("Server Error", f"Could not start server:\n{e}"))
            raise
    
    async def handle_client(self, websocket, path):
        """Handle a client connection."""
        # Register client
        self.connected_clients.add(websocket)
        client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        
        self.root.after(0, lambda: self.log(f"Client connected: {client_addr}", "success"))
        self.root.after(0, self.update_client_count)
        
        # Notify other clients
        if len(self.connected_clients) > 1:
            await self.broadcast(f"[SERVER] New client connected. Total: {len(self.connected_clients)}", websocket)
        
        try:
            # Listen for messages
            async for message in websocket:
                self.root.after(0, lambda m=message: self.log(f"From {client_addr}: {m}", "message"))
                
                # Broadcast to other clients
                broadcast_msg = f"[CLIENT] {message}"
                await self.broadcast(broadcast_msg, websocket)
                
        except websockets.exceptions.ConnectionClosed:
            self.root.after(0, lambda: self.log(f"Client disconnected: {client_addr}", "warning"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error with client {client_addr}: {e}", "error"))
        finally:
            # Unregister client
            self.connected_clients.discard(websocket)
            self.root.after(0, self.update_client_count)
            
            # Notify remaining clients
            if self.connected_clients:
                await self.broadcast(f"[SERVER] Client disconnected. Total: {len(self.connected_clients)}")
    
    async def broadcast(self, message, exclude_client=None):
        """Broadcast message to all clients except excluded one."""
        if self.connected_clients:
            recipients = self.connected_clients - {exclude_client} if exclude_client else self.connected_clients
            
            if recipients:
                await asyncio.gather(
                    *[client.send(message) for client in recipients],
                    return_exceptions=True
                )
    
    def update_client_count(self):
        """Update the client count display."""
        count = len(self.connected_clients)
        self.client_count_label.config(text=f"Connected Clients: {count}")
    
    def stop_server(self):
        """Stop the WebSocket server."""
        if not self.is_running:
            return
        
        self.log("Stopping server...", "warning")
        
        # Update UI
        self.is_running = False
        self.start_button.config(text="Start Server")
        self.status_label.config(text="● Server Stopped", foreground="red")
        
        # Close all connections and stop server
        if self.loop and self.server:
            asyncio.run_coroutine_threadsafe(self.shutdown_server(), self.loop)
        
        self.log("Server stopped", "info")
        self.update_client_count()
    
    async def shutdown_server(self):
        """Shutdown the server and close connections."""
        # Close all client connections
        if self.connected_clients:
            await asyncio.gather(
                *[client.close() for client in self.connected_clients.copy()],
                return_exceptions=True
            )
            self.connected_clients.clear()
        
        # Stop server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
    
    def on_closing(self):
        """Handle window close event."""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Server is running. Do you want to stop it and quit?"):
                self.stop_server()
                self.root.after(500, self.root.destroy)
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = BroadcastServerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
