import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5) # become a server socket, maximum 5 connections
print "server ready"

while True:
    connection, address = serversocket.accept()
    print connection, address
    buf = connection.recv(64)
    print buf
    connection.send("response")