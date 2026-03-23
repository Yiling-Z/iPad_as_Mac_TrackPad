import asyncio
import websockets
import pyautogui
import socket

# 核心优化：关闭pyautogui的平滑移动，减少漂移
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.001  # 最小延迟，避免卡顿
SPEED = 8  # 降低灵敏度，减少抖动放大（原15太高）
MIN_MOVE = 1  # 最小位移阈值：小于1px不处理，防抖

async def handle_connection(websocket):
    """处理iPad连接，增加位移防抖"""
    client_addr = websocket.remote_address
    print(f"✅ 已连接iPad: {client_addr}")
    try:
        async for message in websocket:
            parts = message.split()
            if not parts:
                continue
            
            cmd = parts[0]
            # 移动光标：增加最小位移判定，防抖
            if cmd == "move" and len(parts) >= 3:
                dx = float(parts[1]) * SPEED
                dy = float(parts[2]) * SPEED
                # 过滤微小位移，避免漂移
                if abs(dx) > MIN_MOVE or abs(dy) > MIN_MOVE:
                    pyautogui.moveRel(dx, dy, duration=0)  # 0延迟，精准跟手
            elif cmd == "click":
                pyautogui.click()
            elif cmd == "right":
                pyautogui.rightClick()
            elif cmd == "scroll" and len(parts) >= 2:
                dy = int(parts[1])
                pyautogui.scroll(dy)
    except Exception as e:
        print(f"⚠️ iPad连接已断开: {e}")
    finally:
        print("🔌 鼠标服务已关闭")

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8888):
        print("✅ 鼠标控制服务启动成功（端口8888）")
        print("等待 iPad 连接...")
        mac_ip = socket.gethostbyname(socket.gethostname())
        print(f"📌 你的 Mac 局域网IP：{mac_ip}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
