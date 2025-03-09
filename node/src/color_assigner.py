import random
import time
from config import *
from communication import Communication
from threading import Thread
from typing import Dict


class ColorAssigner(Thread):

    def __init__(self):
        super(ColorAssigner, self).__init__()

        self.color:str = None
        self.table:Dict[str, str] = {}

        self.randomize_color()

    def randomize_color(self):
        total = sum(COLOR_DITRIBUTION.values())
        value = random.randrange(0, total)
        for color, dist in COLOR_DITRIBUTION.items():
            value -= dist
            if value <= 0:
                self.color = color
                return

    def update(self, node, value):
        print(f"Received: {value} from {node}")
        self.table[node] = value

    def send_color(self):
        while True:
            self.randomize_color()
            print(f"Sending: {self.color}")
            Communication.send(self.color)
            time.sleep(1)
    
    def run(self):
        listen_thread = Thread(target=Communication.listen, args=[self.update])
        send_thread = Thread(target=self.send_color)

        listen_thread.start()
        send_thread.start()

        listen_thread.join()
        send_thread.join()
        
