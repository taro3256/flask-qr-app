from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView

app = Flask(__name__)
app.secret_key = b'abcdedadad'

member_data = {}
message_data = []

@app.route('/', methods=['GET'])
def index():
    global message_data
    if 'login' in session and session['login']:
        msg = 'Login id:' + session['id']
        return render_template('messages.html', title='Messages', message=msg, data=message_data)
    else:
        return redirect('/login')

@app.route('/', methods=['POST'])
def form():
    msg = request.form.get('comment')
    message_data.append((session['id'], msg))
    if len(message_data) > 25:
        message_data.pop(0)
    return redirect('/')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='Login', err=False, message='IDとパスワードを入力：', id='')

@app.route('/login', methods=['POST'])
def login_post():
    global member_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            session['login'] = True
        else:
            session['login'] = False
    else:
        member_data[id] = pswd
        session['login'] = True
    session['id'] = id
    if session['login']:
        return redirect('/')
    else:
        return render_template('login.html', title='Login', err=False, message='パスワードが違います', id=id)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.pop('login')
    return redirect('/login')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')