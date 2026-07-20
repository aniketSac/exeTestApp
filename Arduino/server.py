import asyncio
import websockets
import os
import sys
import webbrowser
import serial

ARDUINO_PORT = "rfc2217://localhost:4000"
BAUD_RATE = 9600

# Global reference for the serial connection
arduino = None

def connect_to_arduino():
    """Attempts to connect to the Wokwi serial port. Returns serial instance or None."""
    global arduino
    try:
        if arduino is None or not arduino.is_open:
            print(f"🔌 Connecting to Wokwi Mega Serial Bridge ({ARDUINO_PORT})...")
            # Using write_timeout to prevent the event loop from hanging indefinitely
            arduino = serial.serial_for_url(ARDUINO_PORT, baudrate=BAUD_RATE, timeout=0.1, write_timeout=1)
            print("✅ Connected to virtual Arduino!")
        return arduino
    except Exception:
        arduino = None
        return None

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
                    print(f"🎯 Action: Bitmask Updated -> {bin(value)[2:].zfill(6)} (Dec: {value}), byte {bytes([value])}")
                elif component_id == 2:
                    print(f"🎯 Action: Toggle 1 flipped -> {'ON' if value == 1 else 'OFF'}, byte {bytes([value])}")
                elif component_id == 3:
                    print(f"🎯 Action: Toggle 2 flipped -> {'ON' if value == 1 else 'OFF'}, byte {bytes([value])}")
                elif component_id == 4:
                    print(f"🎯 Action: Radio Group A changed -> Option {value}, byte {bytes([value])}")
                elif component_id == 5:
                    print(f"🎯 Action: Radio Group B changed -> Option {value}, byte {bytes([value])}")
                else:
                    print(f"⚠️ Unknown Component ID received: {component_id}")
                print("------------------------------")
            else:
                print(f"Incomplete payload layout received: {len(payload)} bytes.")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket engine spinning on port 8765...")
        await asyncio.Future();

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Python pipeline. Goodbye!")