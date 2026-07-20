import asyncio
import websockets
import os
import sys
import webbrowser
import serial

# ARDUINO_PORT = "rfc2217://localhost:4000"
ARDUINO_PORT = "socket://127.0.0.1:4000"
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
                                # Check / establish connection to Wokwi Serial
                board = connect_to_arduino()
                if board and board.is_open:
                    try:
                        # Convert to ASCII text format: "ID,VALUE\n" (e.g., "2,1\n")
                        text_packet = f"{component_id},{value}\n"
                        board.write(text_packet.encode('utf-8'))
                        board.flush()  # Instantly push buffer through network pipe
                        
                        # Give the simulated board a split second to process and respond
                        await asyncio.sleep(0.05) 
                        
                        # --- Read Arduino response ---
                        if board.in_waiting:
                            # data = board.readline().decode(errors="ignore").strip()
                            # if data:
                            #     print(f"📟 Arduino Log: {data}")
                            #     await websocket.send(data)
                            
                            # Run the synchronous readline() inside executor so it doesn't block asyncio
                            loop = asyncio.get_event_loop()
                            data_bytes = await loop.run_in_executor(None, board.readline)
                            data = data_bytes.decode(errors="ignore").strip()
                            if data:
                                print(f"📟 Arduino Log: {data}")
                                await websocket.send(data)
                                
                    except (serial.SerialException, OSError) as e:
                        print(f"🔌 Connection to Wokwi lost: {e}. Reconnecting on next message.")
                        if arduino:
                            try:
                                arduino.close()
                            except Exception:
                                pass
                            arduino = None
                else:
                    print("⚠️ Command dropped: Wokwi simulation is not running or port 4000 is blocked.")
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