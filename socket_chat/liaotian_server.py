import socket
import threading
import os
import datetime
tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = input("请输入要开启的端口号：")
tcp_socket.bind(('',int(port)))
tcp_socket.listen(5)
sockets = {}
filename = 'liaotian_log'
if not (os.path.exists(filename)):
    os.mkdir(filename)
logname = datetime.datetime.now().date()
fp = open(filename+'/'+str(logname)+'.txt','a+',encoding='utf-8')
def lianijie(client_socket,ip):
    global sockets
    print(ip+"上线")
    while True:
        try:
            xinxi = client_socket.recv(1024)
        except:
            print(ip+"连接断开")
            lock.acquire()
            del sockets[ip]
            lock.release()
            return
        if len(xinxi) <= 0:
            return
        xinxi = xinxi.decode("utf-8")
        for sock in sockets:
            if sock != ip:
                xinxi = ip+':'+xinxi
                try:
                    sockets[sock].send(xinxi.encode('utf-8'))
                except:
                    print(ip + "连接断开")
                    lock.acquire()
                    del sockets[ip]
                    lock.release()
                    return
                fp.write(xinxi+'\n')
lock = threading.Lock()
while True:
    client_socket,client_addr = tcp_socket.accept()
    ip = str(client_addr[0])
    lt1 = threading.Thread(target=lianijie,args=(client_socket,ip))
    lock.acquire()
    sockets[ip] = client_socket
    lock.release()
    lt1.start()

socket.close()
