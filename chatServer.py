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
            message = 'Disconnected by ' + name
            messageQ.put(message)
            print(message + ' ' + str(addr[0]) + ":" + str(addr[1]))
            
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
    serverSock.settimeout(10)
    while True:
        try:
            connectionSock, addr = serverSock.accept()
            lock.acquire()
            nickname = name[nameIndex] + '_' + str(nameIndex)
            client.append((connectionSock, nickname, addr))
            print('Connected from', addr, 'Nickname is', nickname)
            connectionSock.send(str('Your name is ' + nickname + '.').encode('utf-8'))
            receiver.append(threading.Thread(target=receive, args=(connectionSock, nickname, addr)))
            receiver[-1].daemon = True
            receiver[-1].start()
            nameIndex = (nameIndex + 1) % 8
            lock.release()
        except:
            time.sleep(0.01)
    
    serverSock.close()