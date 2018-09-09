#!/usr/bin/python3

import threading
import socket


if __name__ == '__main__':

    # Make connections based on '<ip>:<port>:<msg>'
    while True:
        cmd = input('>> ')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('127.0.0.1',3999))
                sock.sendall(bytes(cmd,'utf8'))
                print(str(sock.recv(1024),'utf8'))

        except Exception as e:
            print(e)
