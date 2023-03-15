from tkinter import *
import struct

import DBConnection
import PythonAPI.DBMap
import PythonAPI.INETConsts as INETConsts

CONNECTION_LABEL_ROW = 0
CONNECTION_ENTRY_ROW = 1

OBJECT_LABEL_ROW = 2
OBJECT_ENTRY_ROW =  3
OBJECT_VALUE_ROW = 4
OBJECT_BUTTON_ROW = 5

COMPONENT_WIDTH = 20

class View(Frame):
    def __init__(self, master:Tk):
        self.master = master
        Frame.__init__(self, self.master)
        self.connection = None
        master.title = "Remote kDB Viewer"
        self.initWindow()
        
    def initWindow(self):
        
        self.AddressLabel = Label(self.master, text="kDB Address", width=COMPONENT_WIDTH)
        self.PortLabel = Label(self.master, text="kDB Port", width=COMPONENT_WIDTH)
        self.AddressValue = StringVar(value=INETConsts.DB_INET_ADDRESS)
        self.PortValue = StringVar(value=INETConsts.DB_INET_PORT)
        self.AddressEntry = Entry(self.master, textvariable=self.AddressValue, width=COMPONENT_WIDTH)
        self.PortEntry = Entry(self.master, textvariable=self.PortValue, width=COMPONENT_WIDTH)
        
        self.AddressLabel.grid(column=0, row=CONNECTION_LABEL_ROW)
        self.PortLabel.grid(column=1, row=CONNECTION_LABEL_ROW)
        self.AddressEntry.grid(column=0, row=CONNECTION_ENTRY_ROW)
        self.PortEntry.grid(column=1, row=CONNECTION_ENTRY_ROW)
        
        self.ConnectButton = Button(self.master, text="Connect", command=self.connectDB)
        self.ConnectButton.grid(column=2, row=CONNECTION_ENTRY_ROW)
        
        self.ObjectLabel = Label(self.master, text="OBJECT")
        self.FieldLabel = Label(self.master, text="FIELD")
        self.RecordLabel = Label(self.master, text="RECORD")
        self.IndexLabel = Label(self.master, text="INDEX")
        
        self.ObjectLabel.grid(column = 0, row = OBJECT_LABEL_ROW)
        self.FieldLabel.grid(column = 1, row = OBJECT_LABEL_ROW)
        self.RecordLabel.grid(column = 2, row = OBJECT_LABEL_ROW)
        self.IndexLabel.grid(column = 3, row = OBJECT_LABEL_ROW)
        
        # Set up db entries
        self.entry_values = [StringVar() for _ in range(4)]
        self.db_entries = [Entry(self.master, width=COMPONENT_WIDTH, textvariable=self.entry_values[index]) for index in range(4)]
        col_num = 0
        for entry in self.db_entries:
            entry.grid(column = col_num, row=OBJECT_ENTRY_ROW)
            col_num += 1
            
        self.entry_values[0].set("DCC_CHAR")
        self.entry_values[1].set("0")
        self.entry_values[2].set("0")
        self.entry_values[3].set("0")
        
        self.getDBButton = Button(self.master, text="Get DB value", command=self.getDBValue, width=COMPONENT_WIDTH)
        self.getDBButton.grid(column=0, row=OBJECT_BUTTON_ROW)
        self.DBValue = StringVar()
        self.DBLabel = Label(self.master, textvariable=self.DBValue)
        self.DBLabel.grid(column=0, row=OBJECT_VALUE_ROW, columnspan=5, sticky = W)
        
        self.setDBButton = Button(self.master, text="Set DB value", command=self.setDBValue, width=COMPONENT_WIDTH)
        self.setDBButton.grid(column=1, row=OBJECT_BUTTON_ROW)
        self.DBUpdateValue = StringVar()
        self.DBUpdateValue.set("Enter new value")
        self.DBValueSet = Entry(self.master, width=COMPONENT_WIDTH, textvariable=self.DBUpdateValue)
        self.DBValueSet.grid(column=3, row=OBJECT_BUTTON_ROW)
        

    def connectDB(self):
        if self.connection:
            self.connection.connect(self.AddressValue.get(), int(self.PortEntry.get()))
        else:
            self.connection = DBConnection.DBConnection(self.AddressValue.get(), int(self.PortValue.get()))
        
        if self.connection.connected:
            self.AddressEntry.config(bg='green')
            self.PortEntry.config(bg='green')
        else:
            self.AddressEntry.config(bg='red')
            self.PortEntry.config(bg='red')

    def readOFRIEntries(self):
        o = self.db_entries[0].get()
        f = self.db_entries[1].get()
        r = self.db_entries[2].get()
        i = self.db_entries[3].get()
        
        if '' == o or '' == f or '' == r or '' == i:
            return (None, None, None, None)
        
        return (o, f, r, i)

    def showDBValue(self, data, obj):
        
        if obj not in PythonAPI.DBMap.ALL_OBJECTS or not data:
            self.DBLabel.configure(bg='red')
            self.DBValue.set("INVALID OFRI")
            return
        
        c_msg = struct.unpack(PythonAPI.DBMap.ALL_OBJECTS[obj].FORMAT, data)
        db_obj = PythonAPI.DBMap.ALL_OBJECTS[obj](c_msg)
        self.DBValue.set(str(db_obj))
        self.DBLabel.configure(bg='green')


    def getDBValue(self):
        ofri = self.readOFRIEntries()
        if not any(ofri):
            self.DBLabel.configure(bg='red')
            self.DBValue.set("INVALID OFRI")
            return
        
        self.connection.sendOFRI(*ofri)
        _, db_data = self.connection.recv()
        self.showDBValue(db_data, ofri[0])
    
    def setDBValue(self):
        ofri = self.readOFRIEntries()
        if not any(ofri):
            return
        
        self.connection.updateOFRI(*ofri, self.DBUpdateValue.get())
        _, db_data = self.connection.recv()
        self.showDBValue(db_data, ofri[0])

if __name__ == "__main__":
    root = Tk()
    app = View(master=root)
    root.mainloop()