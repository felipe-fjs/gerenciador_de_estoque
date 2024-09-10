from flask import Flask
from CONFIG import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysql+pymysql://'+SECRET_KEY
