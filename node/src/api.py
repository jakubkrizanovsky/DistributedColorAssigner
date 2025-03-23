from color_assigner import ColorAssigner
from communication import Communication
from flask import Flask
from threading import Thread

API_PORT:int = 10000

app = Flask(__name__)

class Api(Thread):

    communication:Communication = None
    color_assigner:ColorAssigner = None

    def __init__(self, communication:Communication, color_assigner:ColorAssigner):
        super(Api, self).__init__()
        Api.communication = communication
        Api.color_assigner:ColorAssigner = color_assigner

    @app.route('/')
    def home():
        response:str =  "<html><head><title>DSA</title></head>\n" + \
            "<body>\n" + \
                "<h2>Distributed Color Assigner</h2>\n" + \
                f"<h3>Node address: {Api.communication.own_addr}</h3>" + \
                f"<h3>Correct distribution: {Api.color_assigner.is_target_distribution()}</h3>"
        
        response += Api.get_color_table()
        response += Api.footer()

        response += "</body></html>\n"

        return response
    

    def get_color_table() -> str:
        html = ""
        for node, value in Api.color_assigner.color_table.items():
            html += f"<div>{node}: <span style=\"color:{value}\">{value}</span></div>"
        return html
    

    def footer() -> str:
        #TODO
        return "<br><div><a href=\"http://localhost:8081\">prev</a> | <a href=\"http://localhost:8081\">next</a></div>"

    def run(self):
        app.run(host="0.0.0.0", port=API_PORT)
