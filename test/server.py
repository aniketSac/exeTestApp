import asyncio
import websockets

async def handle_connection(websocket):
    print(f"Client connected: {websocket.remote_address}")
    try:
        # Keep the connection alive and listen for messages
        async for message in websocket:
            print(f"Received from client: {message}")
            
            # Send a response back to the client
            response = f"Server received: '{message}'"
            await websocket.send(response)
            
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    # Start the server on localhost, port 8765
    # async with websockets.serve(handle_connection, "localhost", 8765):
    async with websockets.serve(handle_connection, "0.0.0.0", 8000):
        print("WebSocket server started on wss://localhost:8000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())