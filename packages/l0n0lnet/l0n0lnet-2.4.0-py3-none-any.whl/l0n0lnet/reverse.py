from l0n0lnet.tcp import base_client, base_server
from l0n0lnet.tcp import session_read_size, close_tcp, client_read_size
from l0n0lnet.stream_parser import stream_parser
from l0n0lnet.utils import call_after
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

    def on_session_connected(self, session_id):
        # 创建会话数据
        self.session_data[session_id] = {"state": "get_pass_index"}
        # 读取2个字节的加密索引
        session_read_size(session_id, 2)

    def on_session_disconnected(self, session_id):
        # 获取会话数据
        session_data = self.session_data.get(session_id)
        if not session_data:
            return

        # 关闭会话对应的该服务器
        server = session_data.get("server")
        if server:
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
            # 进入数据传输状态
            session_data["state"] = "trans_data"
            session_read_size(session_id, 12)
        elif session_data["state"] == "trans_data":
            # 将数据传输给对外服务器
            session_data["server"].on_get_response(data)


class proxy_cmd(IntEnum):
    connect = 1
    close = 2
    data = 3


def pack_proxy_msg(session_id: int, cmd: int, data: bytes):
    return pack("!III", session_id, cmd, len(data)) + data


def unpack_proxy_header(data):
    return unpack("!III", data)


class reverse_server_server(base_server):
    def __init__(self, owner: reverse_server, session_id: int, port: int, parser: stream_parser):
        super().__init__(b'0.0.0.0', port)
        self.owner = owner
        self.session_id = session_id
        self.cur_session_id = 0
        self.cur_cmd = 0
        self.parser = parser
        # 进入获取包头的状态(12个字节,3个int32;[会话ID, 命令, 数据大小])
        self.state = "get_header"
        session_read_size(session_id, 12)

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

    def on_get_response(self, data):
        # 获取包头
        if self.state == "get_header":
            # 分析包头数据
            session_id, cmd, data_len = unpack_proxy_header(data)
            # 关闭连接命令
            if cmd == proxy_cmd.close:
                close_tcp(session_id)
            # 传输数据命令
            elif cmd == proxy_cmd.data:
                # 进入数据获取状态
                self.state = "get_data"
                self.cur_session_id = session_id
                session_read_size(self.session_id, data_len)
            # 未知命令,关闭连接
            else:
                close_tcp(session_id)
                close_tcp(self.session_id)
        # 获取到真实服务器的数据
        elif self.state == "get_data":
            # 解密数据
            self.parser.decrypt(data)
            # 将数据发送给当用户会话
            self.send_msg(self.cur_session_id, data)
            # 进入包头获取状态
            self.state = "get_header"
            session_read_size(self.session_id, 12)


class reverse_client(base_client):
    def __init__(self, ip: bytes, port: int, keys: list, remote_port: int, tip: bytes, tport: int):
        super().__init__(ip, port)
        self.parsers = []
        for key in keys:
            parser = stream_parser()
            parser.set_password(key)
            self.parsers.append(parser)
        self.parser_index = randint(0, len(self.parsers) - 1)
        self.parser = self.parsers[self.parser_index]
        self.remote_port = remote_port
        self.tip = tip
        self.tport = tport
        self.clients = {}
        self.state = "get_header"
        self.cur_session_id = 0
        self.cur_cmd = 0
        client_read_size(self.id, 12)

    def on_connected(self):
        # 发送密钥和端口
        self.send_msg(pack("!HH", self.parser_index, self.remote_port))

    def on_connect_failed(self):
        # 重新连接服务器
        pass

    def on_disconnected(self):
        # 重新连接服务器
        pass

    def on_read(self, data, size):
        if self.state == "get_header":
            self.cur_session_id, self.cur_cmd, data_len = unpack_proxy_header(
                data)
            # 关闭连接
            if self.cur_cmd == proxy_cmd.close:
                client: reverse_client_client = self.clients.get(
                    self.cur_session_id)
                if not client:
                    return
                client.close()
            # 读取数据
            elif self.cur_cmd == proxy_cmd.data:
                self.state = "get_data"
                client_read_size(self.id, data_len)
            # 连接新会话
            elif self.cur_cmd == proxy_cmd.connect:
                self.clients[self.cur_session_id] = reverse_client_client(
                    self, self.cur_session_id, self.tip, self.tport)
                return
            # 不识别的命令
            else:
                client = self.clients.get(self.cur_session_id)
                if not client:
                    return
                client.close()
        # 将数据传送给本地客户端
        elif self.state == "get_data":
            client: reverse_client_client = self.clients.get(
                self.cur_session_id)
            if not client:
                return
            # 解密数据
            self.parser.decrypt(data)
            client.send_msg(data)
            self.state = "get_header"
            client_read_size(self.id, 12)


class reverse_client_client(base_client):
    def __init__(self, owner: reverse_client, session_id: int, ip: bytes, port: int):
        super().__init__(ip, port)
        self.owner = owner
        self.session_id = session_id

    def send_msg_to_real_client(self, cmd: int, data: bytes):
        # 加密数据
        self.owner.parser.encrypt(data)
        # 打包包头
        data = pack_proxy_msg(self.session_id, cmd, data)
        # 发送到被代理的服务器
        self.owner.send_msg(data)

    def on_connect_failed(self):
        self.send_msg_to_real_client(proxy_cmd.close, b"")

    def on_disconnected(self):
        self.send_msg_to_real_client(proxy_cmd.close, b"")

    def on_read(self, data, size):
        self.send_msg_to_real_client(proxy_cmd.data, data)
