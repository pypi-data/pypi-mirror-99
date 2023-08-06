### 一、介绍
基于libuv的c++网络库

### 二、支持平台

#### 1.windows (x86 x64 amd64)
#### 2.linux

### 三、安装
```bash
# 1.安装基础包
pip install l0n0lnet

# tip: Windows不需以下步骤。但windows仅支持x86 x64 amd64架构的cpu

# 2.安装build tools 和 git(ubuntu2004)
apt install build-essential git

# 2.安装build tools 和 git(centos)
yum -y groupinstall "Development Tools" git

# 3.linux第一次运行会自动下载c++源代码并编译，需要手动import一次库
Python 3.8.5 (default, Jul 28 2020, 12:59:40)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import l0n0lnet
-- The C compiler identification is GNU 9.3.0
-- The CXX compiler identification is GNU 9.3.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Performing Test UV_LINT_W4
-- Performing Test UV_LINT_W4 - Failed
-- Performing Test UV_LINT_NO_UNUSED_PARAMETER_MSVC
-- Performing Test UV_LINT_NO_UNUSED_PARAMETER_MSVC - Failed
-- Performing Test UV_LINT_NO_CONDITIONAL_CONSTANT_MSVC
-- Performing Test UV_LINT_NO_CONDITIONAL_CONSTANT_MSVC - Failed
-- Performing Test UV_LINT_NO_NONSTANDARD_MSVC
-- Performing Test UV_LINT_NO_NONSTANDARD_MSVC - Failed
-- Performing Test UV_LINT_NO_NONSTANDARD_EMPTY_TU_MSVC
-- Performing Test UV_LINT_NO_NONSTANDARD_EMPTY_TU_MSVC - Failed
-- Performing Test UV_LINT_NO_NONSTANDARD_FILE_SCOPE_MSVC
-- Performing Test UV_LINT_NO_NONSTANDARD_FILE_SCOPE_MSVC - Failed
-- Performing Test UV_LINT_NO_NONSTANDARD_NONSTATIC_DLIMPORT_MSVC
-- Performing Test UV_LINT_NO_NONSTANDARD_NONSTATIC_DLIMPORT_MSVC - Failed
-- Performing Test UV_LINT_NO_HIDES_LOCAL
-- Performing Test UV_LINT_NO_HIDES_LOCAL - Failed
-- Performing Test UV_LINT_NO_HIDES_PARAM
-- Performing Test UV_LINT_NO_HIDES_PARAM - Failed
-- Performing Test UV_LINT_NO_HIDES_GLOBAL
-- Performing Test UV_LINT_NO_HIDES_GLOBAL - Failed
-- Performing Test UV_LINT_NO_CONDITIONAL_ASSIGNMENT_MSVC
-- Performing Test UV_LINT_NO_CONDITIONAL_ASSIGNMENT_MSVC - Failed
-- Performing Test UV_LINT_NO_UNSAFE_MSVC
-- Performing Test UV_LINT_NO_UNSAFE_MSVC - Failed
-- Performing Test UV_LINT_WALL
-- Performing Test UV_LINT_WALL - Success
-- Performing Test UV_LINT_NO_UNUSED_PARAMETER
-- Performing Test UV_LINT_NO_UNUSED_PARAMETER - Success
-- Performing Test UV_LINT_STRICT_PROTOTYPES
-- Performing Test UV_LINT_STRICT_PROTOTYPES - Success
-- Performing Test UV_LINT_EXTRA
-- Performing Test UV_LINT_EXTRA - Success
-- Performing Test UV_LINT_UTF8_MSVC
-- Performing Test UV_LINT_UTF8_MSVC - Failed
-- summary of build options:
    Install prefix:  /usr/local
    Target system:   Linux
    Compiler:
      C compiler:    /usr/bin/cc
      CFLAGS:

-- Configuring done
-- Generating done
-- Build files have been written to: /tmp/l0n0lnet/cppsrc/build
make: Entering directory '/tmp/l0n0lnet/cppsrc/build'
make[1]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
Scanning dependencies of target uv_a
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
[  1%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/fs-poll.c.o
[  2%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/idna.c.o
[  3%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/inet.c.o
[  5%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/random.c.o
[  6%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/strscpy.c.o
[  7%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/threadpool.c.o
[  8%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/timer.c.o
[ 10%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/uv-common.c.o
[ 11%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/uv-data-getter-setters.c.o
[ 12%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/version.c.o
[ 13%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/async.c.o
[ 15%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/core.c.o
[ 16%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/dl.c.o
[ 17%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/fs.c.o
[ 18%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/getaddrinfo.c.o
[ 20%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/getnameinfo.c.o
[ 21%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/loop-watcher.c.o
[ 22%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/loop.c.o
[ 24%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/pipe.c.o
[ 25%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/poll.c.o
[ 26%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/process.c.o
[ 27%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/random-devurandom.c.o
[ 29%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/signal.c.o
[ 30%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/stream.c.o
[ 31%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/tcp.c.o
[ 32%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/thread.c.o
[ 34%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/tty.c.o
[ 35%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/udp.c.o
[ 36%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/proctitle.c.o
[ 37%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/linux-core.c.o
[ 39%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/linux-inotify.c.o
[ 40%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/linux-syscalls.c.o
[ 41%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/procfs-exepath.c.o
[ 43%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/random-getrandom.c.o
[ 44%] Building C object dep/libuv/CMakeFiles/uv_a.dir/src/unix/random-sysctl-linux.c.o
[ 45%] Linking C static library ../../../lib/libuv_a.a
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
[ 45%] Built target uv_a
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
Scanning dependencies of target se
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
[ 46%] Building CXX object CMakeFiles/se.dir/src/se_allocator.cpp.o
[ 48%] Building CXX object CMakeFiles/se.dir/src/se_buffer.cpp.o
[ 49%] Building CXX object CMakeFiles/se.dir/src/se_export_to_python.cpp.o
[ 50%] Building CXX object CMakeFiles/se.dir/src/se_tcp.cpp.o
[ 51%] Building CXX object CMakeFiles/se.dir/src/se_udp.cpp.o
[ 53%] Building CXX object CMakeFiles/se.dir/src/se_utils.cpp.o
[ 54%] Linking CXX shared library ../lib/libse.so
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
[ 54%] Built target se
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
Scanning dependencies of target uv
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
make[2]: Entering directory '/tmp/l0n0lnet/cppsrc/build'
[ 55%] Building C object dep/libuv/CMakeFiles/uv.dir/src/fs-poll.c.o
[ 56%] Building C object dep/libuv/CMakeFiles/uv.dir/src/idna.c.o
[ 58%] Building C object dep/libuv/CMakeFiles/uv.dir/src/inet.c.o
[ 59%] Building C object dep/libuv/CMakeFiles/uv.dir/src/random.c.o
[ 60%] Building C object dep/libuv/CMakeFiles/uv.dir/src/strscpy.c.o
[ 62%] Building C object dep/libuv/CMakeFiles/uv.dir/src/threadpool.c.o
[ 63%] Building C object dep/libuv/CMakeFiles/uv.dir/src/timer.c.o
[ 64%] Building C object dep/libuv/CMakeFiles/uv.dir/src/uv-common.c.o
[ 65%] Building C object dep/libuv/CMakeFiles/uv.dir/src/uv-data-getter-setters.c.o
[ 67%] Building C object dep/libuv/CMakeFiles/uv.dir/src/version.c.o
[ 68%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/async.c.o
[ 69%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/core.c.o
[ 70%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/dl.c.o
[ 72%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/fs.c.o
[ 73%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/getaddrinfo.c.o
[ 74%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/getnameinfo.c.o
[ 75%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/loop-watcher.c.o
[ 77%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/loop.c.o
[ 78%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/pipe.c.o
[ 79%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/poll.c.o
[ 81%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/process.c.o
[ 82%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/random-devurandom.c.o
[ 83%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/signal.c.o
[ 84%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/stream.c.o
[ 86%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/tcp.c.o
[ 87%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/thread.c.o
[ 88%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/tty.c.o
[ 89%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/udp.c.o
[ 91%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/proctitle.c.o
[ 92%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/linux-core.c.o
[ 93%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/linux-inotify.c.o
[ 94%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/linux-syscalls.c.o
[ 96%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/procfs-exepath.c.o
[ 97%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/random-getrandom.c.o
[ 98%] Building C object dep/libuv/CMakeFiles/uv.dir/src/unix/random-sysctl-linux.c.o
[100%] Linking C shared library ../../../lib/libuv.so
make[2]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
[100%] Built target uv
make[1]: Leaving directory '/tmp/l0n0lnet/cppsrc/build'
make: Leaving directory '/tmp/l0n0lnet/cppsrc/build'

# 没有错误表示编译成功
```

