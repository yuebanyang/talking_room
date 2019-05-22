'''
客户端
'''
from socket import *
import os,sys

#服务器地址
ADDR = ('172.40.91.188',8888)

#发送消息
def send_msg(s,name):
    while True:
        try:
            text = input('发言：\n')
        except KeyboardInterrupt:
            text = 'quit' #如此赋值，进入下面if的程序
        #退出聊天室
        if text == 'quit':
            msg = 'Q ' + name  #规范格式
            s.sendto(msg.encode(),ADDR)
            sys.exit('退出聊天室')

        msg = 'C %s %s' % (name,text) #规范格式
        s.sendto(msg.encode(),ADDR)

#接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        #服务端发送EXIT表示让客户端退出
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + '\n发言：',end = '')

#创建网络链接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input ('请输入姓名：')
        msg  = 'L ' + name  #规定发送协议
        s.sendto(msg.encode(),ADDR)
        #等待回应
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('已进入聊天室')
            break
        else:
            print(data.decode()) #登录失败原因

    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('error')
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)




if __name__ == "__main__":
    main()











































