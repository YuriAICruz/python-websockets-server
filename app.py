from SocketWrapperServer import Message
from SocketWrapperServer import Connection
from flask import Flask
from flask_sockets import Sockets
import json
from StringIO import StringIO


app = Flask(__name__)
sockets = Sockets(app)

connections = []


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@sockets.route('/gameServer')
def game_messages_listener(ws):
    while True:
        res = ws.receive()
        msg = Message(json.loads(str(res)))

        if msg.id == 1:
            print ("add client: " + msg.uid)
            connections.append(Connection(msg.uid, msg.message, ws))

        json_string = json.dumps(msg.__dict__)
        print (json_string)
        send(ws, "ok")


@app.route('/')
def hello():
    return 'Hello World!'


def send(ws, msg):
    ws.send(msg)


def send_all(msg):
    for conn in connections:
        conn.websocket.send(msg)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
