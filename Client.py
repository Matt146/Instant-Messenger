from tkinter import *
import subprocess
import threading
import socket
import time
import os

BUFF_SIZE = 1024
PORT = 9999

tk = Tk()
canvas = Canvas(tk, height=500, width=400)
canvas.pack()
tk.resizable(False, False)
tk.title("Instant Messenger Client Version 0.0.6")

class Client:
    def __init__(self):
        self.messages = []
        self.title = Label(tk, text="Instant Messenger Client", font="Times, 25")
        self.title.place(x=20, y=0)
        self.main_msg_box = Text(tk, height=20, width=44)
        self.main_msg_box.place(x=20, y=50)
        self.scrollbar = Scrollbar(tk, command=self.main_msg_box.yview)
        self.scrollbar.place(x=380, y=200)
        self.send_msg_box = Text(tk, height=5, width=33)
        self.send_msg_box.place(x=20, y=400)
        self.send_msg_btn = Button(tk,text="Send", height=4, width=7, font="Times, 13", bg="#efcf40", command=self.send)
        self.send_msg_btn.place(x=300, y=400)
        self.username_box = Entry(tk)
        self.username_box.pack(side=LEFT)
        self.username_box.insert(END, "Enter username here:")
        self.host_box = Entry(tk)
        self.host_box.pack(side=LEFT)
        self.host_box.insert(END, "Enter host ip here:")
        self.submit_hostandusernamebtn = Button(tk, text="Connect!", bg="#efcf40", command=self.submit_credentials).pack(side=LEFT)
        self.clsbtn = Button(tk, text="Clear chat!", bg="#efcf40", command=self.cls).pack(side=RIGHT)
    def cls(self):
        self.main_msg_box.delete("1.0", END)
    def recver(self):
        while True:
            self.data = self.sock.recv(1024).decode("utf-8")
            self.messages.append(self.data)
            self.main_msg_box.insert(END, self.data)
            self.char_count = len(str(self.main_msg_box.get("1.0", END)))
            tk.update()
            time.sleep(.01)
    def send(self):
        self._data_to_send = str(self.send_msg_box.get("1.0", END))
        if len(self._data_to_send) > 1:
            try:
                self.data_to_send = self.username + " --> " + self._data_to_send
                self.send_msg_box.delete("1.0", END)
                self.sock.send(str(self.data_to_send).encode("utf-8"))
            except Exception as e:
                self.send_msg_box.delete("1.0", END)
                self.send_msg_box.insert(END, "Error:Could not send message!\nPlease make sure to fill out the box below!")
        tk.update()
    def submit_credentials(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tk.update()
        self.host = str(self.host_box.get())
        self.username = str(self.username_box.get())
        self.port = PORT
        try:
            self.sock.connect((self.host, self.port))
            self.send_msg_box.delete("1.0", END)
            self.send_msg_box.insert(END, "Connected to server!")
            tk.update()
            threading.Thread(target=self.recver).start()
        except:
            self.send_msg_box.delete("1.0", END)
            self.send_msg_box.insert(END, "Error:Could not connect to server!")


client = Client()

tk.mainloop()
