import socket
import struct

MCAST_PORT:int = 8888
MCAST_ADDR:str = "224.1.1.1"
MCAST_TTL = 2

class Communication:

    last_msg:str = ""
    last_addr = None
    own_addr = socket.gethostbyname(socket.gethostname())

    def listen():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_ADDR, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_ADDR), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, addr = sock.recvfrom(1024)
            Communication.last_msg = data.decode("utf-8")
            Communication.last_addr = addr[0]
        

    def send(msg:str):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)
        sock.sendto(bytes(msg, "utf-8"), (MCAST_ADDR, MCAST_PORT))
