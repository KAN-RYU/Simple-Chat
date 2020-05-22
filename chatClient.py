from socket import *
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import uic

form_class = uic.loadUiType("client.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class ChatWindow(QMainWindow, form_class) :
    message = pyqtSignal(str)
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        
        self.network = threading.Thread(target = self.networkRunner, args = ())
        self.TextInput.returnPressed.connect(self.textSend)
        self.ButtonSend.clicked.connect(self.textSend)
        self.network.daemon = True
        self.network.start()
        
        self.message.connect(self.textRec)
                
    def textSend(self):
        self.clientSock.send(self.TextInput.text().encode('utf-8'))
        self.TextInput.setText('')
    
    @pyqtSlot(str)
    def textRec(self, message):
        self.TextReceive.append(message)
    
    def networkRunner(self):
        port = 8081
        
        self.clientSock.connect(('127.0.0.1', port))

        self.message.emit('Server Connected.')
        self.message.emit('your name is.')
        
        while True:
            recvData = self.clientSock.recv(1024)
            self.message.emit('상대방 :' + recvData.decode('utf-8'))

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = ChatWindow() 
    myWindow.show()
    app.exec_()
    