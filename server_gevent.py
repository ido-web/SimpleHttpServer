import socket
import re

import gevent
from gevent import monkey

monkey.patch_all()





class SimpleServer(object):

    def __init__(self,server_address):
        # 1.创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # 2. 绑定ip和port信息
        self.tcp_server_socket.bind(server_address)

        # 3.变为监听套接字
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
        self.tcp_server_socket.listen(128)

    def service_client(self,new_socket):
        '''
            处理客户端的请求
            使用http协议来与客户端交流
        '''
        # 1. 接受浏览器发送过来的请求，即http请求
        # GET / HTTP/1.1
        request  = new_socket.recv(1024).decode('utf-8')
        # 按行截取
        request_data = request.splitlines()
        # 提出出用户请求的路径
        file_name = ""
        if len(request_data) > 0:
            ret = re.match(r"[^/]+(/[^ ]*)",request_data[0])

            if ret:
                file_name = ret.group(1)
                if file_name == '/':
                    # 如果没有想写路径，则默认路径为'index.html'
                    file_name = '/index.html'

        # body
        try:
            # 以二进制只读的方式打开 python_doc 目录下file_name文件
            f = open('./python_doc' + file_name,'rb')
        except:
            header = "HTTP/1.1 404 NOT FUND\r\n"
            # 因为按照http协议，header和body中间有一个空行，这里创建一个空行
            space = '\r\n'
            # 拼接响应头
            response = header + space + "------file not found-----"
            # 将header发送给浏览器
            new_socket.send(response.encode('utf-8'))
        else:
            # 没有异常
            body = f.read()
            f.close()
            # 返回http格式的数据，给浏览器
            # 准备头部数据 浏览器解析换行为 \r\n
            header = "HTTP/1.1 200 OK\r\n"
            # 因为按照http协议，header和body中间有俩个空行，这里创建俩个空行
            space = '\r\n'
            # 拼接响应头
            response = header + space
            # 将header发送给浏览器
            new_socket.send(response.encode('utf-8'))
            # 将body发送给浏览器
            new_socket.send(body)
        new_socket.close()



    def run(self):

        while True:
            # 4.等待新客户端的链接
            client_socket,client_address = self.tcp_server_socket.accept()
            # 5.为这个客户端服务
            gevent.spawn(self.service_client,client_socket)

            # new_thread.start()


        # 关闭监听套接 字,短连接
        tcp_server_socket.close()



# 设定服务器端口号、
port = 6789
address = ''

server_address = (address,port)
server  = SimpleServer(server_address)
server.run()