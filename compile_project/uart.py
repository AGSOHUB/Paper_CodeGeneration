import socket

def read_from_socket(host='localhost', port=3456):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
        while True:
            data = s.recv(1024)
            if not data:
                break
            # print(data)
            print(f"Received: {data.decode('ascii')}")

if __name__ == "__main__":
    read_from_socket()