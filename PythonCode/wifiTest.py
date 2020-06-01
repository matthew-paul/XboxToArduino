import socket

HOST = '192.168.1.226'  # The server's hostname or IP address
PORT = 80  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f'Connected to {HOST}')
    s.sendall(f'F{chr(15)}'.encode())
    data = s.recv(1024)

print('Received', repr(data))
