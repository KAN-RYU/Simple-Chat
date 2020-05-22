from socket import *
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

def run():
    def send(sock):
        while True:
            sendData = input('>>>')
            sock.send(sendData.encode('utf-8'))


    def receive(sock):
        while True:
            recvData = sock.recv(1024)
            print('상대방 :', recvData.decode('utf-8'))


    port = 8081

    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('127.0.0.1', port))

    print('접속 완료')

    sender = threading.Thread(target=send, args=(clientSock,))
    receiver = threading.Thread(target=receive, args=(clientSock,))

    sender.start()
    receiver.start()

    while True:
        time.sleep(1)
        pass
    
form_class = uic.loadUiType("client.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class ChatWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.TextInput.returnPressed.connect(self.textSend)
        self.ButtonSend.clicked.connect(self.textSend)
        
    def textSend(self):
        self.TextReceive.insertHtml(self.TextInput.text())
        self.TextInput.setText('')

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = ChatWindow() 
    myWindow.show()
    ui = threading.Thread(target = app.exec_, args = ())
    print('hi')
    myWindow.TextReceive.append('test')
    input()