import threading
import hashlib
import time
import socket
import subprocess
import os
import struct

#Feel free to change username
USERNAME = "45b16b211b670549fa647a66a144d95abedb4cb878846f067e579bc2a7df9050871a4468bf6ec600d42f1766695b245608234c05bb1f75dfd22da06fd669bc9a"
#Feel free to change password
PASSWORD = "6f3e0cb2e31b74b374f568e00db71b72c92ca1929f0a84419e4cce889f9d0dbded5923c96038d11055f7b61fd66c170ba51e4a31b0d86717b408d5a76930bda4"

class Server_Control_Client:
    def start(self):
        self.username_logged = False
        self.password_logged = False
        self.start_server() # starting the server
        self.username = self.conn.recv(100).decode("utf-8")
        time.sleep(.1)
        self.password = self.conn.recv(1000).decode("utf-8")
        if self.validate_login(USERNAME, PASSWORD, self.username, self.password):
            self.conn.send("Logged in!".encode("utf-8"))
            self.run_commands()
        else:
            self.conn.send("Login failed!... :(".encode("utf-8"))
            self.sock.close()
            self.conn.close()
    def validate_login(self, username_set, password_set, username_input, password_input):
        self.username_hasher = hashlib.sha512()
        self.username_hasher.update(username_input.encode("utf-8"))
        self.username_hashed = self.username_hasher.hexdigest()
        self.password_hasher = hashlib.sha512()
        self.password_hasher.update(password_input.encode("utf-8"))
        self.password_hashed = self.password_hasher.hexdigest()
        if self.username_hashed == username_set:
            self.username_logged = True
        else:
            self.username_logged = False
        if self.password_hashed == password_set:
            self.password_logged = True
        else:
            self.password_logged = False
        if self.username_logged and self.password_logged == True:
            return True;
        else:
            return False;
    def start_server(self):
        self.host = ""
        self.port = 6000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print("Connection established! | Connected to: {}".format(self.addr))
    def run_commands(self):
        while True:
            data = self.conn.recv(1024)
            if data[:2].decode("utf-8") == "cd":
                directory = data[3:].decode("utf-8")
                try:
                    os.chdir(directory.strip())
                    self.conn.send("Directory change successful!".encode("utf-8"))
                except Exception as e:
                    output_str = "Could not change directory: %s\n" %str(e)
                    self.conn.send(output_str.encode("utf-8"))
            else:
                try:
                    cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    self.conn.send(output_bytes)
                except Exception as e:
                    self.conn.send("Error occured: {}".format(e).encode('utf-8'))
def main():
    while True:
        scc = Server_Control_Client()
        scc.start()

main()
