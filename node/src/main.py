from api import Api
from communication import Communication
from color_assigner import ColorAssigner
from threading import Thread
import time


def send_data():
    i = 0
    while True:
        print(f"sending: Hello World - {i}")
        Communication.send(str(i))
        time.sleep(1)
        i += 1

def callback(data:str, addr:str):
    print(f"Received: {data} from {addr}")

if __name__ == '__main__':
    color_assigner = ColorAssigner()
    api_thread = Api(color_assigner)
    send_thread = Thread(target=send_data)
    # listen_thread = Thread(target=Communication.listen, args=[callback])

    api_thread.start()
    send_thread.start()
    color_assigner.start()
    # listen_thread.start()

    api_thread.join()
    send_thread.join()
    color_assigner.join()
    # listen_thread.join()

    print("Done")
