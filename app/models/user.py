from app import db, bcrypt
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, EmailField, PasswordField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    email_confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nullable=False)
    pwd = Column(String(128), nullable=True)

    def __init__(self, name, email, pwd):
        self.name = name
        self.email = email
        self.pwd = pwd

    def __repr__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nConfirmed: {self.email_confirmed}\nCreated at : {self.created_at}"

    def verify_pwd(self, pwd):
        return bcrypt.check_password_hash(self.pwd, pwd)


class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    cod = Column(Integer)
    desc = Column(String(256), nullable=False)
    preco = Column(Float(), nullable=False)
    quant = Column(Integer, default=1, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, cod, desc, preco, quant, user_id):
        self.cod = cod
        self.desc = desc 
        self.preco = preco
        self.quant = quant
        self.user_id

    def __repr__(self):
        return f"Cód: {self.cod}\npreco: {self.preco}\nQuant: {self.quant}\nValor Total desse produto: {self.preco * self.quant}"


class LoginForm(FlaskForm):
    name = StringField("Nome: ", validators=[DataRequired(), Length(min=3)])
    email = EmailField("Email: ", validators=[DataRequired()])
    pwd = PasswordField("Senha:", validators=[DataRequired()])


class SignupForm(FlaskForm):
    name = StringField("Nome: ", validators=[DataRequired(), Length(min=3)])
    email = EmailField("Email: ", validators=[DataRequired()])
    pwd = PasswordField("Senha:", validators=[DataRequired()])
    check_pwd = PasswordField("Senha:", validators=[DataRequired(), EqualTo('pwd', 'As senhas devem ser iguais!')])


class ProductForm(FlaskForm):
    cod = StringField("Código do Produto:", validators=[DataRequired()])
    desc = StringField("Descrição do produto: ", validators=[DataRequired()])
    preco = FloatField("Preço Produto: ", validators=[DataRequired()])
    quant = IntegerField("Quantidade: ", validators=[DataRequired()])
    
