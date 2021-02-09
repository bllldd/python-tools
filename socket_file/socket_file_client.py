import socket
import threading
import sys
print("要下载的文件请不要带有单引号！")
tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
addr = input("请输入服务的IP地址：")
potr = int(input("请输入端口号："))
server_addr = (addr,potr)
tcp_socket.connect(server_addr)
file_name = input("请输入要下载的文件名:")
tcp_socket.send(file_name.encode("utf-8"))
data_size = 0
data_list = []
is_xiewan = True
zong_size = tcp_socket.recv(1024 * 3).decode("utf-8")
print("文件总大小： %s" %(zong_size))
if zong_size == "文件不存在":
    tcp_socket.close()
    sys.exit(0)
new_name = input("文件名保存为：")
f = open(new_name,"ab")
def jie_shou():
    global data_list
    global data_size
    global is_xiewan
    global zong_size
    while data_size < int(zong_size):
        lock.acquire()
        data = tcp_socket.recv(1024 * 100)
        data_list.append(data)
        lock.release()
        data_size = data_size + len(data)
        print("已经传输大小：%d" % (data_size))
    is_xiewan = False
def xie_ru():
    global data_list
    is_xiewan_2 = True
    data_len = 0
    while is_xiewan_2:
        lock.acquire()
        data_list2 = data_list[:]
        data_list.clear()
        lock.release()
        if data_list2:
            for d in data_list2:
                data_len = data_len + len(d)
                print("当前写入大小：%d" % (data_len))
                f.write(d)
            data_list2.clear()
        if not is_xiewan:
            is_xiewan_2 = False
    lock.acquire()
    data_list2 = data_list[:]
    data_list.clear()
    lock.release()
    if data_list2:
        for d in data_list2:
            data_len = data_len + len(d)
            print("当前写入大小：%d" % (data_len))
            f.write(d)
        data_list2.clear()


class mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        xie_ru()
thread1 = mythread()
lock = threading.Lock()
thread1.start()
jie_shou()
thread1.join()
f.close()
print("文件传输成功！")

