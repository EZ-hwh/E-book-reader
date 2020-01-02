from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainwindow import *
from register import *
from client import *

class Login(QtWidgets.QMainWindow):

    def __init__(self,sock,bufsize):
        
        super(Login,self).__init__()

        self.sock = sock
        self.bufsize = bufsize
        self.setWindowTitle("登录")
        self.screen = QDesktopWidget().screenGeometry()

        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon('source/book.png'))
        self.width = self.screen.width() * 0.3
        self.height = self.screen.height() * 0.3
        self.setFixedSize(self.width, self.height)
        self.move( (self.screen.width() - self.width) * 0.5 ,(self.screen.height() - self.height) * 0.5 )

        self.setStyleSheet("border-image:url(source/login2.jpg);")
        #self.window.show()
        self.setupUi()

    def setupUi(self):
        #self.centralWidget = QtWidgets.QWidget(MainWindow)
        #self.centralWidget.setObjectName("centralWidget")
        #self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit.setStyleSheet("border-image:none;")
        self.lineEdit_2.setStyleSheet("border-image:none;")
        
        vbox = QHBoxLayout()
        op1 = QtWidgets.QGraphicsOpacityEffect()
        op1.setOpacity(0.6)
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0.3)

        self.lineEdit.setGeometry(QtCore.QRect(self.width*0.25, self.height*0.20, self.width*0.5, self.height*0.135))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText("请输入账号")
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setStyleSheet("background-color:white")
        #self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(self.width*0.25,self.height*0.45, self.width*0.5, self.height*0.135))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText("请输入密码")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(self.width*0.27,self.height * 0.7, self.width *0.46 , self.height * 0.15))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("确定")
        self.pushButton.setStyleSheet("border-image:none;")
        self.pushButton.setGraphicsEffect(op1)

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(self.width * 0, self.height * 0.90, self.width * 0.1 , self.height * 0.1))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("注册")
        self.pushButton_2.setStyleSheet("border-image:none;")
        self.pushButton_2.setGraphicsEffect(op2)
        #MainWindow.setCentralWidget(self.centralWidget)
        #centralWidget = QtWidgets.QWidget()
        #centralWidget.setLayout(vbox)
        #self.setCentralWidget(centralWidget)
        self.setLayout(vbox)
        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(self.register)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    def word_get(self):
        login_user = self.lineEdit.text()
        login_password = self.lineEdit_2.text()
        if (login(self.sock,login_user,login_password,self.bufsize) == 1):#login_user == 'admin' and login_password == '123456':
            mainwindow.set_login(login_user)
            mainwindow.initUi()
            mainwindow.show()
            self.close()
        else:
            QMessageBox.warning(self.pushButton,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()
    
    def register(self):
        ui2.show()
        #self.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    host = '127.0.0.1'
    port = 4396
    addr = (host,port)
    bufsize = 8192

    sock = socket.socket()
    try:
        sock.connect(addr)
        print('have connected with server')
        '''
        while True:
            type = input('type: ')
            if type=='1':
                register()
            elif type=='2':
                login()
            elif type=='3':
                get_title()
            elif type=='4':
                get_content()
            elif type=='5':
                add_path()
            elif type=='6':
                get_path()
            else:
                sock.close()
                break
            print()
        '''     
    except Exception:
        print('error')
        sock.close()
        sys.exit()

    #MainWindow = QtWidgets.QMainWindow()
    ui1 = Login(sock,bufsize)
    ui2 = Register(sock,bufsize)
    mainwindow = Reader(sock,bufsize)
    
    sys.exit(app.exec_())

