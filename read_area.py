import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Read_area(QWidget):
    def __init__(self,text,page,local,fname):
        super(Read_area, self).__init__()
        self.page = page
        self.local = local
        self.fname = fname
        self.create_layout(text)

    def create_layout(self,text):
        
        self.textbrower = QTextBrowser(self)
        self.textbrower.setText(text)
        self.textbrower.setStyleSheet("font-family:Simsun")
        self.textbrower.setFixedWidth(1266)

        self.FirstButton = QPushButton("")
        self.FirstButton.setFixedSize(50,50)
        #self.UpButton.setIconSize((60,60))
        #self.UpButton.setStyleSheet('border-image:url(source/Up.png)')
        self.FirstButton.setIcon(QIcon('source/Firstpage.png'))
        self.FirstButton.setToolTip("转跳至首页")

        self.UpButton = QPushButton("")
        self.UpButton.setFixedSize(50,50)
        #self.UpButton.setIconSize((60,60))
        #self.UpButton.setStyleSheet('border-image:url(source/Up.png)')
        self.UpButton.setIcon(QIcon('source/Up.png'))
        self.UpButton.setToolTip("上一页")
        '''
        self.UpButton.setStyleSheet("QPushButton{color:black}"
                                       "QPushButton:hover{color:red}"
                                       "QPushButton{background-color:lightgreen}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}")
        '''
        #self.UpButton.clicked.connect(self.up)

        self.DownButton = QPushButton("")
        self.DownButton.setFixedSize(50,50)
        #self.DownButton.setStyleSheet('border-image:url(source/Down.jpg)')
        self.DownButton.setIcon(QIcon('source/Down.png'))
        self.DownButton.setToolTip("下一页")
        '''
        self.DownButton.setStyleSheet("QPushButton{color:black}"
                                       "QPushButton:hover{color:red}"
                                       "QPushButton{background-color:lightgreen}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}")
        '''

        self.LastButton = QPushButton("")
        self.LastButton.setFixedSize(50,50)
        #self.UpButton.setIconSize((60,60))
        #self.UpButton.setStyleSheet('border-image:url(source/Up.png)')
        self.LastButton.setIcon(QIcon('source/Lastpage.png'))
        self.LastButton.setToolTip("转跳至最后一页")

        self.downloadButton = QPushButton('')
        self.downloadButton.setFixedSize(50,50)
        #self.downloadButton.setStyleSheet("border-image:url(source/download.png)")
        #self.downloadButton.clicked.connect(self.download)
        self.downloadButton.setIcon(QIcon('source/download.png'))
        self.downloadButton.setToolTip("下载")
        '''
        self.downloadButton.setStyleSheet("QPushButton{color:black}"
                                       "QPushButton:hover{color:red}"
                                       "QPushButton{background-color:lightgreen}"
                                       "QPushButton{border:2px}"
                                       "QPushButton{border-radius:10px}"
                                       "QPushButton{padding:2px 4px}")
        '''
        self.pagetext = QLineEdit()
        self.pagetext.setValidator(QIntValidator())
        self.pagetext.setFixedSize(60,20)

        self.pageinfo = QLabel()
        self.pageinfo.setFixedSize(60,20)
        self.pageinfo.setText("当前页数")

        self.pageinfo1 = QLabel()
        self.pageinfo1.setFixedSize(60,20)
        self.pageinfo1.setText(str(self.page))

        self.TurnpageButton = QPushButton("")
        self.TurnpageButton.setFixedSize(40,20)

        self.TurnpageButton.setIcon(QIcon('source/Enter.png'))
        #self.DownButton.clicked.connect(self.down)

        '''
        StarButton = QPushButton('')
        StarButton.setFixedSize(60,60)
        StarButton.setStyleSheet('border-image:url(source/star.jpg)')
        '''
        vbox = QHBoxLayout()
        hbox = QVBoxLayout()

        hbox.addWidget(self.FirstButton)
        hbox.addWidget(self.UpButton)
        hbox.addWidget(self.DownButton)
        hbox.addWidget(self.LastButton)
        hbox.addWidget(self.downloadButton)
        hbox.addStretch(1)
        hbox.addWidget(self.pageinfo)
        hbox.addWidget(self.pageinfo1)
        hbox.addWidget(self.pagetext)
        hbox.addWidget(self.TurnpageButton)
        #hbox.addWidget(StarButton)
        buttonbar = QWidget()
        buttonbar.setLayout(hbox)
        
        vbox.addWidget(self.textbrower)
        vbox.addStretch(1)
        vbox.addWidget(buttonbar)
        self.setLayout(vbox)
        #return vbox

    def set_text(self,text):
        self.textbrower.setText(text)

    def get_page(self):
        return self.page

    def get_local(self):
        return self.local
    
    def get_fname(self):
        return self.fname
    
    def get_turn_page(self):
        return int(self.pagetext.text())

    def set_page(self,page):
        self.page = page
        self.pageinfo.setText("当前页数")
        self.pageinfo1.setText(str(self.page))