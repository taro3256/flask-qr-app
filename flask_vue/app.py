from flask import Flask, render_template, request, session, redirect, jsonify
from flask.views import MethodView
import pickle

app = Flask(__name__)
app.select_key = b'random string...'

member_data = {}
message_data = []
member_data_file = 'member_data.dat'
message_data_file = 'message_data.dat'

try:
    with open(member_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            member_data = list
except:
    pass

try:
    with open(message_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            message_data = list
except:
    pass

# トップページにアクセス
@app.route('/', methods=['GET'])
def index():
    global message_data
    return render_template('messages.html', login=False, title='Messages', message='not logined...', data=message_data)
    
# メッセージ情報を取得
@app.route('/post', methods=['POST'])
def postMsg():
    global message_data
    id = request.form.get('id')
    msg = request.form.get('comment')
    message_data.append((id, msg))
    if len(message_data) > 10:
        message_data.pop(0)
    try:
        with open(message_data_file, 'wb') as f:
            pickle.dump(message_data, f)
    except:
        pass
    return 'True'

@app.route('/messages', methods=['POST'])
def getMsg():
    global message_data
    return jsonify(message_data)

@app.route('/login', methods=['POST'])
def login_post():
    global member_data, message_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            flg = 'True'
        else:
            flg = 'False'
    else:
        member_data[id] = pswd
        flg = 'True'
        try:
            with open(member_data_file, 'wb') as f:
                pickle.dump(member_data, 'f')
        except:
            pass
    return flg

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')