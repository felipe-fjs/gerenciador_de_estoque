from flask import Blueprint, url_for

stock_route = Blueprint('stock', __name__)

@stock_route.route('/home')
def home():
    print(url_for('user.new_pwd', token='12jh1j21bnkhjb321l3bnjbfskj2b31kh'))
    return "<h1>Home do estoque</h1>"