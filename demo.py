#!/usr/bin/env python3
"""
Demo script to show off the broadcast server features
This creates an automated demo of the system
"""

import asyncio
import websockets
import random
from datetime import datetime


# Demo users
DEMO_USERS = [
    ("Alice", ["Hello everyone!", "How's everyone doing?", "This is amazing!", "Great to be here!"]),
    ("Bob", ["Hi Alice!", "I'm doing great!", "This is so cool!", "Real-time chat!"]),
    ("Charlie", ["Hey folks!", "Nice to meet you all!", "Love this system!", "Works perfectly!"]),
    ("Diana", ["Good morning!", "This is fantastic!", "Real-time messaging rocks!", "Very impressive!"])
]


class DemoClient:
    """Automated demo client that sends predefined messages."""
    
    def __init__(self, username, messages, delay_range=(2, 5)):
        self.username = username
        self.messages = messages
        self.delay_range = delay_range
        self.uri = "ws://localhost:8765"
    
    async def run(self):
        """Run the demo client."""
        print(f"[{self.timestamp()}] {self.username} is connecting...")
        
        try:
            async with websockets.connect(self.uri) as websocket:
                print(f"[{self.timestamp()}] {self.username} connected!")
                
                # Send each message with random delays
                for message in self.messages:
                    # Random delay between messages
                    delay = random.uniform(*self.delay_range)
                    await asyncio.sleep(delay)
                    
                    # Send message
                    full_message = f"{self.username}: {message}"
                    await websocket.send(full_message)
                    print(f"[{self.timestamp()}] {self.username}: {message}")
                
                # Stay connected for a bit
                await asyncio.sleep(2)
                print(f"[{self.timestamp()}] {self.username} is leaving...")
                
        except Exception as e:
            print(f"[{self.timestamp()}] {self.username} error: {e}")
    
    @staticmethod
    def timestamp():
        """Get current timestamp."""
        return datetime.now().strftime("%H:%M:%S")


async def run_demo():
    """Run the complete demo."""
    print("=" * 70)
    print("BROADCAST SERVER DEMO")
    print("=" * 70)
    print("\nThis demo simulates multiple users chatting in real-time.")
    print("Make sure the server is running before starting!")
    print()
    
    # Wait for server
    print("Checking if server is running...")
    try:
        async with websockets.connect("ws://localhost:8765") as ws:
            print("✓ Server is running!\n")
    except:
        print("✗ Server is not running!")
        print("\nPlease start the server first:")
        print("  GUI: python gui_server.py")
        print("  CLI: python broadcast_server.py start")
        print()
        return
    
    print(f"Starting demo with {len(DEMO_USERS)} users...\n")
    print("-" * 70)
    
    # Create demo clients
    clients = []
    for username, messages in DEMO_USERS:
        client = DemoClient(username, messages)
        clients.append(client)
    
    # Run all clients concurrently
    tasks = [client.run() for client in clients]
    await asyncio.gather(*tasks)
    
    print("-" * 70)
    print("\nDemo completed!")
    print("\nWhat just happened:")
    print("  • 4 virtual users connected to the server")
    print("  • Each sent several messages")
    print("  • All messages were broadcasted to everyone")
    print("  • Users disconnected gracefully")
    print()
    print("Try opening a client GUI to see these messages in real-time!")
    print("  python gui_client.py")
    print()
    print("=" * 70)


def main():
    """Main entry point."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                  BROADCAST SERVER DEMO                           ║
║                                                                  ║
║  This demo will simulate 4 users having a conversation.         ║
║  Perfect for testing and demonstration purposes!                ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to start the demo... ")
    print()
    
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError running demo: {e}")


if __name__ == "__main__":
    main()