### 四、使用方法
#### 1、实现一个tcp echo server (方法一)
```python
from l0n0lnet.tcp *
from l0n0lnet import *

@on_session_connected("test")
def on_connect(session_id):
    print("链接", session_id)

@on_session_read("test")
def on_read(session_id, data, size):
    print(session_id, data, size)
    # close_tcp_by_name("test")
    send_message(session_id, data)
    call_after(1000, lambda: close_tcp(session_id))

@on_session_disconnected("test")
def on_close(session_id):
    print("断开", session_id)

create_tcp_server("test", b'127.0.0.1', 1234)

run()
```

#### 2、实现一个tcp echo server (方法二)
```python
from l0n0lnet.tcp import base_server
from l0n0lnet import run
class test_server(base_server):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def on_session_connected(self, session_id):
        print("链接", session_id)

    def on_session_disconnected(self, session_id):
        print("断开", session_id)

    def on_session_read(self, session_id, data, size):
        self.send_msg(session_id, data)
        print(session_id, data, size)

test_server(b'127.0.0.1', 1234)
run()
```
#### 3、实现一个tcp echo client (方法一)
```python
from l0n0lnet.tcp import *
from l0n0lnet import run

def on_connected( id):
    print("连接成功", id)
    self.send_msg(b'hello!')
    self.close()

def on_connect_failed( id):
    print("连接失败", id)

def on_disconnected( id):
    print("断开连接", id)

def on_read(id, data, size):
    print(id, data, size)

connect_to("test", b'127.0.0.1', 1234)
set_cb("test", "on_connected", on_connected)
set_cb("test", "on_connect_failed", on_connect_failed)
set_cb("test", "on_disconnected", on_disconnected)
set_cb("test", "on_read", on_read)
run()
```

