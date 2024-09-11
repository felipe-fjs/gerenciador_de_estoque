from app import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    email_confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    pwd = Column(String(128), nullable=True)

    def __init__(self, name, email, pwd):
        self.name = name
        self.email = email
        self.pwd = pwd

    def __repr__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nConfirmed: {self.email_confirmed}\nCreated at : {self.created_at}"


class LoginForm(FlaskForm):
    name = StringField("Nome: ", validators=[DataRequired(), Length(min=3)])
    email = EmailField("Email: ", validators=[DataRequired()])
    pwd = PasswordField("Senha:", validators=[DataRequired()])


class SignupForm(FlaskForm):
    name = StringField("Nome: ", validators=[DataRequired(), Length(min=3)])
    email = EmailField("Email: ", validators=[DataRequired()])
    pwd = PasswordField("Senha:", validators=[DataRequired()])
    check_pwd = PasswordField("Senha:", validators=[DataRequired(), EqualTo(pwd, 'As senhas devem ser iguais!')])
    