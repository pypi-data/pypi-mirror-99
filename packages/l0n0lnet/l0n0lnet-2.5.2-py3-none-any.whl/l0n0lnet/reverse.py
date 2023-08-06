from l0n0lnet.tcp import base_client, base_server
from l0n0lnet.tcp import session_read_size, close_tcp, client_read_size
from l0n0lnet.stream_parser import stream_parser
from l0n0lnet.utils import call_after
from l0n0lnet.tcp import get_ip_port
from struct import pack, unpack
from copy import deepcopy
from random import randint
from enum import IntEnum


class reverse_server(base_server):
    def __init__(self, ip: bytes, port: int, keys: list):
        super().__init__(ip, port)
        self.session_data = {}
        self.parsers = []
        for key in keys:
            parser = stream_parser()
            parser.set_password(key)
            self.parsers.append(parser)

        call_after(1000, self.on_heart, 1000)

    def on_heart(self):
        for session_id, session_data in self.session_data.items():
            heart = session_data["heart"]
            heart += 1
            if heart >= 10:
                close_tcp(session_id)
            session_data["heart"] = heart

    def on_session_connected(self, session_id):
        # 创建会话数据
        self.session_data[session_id] = {"state": "get_pass_index", "heart": 0}
        # 读取2个字节的加密索引
        session_read_size(session_id, 2)
        # 打印数据
        print(get_ip_port(session_id), "connected to server")

    def on_session_disconnected(self, session_id):
        print(get_ip_port(session_id), "disconnected")
        # 获取会话数据
        session_data = self.session_data.get(session_id)
        if not session_data:
            return

        # 关闭会话对应的该服务器
        server = session_data.get("server")
        if server:
            print(get_ip_port(session_id), "closing opened server.")
            server.close()

        # 删除会话数据
        del self.session_data[session_id]

    def on_session_read(self, session_id, data, size):
        # 获取会话数据
        session_data = self.session_data.get(session_id)
        if not session_data:
            close_tcp(session_id)
            return
        # 获取加密索引
        if session_data["state"] == "get_pass_index":
            index = unpack("!H", data)[0]
            # 校验索引是否超出范围
            if index >= len(self.parsers):
                close_tcp(session_id)
                return
            # 为会话匹配加密parser
            session_data["parser"] = self.parsers[index]
            # 进入获取端口状态
            session_data["state"] = "get_port"
        # 获取要代理的端口，创建服务器
        elif session_data["state"] == "get_port":
            # 获取端口
            port = unpack("!H", data)[0]
            # 创建对外服务器
            session_data["server"] = reverse_server_server(
                self, session_id, port, session_data["parser"])
            # 进入包头读取
            session_data["state"] = "get_header"
            session_read_size(session_id, 12)
        elif session_data["state"] == "get_header":
            # 分析包头数据
            server_session_id, cmd, data_len = unpack_proxy_header(data)
            if cmd == proxy_cmd.data:
                # 缓存命令数据
                session_data["server_session_id"] = server_session_id
                session_data["cmd"] = cmd

                # 进入数据获取状态
                session_data["state"] = "get_data"
                session_read_size(session_id, data_len)
                return
            
            # 心跳包
            elif cmd == proxy_cmd.heart:
                session_data["heart"] = 0
                return

            # 将数据传输给对外服务器
            session_data["server"].on_get_response(server_session_id, cmd)
        elif session_data["state"] == "get_data":
            server_session_id = session_data["server_session_id"]
            cmd = session_data["cmd"]

            # 将数据传输给对外服务器
            session_data["server"].on_get_response(
                server_session_id, cmd, data)

            # 进入包头读取
            session_data["state"] = "get_header"
            session_read_size(session_id, 12)


class proxy_cmd(IntEnum):
    connect = 1
    close = 2
    data = 3
    heart = 4


def pack_proxy_msg(session_id: int, cmd: int, data: bytes = None):
    if data is not None:
        return pack("!III", session_id, cmd, len(data)) + data
    return pack("!III", session_id, cmd, 0)


def unpack_proxy_header(data):
    return unpack("!III", data)


class reverse_server_server(base_server):
    def __init__(self, owner: reverse_server, session_id: int, port: int, parser: stream_parser):
        super().__init__(b'0.0.0.0', port)
        self.owner = owner
        self.session_id = session_id
        self.parser = parser

    def send_msg_to_real_server(self, session_id: int, cmd: int, data: bytes):
        # 加密数据
        self.parser.encrypt(data)
        # 打包包头
        data = pack_proxy_msg(session_id, cmd, data)
        # 发送到被代理的服务器
        self.owner.send_msg(self.session_id, data)

    def on_session_connected(self, session_id):
        # 向真实服务器开一个会话
        self.send_msg_to_real_server(session_id, proxy_cmd.connect, b"")

    def on_session_disconnected(self, session_id):
        # 向真实服务器关闭一个会话
        self.send_msg_to_real_server(session_id, proxy_cmd.close, b"")

    def on_session_read(self, session_id, data, size):
        # 将数据传送给真实服务器
        self.send_msg_to_real_server(session_id, proxy_cmd.data, data)

    def on_get_response(self, session_id, cmd, data=None):
        # 关闭连接命令
        if cmd == proxy_cmd.close:
            close_tcp(session_id)
        # 传输数据命令
        elif cmd == proxy_cmd.data:
            # 解密数据
            self.parser.decrypt(data)
            # 将数据发送给当用户会话
            self.send_msg(session_id, data)


