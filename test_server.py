#!/usr/bin/env python3
"""
Test script for the broadcast server.
This script runs automated tests to verify the server functionality.
"""

import asyncio
import websockets
import time


async def test_server_connection():
    """Test basic connection to the server."""
    print("Test 1: Testing server connection...")
    
    try:
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            print("✓ Successfully connected to server")
            return True
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        return False


async def test_message_broadcast():
    """Test message broadcasting between clients."""
    print("\nTest 2: Testing message broadcasting...")
    
    try:
        uri = "ws://localhost:8765"
        
        # Connect two clients
        async with websockets.connect(uri) as client1, \
                   websockets.connect(uri) as client2:
            
            print("✓ Two clients connected")
            
            # Client 1 sends a message
            test_message = "Test message from client 1"
            await client1.send(test_message)
            print(f"✓ Client 1 sent: '{test_message}'")
            
            # Client 2 should receive the broadcasted message
            try:
                received = await asyncio.wait_for(client2.recv(), timeout=2.0)
                if test_message in received:
                    print(f"✓ Client 2 received: '{received}'")
                    return True
                else:
                    print(f"✗ Unexpected message: '{received}'")
                    return False
            except asyncio.TimeoutError:
                print("✗ Client 2 did not receive message (timeout)")
                return False
                
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


async def test_multiple_clients():
    """Test multiple clients connecting and communicating."""
    print("\nTest 3: Testing multiple clients...")
    
    try:
        uri = "ws://localhost:8765"
        
        # Connect three clients
        async with websockets.connect(uri) as c1, \
                   websockets.connect(uri) as c2, \
                   websockets.connect(uri) as c3:
            
            print("✓ Three clients connected")
            
            # Client 1 sends message
            await c1.send("Hello from C1")
            
            # Both other clients should receive it
            msg2 = await asyncio.wait_for(c2.recv(), timeout=2.0)
            msg3 = await asyncio.wait_for(c3.recv(), timeout=2.0)
            
            if "Hello from C1" in msg2 and "Hello from C1" in msg3:
                print("✓ Message broadcasted to all clients")
                return True
            else:
                print("✗ Message not received by all clients")
                return False
                
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


async def test_client_disconnect():
    """Test client disconnection handling."""
    print("\nTest 4: Testing client disconnection...")
    
    try:
        uri = "ws://localhost:8765"
        
        # Connect two clients
        client1 = await websockets.connect(uri)
        client2 = await websockets.connect(uri)
        
        print("✓ Two clients connected")
        
        # Disconnect client 1
        await client1.close()
        print("✓ Client 1 disconnected")
        
        # Give server time to process disconnect
        await asyncio.sleep(0.5)
        
        # Client 2 should still be able to send/receive
        await client2.send("Test after disconnect")
        print("✓ Client 2 can still send messages")
        
        await client2.close()
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


async def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Broadcast Server Test Suite")
    print("=" * 60)
    print("\nMake sure the server is running before running tests!")
    print("Start the server with: python broadcast_server.py start")
    print("\nWaiting 3 seconds before starting tests...")
    await asyncio.sleep(3)
    
    results = []
    
    # Run tests
    results.append(await test_server_connection())
    results.append(await test_message_broadcast())
    results.append(await test_multiple_clients())
    results.append(await test_client_disconnect())
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
    else:
        print(f"✗ {total - passed} test(s) failed")
    
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  NOTE: This test requires the server to be running!")
    print("Open another terminal and run: python broadcast_server.py start\n")
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
