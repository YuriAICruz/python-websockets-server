from SocketWrapperServer import Message
from SocketWrapperServer import Connection
from SocketWrapperServer import ObjectData
from flask import Flask, redirect
from flask_sockets import Sockets
from flask_cors import CORS
import json
from StringIO import StringIO

app = Flask(__name__)
# CORS(app) # remember to remove before publish
sockets = Sockets(app)

nullguid = "00000000-0000-0000-0000-000000000000"

connections = []

dynamicObjects = []

instanced_object = 0


def remove_connection(ws):
    conn = find(lambda c: c.websocket == ws, connections)

    if conn is not None:
        removed = find_all(lambda c: c.owner == conn.uid, dynamicObjects)
        if len(removed) > 0:
            data_message = json.dumps(list(map(lambda x: x.__dict__, removed)))
            dymsg = Message(None)
            dymsg.init_from_args(47, nullguid, data_message)
            send(ws, json.dumps(dymsg.__dict__))
        remove(lambda c: c.owner == conn.uid, dynamicObjects)
        remove(lambda c: c.websocket == ws, connections)
        smsg = Message(None)
        smsg.init_from_args(2, "", "closed")
        json_string = json.dumps(smsg.__dict__)
        send_all(json_string)
        print ("connection from " + conn.uid + " closed")
    else:
        print ("connection closed")


def check_connection(ws):
    conn = find(lambda c: c.websocket == ws, connections)

    if conn == None:
        conn = Connection(nullguid, " ", ws)
        connections.append(conn)

    return conn


def parse_message(msg):
    return Message(json.loads(str(msg)))


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
        global nullguid

        if ws.closed:
            remove_connection(ws)
            break

        global connections
        conn = check_connection(ws)

        message = ws.receive()
        if message is None:
            continue

        msg = parse_message(message)

        if conn.uid == nullguid:
            conn.uid = msg.uid
            print ("Client " + msg.uid + " connected")

        if msg.id == 1:
            if len(dynamicObjects) > 0:
                data_message = json.dumps(list(map(lambda x: x.__dict__, dynamicObjects)))
                dymsg = Message(None)
                dymsg.init_from_args(48, nullguid, data_message)
                send(ws, json.dumps(dymsg.__dict__))

        if msg.id == 49:
            data = json.loads(str(msg.message))
            dynamicObjects.append(ObjectData(data["index"], data["id"], msg.uid))
            print ("Sending instances " + str(len(dynamicObjects)))

        # send(ws, message)
        send_all(message)


@app.route('/')
def hello():
    return redirect("http://127.0.0.1:8000/static/index.html")


@app.route('/static/{file}')
def serve_static(file):
    return app.send_static_file(file)


@app.route('/nextId')
def testRequest():
    # if request.method == 'POST':
    global instanced_object
    instanced_object += 1
    return str(instanced_object)


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


def find_all(f, seq):
    res = []
    for item in seq:
        if f(item):
            res.append(item)
    return res


def remove(f, seq):
    i = 0
    for item in seq:
        if f(item):
            seq.pop(i)
            continue
        i += 1


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    print(server)
    print (server.connections)
    server.serve_forever()
