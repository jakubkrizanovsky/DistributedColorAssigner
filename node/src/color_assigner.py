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


    def update_loop(self):
        while True:
            target_distribution = self.get_target_distribution()
            actual_distribution = self.get_actual_distribution()
            print(f"Is target distribution: {self.is_target_distribution(target_distribution, actual_distribution)}")
            self.randomize_color()
            self.send_color()


    def get_target_distribution(self) -> Dict[str, int]:
        target_distribution: Dict[str, int] = {}
        node_count = len(self.color_table)
        total = sum(COLOR_DITRIBUTION.values())
        actual_sum = 0
        
        for color, dist in COLOR_DITRIBUTION.items():
            x = int(dist / total * node_count)
            target_distribution[color] = x
            actual_sum += x

        if actual_sum < node_count:
            target_distribution[FILL_COLOR] += node_count - actual_sum

        print("Target distribution")
        for color, value in target_distribution.items():
            print(f"{color} : {value}")

        return target_distribution
    
    
    def get_actual_distribution(self) -> Dict[str, int]:
        actual_distribution: Dict[str, int] = {}
        for color in COLOR_DITRIBUTION.keys():
            actual_distribution[color] = 0

        for color in self.color_table.values():
            actual_distribution[color] += 1

        print("Actual distribution")
        for color, value in actual_distribution.items():
            print(f"{color} : {value}")

        return actual_distribution


    def is_target_distribution(self, target_distribution:Dict[str, int], actual_distribution:Dict[str, int]) -> bool:
        for color, count in target_distribution.items():
            if(count != actual_distribution[color]):
                return False
            
        return True


    def update_table(self, node, msg):
        if(msg["type"]) == "update":
            self.color_table[node] = msg["value"]


    def send_color(self):
        msg = {
            "type":"update",
            "value":self.color
        }

        self.communication.send(msg)
        time.sleep(1)


    def run(self):
        listen_thread = Thread(target=self.communication.listen, args=[self.update_table])
        send_thread = Thread(target=self.update_loop)

        listen_thread.start()
        send_thread.start()

        listen_thread.join()
        send_thread.join()
        
