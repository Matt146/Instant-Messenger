##########################################
#Written By: Matt T
#Date of Last Edit: 1/3/2018
#Purpose: Instant Messenger Server
##########################################

import socket
import threading
import sys
import time

print("Startin server...")

USERNAME = str(input("Enter your username: "))
MAX_CLIENTS = int(input("How many clients: "))
BUFF_SIZE = 1024
HOST = ''
PORT = 9999

lock = threading.Lock()

class Server:
    def __init__(self):
        self.clients = [] #list of clients
        self.messages = [] #messages
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.sock.bind((self.host, self.port))
        threading.Thread(self.listener()).start()
    def conn_handler(self, conn):
        while True:
            self.data = conn.recv(BUFF_SIZE).decode("utf-8")
            if self.data:
                with lock:
                    self.msg = "[" + str(time.time()) + "]" + str(" -->") + str(self.data)
                    print(self.data)
                    self.messages.append(self.msg)
                    for client in self.clients:
                        try:
                            client.send(self.data.encode("utf-8")) #error occurs here, cannot send data to all clients
                        except:
                            pass
                    time.sleep(.01)
    def listener(self):
        for x in range(MAX_CLIENTS):
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            print("{} has connected!".format(addr))
            self.clients.append(conn)
            threading.Thread(target=self.conn_handler, args=(conn,)).start()

server = Server()

