import socket
import select
import struct
import PythonAPI.INETConsts as INETConsts

class DBConnection:
    
    RECV_POLL_WAIT = 5
    
    def __init__(self, address:str = None, port:int = None, poll_wait:int = RECV_POLL_WAIT):
        self.poll_wait = poll_wait
        self.sock = None
        if address and port:
            self.connect(address, port)
            
    def connect(self, address:str, port:int):
        if self.sock:
            self.sock.close()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.address = address
        self.connected = False
        
        if self.sock.connect_ex((bytes(address, 'UTF-8'), port)):
            print(f"Couldn't connect to {address}:{port}")
        else:
            self.connected = True
            self.sendAcknowledge()
            print(f"connected to {address}:{port}")
        
    
    def send(self, message:tuple):
        if self.sock.fileno() != -1:
            self.sock.send(message)
        else:
            self.connected = False
            
    def recv(self):
        if self.sock.fileno() == -1:
            self.connected = False
            return None
        
        ready = select.select([self.sock], [], [], self.poll_wait)
        if ready[0]:
            header_data = self.sock.recv(INETConsts.INET_HEADER_SIZE)
            if header_data:
                header = struct.unpack(INETConsts.INET_HEADER_FORMAT,
                                       header_data)
                # header[2] is msg_size
                data = self.sock.recv(header[2])
                return header, data
            else:
                return None, None
            
    
    def sendAcknowledge(self):
        message = self.packMessage(INETConsts.ACK_FORMAT,
                                       INETConsts.MESSAGE_TYPE.ACK,
                                       (INETConsts.SERVER_VERION,))
        self.send(message)
        
    def sendText(self, text:str):
        message = self.packMessage(f"{len(text)}s",
                                   INETConsts.MESSAGE_TYPE.TEXT,
                                   (bytes(text, 'UTF-8'),))
        self.send(message)
        
    def sendOFRI(self, o:str, f:int, r:int, i:int):
        message = self.packMessage(INETConsts.OFRI_FORMAT,
                                   INETConsts.MESSAGE_TYPE.DB,
                                   (bytes(o, 'UTF-8'),
                                    int(f), int(r), int(i)))
        self.send(message)
        
    def updateOFRI(self, o:str, f:int, r:int, i:int, value:str):
        message = self.packMessage(INETConsts.OFRI_FORMAT + f"{len(value)}s",
                                   INETConsts.MESSAGE_TYPE.DB,
                                   (bytes(o, 'UTF-8'),
                                    int(f), int(r), int(i),
                                    bytes(value, 'UTF-8')))
        self.send(message)
            
    def packMessage(self, format:str, data_type:int, data:tuple):
        return struct.pack(INETConsts.INET_HEADER_FORMAT + format,
                        self.port, bytes(self.address, 'UTF-8'),
                        struct.calcsize(format), data_type, *data)