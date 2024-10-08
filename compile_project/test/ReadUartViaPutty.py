import socket

class ReadUartViaPutty:
    def __init__(self):
        self.s = None
    def socket_connect(self, host='localhost', port=3456):
        self.s=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print(f"Connected to {host}:{port}")
    def read_from_socket(self ):
        # while True:
        data = self.s.recv(1024)
        print(f"Received: {data.decode('ascii')}")
        return data.decode('ascii')
    def socket_disconnect(self):
        self.s.close() 
        self.s = None       

