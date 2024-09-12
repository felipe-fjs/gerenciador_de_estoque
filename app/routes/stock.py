from flask import Blueprint

stock_route = Blueprint('stock', __name__)

@stock_route.route('/home')
def home():
    return "<h1>Home do estoque</h1>"