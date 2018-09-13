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
        send(ws, message)


@sockets.route('/status.sock')
def status_sock(ws):
    while True:
        message = ws.receive()
        print (message)


@sockets.route('/gameServer')
def game_messages_listener(ws):
    while True:
        if ws.closed:
            conn = find(lambda c: c.websocket == ws, connections)

            if conn is not None:
                remove(lambda c: c.websocket == ws, connections)
                smsg = Message(None)
                smsg.init_from_args(2, "", "closed")
                send_all(smsg)
                print ("connection from " + conn.uid + " closed")
            else:
                print ("connection closed")
            break

        res = ws.receive()

        if res is None:
            continue

        msg = Message(json.loads(str(res)))

        if msg.id == 1:
            print ("add client: " + msg.uid)
            connections.append(Connection(msg.uid, msg.message, ws))
            print (connections)

        json_string = json.dumps(msg.__dict__)
        print (json_string)
        send(ws, "ok")


@app.route('/')
def hello():
    return 'Hello World!'


def send(ws, msg):
    try:
        ws.send(msg)
    except Exception as e:
        print (e)


def send_all(msg):
    for conn in connections:
        try:
            conn.websocket.send(msg)
        except Exception as e:
            print (e)


def find(f, seq):
    for item in seq:
        if f(item):
            return item


def remove(f, seq):
    i = 0
    for item in seq:
        if f(item):
            seq.pop(i)
            return
        i = i + 1


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    print(server)
    print (server.connections)
    server.serve_forever()