#### 4、实现一个tcp echo client (方法二)
```python
from l0n0lnet import run
from l0n0lnet.tcp import base_client

class testclient(base_client):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def on_connected(self, id):
        print("连接成功", id)
        self.send_msg(b'hello!')
        self.close()

    def on_connect_failed(self, id):
        print("连接失败", id)

    def on_disconnected(self, id):
        print("断开连接", id)

    def on_read(self, id, data, size):
        print(id, data, size)

testclient(b'127.0.0.1', 1234)
run()
```

#### 5、实现一个udp echo server  (方法一)
```python
from l0n0lnet import run
from l0n0lnet.udp import *
class udp_echo_server(base_udp):
    def __init__(self):
        super().__init__(b'127.0.0.1', 20001)

    def on_read(self, tip: bytes, tport: int, data: bytes, size: int):
        print(tip, tport, data, size)
        self.send_to(tip, tport, data)
udp_echo_server()
run()
```

#### 6、实现一个udp echo server  (方法二)
```python
from l0n0lnet import run
from l0n0lnet.udp import *
@as_udp("test", b'127.0.0.1', 30003)
def test1_on_read(tip, tport, data, size):
    send_udp_msg("test", tip, tport, data)
run()
```

#### 7、实现一个udp echo client  (方法一)
```python
from l0n0lnet import run
from l0n0lnet.udp import *
class udp_echo_client(base_udp):
    def __init__(self):
        super().__init__(b'127.0.0.1', 20002)
        self.send_to(b'127.0.0.1', 20001, b'123123123')

    def on_read(self, tip: bytes, tport: int, data: bytes, size: int):
        print(tip, tport, data, size)
udp_echo_client()
run()
```

#### 8、实现一个udp echo client  (方法二)
```python
from l0n0lnet import run
from l0n0lnet.udp import *
def on_read(tip, tport, data, size):
    print(data)
create_udp("echo_client", b'127.0.0.1', 30002)
set_udp_on_read("echo_client", on_read)
send_udp_msg("echo_client", b'127.0.0.1', 30003, b'123')
run()
```

#### 9、socks5代理服务器
```python
from l0n0lnet.socks import socks5_server
from l0n0lnet import run, add_quit_func

server = socks5_server(b"127.0.0.1", 1080)

def on_close():
    socks5.close()
    print("closing")
    
add_quit_func(on_close)

run()

```

#### 10、tcp代理
通过9999端口访问9997端口开放的socks5服务器
```python
from l0n0lnet.socks import socks5_server
from l0n0lnet.transform import trans_server
from l0n0lnet import run, add_quit_func
from l0n0lnet.stream_parser import stream_parser
keys = [
    stream_parser.gen_password(),
    stream_parser.gen_password()
]
socks5 = socks5_server(b'127.0.0.1', 9997)
ts = trans_server(b'127.0.0.1', 9998, b'127.0.0.1', 9997, keys, 'server')
tc = trans_server(b'127.0.0.1', 9999, b'127.0.0.1', 9998, keys, 'client')
def on_close():
    ts.close()
    tc.close()
    socks5.close()
    print("closing")

add_quit_func(on_close)
run()
```


