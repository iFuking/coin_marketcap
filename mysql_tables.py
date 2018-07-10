from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float
import flask_conf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = flask_conf.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Trading_pair(db.Model):
    __tablename__ = 'trading_pair'
    id = db.Column('id', Integer, primary_key=True)
    token = db.Column('token', String(25))
    date = db.Column('date', String(10))
    rank = db.Column('rank', Integer)
    source = db.Column('source', String(15))
    pair = db.Column('pair', String(15))
    volume = db.Column('volume', Integer)
    price = db.Column('price', Float)
    percent = db.Column('percent', Float)


if __name__ == '__main__':
    db.create_all()
