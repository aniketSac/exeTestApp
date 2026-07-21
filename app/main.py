import asyncio
import os
import sys
import threading
import websockets
import webview


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller _MEIPASS."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

async def handle_client(websocket):
    print("🚀 Browser UI hooked into Python pipeline!")
    
    async for message in websocket:
        if isinstance(message, bytes):
            payload = list(message)
            
            # Make sure we received all expected index fields
            if len(payload) == 2:
                component_id = payload[0]
                value = payload[1]
                
                print("\n------------------------------")
                if component_id == 1:
                    print(f"🎯 Component ID : {component_id} Action: Bitmask Updated -> {bin(value)[2:].zfill(6)} (Dec: {value}), byte {bytes([value])}")
                elif component_id == 2:
                    print(f"🎯 Component ID : {component_id} Action: Toggle 1 flipped -> {'ON' if value == 1 else 'OFF'}, byte {bytes([value])}")
                elif component_id == 3:
                    print(f"🎯 Component ID : {component_id} Action: Toggle 2 flipped -> {'ON' if value == 1 else 'OFF'}, byte {bytes([value])}")
                elif component_id == 4:
                    print(f"🎯 Component ID : {component_id} Action: Radio Group A changed -> Option {value}, byte {bytes([value])}")
                elif component_id == 5:
                    print(f"🎯 Component ID : {component_id} Action: Radio Group B changed -> Option {value}, byte {bytes([value])}")
                else:   
                    print(f"⚠️ Unknown Component ID received: {component_id}")
                print("------------------------------")
            else:
                print(f"Incomplete payload layout received: {len(payload)} bytes.")

def run_websocket_server():
    """Starts the asyncio WebSocket loop in a background thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_server():
        async with websockets.serve(handle_client, "127.0.0.1", 8765):
            print("WebSocket engine spinning on port 8765...")
            await asyncio.Future()  # Keeps the server alive

    try:
        loop.run_until_complete(start_server())
    except KeyboardInterrupt:
        print("\nShutting down WebSocket engine...")


if __name__ == "__main__":
    # 1. Start the WebSocket server in a daemon thread so it doesn't block GUI execution
    server_thread = threading.Thread(target=run_websocket_server, daemon=True)
    server_thread.start()

    # 2. Get the local file path for index.html
    html_path = get_resource_path("index.html")

    # 3. Initialize the desktop window
    webview.create_window(
        title="Control Panel",
        url=f"file://{os.path.abspath(html_path)}",
        width=850,
        height=900,
        min_size=(850, 900),
        resizable=True,
    )

    # 4. Start the native window event loop (must run on the main thread)
    webview.start()