from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Index', message='何か入力してくれ!')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')