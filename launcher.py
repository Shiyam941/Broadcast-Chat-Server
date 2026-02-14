#!/usr/bin/env python3
"""
Broadcast Server Launcher - Launch GUI or CLI versions
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os


class LauncherGUI:
    """Main launcher for broadcast server applications."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Broadcast Server Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set icon and styling
        try:
            self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='icon.png'))
        except:
            pass
        
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🌐 Broadcast Server",
            font=("Segoe UI", 24, "bold"),
            foreground="#0066cc"
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Real-time WebSocket Broadcasting",
            font=("Segoe UI", 11),
            foreground="#666666"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # GUI Section
        gui_label = ttk.Label(
            main_frame,
            text="Graphical Interface (Recommended)",
            font=("Segoe UI", 12, "bold")
        )
        gui_label.grid(row=2, column=0, pady=(0, 10), sticky=tk.W)
        
        # GUI buttons frame
        gui_buttons = ttk.Frame(main_frame)
        gui_buttons.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        gui_buttons.columnconfigure(0, weight=1)
        gui_buttons.columnconfigure(1, weight=1)
        
        # Server GUI button
        server_gui_btn = ttk.Button(
            gui_buttons,
            text="🖥️ Start Server GUI",
            command=self.launch_server_gui,
            width=20
        )
        server_gui_btn.grid(row=0, column=0, padx=(0, 10), ipady=10)
        
        # Client GUI button
        client_gui_btn = ttk.Button(
            gui_buttons,
            text="💬 Start Client GUI",
            command=self.launch_client_gui,
            width=20
        )
        client_gui_btn.grid(row=0, column=1, ipady=10)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=4, column=0, sticky=(tk.W, tk.E), pady=20
        )
        
        # CLI Section
        cli_label = ttk.Label(
            main_frame,
            text="Command Line Interface",
            font=("Segoe UI", 12, "bold")
        )
        cli_label.grid(row=5, column=0, pady=(0, 10), sticky=tk.W)
        
        # CLI buttons frame
        cli_buttons = ttk.Frame(main_frame)
        cli_buttons.grid(row=6, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        cli_buttons.columnconfigure(0, weight=1)
        cli_buttons.columnconfigure(1, weight=1)
        
        # Server CLI button
        server_cli_btn = ttk.Button(
            cli_buttons,
            text="⌨️ Start Server CLI",
            command=self.launch_server_cli,
            width=20
        )
        server_cli_btn.grid(row=0, column=0, padx=(0, 10), ipady=10)
        
        # Client CLI button
        client_cli_btn = ttk.Button(
            cli_buttons,
            text="⌨️ Start Client CLI",
            command=self.launch_client_cli,
            width=20
        )
        client_cli_btn.grid(row=0, column=1, ipady=10)
        
        # Exit button
        exit_btn = ttk.Button(
            main_frame,
            text="Exit",
            command=self.root.quit,
            width=15
        )
        exit_btn.grid(row=7, column=0, pady=(10, 0))
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Tip: Start the server first, then connect clients to it",
            font=("Segoe UI", 9, "italic"),
            foreground="#999999"
        )
        info_label.grid(row=8, column=0, pady=(20, 0))
    
    def launch_server_gui(self):
        """Launch the server GUI."""
        try:
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, "gui_server.py"], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, "gui_server.py"])
        except Exception as e:
            self.show_error("Failed to launch Server GUI", str(e))
    
    def launch_client_gui(self):
        """Launch the client GUI."""
        try:
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, "gui_client.py"],
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, "gui_client.py"])
        except Exception as e:
            self.show_error("Failed to launch Client GUI", str(e))
    
    def launch_server_cli(self):
        """Launch the server CLI."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/k", "python", "broadcast_server.py", "start"])
            else:
                subprocess.Popen(["x-terminal-emulator", "-e", 
                                "python3 broadcast_server.py start"])
        except Exception as e:
            self.show_error("Failed to launch Server CLI", str(e))
    
    def launch_client_cli(self):
        """Launch the client CLI."""
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/k", "python", "broadcast_server.py", "connect"])
            else:
                subprocess.Popen(["x-terminal-emulator", "-e", 
                                "python3 broadcast_server.py connect"])
        except Exception as e:
            self.show_error("Failed to launch Client CLI", str(e))
    
    def show_error(self, title, message):
        """Show error dialog."""
        from tkinter import messagebox
        messagebox.showerror(title, message)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
