import time
from config import *
import json
import uuid
from threading import Thread
import socket
import struct
from typing import Callable

class Communication:

    def __init__(self):
        self.own_addr = None
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.listening = False

    def listen(self, callback:Callable[[str, str], None]):
        self.listening = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_ADDR, MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_ADDR), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while self.listening:
            data, addr = sock.recvfrom(1024)

            # Ignore packets from yourself
            if addr[0] == self.own_addr:
                continue

            msg = json.loads(data.decode("utf-8"))
            print(f"Received: {msg} from {addr[0]}")
            callback(addr[0], msg)
        
    def send(self, msg):
        print(f"Sending: {msg}")
        self.send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)
        self.send_socket.sendto(bytes(json.dumps(msg), "utf-8"), (MCAST_ADDR, MCAST_PORT))

    def discover_self(self):
        discover_uuid = uuid.uuid4().int

        def callback(addr:str, msg:str):
            if msg["type"] == "discover" and msg["value"] == discover_uuid:
                self.own_addr = addr
                self.listening = False

        listen_thread = Thread(target=self.listen, args=[callback])
        listen_thread.start()

        while self.listening:
            msg = {
                "type":"discover",
                "value":discover_uuid
            }
            self.send(msg)
            time.sleep(1)

        listen_thread.join()