from communication import Communication
from flask import Flask
from threading import Thread

API_PORT:int = 10000

app = Flask(__name__)

class Api(Thread):
    @app.route('/')
    def home():
        return "<html><head><title>DSA</title></head>\n" + \
            "<body>\n" + \
                "<h2>Hello World</h2>\n" + \
                f"<p>{Communication.last_msg}</p>\n" + \
                f"<p>{Communication.last_addr}</p>\n" + \
                f"<p>{Communication.own_addr}</p>\n" + \
            "</body></html>\n"

    def run(self):
        app.run(host="0.0.0.0", port=API_PORT)
