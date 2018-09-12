import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


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

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    def init(self):
        websocket.enableTrace(True)
        uri = "ws://" + self.url + ":" + str(self.port)
        print("Starting Server on: " + uri)
        ws = websocket.WebSocketApp(uri,
                                    on_message=lambda w, msg: self.on_message(w, msg),
                                    on_error=lambda w, error: self.on_error(w, error),
                                    on_close=lambda w: self.on_close(w)
                                    )
        ws.on_open = self.on_open
        ws.run_forever()
