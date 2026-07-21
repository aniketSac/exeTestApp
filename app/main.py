import os
import sys
from pathlib import Path

import asyncio
import threading
import websockets
import webview

from runtime_config import configure_pythonnet_runtime_before_webview

# ==============================================================================
# CRITICAL FIX FOR WINDOWS 10 & 11 (PyInstaller + pywebview + pythonnet)
# ==============================================================================
configure_pythonnet_runtime_before_webview()
# ============================================================================== 


# 1. Resolve asset path for PyInstaller bundle
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return os.path.join(base_path, relative_path)

    base_path = Path(__file__).resolve().parent
    return str((base_path / relative_path).resolve())

# 2. WebSocket Handler (Port 8765)
async def handle_client(websocket):
    print("🚀 Browser UI hooked into Python pipeline!")
    
    async for message in websocket:
        if isinstance(message, bytes):
            payload = list(message)
            
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

# 3. Start the Asyncio Loop in a background thread
def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_server():
        async with websockets.serve(handle_client, "127.0.0.1", 8765):
            print("⚡ WebSocket engine spinning on ws://127.0.0.1:8765...")
            await asyncio.Future()  # Keep running

    loop.run_until_complete(run_server())

if __name__ == "__main__":
    # Start WebSocket server thread
    server_thread = threading.Thread(target=start_websocket_server, daemon=True)
    server_thread.start()

    # Load local index.html directly into pywebview GUI window
    html_file = resource_path("index.html")
    
    window = webview.create_window(
        title="My Control App", 
        url=html_file, 
        width=900, 
        height=700
    )

    # Force EdgeChromium runtime
    webview.start(gui='edgechromium')