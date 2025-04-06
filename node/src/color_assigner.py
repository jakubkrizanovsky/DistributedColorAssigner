import random
import time
from config import *
from communication import Communication
from threading import Thread, Lock
from typing import Dict


class ColorAssigner(Thread):

    def __init__(self, communication:Communication):
        super(ColorAssigner, self).__init__()
        self.communication = communication

        self.color:str = None
        self.mutex = Lock()
        self.color_table:Dict[str, str] = {}
        self.last_seen_table:Dict[str, int] = {}

        self.randomize_color()


    def set_color(self, color:str):
        print(f"Changing color from {self.color} to {color}", flush=True)
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
            is_target_distribution = self.is_target_distribution(target_distribution, actual_distribution)
            if not is_target_distribution:
                self.adjust_color(target_distribution, actual_distribution)

            self.send_color()
            time.sleep(TIME_INTERVAL)
            self.tick_last_seen()


    def get_target_distribution(self) -> Dict[str, int]:
        target_distribution: Dict[str, int] = {}
        with self.mutex:
            node_count = len(self.color_table)
        total = sum(COLOR_DITRIBUTION.values())
        actual_sum = 0
        
        for color, dist in COLOR_DITRIBUTION.items():
            x = int(dist / total * node_count)
            target_distribution[color] = x
            actual_sum += x

        while actual_sum < node_count:
            remainders: Dict[str, float] = {}
            for color, dist in COLOR_DITRIBUTION.items():
                remainders[color] = (dist / total * node_count) - target_distribution[color]
            top_color = max(remainders, key=remainders.get)
            target_distribution[top_color] += 1
            actual_sum += 1

        return target_distribution
    
    
    def get_actual_distribution(self) -> Dict[str, int]:
        actual_distribution: Dict[str, int] = {}
        for color in COLOR_DITRIBUTION.keys():
            actual_distribution[color] = 0

        with self.mutex:
            for color in self.color_table.values():
                actual_distribution[color] += 1

        return actual_distribution


    def is_target_distribution(self, target_distribution:Dict[str, int] = None, actual_distribution:Dict[str, int] = None) -> bool:
        if target_distribution is None:
            target_distribution = self.get_target_distribution()

        if actual_distribution is None:
            actual_distribution = self.get_actual_distribution()

        for color, count in target_distribution.items():
            if(count != actual_distribution[color]):
                return False
            
        return True
    
    
    def adjust_color(self, target_distribution:Dict[str, int], actual_distribution:Dict[str, int]):
        change_probability = 1 - target_distribution[self.color] / actual_distribution[self.color]

        if change_probability <= 0: 
            # don't change color if actual count of nodes for this color is ok, or less than target
            return
        
        if random.random() > change_probability:
            # not randomly selected for color change
            return
        
        color_diffs = {color : actual_distribution[color] - target_count for color, target_count in target_distribution.items()}
        ideal_changes = sum(value for value in color_diffs.values() if value > 0)

        # calculate probabilities to change to each color
        color_probabilities = {color : -diff/ideal_changes for color, diff in color_diffs.items() if diff < 0}

        # pick a color to change to based on probabilities
        rng_value = random.random()
        for color, probability in color_probabilities.items():
            rng_value -= probability
            if rng_value <= 0:
                self.set_color(color)
                return
            
    
    def tick_last_seen(self):
        nodes = list(self.last_seen_table.keys())
        for node in nodes:
            with self.mutex:
                self.last_seen_table[node] += 1
                if self.last_seen_table[node] >= NODE_TIMEOUT:
                    self.node_timeout(node)


    def node_timeout(self, node):
        print(f"Node {node} timed out", flush=True)
        self.color_table.pop(node)
        self.last_seen_table.pop(node)


    def update_table(self, node, msg):
        if(msg["type"]) == "update":
            with self.mutex:
                self.color_table[node] = msg["value"]
                self.last_seen_table[node] = 0


    def send_color(self):
        msg = {
            "type":"update",
            "value":self.color
        }

        self.communication.send(msg)


    def run(self):
        listen_thread = Thread(target=self.communication.listen, args=[self.update_table])
        send_thread = Thread(target=self.update_loop)

        listen_thread.start()
        send_thread.start()

        listen_thread.join()
        send_thread.join()
        
