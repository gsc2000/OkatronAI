import asyncio
import websockets
import cv2
import base64
import json
import numpy as np

async def capture_camera(websocket):
    img = cv2.imread("test.jpg")
    img = cv2.imencode('.jpg', img)[1]
    # img_base64 = base64.b64encode(img).decode('utf-8')
    print(type(img))
    print(img.shape)
    await websocket.send(img.tobytes())
    await asyncio.sleep(0.1)

# async def run_websocket_server():
#     async with websockets.serve(websocket_handler, "localhost", 8081):
#         await asyncio.Future()  # run forever

async def websocket_handler(websocket, path):
    while True:
        try:
            await websocket.recv()
            print("Recv")
            await capture_camera(websocket)
        except:
            pass

async def main():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8050):
        await asyncio.Future()

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

asyncio.run(main())
