from api import Api
from communication import Communication
from threading import Thread
import time

def send_data():
    i = 0
    while True:
        print(f"sending: Hello World - {i}")
        Communication.send(f"Hello World - {i}")
        time.sleep(1)
        i += 1

if __name__ == '__main__':
    flask_thread = Api()
    send_thread = Thread(target=send_data)
    listen_thread = Thread(target=Communication.listen)

    flask_thread.start()
    send_thread.start()
    listen_thread.start()

    flask_thread.join()
    send_thread.join()
    listen_thread.join()

    print("Done")
