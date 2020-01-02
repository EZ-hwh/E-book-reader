#! /usr/bin/env python3
# coding utf-8 
from socketserver import BaseRequestHandler,ThreadingTCPServer
import threading
import socket
import threading
from threading import Thread
import threading
import sys
import time
import random
from queue import Queue
import sqlite3

class ThreadPoolManger():
    """线程池管理器"""
    def __init__(self, thread_num):
        # 初始化参数
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        # 初始化线程池，创建指定数量的线程池
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue)
            thread.start()

    def add_job(self, func, *args):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((func, args))

class ThreadManger(Thread):
    """定义线程类，继承threading.Thread"""
    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        # 启动线程
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()

# 创建一个有5个线程的线程池
thread_pool = ThreadPoolManger(5)  
size = 2500

def handle_request(conn_socket):
    name = 'client '+threading.current_thread().name[7]
    print ('%s is running ' % name)
    while True:
        rec = conn_socket.recv(8192)
        rec = rec.decode('utf-8')
        if len(rec)>0:
            print('receive')
            data = ''
            data = data + rec[0]
            vec = rec.split()
            
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            if rec[0]=='0':
                title = vec[2]
                cursor = c.execute("select words from novel where title='%s'"%title)
                valid = 1
                a = []
                for x in cursor:
                    a.append(x)
                if len(a)==0:
                    valid = 0
                data = data + str(valid) + '\n'   
                if valid==1:
                    l = len(a[0][0])
                    maxpage = (l-1)//size+1
                    data = data + 'maxpage: ' + str(maxpage) + '\n'
            elif rec[0]=='1':   
                cursor = c.execute("select username,password from user")
                username = vec[2]
                password = vec[4]
                valid = 1
                for x in cursor:
                    if username==x[0]:
                        valid = 0
                        break
                if valid==1:
                    c.execute("insert into user(username,password)\
                        values('%s','%s')"%(username,password))
                data = data + str(valid) + '\n'                            
            elif rec[0]=='2':
                cursor = c.execute("select username,password from user")
                username = vec[2]
                password = vec[4]
                valid = 0
                for x in cursor:
                    if username==x[0] and password==x[1]:
                        valid = 1
                        break
                data = data + str(valid)                     
            elif rec[0]=='3':
                title = vec[2]
                if title=='*':
                    cursor = c.execute("select title from novel")
                else :
                    cursor = c.execute("select title from novel where title like '%%%s%%'"%title)
                valid = 1
                a = []
                for x in cursor:
                    a.append(x)
                if len(a)==0:
                    valid = 0
                data = data + str(valid) +'\n'
                for x in a:
                    data = data + 'title: ' + str(x[0]) + '\n'                
            elif rec[0]=='4':
                title = vec[2]
                page = int(vec[4])
                cursor = c.execute("select words from novel where title='%s'"%title)
                valid = 1
                a = []
                for x in cursor:
                    a.append(x)
                if len(a)==0 :
                    valid = 0
                data = data + str(valid) +'\n'
                if valid==1:
                    l = len(a[0][0])
                    maxpage = (l-1)//size+1
                    if page<1:
                        page = 1
                    if page>maxpage:
                        page = maxpage
                    data = data + 'page: ' + str(page) +'\n'
                    data = data + 'text: '
                    while len(data)<19:
                        data = data + ' '
                    data = data + '\n'
                    data = data + a[0][0][(page-1)*size:page*size] 
            elif rec[0]=='5':
                username = vec[2]
                title = vec[4]
                path = vec[6]
                valid = 1
                cursor = c.execute("select username,title from upload")
                for x in cursor:
                    if username==x[0] and title==x[1]:
                        valid = 0
                        break
                data = data + str(valid) +'\n' 
                if valid==1:
                    c.execute("insert into upload(username,title,path) \
                            values('%s','%s','%s')"%(username,title,path))     
            elif rec[0]=='6':
                username = vec[2]
                cursor = c.execute("select title,path from upload where username='%s'"%username)
                valid = 1
                a = []
                for x in cursor:
                    a.append(x)
                if len(a)==0:
                    valid = 0
                data = data + str(valid) +'\n'
                for x in a:
                    data = data + 'title: ' + str(x[0]) + '\n'    
                    data = data + 'path: ' + str(x[1]) + '\n'   
            elif rec[0]=='7':
                username = vec[2]
                local = vec[4]
                title = vec[6]
                page = vec[8]
                c.execute("delete from last \
                        where username='%s' and local='%s' and title='%s'"%(username,local,title))
                conn.commit()
                c.execute("insert into last(username,local,title,page) \
                        values('%s','%s','%s','%s')"%(username,local,title,page))
                valid = 1
                data = data + str(valid) +'\n'  
            elif rec[0]=='8': 
                username = vec[2]
                local = vec[4]
                title = vec[6]
                cursor = c.execute("select page from last \
                    where username='%s' and local='%s' and title='%s'"%(username,local,title))
                valid = 1
                a = []
                for x in cursor:
                    a.append(x)
                if len(a)==0:
                    valid = 0
                data = data + str(valid) +'\n'
                for x in a:   
                    data = data + 'page: ' + str(x[0]) + '\n' 
            elif rec[0]=='9': 
                username = vec[2]
                title = vec[4]
                c.execute("delete from upload \
                        where username='%s' and title='%s'"%(username,title))
                c.execute("delete from last \
                    where username='%s' and local='0' and title='%s'"%(username,title))
                valid = 1
                data = data + str(valid) +'\n'
                
            conn.commit()
            conn.close()
                
            conn_socket.sendall(data.encode('utf-8'))
            print('response')
            print()
        else:
            print('%s is closed ' % name)
            break
    
    conn_socket.close()

if __name__ == '__main__':
    '''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    c.execute('create table novel(title char(50) primary key not null, \
                                    words text not null);')
    c.execute('create table user(username char(50) primary key not null, \
                                    password char(50) not null);')
    c.execute('create table upload(username char(50) not null, \
                                    title char(50) not null, \
                                    path char(50) not null, \
                                    primary key(username, title));')
    c.execute('create table last(username char(50) not null, \
                                    local char(1) not null, \
                                    title char(50) not null, \
                                    page char(50) not null, \
                                    primary key(username, local, title));')                               
    f = open("三体.txt", "r",encoding='utf8')
    title = '三体'
    s = f.read()
    c.execute("insert into novel(title,words) \
                        values('%s','%s')"%(title,s))
    conn.commit()
    conn.close()
    '''
    
    host = '127.0.0.1'
    port = 4396
    addr = (host,port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    print('server start!')
    
    index = 0
    # 循环等待接收客户端请求
    while True:
        # 阻塞等待请求
        conn_socket, addr = s.accept()
        index += 1
        # 一旦有请求了，把socket扔到我们指定处理函数handle_request处理，等待线程池分配线程处理
        thread_pool.add_job(handle_request, *(conn_socket, ))
        if index>500:
            break

    s.close()
   
   
   
   