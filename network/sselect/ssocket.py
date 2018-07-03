import socket

class Ssocket(socket):

    def send(self, data, flags=None):
        super().send(data.encode("utf-8"))