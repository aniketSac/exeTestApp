# for pyinstaller
import os
import sys
from pathlib import Path
# program lib
import asyncio
import websockets
import threading
import webview

# ==============================================================================
# CRITICAL FIX FOR WINDOWS 10 & 11 (PyInstaller + pywebview + pythonnet)
# ==============================================================================
if getattr(sys, 'frozen', False):
    # PyInstaller unpacks bundled DLLs into sys._MEIPASS
    base_path = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
    
    # Search for python3xx.dll in the bundle root and _internal subfolder
    dll_candidates = list(base_path.glob("python3*.dll")) + list((base_path / "_internal").glob("python3*.dll"))
    
    if dll_candidates:
        os.environ["PYTHONNET_PYDLL"] = str(dll_candidates[0].resolve())

# Explicitly initialize pythonnet to use .NET Framework BEFORE webview imports clr
try:
    from pythonnet import set_runtime
    set_runtime("netfx")
except Exception:
    pass
# ==============================================================================


# 1. Resolve asset path for PyInstaller bundle
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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