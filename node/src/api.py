from color_assigner import ColorAssigner
from communication import Communication
from flask import Flask
from threading import Thread
import os

API_DEFAULT_PORT:int = 8080

app = Flask(__name__)

class Api(Thread):

    communication:Communication = None
    color_assigner:ColorAssigner = None
    my_api_port:int = None
    min_api_port:int = None
    max_api_port:int = None

    def __init__(self, communication:Communication, color_assigner:ColorAssigner):
        super(Api, self).__init__()
        Api.communication = communication
        Api.color_assigner:ColorAssigner = color_assigner
        try:
            Api.my_api_port = int(os.getenv("MY_API_PORT"))
            Api.min_api_port = int(os.getenv("MIN_API_PORT"))
            Api.max_api_port = int(os.getenv("MAX_API_PORT"))
        except:
            print(f"Cannot read api ports from env variables, using default port {API_DEFAULT_PORT}")


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
        for node, value in sorted(Api.color_assigner.color_table.items(), key=lambda item: item[0]):
            html += f"<div>{node}: <span style=\"color:{value}\">{value}</span></div>"
        return html
    

    def footer() -> str:
        if Api.my_api_port is None:
            return ""
        
        prev_link = f"<a href=\"http://localhost:{Api.my_api_port - 1}\">previous node</a>" \
            if Api.my_api_port - 1 >= Api.min_api_port else "<span>first node</span>"
        
        next_link = f"<a href=\"http://localhost:{Api.my_api_port + 1}\">next node</a>" \
            if Api.my_api_port + 1 <= Api.max_api_port else "<span>last node</span>"

        return f"<br><div>{prev_link} | {next_link}</div>"

    def run(self):
        api_port = Api.my_api_port if Api.my_api_port is not None else API_DEFAULT_PORT
        app.run(host="0.0.0.0", port=api_port)
