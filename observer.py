from flask import Flask
from util import rest
from flask import send_file

app = Flask(__name__,static_folder="static")


@app.route('/search/<string:mobile>')
def search_by_mobile(mobile):
    return rest.response_to("hello")

# @app.route('/<string:name>')
# def watch(name):
#     return send_file('static/'+name)

if __name__ == '__main__':
    app.run(threaded=True)
