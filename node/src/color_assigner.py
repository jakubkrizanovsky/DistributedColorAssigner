import json
import random
import time
from config import *
from communication import Communication
from threading import Thread
from typing import Dict


class ColorAssigner(Thread):

    def __init__(self, communication:Communication):
        super(ColorAssigner, self).__init__()
        self.communication = communication

        self.color:str = None
        self.color_table:Dict[str, str] = {}

        self.randomize_color()

    def set_color(self, color:str):
        self.color = color
        self.color_table[self.communication.own_addr + " (this node)"] = color

    def randomize_color(self):
        total = sum(COLOR_DITRIBUTION.values())
        value = random.randrange(0, total)
        for color, dist in COLOR_DITRIBUTION.items():
            value -= dist
            if value <= 0:
                self.set_color(color)
                return

    def update(self, node, msg):
        if(msg["type"]) == "update":
            self.color_table[node] = msg["value"]

    def send_color(self):
        while True:
            self.randomize_color()

            msg = {
                "type":"update",
                "value":self.color
            }

            self.communication.send(msg)
            time.sleep(1)
    
    def run(self):
        listen_thread = Thread(target=self.communication.listen, args=[self.update])
        send_thread = Thread(target=self.send_color)

        listen_thread.start()
        send_thread.start()

        listen_thread.join()
        send_thread.join()
        
