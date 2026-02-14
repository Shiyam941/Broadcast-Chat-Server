#!/usr/bin/env python3
"""
GUI Broadcast Client - Graphical interface for the broadcast client
"""

import asyncio
import websockets
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading


class BroadcastClientGUI:
    """GUI for the broadcast client."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Broadcast Client")
        self.root.geometry("700x600")
        self.root.minsize(500, 400)
        
        # Client state
        self.websocket = None
        self.is_connected = False
        self.loop = None
        self.client_thread = None
        self.receive_task = None
        self.username = tk.StringVar(value="User")
        
        # Connection settings
        self.host = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="8765")
        
        # Create UI
        self.create_widgets()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind Enter key to send message
        self.root.bind('<Return>', lambda e: self.send_message())
    
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
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection", padding="10")
        conn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        conn_frame.columnconfigure(1, weight=1)
        
        # Username
        ttk.Label(conn_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        username_entry = ttk.Entry(conn_frame, textvariable=self.username, width=15)
        username_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Host
        ttk.Label(conn_frame, text="Host:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        host_entry = ttk.Entry(conn_frame, textvariable=self.host, width=15)
        host_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        # Port
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        port_entry = ttk.Entry(conn_frame, textvariable=self.port, width=8)
        port_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 10))
        
        # Connect button
        self.connect_button = ttk.Button(
            conn_frame,
            text="Connect",
            command=self.toggle_connection,
            width=12
        )
        self.connect_button.grid(row=0, column=6)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            status_frame,
            text="● Disconnected",
            foreground="red",
            font=("", 10, "bold")
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Clear button
        ttk.Button(
            status_frame,
            text="Clear Chat",
            command=self.clear_chat,
            width=12
        ).grid(row=0, column=1, padx=(20, 0))
        
        # Chat frame
        chat_frame = ttk.LabelFrame(main_frame, text="Chat", padding="5")
        chat_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Segoe UI", 10),
            state=tk.DISABLED,
            bg="#f5f5f5"
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags
        self.chat_display.tag_config("server", foreground="#666666", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("client", foreground="#0066cc", font=("Segoe UI", 10))
        self.chat_display.tag_config("self", foreground="#00aa00", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#ff6600", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("timestamp", foreground="#999999", font=("Segoe UI", 8))
        
        # Message input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Message entry
        self.message_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.message_entry.config(state=tk.DISABLED)
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            width=10,
            state=tk.DISABLED
        )
        self.send_button.grid(row=0, column=1)
    
    def add_message(self, message, tag="client"):
        """Add a message to the chat display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message with appropriate tag
        self.chat_display.insert(tk.END, f"{message}\n", tag)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def toggle_connection(self):
        """Connect or disconnect from server."""
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        """Connect to the server."""
        try:
            host = self.host.get()
            port = int(self.port.get())
            username = self.username.get().strip()
            
            if not username:
                messagebox.showerror("Error", "Please enter a username")
                return
            
            # Validate port
            if port < 1 or port > 65535:
                messagebox.showerror("Error", "Port must be between 1 and 65535")
                return
            
            # Update UI
            self.is_connected = True
            self.connect_button.config(text="Disconnect")
            self.status_label.config(text="● Connecting...", foreground="orange")
            self.message_entry.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            
            # Add system message
            self.add_message(f"Connecting to {host}:{port}...", "system")
            
            # Start client in separate thread
            self.client_thread = threading.Thread(
                target=self.run_client,
                args=(host, port),
                daemon=True
            )
            self.client_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")
            self.is_connected = False
            self.connect_button.config(text="Connect")
            self.status_label.config(text="● Disconnected", foreground="red")
    
    def run_client(self, host, port):
        """Run the asyncio client loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self.connect_to_server(host, port))
        except Exception as e:
            self.root.after(0, lambda: self.add_message(f"Connection error: {e}", "system"))
            self.root.after(0, self.disconnect)
    
    async def connect_to_server(self, host, port):
        """Connect to the WebSocket server."""
        uri = f"ws://{host}:{port}"
        
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                
                # Update UI
                self.root.after(0, lambda: self.status_label.config(
                    text="● Connected",
                    foreground="green"
                ))
                self.root.after(0, lambda: self.add_message(
                    f"Connected to server! You are {self.username.get()}",
                    "system"
                ))
                
                # Focus on message entry
                self.root.after(0, lambda: self.message_entry.focus())
                
                # Start receiving messages
                await self.receive_messages()
                
        except ConnectionRefusedError:
            self.root.after(0, lambda: self.add_message(
                "Could not connect to server. Make sure the server is running.",
                "system"
            ))
            self.root.after(0, lambda: messagebox.showerror(
                "Connection Error",
                "Could not connect to server.\nMake sure the server is running."
            ))
        except Exception as e:
            self.root.after(0, lambda: self.add_message(f"Error: {e}", "system"))
        finally:
            self.root.after(0, self.disconnect)
    
    async def receive_messages(self):
        """Receive messages from the server."""
        try:
            async for message in self.websocket:
                # Determine message type and display accordingly
                if message.startswith("[SERVER]"):
                    self.root.after(0, lambda m=message: self.add_message(m, "server"))
                elif message.startswith("[CLIENT]"):
                    # Remove [CLIENT] prefix
                    clean_msg = message[9:]
                    self.root.after(0, lambda m=clean_msg: self.add_message(m, "client"))
                else:
                    self.root.after(0, lambda m=message: self.add_message(m, "client"))
                    
        except websockets.exceptions.ConnectionClosed:
            self.root.after(0, lambda: self.add_message("Connection closed", "system"))
        except Exception as e:
            self.root.after(0, lambda: self.add_message(f"Error: {e}", "system"))
    
    def send_message(self):
        """Send a message to the server."""
        if not self.is_connected or not self.websocket:
            return
        
        message = self.message_entry.get().strip()
        
        if not message:
            return
        
        # Create message with username
        full_message = f"{self.username.get()}: {message}"
        
        # Display own message
        self.add_message(f"You: {message}", "self")
        
        # Send to server
        asyncio.run_coroutine_threadsafe(
            self.websocket.send(full_message),
            self.loop
        )
        
        # Clear entry
        self.message_entry.delete(0, tk.END)
    
    def disconnect(self):
        """Disconnect from the server."""
        if not self.is_connected:
            return
        
        self.add_message("Disconnecting...", "system")
        
        # Update UI
        self.is_connected = False
        self.connect_button.config(text="Connect")
        self.status_label.config(text="● Disconnected", foreground="red")
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        
        # Close websocket
        if self.websocket and self.loop:
            asyncio.run_coroutine_threadsafe(
                self.websocket.close(),
                self.loop
            )
        
        self.websocket = None
        
        self.add_message("Disconnected from server", "system")
    
    def on_closing(self):
        """Handle window close event."""
        if self.is_connected:
            self.disconnect()
            self.root.after(500, self.root.destroy)
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = BroadcastClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
