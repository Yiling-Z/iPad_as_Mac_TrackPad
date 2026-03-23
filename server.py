import asyncio
import websockets
import pyautogui
import socket

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.001  
SPEED = 8 
MIN_MOVE = 1  

async def handle_connection(websocket):
    client_addr = websocket.remote_address
    print(f"已连接iPad: {client_addr}")
    try:
        async for message in websocket:
            parts = message.split()
            if not parts:
                continue
            
            cmd = parts[0]

            if cmd == "move" and len(parts) >= 3:
                dx = float(parts[1]) * SPEED
                dy = float(parts[2]) * SPEED

                if abs(dx) > MIN_MOVE or abs(dy) > MIN_MOVE:
                    pyautogui.moveRel(dx, dy, duration=0)  
            elif cmd == "click":
                pyautogui.click()
            elif cmd == "right":
                pyautogui.rightClick()
            elif cmd == "scroll" and len(parts) >= 2:
                dy = int(parts[1])
                pyautogui.scroll(dy)
    except Exception as e:
        print(f"iPad连接已断开: {e}")
    finally:
        print("鼠标服务已关闭")

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8888):
        print("鼠标服务启动")
        print("等待 iPad 连接...")
        mac_ip = socket.gethostbyname(socket.gethostname())
        print(f"你的 Mac 局域网IP：{mac_ip}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
