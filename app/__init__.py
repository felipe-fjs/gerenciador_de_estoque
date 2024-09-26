from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mailman import Mail
from CONFIG import SECRET_KEY, SQLALCHEMY_URI, EMAIL_USERNAME, EMAIL_PWD
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ SQLALCHEMY_URI
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

email_config = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT' : 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL':False,
    'MAIL_USERNAME': EMAIL_USERNAME,
    'MAIL_PASSWORD' : EMAIL_PWD
}
app.config.update(email_config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from app.models.user import *
with app.app_context():
    db.create_all()
    

from app.routes.auth_user import user_route
from app.routes.stock import stock_route

login_manager.login_view = 'user.login'

app.register_blueprint(stock_route, url_prefix='/estoque')
app.register_blueprint(user_route, url_prefix='/auth')