#### 11、内网穿透
通过访问公网所在的9999端口，就可以访问内网的80端口
```python
from l0n0lnet.reverse import reverse_server, reverse_client
from l0n0lnet.stream_parser import stream_parser
from l0n0lnet import run, add_quit_func

keys = [
    stream_parser.gen_password(),
    stream_parser.gen_password()
]


ss = reverse_server(b'0.0.0.0', 12345, keys)

sc = reverse_client(b"0.0.0.0", 12345, keys, 9999, b'127.0.0.1', 80)

def on_close():
    ss.close()
    sc.close()
    print("quit")


add_quit_func(on_close)

run()
```

### 五、命令介绍
#### 1、创建混淆密钥
```
usage: l0n0lgenpass [-h] filename count

创建混淆文件

positional arguments:
  filename    文件名
  count       文件行数

optional arguments:
  -h, --help  show this help message and exit
```

实例：创建了一个拥有100行的密钥文件 </br>
__l0n0lgenpass pass.txt 100__

#### 2、socks5服务器
```
usage: l0n0lsocks5 [-h] listenip listenport

创建socks5服务器

positional arguments:
  listenip    监听IP
  listenport  监听端口

optional arguments:
  -h, --help  show this help message and exit
```
实例：创建socks5服务器，监听80端口 </br>
__l0n0lsocks5 127.0.0.1 1080__

#### 3、带数据混淆的分离socks5服务器
##### 1 ) 服务器
```
usage: l0n0ltsocks5server [-h] listenip listenport sockport passfile

创建数据混淆socks5服务器

positional arguments:
  listenip    本地监听IP
  listenport  监听端口
  sockport    sock5s服务器端口
  passfile    密码文件

optional arguments:
  -h, --help  show this help message and exit
```
##### 2 ) 客户端
```
usage: l0n0ltsocks5client [-h] listenip listenport ip port passfile

链接混淆服务器

positional arguments:
  listenip    本地监听IP
  listenport  本地监听端口
  ip          服务器IP
  port        服务器端口
  passfile    密码文件

optional arguments:
  -h, --help  show this help message and exit
```

实例：通过访问本地1080端口访问远方服务器的socks5服务器</br>
假定服务器IP地址为192.168.1.2</br>
在远方服务器执行：__l0n0ltsocks5server 0.0.0.0 8002 8080 pass.txt__ </br>
在本地电脑执行：__l0n0ltsocks5client 0.0.0.0 1080 192.168.1.2 8002 pass.txt__

#### 4、tcp代理
```
usage: l0n0ltcpproxy [-h] listenip listenport targetip targetport passfile role

创建正向tcp混淆代理服务器

positional arguments:
  listenip    监听IP
  listenport  监听端口
  targetip    目标IP
  targetport  目标端口
  passfile    密码文件
  role        (client | server)作为服务器还是客户端

optional arguments:
  -h, --help  show this help message and exit
```

实例：通过访问本地1080端口访问远方服务器的8080端口服务</br>
假定服务器IP地址为192.168.1.2</br>
在远方服务器执行：__l0n0ltcpproxy 0.0.0.0 8002 127.0.0.1 8080 pass.txt__ </br>
在本地电脑执行：__l0n0ltsocks5client 0.0.0.0 1080 192.168.1.2 8002 pass.txt__


#### 5、内网穿透
##### 1 ) 服务器
```
usage: l0n0lrserver [-h] listenip listenport passfile

创建反向代理服务器

positional arguments:
  listenip    监听ip
  listenport  监听端口
  passfile    混淆文件

optional arguments:
  -h, --help  show this help message and exit
```
##### 2 ) 客户端
```
usage: l0n0lrclient [-h] serverip serverport remoteport localip localport passfile

创建反向代理客户端

positional arguments:
  serverip    服务器IP
  serverport  服务器端口
  remoteport  服务器代理端口
  localip     本地服务器IP
  localport   本地服务端口
  passfile    本地服务端口

optional arguments:
  -h, --help  show this help message and exit
```
实例：通过访问服务器1080端口访问本地的80端口服务</br>
假定服务器IP地址为192.168.1.2</br>
在远方服务器执行：__l0n0lrserver 0.0.0.0 8002 pass.txt__ </br>
在本地电脑执行：__l0n0lrclient 192.168.1.2 8002 1080 127.0.0.1 80 pass.txt__
