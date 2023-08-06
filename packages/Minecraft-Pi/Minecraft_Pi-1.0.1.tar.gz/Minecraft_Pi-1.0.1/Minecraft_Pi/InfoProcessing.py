from ServerType import ServerType


def get_server_type(server_info):
    if server_info["type"] == "Bukkit":
        return ServerType.BUKKIT
    elif server_info["type"] == "Forge":
        return ServerType.FORGE
    elif server_info["type"] == "Fabric":
        return ServerType.FABRIC
