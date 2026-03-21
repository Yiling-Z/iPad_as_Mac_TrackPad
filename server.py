import asyncio
import websockets
import pyautogui
import socket

pyautogui.FAILSAFE = False
SPEED = 5

async def handle_connection(websocket):
    client_addr = websocket.remote_address
    print(f"✅ Successfully connected your iPad: {client_addr}")
    try:
        async for message in websocket:
            parts = message.split()
            if not parts:
                continue
            
            cmd = parts[0]
            if cmd == "move" and len(parts) >= 3:
                dx = float(parts[1]) * SPEED
                dy = float(parts[2]) * SPEED
                pyautogui.moveRel(dx, dy)
            elif cmd == "click":
                pyautogui.click()
            elif cmd == "right":
                pyautogui.rightClick()
            elif cmd == "scroll" and len(parts) >= 2:
                dy = int(parts[1])
                pyautogui.scroll(dy)
    except Exception as e:
        print(f"⚠️ iPad disconnected: {e}")
    finally:
        print("🔌 Shutdown service")

async def main():
    """Launch WebSocket"""
    async with websockets.serve(handle_connection, "0.0.0.0", 8888):
        print("✅ Success（Port 8888）")
        print("Waiting for iPad connection...")
        mac_ip = socket.gethostbyname(socket.gethostname())
        print(f"📌 Your Mac IP：{mac_ip}")
        await asyncio.Future()  

if __name__ == "__main__":
    asyncio.run(main())