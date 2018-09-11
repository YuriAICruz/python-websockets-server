import SocketServer
import asyncio

server = SocketServer.Server("127.0.0.1", 5000)
server.init()


