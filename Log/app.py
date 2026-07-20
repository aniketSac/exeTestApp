import asyncio
import websockets
import os
import sys
import webbrowser
import serial


arduino = serial.Serial('COM3', 9600) 
def get_asset_path(relative_path):
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
                    print(f"🎯 Action: Bitmask Updated -> {bin(value)[2:].zfill(6)} (Dec: {value})")
                elif component_id == 2:
                    print(f"🎯 Action: Toggle 1 flipped -> {'ON' if value == 1 else 'OFF'}")
                elif component_id == 3:
                    print(f"🎯 Action: Toggle 2 flipped -> {'ON' if value == 1 else 'OFF'}")
                elif component_id == 4:
                    print(f"🎯 Action: Radio Group A changed -> Option {value}")
                elif component_id == 5:
                    print(f"🎯 Action: Radio Group B changed -> Option {value}")
                else:
                    print(f"⚠️ Unknown Component ID received: {component_id}")
                print("------------------------------")
                
                arduino.write(bytes([component_id, value]))

                # --- Read Arduino response (if any) ---
                if arduino.in_waiting:
                    data = arduino.readline().decode(errors="ignore").strip()
                    if data:
                        await websocket.send(data)
            else:
                print(f"Incomplete payload layout received: {len(payload)} bytes.")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket engine spinning on port 8765...")

        # 2. Get the path to your index.html and open it automatically
        html_file_path = get_asset_path("frontend/index.html")
        if os.path.exists(html_file_path):
            webbrowser.open(f"file://{html_file_path}")
        else:
            print(f"⚠️ Error: Could not find HTML file at {html_file_path}")
        
        await asyncio.Future();

if __name__ == "__main__":
    asyncio.run(main())