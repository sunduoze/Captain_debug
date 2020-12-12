#cilent
# 客户端编程模型如下：
# 1、创建一个socket套接字。
# 2、调用connect()函数将套接字连接到服务器。
# 3、调用send()函数向服务器发送数据，调用recv()函数接收来自服务器的数据。
# 4、与服务器的通信结束后，客户端程序可以调用close()函数关闭套接字。
import socket
import time

import tkinter
# from tkinter import *
# root = Tk()  # 创建窗口对象的背景色
# # 创建两个列表
# li = ['C', 'python', 'php', 'html', 'SQL', 'java']
# movie = ['CSS', 'jQuery', 'Bootstrap']
#
# listb = Listbox(root)  # 创建两个列表组件
# listb2 = Listbox(root)
# for item in li:  # 第一个小部件插入数据
#     listb.insert(0, item)
#
# for item in movie:  # 第二个小部件插入数据
#     listb2.insert(0, item)
#
# listb.pack()  # 将小部件放置到主窗口中
# # listb2.pack()
# root.mainloop()  # 进入消息循环

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(("127.0.0.1", 3288))
    sock.connect(("169.254.246.99", 8888))
    # print(sock.recv(1024).decode("utf-8"))

    # 持续与服务器交互：
    while True:
        # 获取用户输入:
        msg = input('Your input:')
        # msg = "ocv(0,0.0)\r\n"
        if not msg or msg == 'quit':
            break
        # 包装数据
        msg = msg + "\r\n"
        # 发送数据
        sock.send(msg.encode('GBK'))
        # print('input:', msg)
        # 输出服务器返回的消息
        time.sleep(0.001)
        # print('From server：', sock.recv(1024).decode('utf-8'))

    # 发送断开连接的指令
    sock.send(b'disconnect')
    # 套接字关闭
    sock.close()