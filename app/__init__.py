from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from CONFIG import SECRET_KEY, SQLALCHEMY_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ SQLALCHEMY_URI

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models.user import *
with app.app_context():
    db.create_all()
    
