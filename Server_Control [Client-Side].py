import threading
import socket
import random
import hashlib
import time

BUFF_SIZE = 65535

lock = threading.Lock()

class ServerControl:
	def __init__(self):
		self.username = str(input("Enter username: "))
		self.password = str(input("Enter password: "))
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = str(input("Enter host ip: "))
		self.port = int(input("Enter port: "))
		self.sock.connect((self.host, self.port))
		self.sock.send(self.username.encode("utf-8"))
		time.sleep(1)
		self.sock.send(self.password.encode("utf-8"))
		self.send_commands()
	def send_commands(self):
		while True:
			self.data = self.sock.recv(BUFF_SIZE)
			print("Server -->$ " + self.data.decode("utf-8"))
			time.sleep(.01)
			self.command_to_send = str(input(">>> ")).encode("utf-8")
			self.sock.send(self.command_to_send)

servercontrol = ServerControl()
