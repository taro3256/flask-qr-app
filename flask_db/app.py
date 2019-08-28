import pickle
import sqlite3

from flask import (Flask, g, jsonify, redirect, render_template, request, session)
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///sample.sqlite3')
Base = declarative_base()

class Mydata(Base):
    __tablename__ = 'mydata'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail = Column(String(255))
    age = Column(Integer)

    def toDict(self):
        return {
            'id':int(self.id),
            'name':str(self.name),
            'mail':str(self.mail),
            'age':int(self.age)
        }
def getByList(arr):
    res = []
    for item in arr:
        res.append(item.toDict())
    return res

def getAll():
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Mydata).all()
    ses.close()
    return res

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Index', message='SQLite3 DB', alert='This is SQLite3 DB sample')

@app.route('/<id>', methods=['GET'])
def index_id(id):
    return render_template('index.html', title='Index', message='SQLite3 DB', alert='This is SQLite3 DB sample', id=id)

@app.route('/ajax', methods=['GET'])
def ajax():
    # db = get_db()
    # cur = db.execute("select * from mydata where id={id}".format(id=id))
    # mydata = cur.fetchall()
    mydata = getAll()
    # return jsonify(mydata)
    return jsonify(getByList(mydata))

@app.route('/ajax/<id>', methods=['GET'])
def ajax_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    ses.close()
    return jsonify(mydata.toDict())

@app.route('/form', methods=['POST'])
def form():
    name = request.form.get('name')
    mail = request.form.get('mail')
    age = int(request.form.get('age'))
    mydata = Mydata(name=name, mail=mail, age=age)
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.add(mydata)
    ses.commit()
    ses.close()
    return 'ok'

@app.route('/form/<id>', methods=['POST'])
def form_id(id):
    name = request.form.get('name')
    mail = request.form.get('mail')
    age = int(request.form.get('age'))
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    mydata.name = name
    mydata.mail = mail
    mydata.age = age
    ses.add(mydata)
    ses.commit()
    ses.close()
    return 'ok'

@app.route('/delete/<id>', methods=['GET'])
def delete_id(id):
    Session = sessionmaker(bind=engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    ses.delete(mydata)
    ses.close()
    return "delete id = " + id

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('sample.sqlite3')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
