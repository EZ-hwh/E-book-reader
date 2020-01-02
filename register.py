from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from client import *

class Register(QtWidgets.QMainWindow):
    
    def __init__(self,sock,bufsize):
        
        super(Register,self).__init__()

        self.sock = sock
        self.bufsize = bufsize
        self.setWindowTitle("注册")
        self.screen = QDesktopWidget().screenGeometry()

        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon('source/book.png'))
        self.width = self.screen.width() * 0.3
        self.height = self.screen.height() * 0.4
        self.setFixedSize(self.width, self.height)
        self.move( (self.screen.width() - self.width) * 0.5 ,(self.screen.height() - self.height) * 0.5 )

        #self.window = QtWidgets.QMainWindow(self)
        #palette1 = QPalette()
       #填写图片的绝对路径
        #palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('source/login.jpg')))
        #self.setPalette(palette1)
        #pixmap = QPixmap("source/login.jpg")
        #pixmap.scaled(self.screen.width()//4, self.screen.height()//4,QtCore.Qt.AspectRatio)
        #palette = QPalette()
        #palette.setBrush(QPalette.Background, QBrush(pixmap))
        #self.setPalette(palette)
        self.setStyleSheet("border-image:url(source/login3.jpg);")
        #self.window.show()
        self.setupUi()

    def setupUi(self):
        #self.centralWidget = QtWidgets.QWidget(MainWindow)
        #self.centralWidget.setObjectName("centralWidget")
        #self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit.setStyleSheet("border-image:none;")
        self.lineEdit_2.setStyleSheet("border-image:none;")
        self.lineEdit_3.setStyleSheet("border-image:none;")
        
        vbox = QHBoxLayout()
        op1 = QtWidgets.QGraphicsOpacityEffect()
        op1.setOpacity(0.6)
        op2 = QtWidgets.QGraphicsOpacityEffect()
        op2.setOpacity(0.3)

        self.lineEdit.setGeometry(QtCore.QRect(self.width*0.25, self.height*0.20, self.width*0.5, self.height*0.115))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText("请输入账号")
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setStyleSheet("background-color:white")
        #self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(self.width*0.25,self.height*0.40, self.width*0.5, self.height*0.115))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText("请输入密码")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3.setGeometry(QtCore.QRect(self.width*0.25,self.height*0.60, self.width*0.5, self.height*0.115))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setPlaceholderText("请输入密码")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_2")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(self.width*0.27,self.height * 0.80, self.width *0.46 , self.height * 0.13))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("确定")
        self.pushButton.setStyleSheet("border-image:none;")
        self.pushButton.setGraphicsEffect(op1)
        #MainWindow.setCentralWidget(self.centralWidget)
        self.setLayout(vbox)
        self.pushButton.clicked.connect(self.word_get)

        QtCore.QMetaObject.connectSlotsByName(self)


    def word_get(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        password2 = self.lineEdit_3.text()
        if (password == password2):
            # FIXME: 加载登录的数据
            if (register(self.sock,username,password,self.bufsize) == 1):
                self.close()
            else:
                QMessageBox.warning(self.pushButton,
                        "警告",
                        "用户名已被注册！",
                        QMessageBox.Yes)
                self.lineEdit.setFocus()
        else:
            QMessageBox.warning(self.pushButton,
                    "警告",
                    "请保证两次密码相同！",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()
