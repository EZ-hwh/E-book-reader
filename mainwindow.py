
# -*- coding: utf-8 -*-
# @Date    : 2018/6/4 19:28 
# @Author  : yw 


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_PyReader import Ui_MainWindow
from client import *
from read_area import Read_area

class Reader(QMainWindow, Ui_MainWindow):

    def __init__(self,sock,bufsize):
        super(Reader, self).__init__()

        self.sock = sock
        self.bufsize = bufsize 

        self.setWindowTitle("电子书阅读系统")
        self.setWindowIcon(QIcon('source/book.png'))
        self.screen = QDesktopWidget().screenGeometry()
        self.setupUi(self)
        
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)
        self.setFixedSize(self.screen.width(), self.screen.height() - 75)
        self.table = QTableWidget()
        self.table1 = QTableWidget()
        self.local_tab = QWidget()
        self.network_tab = QWidget()
        self.tabwidget = QTabWidget()
        
        self.set_serach_bar()


        self.tabwidget.addTab(self.table, '本地书库')
        self.setCentralWidget(self.tabwidget)
        self.tabwidget.addTab(self.network_tab,'网络书库')
        self.tabwidget.setTabsClosable(True)
        
        self.tabwidget.tabCloseRequested[int].connect(self.remove_tab)
        #self.initUi()

    def set_login(self,username):
        self.username = username

    def set_serach_bar(self):
        #local
        '''
        self.local_search_widget = QWidget() # 右侧顶部搜索框部件
        local_search_layout = QHBoxLayout() # 右侧顶部搜索框网格布局
        self.local_search_icon = QLabel(chr(0xf002) + ' '+'搜索  ')
        self.local_search_input = QLineEdit()
        self.local_search_input.setPlaceholderText("输入歌手、歌曲或用户，回车进行搜索")

        local_search_layout.addWidget(self.local_search_icon)
        local_search_layout.addWidget(self.local_search_input)
        hbox = QVBoxLayout()
        self.local_search_widget.setLayout(local_search_layout)
        hbox.addWidget(self.local_search_widget)
        hbox.addWidget(self.table)
        self.local_tab.setLayout(hbox)
        '''
        #network
        self.network_search_widget = QWidget() # 右侧顶部搜索框部件
        network_search_layout = QHBoxLayout() # 右侧顶部搜索框网格布局
        self.network_search_icon = QLabel('搜索  ')
        self.network_search_input = QLineEdit()

        self.network_search_button = QPushButton('')
        self.network_search_button.setFixedSize(50,30)
        self.network_search_button.setIcon(QIcon('source/search.png'))

        self.network_search_input.setPlaceholderText("输入书名，回车进行搜索")
        self.network_search_button.clicked.connect(self.search)

        network_search_layout.addWidget(self.network_search_icon)
        network_search_layout.addWidget(self.network_search_input)
        network_search_layout.addWidget(self.network_search_button)
        hbox = QVBoxLayout()
        self.network_search_widget.setLayout(network_search_layout)
        hbox.addWidget(self.network_search_widget)
        hbox.addWidget(self.table1)
        self.network_tab.setLayout(hbox)

    def initUi(self):
        # 连接
        self._init_bookset()
        self.local_x = 0
        self.local_y = 0
        self.local_crow = self.local_ccol = -1

        self.network_x = 0
        self.network_y = 0
        self.network_crow = self.network_ccol = -1

        self._set_table_style(self.table)
        self._set_table1_style(self.table1)
        self._init_table()
        self._init_table1()
        self.addbar.triggered.connect(self.open)
        #self.update_network_booklist(self.table1)

    def _set_table_style(self,table):
        # 开启水平与垂直滚轴
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置 5 行 8 列 的表格
        table.setColumnCount(8)
        table.setRowCount(5)
        # 设置标准宽度
        self.width = self.screen.width() // 8
        # 设置单元格的宽度
        for i in range(8):
            table.setColumnWidth(i, self.width)
        # 设置单元格的高度
        # 设置纵横比为 4 : 3
        for i in range(5):
            table.setRowHeight(i, self.width * 4 // 3)
        # 隐藏标题栏
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        # 禁止编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不显示网格线
        #table.setShowGrid(False)
        # 将单元格绑定右键菜单
        # 点击单元格，调用 self.generateMenu 函数
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.generate_local_menu)

    def _set_table1_style(self,table):
        # 开启水平与垂直滚轴
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # 设置 5 行 8 列 的表格
        table.setColumnCount(8)
        table.setRowCount(5)
        # 设置标准宽度
        self.width = self.screen.width() // 8
        # 设置单元格的宽度
        for i in range(8):
            table.setColumnWidth(i, self.width)
        # 设置单元格的高度
        # 设置纵横比为 4 : 3
        for i in range(5):
            table.setRowHeight(i, self.width * 4 // 3)
        # 隐藏标题栏
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        # 禁止编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不显示网格线
        #table.setShowGrid(False)
        # 将单元格绑定右键菜单
        # 点击单元格，调用 self.generateMenu 函数
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.generate_network_menu)

    def _init_table(self):
        for i in self.local_booklist:
            self.set_local_icon(i)

    def _init_table1(self):
        for i in self.network_booklist:
            self.set_network_icon(i)

    #def update_network_booklist(self,table):
    #    print("The network booklist is connected!")

    def _init_bookset(self):
        self.network_booklist = get_title(self.sock,self.network_search_input.text(),self.bufsize)
        _, self.local_booklist = get_path(self.sock,self.username,self.bufsize)
        self.read_list = [None,None]
        self.current_page = 0
        self.size = (2.6,2.6)

    def filter_book(self, fname):
        if not fname:
            return False
        if fname not in self.local_booklist:
            self.local_booklist.append(fname)
            title = fname.split('/' or '\\')[-1].replace('.txt','')
            add_path(self.sock,self.username,title,fname,self.bufsize)
            add_record(self.sock,self.username,"0",fname,"1",self.bufsize)
            return True
        return False

    def get_file(self):
        # 打开单个文件
        fname, _ = QFileDialog.getOpenFileName(self, 'Open files', './', '(*.txt)')
        return fname
    
    def open(self):
        # 打开文件
        fname = self.get_file().replace(' ','$')
        if self.filter_book(fname):
            self.set_local_icon(fname)
                
    def set_local_icon(self, fname):
        label = QLabel(self)
        
        label.resize(self.width, self.width * 4 // 3)
        label.setText(fname.split('/' or '\\')[-1].replace('.txt','').replace('$',' '))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Yahei",13))
        label.setStyleSheet("background-color: white;border-image:url(source/bookss.png);border-radius:100px")
        self.table.setCellWidget(self.local_x, self.local_y, label)

        del label

        self.local_crow, self.local_ccol = self.local_x, self.local_y

        if (not self.local_y % 7) and (self.local_y):
            self.local_x += 1
            self.local_y = 0
        else:
            self.local_y += 1
        '''
        FIXME:
        self.table.setCellWidget(self.local_x, self.local_y, label)

        del label

        self.local_crow, self.local_ccol = self.local_x, self.local_y

        if (not self.local_y % 7) and (self.local_y):
            self.local_x += 1
            self.local_y = 0
        else:
            self.local_y += 1
        '''
    def set_network_icon(self, fname):
        label = QLabel(self)
        
        label.resize(self.width, self.width * 4 // 3)
        label.setText(fname.replace('$',' '))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Yahei",13))
        label.setStyleSheet("background-color: white;border-image:url(source/bookss.png);border-radius:100px")
        
        self.table1.setCellWidget(self.network_x, self.network_y, label)

        del label

        self.network_crow, self.network_ccol = self.network_x, self.network_y

        if (not self.network_y % 7) and (self.network_y):
            self.network_x += 1
            self.network_y = 0
        else:
            self.network_y += 1

    def generate_local_menu(self, pos):
        row_num = col_num = -1
        # 获取选中的单元格的行数以及列数
        for i in self.table.selectionModel().selection().indexes():
            row_num = i.row()
            col_num = i.column()
        # 若选取的单元格中有元素，则支持右键菜单
        if (row_num < self.local_crow) or (row_num == self.local_crow and col_num <= self.local_ccol):
            menu = QMenu()
            item1 = menu.addAction('开始阅读')
            item2 = menu.addAction('删除图书')
            # 获取选项
            action = menu.exec_(self.table.mapToGlobal(pos))
            if action == item1:
                index = row_num * 8 + col_num
                fname = self.local_booklist[index]
                if fname not in self.read_list and len(self.read_list) < 10:
                    self.read_list.append(fname)
                    self.read_local_book(fname)
            elif action == item2:
                self.delete_book(row_num, col_num)

    def generate_network_menu(self, pos):
        row_num = col_num = -1
        # 获取选中的单元格的行数以及列数
        for i in self.table1.selectionModel().selection().indexes():
            row_num = i.row()
            col_num = i.column()
        # 若选取的单元格中有元素，则支持右键菜单
        if (row_num < self.network_crow) or (row_num == self.network_crow and col_num <= self.network_ccol):
            menu = QMenu()
            item1 = menu.addAction('开始阅读')
            #item2 = menu.addAction('下载图书')
            # 获取选项
            action = menu.exec_(self.table1.mapToGlobal(pos))
            if action == item1:
                index = row_num * 8 + col_num
                fname = self.network_booklist[index]
                if fname not in self.read_list and len(self.read_list) < 10:
                    self.read_list.append(fname)
                    self.read_network_book(fname)
                    #self.read_book(fname)
            #elif action == item2:
            #    self.delete_book(row_num, col_num)

    # 删除图书
    def delete_book(self, row, col):
        # 获取图书在列表中的位置
        index = row * 8 + col
        self.local_x = row
        self.local_y = col
        title = self.local_booklist[index].split('/' or '\\')[-1].replace('.txt','')
        delete_local(self.sock,self.username,title,self.bufsize)
        if index >= 0:
            self.local_booklist.pop(index)
        i, j = row, col
        while 1:
            # 移除 i 行 j 列单元格的元素
            self.table.removeCellWidget(i, j)
            # 一直删到最后一个有元素的单元格
            if i == self.local_crow and j == self.local_ccol:
                break
            if (not j % 7) and j:
                i += 1
                j = 0
            else:
                j += 1
        # 如果 booklist 为空，设置当前单元格为 -1
        if not self.local_booklist:
            self.local_crow = -1
            self.local_ccol = -1
        # 删除图书后，重新按顺序显示封面图片
        for fname in self.local_booklist[index:]:
            self.set_local_icon(fname)
    
    def read_local_book(self, fname):
        print(fname)
        title = fname.split('/' or '\\')[-1].replace('.txt', '').replace('$',' ')
        page_ = get_record(self.sock,self.username,"0",fname,self.bufsize)
        if (page_ == "-1"):
            print("Record wrong!")
        else:
            page = int(page_)
        page, text = self.read_book_page(page,fname.replace('$',' '))
        self.book_add_tab(title+"(loc)", text, page, "0", fname)

    def read_network_book(self, fname):
        page_ = get_record(self.sock,self.username,"1",fname,self.bufsize)
        page_, text = get_content(self.sock,fname,page_,self.bufsize)
        self.book_add_tab(fname.replace('$',' ')+"(net)", text, int(page_), "1", fname)

    def book_add_tab(self, title, text, page, local, fname):
        tab = Read_area(text,page,local,fname)
        tab.UpButton.clicked.connect(self.up)

        tab.UpButton.setShortcut("Alt+P")

        tab.DownButton.clicked.connect(self.down)
        
        tab.DownButton.setShortcut("Alt+N")
        tab.downloadButton.clicked.connect(self.download)
        tab.FirstButton.clicked.connect(self.first)
        tab.LastButton.clicked.connect(self.last)
        tab.TurnpageButton.clicked.connect(self.turnpage)

        self.tabwidget.addTab(tab, title)
        self.tabwidget.setCurrentWidget(tab)
  
    def read_book_page(self, page, fname):
        #FIXME
        with open(fname.replace('$',' '),'r+') as f:
            text = f.read()
        l = len(text)
        maxpage = (l-1)//2500 + 1
        if (page <= 0):
            page = 1 
        elif (page > maxpage):
            page = maxpage
        if (page < maxpage):
            return (page,text[2500*(page-1):2500*page])
        else:
            return (page,text[2500*(page-1):])

    def download(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "1"):
                text = download(self.sock,fname,self.bufsize)
                filename,filetype = QFileDialog.getSaveFileName(self,
                "Tabbed Text Editor -- Save File As", "./",
                "Text files (*.txt *.*)")
                with open(filename,"w+") as f:
                    f.write(text)
            else:
                QMessageBox.warning(QPushButton(),
                    "警告",
                    "此文件是本地文件，不可下载！",
                    QMessageBox.Yes)
                self.lineEdit.setFocus()
        print("Download")

    def up(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            page = tab.get_page()-1
            #tab.set_page(page)
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "0"):
                page, text = self.read_book_page(page,fname)
            else:
                page, text = get_content(self.sock, fname, str(page), self.bufsize)

            tab.set_page(int(page))
            tab.set_text(text)
        print("up")

    def down(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            page = tab.get_page()+1
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "0"):
                page, text = self.read_book_page(page,fname)
            else:
                page, text = get_content(self.sock, fname, str(page), self.bufsize)

            tab.set_page(int(page))
            tab.set_text(text)
        print("down")

    def turnpage(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            page = tab.get_turn_page()
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "0"):
                page, text = self.read_book_page(page,fname)
            else:
                page, text = get_content(self.sock, fname, str(page), self.bufsize)

            tab.set_page(int(page))
            tab.set_text(text)
        print("turnpage")
    
    def first(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            #page = tab.get_turn_page()
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "0"):
                page, text = self.read_book_page(0,fname)
            else:
                page, text = get_content(self.sock, fname, "0", self.bufsize)

            tab.set_page(int(page))
            tab.set_text(text)
        print("first")

    def last(self):
        tab = self.tabwidget.currentWidget()
        index = self.tabwidget.currentIndex()
        if (index >= 2):
            #page = tab.get_turn_page()
            local = tab.get_local()
            fname = tab.get_fname()
            if (local == "0"):
                page, text = self.read_book_page(999999,fname)
            else:
                page, text = get_content(self.sock, fname, "999999", self.bufsize)

            tab.set_page(int(page))
            tab.set_text(text)
        print("last")

    def remove_tab(self, index):
        if (index>1):
            print(index)
            self.current_page = 0
            tab = self.tabwidget.widget(index)
            page = tab.get_page()
            local = tab.get_local()
            fname = tab.get_fname()
            add_record(self.sock,self.username,local,fname,str(page),self.bufsize)
            self.tabwidget.removeTab(index)

            self.read_list.pop(index)
            print(self.read_list)

    def search(self):
        self.network_booklist = get_title(self.sock,self.network_search_input.text(),self.bufsize)
        print("network_booklist")
        print(self.network_booklist)
        self.network_x = 0
        self.network_y = 0
        i, j = 0, 0
        if (self.network_crow != -1 or self.network_ccol != -1):
            while 1:
                # 移除 i 行 j 列单元格的元素
                self.table1.removeCellWidget(i, j)
                # 一直删到最后一个有元素的单元格
                if i == self.network_crow and j == self.network_ccol:
                    break
                if (not j % 7) and j:
                    i += 1
                    j = 0
                else:
                    j += 1
        # 如果 booklist 为空，设置当前单元格为 -1
        # 删除图书后，重新按顺序显示封面图片
        self.network_crow = -1
        self.network_ccol = -1
        for fname in self.network_booklist:
            self.set_network_icon(fname)
        print()

    def closeEvent(self, event):
        # do stuff
        print("the window is going to close")
        
        reply = QMessageBox.question(self, '警告', '退出后阅读记录将会自动保存,\n你确认要退出吗？',
                                           QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i in range(2,self.tabwidget.count()):
                tab = self.tabwidget.widget(i)

                page = tab.get_page()
                local = tab.get_local()
                fname = tab.get_fname()
                add_record(self.sock,self.username,local,fname,str(page),self.bufsize)
            event.accept()
        else:
            event.ignore()
        # let the window close

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = Reader()
    reader.show()
    sys.exit(app.exec_())

