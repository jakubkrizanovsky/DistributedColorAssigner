from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<html><head><title>Hello World</title></head>' + \
           '<body><h2>It works!</h2></body></html>\n'

if __name__ == '__main__':
    app.run(host="0.0.0.0")