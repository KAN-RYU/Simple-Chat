from socket import *
import threading
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class ChatWindow(QMainWindow) :
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
                
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(347, 258)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TextReceive = QtWidgets.QTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TextReceive.sizePolicy().hasHeightForWidth())
        self.TextReceive.setSizePolicy(sizePolicy)
        self.TextReceive.setBaseSize(QtCore.QSize(0, 0))
        self.TextReceive.setUndoRedoEnabled(False)
        self.TextReceive.setReadOnly(True)
        self.TextReceive.setObjectName("TextReceive")
        self.verticalLayout.addWidget(self.TextReceive)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextInput = QtWidgets.QLineEdit(self.widget_2)
        self.TextInput.setDragEnabled(True)
        self.TextInput.setObjectName("TextInput")
        self.horizontalLayout.addWidget(self.TextInput)
        self.ButtonSend = QtWidgets.QPushButton(self.widget_2)
        self.ButtonSend.setObjectName("ButtonSend")
        self.horizontalLayout.addWidget(self.ButtonSend)
        self.verticalLayout.addWidget(self.widget_2)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 347, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ChatClient"))
        self.ButtonSend.setText(_translate("MainWindow", "Send"))
        
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
    