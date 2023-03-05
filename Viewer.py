from tkinter import *
import socket
import select
import struct
import time

import Connection
import db.BASS, db.OFRI
import INETConsts

DB_INET_ADDRESS = ""
DB_INET_PORT = 5000
RECV_POLL_WAIT = 5

class View(Frame):
    def __init__(self, master:Tk):
        self.master = master
        Frame.__init__(self, self.master)
        master.title = "Remote kDB Viewer"
        self.connectDB()
        self.initWindow()
        
    def initWindow(self):
        
        self.ObjectLabel = Label(self.master, text="OBJECT")
        self.FieldLabel = Label(self.master, text="FIELD")
        self.RecordLabel = Label(self.master, text="RECORD")
        self.IndexLabel = Label(self.master, text="INDEX")
        
        self.ObjectLabel.grid(column = 0, row = 0)
        self.FieldLabel.grid(column = 1, row = 0)
        self.RecordLabel.grid(column = 2, row = 0)
        self.IndexLabel.grid(column = 3, row = 0)
        # Set up db entries
        self.db_entries = [Entry(self.master, width=10) for field in range(4)]
        col_num = 0
        for entry in self.db_entries:
            entry.grid(column = col_num, row=1)
            col_num += 1
        self.getDBButton = Button(self.master, text="Get DB value", command=self.getDBValue, width=10)
        self.getDBButton.grid(column=0, row=2)
        self.DBValue = StringVar()
        self.DBValue.set(" = ")
        self.DBLabel = Label(self.master, textvariable=self.DBValue)
        self.DBLabel.grid(column=5, row=1)
        

    def connectDB(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if self.sock.connect_ex((bytes(DB_INET_ADDRESS, 'UTF-8'), DB_INET_PORT)):
            print(f"Couldn't connect to {DB_INET_ADDRESS}:{DB_INET_PORT}")
            return
        else:
            Connection.ackMessage(None, self.sock)
            print(f"connected to {DB_INET_ADDRESS}:{DB_INET_PORT}")

    def readOFRIEntries(self):
        o = self.db_entries[0].get()
        f = self.db_entries[1].get()
        r = self.db_entries[2].get()
        i = self.db_entries[3].get()
        
        if '' == o or '' == f or '' == r or '' == i:
            return (None, None, None, None)
        
        return bytes(o, 'UTF-8'), int(f), int(r), int(i)

    def showDBValue(self, data):
        c_msg = struct.unpack(db.BASS.BASS_FORMAT, data)
        self.DBValue.set(f" = E:{c_msg[0]} A:{c_msg[1]} D:{c_msg[2]} G:{c_msg[3]}")
        self.DBLabel.configure(bg='green')

    def receiveFromDB(self):
        if self.sock.fileno() == -1:
            print("Connection closed!")
            self.sock.close()
            return
            
        ready = select.select([self.sock], [], [], RECV_POLL_WAIT)
        if ready[0]:
            header_data = self.sock.recv(INETConsts.INET_HEADER_SIZE)
            if not header_data:
                print("Bad header data")
                return None
            else:
                header = struct.unpack(INETConsts.INET_HEADER_FORMAT,
                                       header_data)
                data = self.sock.recv(header[2])
                self.showDBValue(data)

    def getDBValue(self):
        ofri = self.readOFRIEntries()
        if not any(ofri):
            self.DBLabel.configure(bg='red')
            self.DBValue.set(" = INVALID")
            return
        
        c_msg = Connection.packMessage(db.OFRI.OFRI_FORMAT, ofri,
                       INETConsts.MESSAGE_TYPE.DB)
        if c_msg != None and self.sock.fileno() != -1:
            self.sock.send(c_msg)
            self.receiveFromDB()
        else:
            print("Error sending message")

if __name__ == "__main__":
    root = Tk()
    app = View(master=root)
    root.mainloop()