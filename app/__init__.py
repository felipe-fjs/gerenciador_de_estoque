from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from CONFIG import SECRET_KEY, SQLALCHEMY_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SECRET_KEY'] = 'mysql+pymysql://'+ SQLALCHEMY_URI

db = SQLAlchemy(app)

