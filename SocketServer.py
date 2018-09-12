from flask import Flask
from flask_sockets import Sockets


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


app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

class Server:
    def __init__(self, port):
        self.port = port

    port = 5000
    connections = []

    @sockets.route('/echo')
    def echo_socket(self, ws):
        while True:
            message = ws.receive()
            ws.send(message[::-1])

    @app.route('/')
    def hello(self):
        return 'Hello World!'

    @app.route('/echo_test', methods=['GET'])
    def echo_test(self):
        return render_template('echo_test.html')

    def init(self):
        uri = "ws://127.0.0.1:" + str(self.port)
        print("Starting server: " + uri)

        from gevent import pywsgi
        from geventwebsocket.handler import WebSocketHandler
        server = pywsgi.WSGIServer(('', self.port), app, handler_class=WebSocketHandler)
        server.serve_forever()

        app.run()
