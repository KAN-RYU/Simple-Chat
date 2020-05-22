from socket import *
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import uic

form_class = uic.loadUiType("client.ui")[0]

class ChatWindow(QMainWindow, form_class) :
    message = pyqtSignal(str)
    nickname = pyqtSignal(str)
                      
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
        self.nickname.connect(self.setTitle)
                
    def textSend(self):
        self.clientSock.send(self.TextInput.text().encode('utf-8'))
        self.TextInput.setText('')
    
    @pyqtSlot(str)
    def textRec(self, message):
        self.TextReceive.append(message)
        
    @pyqtSlot(str)
    def setTitle(self, nickname):
        self.setWindowTitle(nickname)
    
    def networkRunner(self):
        port = 8081
        
        while True:
            try:
                self.clientSock.connect(('127.0.0.1', port))
            except:
                self.message.emit('Server Connection failed. retry...')
            else:
                break
            
        self.message.emit('Server Connected.')
        firstData = self.clientSock.recv(1024)
        self.message.emit(firstData.decode('utf-8'))
        self.nickname.emit(firstData.decode('utf-8').split(' ')[-1][:-1])
        
        while True:
            recvData = self.clientSock.recv(1024)
            self.message.emit(recvData.decode('utf-8'))

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    myWindow = ChatWindow() 
    myWindow.show()
    app.exec_()
    myWindow.clientSock.close()
    