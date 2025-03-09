from communication import Communication
from threading import Thread
from typing import Dict


class ColorAssigner(Thread):

    def __init__(self):
        super(ColorAssigner, self).__init__()

        self.table:Dict[str, str] = {}

    def update(self, node, value):
        print(f"Received: {value} from {node}")
        self.table[node] = value
    
    def run(self):
        Communication.listen(self.update)
