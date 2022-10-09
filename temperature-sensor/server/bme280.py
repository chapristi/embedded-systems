import aiohttp_cors
import asyncio
from aiohttp import web
import socketio
import os
import  eventlet

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
async def print_message(sid, message):

    print("Socket ID: " , sid)
    print(message)

async def background_task():
    print('background_task called', flush=True)
    while True:       
       command = "read_bme280"
       res = os.popen(command)
       split = res.read().split("\n")
       await sio.emit('test-event', split[2])
       await sio.sleep(5)
	
app.router.add_get('/', index)

async def init_app():
    sio.start_background_task(background_task)
    return app


if __name__ == '__main__':
    web.run_app(init_app())
