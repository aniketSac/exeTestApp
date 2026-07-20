import asyncio
import websockets
import serial

arduino = serial.Serial('COM3', 9600)  # Adjust the port and baud rate as needed
    
async def handle_client(websocket):
    print("🚀 Browser connected! Listening for targeted input streams.")
    
    async for message in websocket:
        if isinstance(message, bytes):
            payload = list(message)
            
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
                   # --- Forward packet to Arduino ---
                arduino.write(bytes([component_id, value]))

                # --- Read Arduino response (if any) ---
                if arduino.in_waiting:
                    data = arduino.readline().decode(errors="ignore").strip()
                    if data:
                        await websocket.send(data)
            else:
                print(f"Error: Expected a 2-byte packet, got {len(payload)} bytes.")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket engine spinning on port 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())