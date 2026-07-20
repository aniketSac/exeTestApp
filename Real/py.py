import asyncio, websockets, serial, time, sys
import serial.tools.list_ports as lp

for p in lp.comports():
    print(f'Device: {p.device} | Descrition : {p.description}')

# Updated to look for clones as well
port = next((p.device for p in lp.comports() if any(k in p.description for k in ("Mega", "Arduino", "CH340", "USB Serial"))), None)
if not port : sys.exit("Arduino not Found")

arduino = serial.Serial(port,9600)
print("\n------------------------------")
print(f"found on {port} waiting for reset")
time.sleep(2)
print(f"\n ready on {port}")
print("\n------------------------------")


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
               
                arduino.write(bytes([component_id,value]))
                text_arduino = arduino.write(bytes([component_id,value]))
                print(f"arduino : {text_arduino}") #2
                print(f"{text_arduino[0]}") # serial read warnL 'int' object is not subscriptable
                # read Arduino
               
                if arduino.in_waiting:
                    loop = asyncio.get_event_loop()
                    while arduino.in_waiting:
                        data_bytes = await loop.run_in_executor(None, arduino.readline)
                        data = data_bytes.decode(errors="ignore").strip()
                        if data:
                            print(f"📟 Arduino Log: {data}")
                            await websocket.send(data)
                                
            else:
                print(f"Incomplete payload layout received: {len(payload)} bytes.")

async def main():
    # async with websockets.serve(handle_client, "0.0.0.0", 8765):
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket engine spinning on port 8765...")
        await asyncio.Future();

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Python pipeline. Goodbye!")