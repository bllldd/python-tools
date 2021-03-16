import socket
import threading
tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
addr = input("请输入服务器ip:")
port = input("请输入服务器端口号：")
server_conn = (addr,int(port))
tcp_socket.connect(server_conn)
xinxi = ''

def jieshou():
    global tcp_socket
    global xinxi
    while xinxi != 'exit':
        try:
            xx = tcp_socket.recv(1024).decode('utf-8')
        except:
            print('连接断开')
            return
        if len(xx) > 0:
            print(xx)
def fasong():
    global tcp_socket
    global xinxi
    while xinxi !='exit':
        xinxi = input()
        if xinxi != 'exit':
            tcp_socket.send(xinxi.encode('utf-8'))
js = threading.Thread(target=jieshou)
fs = threading.Thread(target=fasong)
js.start()
fs.start()
threads = []
threads.append(js)
threads.append(fs)
fs.join()

# for t in threads:
    # t.join()
tcp_socket.close()
exit()
