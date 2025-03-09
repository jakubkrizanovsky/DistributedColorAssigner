from color_assigner import ColorAssigner
from communication import Communication
from flask import Flask
from threading import Thread

API_PORT:int = 10000

app = Flask(__name__)

class Api(Thread):

    color_assigner:ColorAssigner = None

    def __init__(self, color_assigner:ColorAssigner):
        super(Api, self).__init__()
        Api.color_assigner:ColorAssigner = color_assigner

    @app.route('/')
    def home():
        response:str =  "<html><head><title>DSA</title></head>\n" + \
            "<body>\n" + \
                "<h2>Hello World</h2>\n"
                
        for node, value in Api.color_assigner.table.items():
            response += f"<p>{node}: {value}</p>"

        response += "</body></html>\n"

        return response

    def run(self):
        app.run(host="0.0.0.0", port=API_PORT)
