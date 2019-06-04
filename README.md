# SimpleHttpServer
web服务器的简单实现。

### 多线程实现
 当服务器，有多个客户端连接，如果是单线程，那么新来的客户端就需要等待上一个客户端执行完操作，并且关闭了连接的套接字，才会执行新客户端连接，
 使用了多线程的方式，则为每一个连接进来的客户端新开一个线程， 这样，每一个新来的客户端都会马上新开一个线程进行处理。
 ```python
         while True:
             # 4.等待新客户端的链接
             client_socket,client_address = self.tcp_server_socket.accept()
 
             new_thread = threading.Thread(target=self.service_client,args=(client_socket,))
             # 5.为这个客户端服务
             new_thread.start()
```
### 多进程实现
 由于pyhon的GIL。所以多线程，在计算密集型的代码中，等同于单进程， 在IO密集型的代码中，虽然能更快，但是终究不是真正的传统多线程。所以利用多进程来实现。
    
```python
            while True:
                # 4.等待新客户端的链接
                client_socket,client_address = self.tcp_server_socket.accept()
    
                new_process = multiprocessing.Process(target=self.service_client,args=(client_socket,))
                # 5.为这个客户端服务
                new_process.start()
```
### gevent实现
安装
```python
    pip3 install gevent
```
当同时成千上万的客户端同时连接服务器，那么不论是多个线程，还是多个进程。服务器都无法同时承受。所以使用携程gevent

```python
import gevent
from gevent import monkey

monkey.patch_all()

...

        while True:
            # 4.等待新客户端的链接
            client_socket,client_address = self.tcp_server_socket.accept()
            # 5.为这个客户端服务
            gevent.spawn(self.service_client,client_socket)

            # new_thread.start()

```