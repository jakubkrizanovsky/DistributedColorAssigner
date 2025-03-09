from api import Api
from communication import Communication
from color_assigner import ColorAssigner
from threading import Thread

if __name__ == '__main__':
    color_assigner = ColorAssigner()
    api_thread = Api(color_assigner)

    api_thread.start()
    color_assigner.start()

    api_thread.join()
    color_assigner.join()

    print("Done")
