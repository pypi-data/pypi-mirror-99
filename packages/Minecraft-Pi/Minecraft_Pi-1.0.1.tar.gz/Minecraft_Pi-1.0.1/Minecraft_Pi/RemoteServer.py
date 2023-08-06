import json
import socket

from Exception import NotFoundServerException


def _socket_run(info_json):
    try:
        server = socket.socket()
        server.connect((RemoteServer.ip, RemoteServer.port))
        info_json["ip"] = socket.gethostname()
        server.send(bytes(json.dumps(info_json), encoding="utf-8"))
        server.shutdown(1)
        data = server.recv(1024)
        server.close()
        return json.loads(str(data, encoding="utf-8"))
    except ConnectionRefusedError:
        raise NotFoundServerException("未找到服务器（很可能服务器未开启或者服务器不存在）")


class RemoteServer:
    port = None
    ip = None

    @staticmethod
    def set_address(ip, port):
        RemoteServer.port = port
        RemoteServer.ip = ip

    @staticmethod
    def get_info():
        test_json = {"test": True}
        return _socket_run(test_json)

    @staticmethod
    def get_player(player_name):
        player_json = {"player": True, "name": player_name}
        remote_player = _socket_run(player_json)
        if remote_player["playerIsNull"]:
            return None
        else:
            return remote_player
