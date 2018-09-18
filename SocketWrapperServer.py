class Message:
    def __init__(self, obj):
        if obj is None:
            return

        self.id = obj["id"]
        self.objectId = obj["objectId"]
        self.uid = obj["uid"]
        self.message = obj["message"]

    def init_from_args(self, id, uid, message):
        self.id = id
        self.uid = uid
        self.message = message

    id = 0
    uid = ''
    message = ''
    objectId = 0


class ObjectData:
    def __init__(self, index, oId, owner):
        self.index = index
        self.id = oId
        self.owner = owner

    index = 0
    id = 0
    owner = ""


class Connection:
    def __init__(self, uid, name, websocket):
        self.uid = uid
        self.name = name
        self.websocket = websocket

    uid = ''
    name = ''
    websocket = ''
