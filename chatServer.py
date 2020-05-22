from socket import *
import threading
from queue import Queue
import time

messageQ = Queue()

def send(sock):
    while True:
        message = messageQ.get()
        sock.send(message)

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        messageQ.put(recvData)
        print('상대방 :', recvData.decode('utf-8'))


port = 8081

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen()

print('Wait connection from port %d'%port)

connectionSock, addr = serverSock.accept()

print('Connected from', str(addr))

sender = threading.Thread(target=send, args=(connectionSock,))
receiver = threading.Thread(target=receive, args=(connectionSock,))

sender.daemon = True
receiver.daemon = True

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass