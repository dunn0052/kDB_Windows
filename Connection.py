import PythonAPI.INETConsts as INETConsts
import socket
import struct
import threading
import time
import select
import PythonAPI.db.BASS
import PythonAPI.db.OFRI

RECV_POLL_WAIT = 5
INET_ADDRESS = b'192.168.56.1'
INET_PORT = 5000

def packMessage(format, data, data_type):
    return struct.pack(INETConsts.INET_HEADER_FORMAT + format,
                       INET_PORT, INET_ADDRESS,
                       struct.calcsize(format), data_type, *data)

def recvMessage(sock):
    t = threading.currentThread()
    while getattr(t, "connected", True):
        if sock.fileno() == -1:
            print("Connection closed!")
            time.sleep(1)
            sock.close()
            continue
        
        ready = select.select([sock], [], [], RECV_POLL_WAIT)
        if ready[0]:
            header_data = sock.recv(INETConsts.INET_HEADER_SIZE)
            if not header_data:
                print("Bad header data")
                continue
            else:
                header = struct.unpack(INETConsts.INET_HEADER_FORMAT,
                                       header_data)
                data = sock.recv(header[2])
                message_switch[header[3]](data, None)
    print("Recv thread end")

def getOFRI(message):
    ofri_data = message.split('.')
    if len(ofri_data) != 4:
        return None
    
    ofri_data[0] = bytes(ofri_data[0], "UTF-8")
    ofri_data[1] = int(ofri_data[1])
    ofri_data[2] = int(ofri_data[2])
    ofri_data[3] = int(ofri_data[3])
    
    return packMessage(INETConsts.OFRI_FORMAT, ofri_data,
                       INETConsts.MESSAGE_TYPE.DB)

def sendMessage(sock, recvThread):
    sendThread = threading.currentThread()
    while getattr(sendThread, "connected", True):
        message = input()
        
        if message == "end":
            setattr(sendThread, "connected", False)
            setattr(recvThread, "connected", False)
            sock.close()
            continue
        
        if(message == "ofri"):
            message = input()
            c_msg = getOFRI(message)
        else:
            print(f"Sending: {message}")
            message = bytes(message, 'UTF-8') + b'\0'
            c_msg = struct.pack(INETConsts.INET_HEADER_FORMAT + f"{len(message)}s",
                                INET_PORT, INET_ADDRESS, len(message),
                                INETConsts.MESSAGE_TYPE.TEXT, message)
        if c_msg != None:
            sock.send(c_msg)
    print("Ending send thread")

def noneMessage(data, conn):
    print("Got NONE message")
    print(data)
    
def ackMessage(data, conn):
    print("Sending ack")
    # port, host, message size, message type, payload (version number)
    ack = (INET_PORT, INET_ADDRESS, INETConsts.ACK_SIZE,INETConsts.MESSAGE_TYPE.ACK, INETConsts.SERVER_VERION)
    c_ack = struct.pack(INETConsts.ACK_FORMAT, *ack)
    conn.send(c_ack)

def textMessage(data, conn):
    print("Got text!")
    # Use f"{len(data)}s" to get variable payload
    c_msg = struct.pack(INETConsts.INET_HEADER_FORMAT + f"{len(data)}s",
                        INET_PORT, INET_ADDRESS, len(data),
                        INETConsts.MESSAGE_TYPE.TEXT, data)
    text = str(data, 'UTF-8')
    print(f"message {text}")
    conn.send(c_msg)
    
def dbMessage(data, conn):
    c_msg = struct.unpack(db.BASS.BASS_FORMAT, data)
    print(f"BASS E:{c_msg[0]}, A:{c_msg[1]}, D:{c_msg[2]}, G:{c_msg[3]}")

message_switch = {
    INETConsts.MESSAGE_TYPE.NONE:noneMessage,
    INETConsts.MESSAGE_TYPE.TEXT:textMessage,
    INETConsts.MESSAGE_TYPE.ACK:ackMessage,
    INETConsts.MESSAGE_TYPE.DB:dbMessage
    }

def connectTo(address, port, listening_port = 5001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex((address, int(port))):
            print(f"Couldn't connect to {address}:{port}")
            return
        else:
            ackMessage(None, sock)
            print(f"connected to {address}:{port}")
        
        recvThread = threading.Thread(target = recvMessage, args=(sock,))
        recvThread.connected = True
        recvThread.start()
        sendThread = threading.Thread(target = sendMessage, args=(sock, recvThread))
        sendThread.connected = True
        sendThread.start()
        
        while recvThread.connected or sendThread.connected:
            time.sleep(1)