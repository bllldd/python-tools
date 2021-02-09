import socket
import os
import time
socket_listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
potr = input("请输入监听端口号：")
local_addr = ("",int(potr))
socket_listen.bind(local_addr)
socket_listen.listen(5)
cilen_socket,cilen_addr = socket_listen.accept()
file_name = str(cilen_socket.recv(1024))
file_name = file_name.split("'")[1]
if os.path.exists(file_name):
    f = open(file_name,"rb")
    data_size = os.stat(file_name).st_size
    print("文件总大小：%d" % (data_size))
    cilen_socket.send(str(data_size).encode("utf-8"))
    size = 0
    while data_size != size:
        str = f.read(1024 * 100)
        size = size + len(str)
        print("当前传输大小：%d" % (size))
        cilen_socket.send(str)
    f.close()
else:
    cilen_socket.send("文件不存在".encode("utf-8"))
    print("文件不存在")
socket_listen.close()
cilen_socket.close()




