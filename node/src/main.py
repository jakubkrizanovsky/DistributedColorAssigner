import os
import signal
from threading import Thread
from api import Api
from communication import Communication
from color_assigner import ColorAssigner

def signal_handler(signal, frame):
    os._exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    
    communication = Communication()
    t = Thread(target=communication.discover_self)
    t.start()
    t.join()

    color_assigner = ColorAssigner(communication)
    api = Api(communication, color_assigner)

    api.start()
    color_assigner.start()

    api.join()
    color_assigner.join()

    print("Done")
