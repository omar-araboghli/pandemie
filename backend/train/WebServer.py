import socket
import json

HOST = 'localhost'
PORT = 50123

class WebServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(0)

    def acceptConnection(self):
        self.request, addr = self.sock.accept()
        self.request.settimeout(None)

    def recieveMessage(self):
        msg = bytearray()

        while True:
            try:
                receivedData = self.request.recv(1024)
            except:
                raise Exception("connection interrupted")
            if len(receivedData) < 1024:
                msg += receivedData
                break
            else:
                msg += receivedData

        # convert to string and remove headers then return as json
        msg = msg.decode('utf-8')
        msg = msg[msg.find('{'):]

        return json.loads(msg)

    def sendMessage(self, msg):
        msg = json.dumps(msg)
        info = 'HTTP/1.1 200 OK'
        headers = 'Content-Length: {}\nContent-Type: application/json'.format(len(msg))
        response = '{}\n{}\n\n{}'.format(info, headers, msg)
        response = bytearray(response, 'utf-8')
        self.request.send(response)

        # get the next request
        return self.recieveMessage()

    def endConnection(self):
        self.request.close()