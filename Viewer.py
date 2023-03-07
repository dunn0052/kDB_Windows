from tkinter import *
import struct

import DBConnection
import PythonAPI.DBMap
import PythonAPI.INETConsts as INETConsts


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
        self.entry_values = [StringVar() for _ in range(4)]
        self.db_entries = [Entry(self.master, width=10, textvariable=self.entry_values[index]) for index in range(4)]
        col_num = 0
        for entry in self.db_entries:
            entry.grid(column = col_num, row=1)
            col_num += 1
            
        self.entry_values[0].set("BASS")
        self.entry_values[1].set("1")
        self.entry_values[2].set("1")
        self.entry_values[3].set("1")
        
        self.getDBButton = Button(self.master, text="Get DB value", command=self.getDBValue, width=10)
        self.getDBButton.grid(column=0, row=2)
        self.DBValue = StringVar()
        self.DBValue.set(" = ")
        self.DBLabel = Label(self.master, textvariable=self.DBValue)
        self.DBLabel.grid(column=5, row=1)
        

    def connectDB(self):
        self.connection = DBConnection.DBConnection(INETConsts.DB_INET_ADDRESS, INETConsts.DB_INET_PORT)

    def readOFRIEntries(self):
        o = self.db_entries[0].get()
        f = self.db_entries[1].get()
        r = self.db_entries[2].get()
        i = self.db_entries[3].get()
        
        if '' == o or '' == f or '' == r or '' == i:
            return (None, None, None, None)
        
        return (o, f, r, i)

    def showDBValue(self, data, obj):
        
        if obj not in PythonAPI.DBMap.ALL_OBJECTS:
            self.DBLabel.configure(bg='red')
            self.DBValue.set(" = INVALID")
            return
        
        c_msg = struct.unpack(PythonAPI.DBMap.ALL_OBJECTS[obj].FORMAT, data)
        db_obj = PythonAPI.DBMap.ALL_OBJECTS[obj](*c_msg)
        self.DBValue.set(str(db_obj))
        self.DBLabel.configure(bg='green')


    def getDBValue(self):
        ofri = self.readOFRIEntries()
        if not any(ofri):
            self.DBLabel.configure(bg='red')
            self.DBValue.set(" = INVALID")
            return
        
        self.connection.sendOFRI(*ofri)
        _, db_data = self.connection.recv()
        self.showDBValue(db_data, ofri[0])

if __name__ == "__main__":
    root = Tk()
    app = View(master=root)
    root.mainloop()