class reverse_client(base_client):
    def __init__(self, ip: bytes, port: int, keys: list, remote_port: int, tip: bytes, tport: int):
        self.server_ip = ip
        self.server_port = port
        self.remote_port = remote_port
        self.tip = tip
        self.tport = tport
        self.parsers = []

        for key in keys:
            parser = stream_parser()
            parser.set_password(key)
            self.parsers.append(parser)

        # 连接目标
        self.reconnect()

        # 开启timer
        call_after(1000, self.update, 1000)

    def update(self):
        if not self.connected:
            return

        # 发送心跳
        self.send_message_to_remote_server(0, proxy_cmd.heart)

    def reconnect(self):
        # 重置连接状态
        self.connected = False

        # 关闭已有的连接
        if hasattr(self, "clients"):
            clients: dict = getattr(self, "clients")
            if clients:
                for client in clients.values():
                    client.close()

        # 连接服务器
        super().__init__(self.server_ip, self.server_port)

        # 随机密钥索引
        self.parser_index = randint(0, len(self.parsers) - 1)

        # 创建混淆器
        self.parser = self.parsers[self.parser_index]

        # 清空缓存
        self.clients = {}
        self.remote_session_id = 0
        self.remote_cmd = 0

        # 读取数据
        self.state = "get_header"
        client_read_size(self.id, 12)

    def on_connected(self):
        # 设置连接状态
        self.connected = True

        # 发送密钥和端口
        self.send_msg(pack("!HH", self.parser_index, self.remote_port))

    def on_connect_failed(self):
        # 重新连接服务器
        call_after(1000, self.reconnect)
        print("Connect to Server Failed! Reconnect in 1 second.")

    def on_disconnected(self):
        # 设置连接状态
        self.connected = False

        # 重新连接服务器
        call_after(1000, self.reconnect)
        print("DisConnect from server! Reconnect in 1 second.")

    def on_read(self, data, size):
        # 读取包头
        if self.state == "get_header":
            # 解析包头，获取命令
            self.remote_session_id, self.remote_cmd, data_len = unpack_proxy_header(
                data)

            # 连接新会话
            if self.remote_cmd == proxy_cmd.connect:
                self.clients[self.remote_session_id] = reverse_client_client(
                    self, self.remote_session_id, self.tip, self.tport)
                print("Remote session Connected.", self.remote_session_id)
                return

            # 关闭连接
            elif self.remote_cmd == proxy_cmd.close:
                client: reverse_client_client = self.clients.get(
                    self.remote_session_id)
                if not client:
                    return
                client.close()
                print("Remote session closed.", self.remote_session_id)

            # 读取数据
            elif self.remote_cmd == proxy_cmd.data:
                self.state = "get_data"
                client_read_size(self.id, data_len)

            # 不识别的命令
            else:
                client = self.clients.get(self.remote_session_id)
                if not client:
                    return
                client.close()
                print("Invalid cmd. Closing client", self.remote_session_id)

        # 将数据传送给本地客户端
        elif self.state == "get_data":
            client: reverse_client_client = self.clients.get(
                self.remote_session_id)

            # 没找到对应的连接，通知远方服务器关闭会话
            if not client:
                self.send_message_to_remote_server(
                    self.remote_session_id, proxy_cmd.close)
                return

            # 解密数据
            self.parser.decrypt(data)

            # 将数据发送给被代理的服务器
            client.on_get_remote_data(data)

            # 继续读取包头
            self.state = "get_header"
            client_read_size(self.id, 12)

    def send_message_to_remote_server(self, remote_session_id, cmd, data=None):
        # 加密数据
        if data:
            self.parser.encrypt(data)

        # 打包包头
        msg_data = pack_proxy_msg(remote_session_id, cmd, data)

        # 发送到被代理的服务器
        self.send_msg(msg_data)


class reverse_client_client(base_client):
    def __init__(self, owner: reverse_client, session_id: int, ip: bytes, port: int):
        super().__init__(ip, port)
        self.owner = owner
        self.session_id = session_id
        self.cache = b""
        self.connected = False
        self.ip = ip
        self.port = port

    def on_connected(self):
        print(f"Connected to local {self.ip}:{self.port}")

        # 设置连接成功
        self.connected = True

        # 发送缓存数据
        self.send_msg(self.cache)

        # 清空缓存
        self.cache = b""

    def send_msg_to_real_client(self, cmd: int, data: bytes = None):
        self.owner.send_message_to_remote_server(self.session_id, cmd, data)

    def on_connect_failed(self):
        print(f"Failed connect to local {self.ip}:{self.port}")
        # 告知远端服务器关闭连接
        self.send_msg_to_real_client(proxy_cmd.close)

    def on_disconnected(self):
        print(f"Disconnected from local {self.ip}:{self.port}")

        # 设置连接状态
        self.connected = False

        # 告知远端服务器关闭连接
        self.send_msg_to_real_client(proxy_cmd.close)

    def on_read(self, data, size):
        self.send_msg_to_real_client(proxy_cmd.data, data)

    def on_get_remote_data(self, data):
        # 如果还没有连接成功，缓存数据
        if not self.connected:
            self.cache += data
            return

        # 发送数据
        self.send_msg(data)
