"""
Example usage of the broadcast server components programmatically.
This shows how to use the server and client classes in your own code.
"""

import asyncio
from broadcast_server import BroadcastServer, BroadcastClient


async def example_server():
    """Example: Starting a server programmatically."""
    print("Example 1: Starting server programmatically\n")
    
    # Create server instance
    server = BroadcastServer(host="localhost", port=8888)
    
    # Start the server (will run until interrupted)
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.stop()


async def example_client():
    """Example: Connecting a client programmatically."""
    print("Example 2: Connecting client programmatically\n")
    
    # Create client instance
    client = BroadcastClient(host="localhost", port=8888)
    
    # Connect to server
    await client.connect()


async def example_automated_client():
    """Example: Automated client that sends messages programmatically."""
    print("Example 3: Automated client sending messages\n")
    
    import websockets
    
    uri = "ws://localhost:8888"
    
    async with websockets.connect(uri) as websocket:
        # Send some automated messages
        messages = [
            "Hello from automated client!",
            "This is message 2",
            "And this is message 3"
        ]
        
        for msg in messages:
            await websocket.send(msg)
            print(f"Sent: {msg}")
            await asyncio.sleep(1)
        
        print("All messages sent!")


async def example_custom_handler():
    """Example: Server with custom message handling."""
    print("Example 4: Custom message handler\n")
    
    import websockets
    
    async def custom_handler(websocket, path):
        """Custom handler that modifies messages before broadcasting."""
        print(f"New client connected from {websocket.remote_address}")
        
        try:
            async for message in websocket:
                # Custom processing
                modified_message = f"[CUSTOM] {message.upper()}"
                print(f"Processing: {message} -> {modified_message}")
                
                # Send back to sender
                await websocket.send(f"Echo: {modified_message}")
                
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
    
    # Start server with custom handler
    async with websockets.serve(custom_handler, "localhost", 8888):
        print("Custom server running on localhost:8888")
        await asyncio.Future()  # Run forever


# Main menu
def main():
    print("=" * 60)
    print("Broadcast Server - Programmatic Usage Examples")
    print("=" * 60)
    print("\nChoose an example to run:")
    print("1. Start server programmatically")
    print("2. Connect client programmatically") 
    print("3. Automated client (sends predefined messages)")
    print("4. Custom message handler")
    print("\nNote: For examples 2-3, make sure a server is running!")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    examples = {
        "1": example_server,
        "2": example_client,
        "3": example_automated_client,
        "4": example_custom_handler
    }
    
    if choice in examples:
        print(f"\nRunning example {choice}...\n")
        try:
            asyncio.run(examples[choice]())
        except KeyboardInterrupt:
            print("\n\nExample stopped by user")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
