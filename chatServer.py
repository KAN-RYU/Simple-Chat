from socket import *
import threading
from queue import Queue
import time

#TODO optimize thread list

messageQ = Queue()
client = []
name = ['umjoonsik', 'abrium', 'booo', 'foo', 'chris', 'top', 'pot', 'chat']
nameIndex = 0
lock = threading.Lock()

def send():
    while True:
        message = messageQ.get()
        lock.acquire()
        for sock, name, addr in client:
            sock.send(message.encode('utf-8'))
        lock.release()

def receive(sock, name, addr):
    while True:
        try:
            recvData = sock.recv(1024)
            decoded = name + " : " + recvData.decode('utf-8')
            messageQ.put(decoded)
            print(decoded)
        
        except:
            lock.acquire()
            message = 'Disconnected by ' + name + ' ' + str(addr[0]) + ":" + str(addr[1])
            messageQ.put(message)
            print(message)
            
            for i in range(len(client)):
                if client[i][2][0] == addr[0] and client[i][2][1] == addr[1]:
                    client.pop(i)
                    break
            lock.release()
            break
            

if __name__ == "__main__":
    port = 8081

    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(8)

    print('Server Started.')
    sender = threading.Thread(target=send, args=())
    sender.daemon = True
    sender.start()
    
    receiver = []
    while True:
        connectionSock, addr = serverSock.accept()
        lock.acquire()
        client.append((connectionSock, name[nameIndex], addr))
        print('Connected from', addr, 'Name is', name[nameIndex])
        connectionSock.send(str('Your name is ' + name[nameIndex] + '.').encode('utf-8'))
        receiver.append(threading.Thread(target=receive, args=(connectionSock, name[nameIndex], addr)))
        receiver[-1].daemon = True
        receiver[-1].start()
        nameIndex = (nameIndex + 1) % 8
        lock.release()
    
    serverSock.close()