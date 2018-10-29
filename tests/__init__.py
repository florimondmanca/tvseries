import socket


def nope(*args, **kwargs):
    raise Exception('A test tried to access the internet!')


socket.socket = nope
