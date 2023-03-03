import INETConsts
import socket
import struct

def noneMessage(data, conn):
    print("Got NONE message")
    print(data)
    
def ackMessage(data, conn):
    ack = (4, b'', 4, 2, INETConsts.SERVER_VERION)
    c_ack = struct.pack(INETConsts.ACK_FORMAT, *ack)
    conn.send(c_ack)

def textMessage(data, conn):
    c_msg = struct.pack(INETConsts.INET_HEADER_FORMAT + f"{len(data)}s", 4, b'', len(data), 1, data)
    text = str(data, 'UTF-8')
    print(f"message {text}")
    conn.send(c_msg)
    
def dbMessage(data, conn):
    c_msg = struct.unpack("@20sIII", data)
    print(c_msg)
    pass    

message_switch = {
    0:noneMessage,
    1:textMessage,
    2:ackMessage,
    3:dbMessage
    }

def connectTo(address, port, listening_port = 5001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((address, listening_port))
        sock.listen()
        #conn, addr = sock.accept()
        conn, addr = sock.connect(address)
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(INETConsts.INET_HEADER_SIZE)
                if not data:
                    break
                message_header = struct.unpack(INETConsts.INET_HEADER_FORMAT, data)
                #print(f"Message header: {message_header}")
                message_switch[message_header[3]](conn.recv(message_header[2]), conn)
                