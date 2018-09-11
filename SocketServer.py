import asyncio
import json
import websockets


class Message:
    def __init__(self, obj):
        self.id = obj["id"]
        self.uid = obj["uid"]
        self.message = obj["message"]

    def init_from_args(self, id, uid, message):
        self.id = id
        self.uid = uid
        self.message = message

    id = 0
    uid = ''
    message = ''

class Connection:
    def __init__(self, uid, name, websocket):
        self.uid = uid
        self.name = name
        self.websocket = websocket

    uid = ''
    name = ''
    websocket = ''


class Server:
    def __init__(self, url, port):
        self.url = url
        self.port = port

    url = 'localhost'
    port = 5000
    connections = []

    def init(self):
        print("Starting Server")
        start_server = websockets.serve(self.listen, self.url, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)

        print("Server Started")

        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket, path):
        res = await websocket.recv()
        msg = Message(json.loads(res))

        if msg.id == 1:
            self.connections.append(Connection(msg.uid, msg.message, websocket))

        await self.send_all("ok")

        print(self.connections)

    async def send(self, websocket, data):
        await websocket.send(data)

    async def send_all(self, data):
        for conn in self.connections:
            await conn.websocket.send(data)
