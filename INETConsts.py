import struct
import os
from enum import Enum
import db.BASS

# SERVER CONSTS

SERVER_VERION =  2

# INET C STRUCTS

CONNECTION_FORMAT = "@H46s" # port, address
INET_HEADER_FORMAT = CONNECTION_FORMAT + "II" #  CONNECTION, message_size, message_type
INET_PACKAGE_FORMAT = INET_HEADER_FORMAT + "0s" # INET_HEADER , payload
ACK_FORMAT = INET_HEADER_FORMAT + "I"

CONNECTION_SIZE = struct.calcsize(CONNECTION_FORMAT)
INET_HEADER_SIZE = struct.calcsize(INET_HEADER_FORMAT)
INET_PACKAGE_SIZE = struct.calcsize(INET_PACKAGE_FORMAT)
ACK_SIZE = struct.calcsize(ACK_FORMAT)

# INET ENVIRONMENT VARIABLES

KDB_INET_ADDRESS_ENV = "KDB_INET_ADDRESS"
KDB_INET_ADDRESS = os.getenv(KDB_INET_ADDRESS_ENV)

#MESSAGE TYPES
class MESSAGE_TYPE:
    NONE = 0
    TEXT = 1
    ACK  = 2
    DB   = 3