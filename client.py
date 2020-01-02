#! /usr/bin/env python3
# coding utf-8 
import socket,sys

def register(sock,username,password,bufsize): #注册新用户信息
    #valid = 1
    data = ''
    data = data + '1\n'
    #username = input('username: ')
    #password = input('password: ')
    #repeat_password = input('repeat password: ')
    #if username=='' or password=='' or repeat_password=='' or password!=repeat_password:
    #    valid = 0
    data = data + 'username: ' + username + '\n'
    data = data + 'password: ' + password + '\n'
    #if valid==0:
    #    print("Register failed!")   
    #    return

    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Register successfully!")
        return 1
    else :
        print("Register failed!")  
        return 0
    
def login(sock,username,password,bufsize): #登录系统
    data = ''
    data = data + '2\n'
    #username = input('username: ')
    #password = input('password: ')
    data = data + 'username: ' + username + '\n'
    data = data + 'password: ' + password + '\n'

    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Login successfully!")
        return 1
    else :
        print("Login failed!")  
        return 0
    
def get_title(sock,title,bufsize):  #获取网络书库匹配标题的书目
    data = ''
    data = data + '3\n'
    #title = input('title: ')
    if title=='':
        title = '*'
    data = data + 'title: ' + title + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    ans = []
    if rec[1]=='1':
        print("Found!")    
        i = 2
        while i<=len(vec):
            print('%s'%vec[i])
            ans.append(vec[i])
            i = i+2
    else :
        print("Not found!") 
    return ans

def get_content(sock,title,page,bufsize): #获取对应网络书目对应页数的内容
    data = ''
    data = data + '4\n'
    #title = input('title: ')
    #page = input('page: ') 
    data = data + 'title: ' + title + '\n'
    data = data + 'page: ' + page + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Found!") 
        #print(rec[10:])
        return (vec[2],rec[20:])
        
    else :
        print("Not found!") 

def add_path(sock,username,title,path,bufsize): #增加本地书目路径
    data = ''
    data = data + '5\n'
    #username = input('username: ')
    #title = input('title: ')
    #path = input('path: ') 
    data = data + 'username: ' + username + '\n'
    data = data + 'title: ' + title + '\n'
    data = data + 'path: ' + path + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Success!")    
    else :
        print("Failed!") 
        
def get_path(sock,username,bufsize): #获取本地书库
    data = ''
    data = data + '6\n'
    #username = input('username: ')
    data = data + 'username: ' + username + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    title = []
    path = []
    if rec[1]=='1':
        print("Found!")    
        i = 2
        while i<=len(vec):
            print('%s'%vec[i])
            title.append(vec[i])
            i = i+2
            print('%s'%vec[i])
            path.append(vec[i])
            i = i+2
    else :
        print("Not found!") 
    return title,path

def add_record(sock,username,local,title,page,bufsize): #增加书签
    data = ''
    data = data + '7\n'
    #username = input('username: ')
    #local = input('local: ')
    #title = input('title: ')
    #page = input('page: ') 
    data = data + 'username: ' + username + '\n'
    data = data + 'local: ' + local + '\n'
    data = data + 'title: ' + title + '\n'
    data = data + 'page: ' + page + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Success!")    
    else :
        print("Failed!") 
'''          
def get_record(sock,username,bufsize): #获取书签
    data = ''
    data = data + '8\n'
    #username = input('username: ')
    data = data + 'username: ' + username + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Found!")    
        print('%s'%vec[2])
        print('%s'%vec[4])
        print('%s'%vec[6])
    else :
        print("Not found!")    
'''
def get_record(sock,username,local,title,bufsize): #获取书签
    data = ''
    data = data + '8\n'
    #username = input('username: ')
    #local = input('local: ')
    #title = input('title: ')
    data = data + 'username: ' + username + '\n'
    data = data + 'local: ' + local + '\n'
    data = data + 'title: ' + title + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Found!")    
        #print('%s'%vec[2])
        return vec[2]
    else :
        print("Not found!") 
        print("add record")
        add_record(sock,username,local,title,"1",bufsize)
        return "1"

def delete_local(sock,username,title,bufsize): #删除本地书目
    data = ''
    data = data + '9\n'
    #username = input('username: ')
    #title = input('title: ')
    data = data + 'username: ' + username + '\n'
    data = data + 'title: ' + title + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()
    
    if rec[1]=='1':
        print("Success!")
        return 1    
    else :
        print("Failed!")
        return 0 

def download(sock,title,bufsize):
    data = ''
    data = data + '0\n'
    #title = input('title: ')
    data = data + 'title: ' + title + '\n'
    
    sock.sendall(data.encode('utf-8'))  
    recv_data = sock.recv(bufsize)
    rec = recv_data.decode('utf-8')
    vec = rec.split()

    if rec[1]=='1':
        print("Found!") 
    else :
        print("Not found!") 
        return
    
    novel = ''
    maxpage = int(vec[2])
    print(maxpage)
    for i in range(1,maxpage+1):
        data = ''
        data = data + '4\n' 
        data = data + 'title: ' + title + '\n'
        data = data + 'page: ' + str(i) + '\n'
    
        sock.sendall(data.encode('utf-8')) 
        recv_data = sock.recv(bufsize)
        rec = recv_data.decode('utf-8')
        vec = rec.split()
    
        novel = novel + rec[20:]
        
    #print(novel)
    return novel

def connect():
    host = '127.0.0.1'
    port = 4396
    addr = (host,port)
    bufsize = 1024

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

'''
FIXME: 

host = '127.0.0.1'
port = 4396
addr = (host,port)
bufsize = 1024

sock = socket.socket()
try:
    sock.connect(addr)
    print('have connected with server')
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
            
except Exception:
    print('error')
    sock.close()
    sys.exit()
'''