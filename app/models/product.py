from app import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import DataRequired
import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    cod = Column(Integer)
    desc = Column(String(256), nullable=False)
    categoria = Column(Integer, ForeignKey('categorias.id'))
    preco = Column(Float(), nullable=False)
    quant = Column(Integer, default=1, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    altered_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    def __init__(self, cod, desc, categoria, preco, quant, user_id):
        self.cod = cod
        self.desc = desc 
        self.categoria = categoria
        self.preco = preco
        self.quant = quant
        self.user_id = user_id


    def __repr__(self):
        return f"Cód: {self.cod}\npreco: R$ {self.preco:.2f}\nQuant: {self.quant}\nValor Total desse produto: R$ {self.preco * self.quant:.2f}"

    def get_total(self):
        return self.quant*self.preco
    
    def get_total_str(self):
        total = self.get_total()
        total_spt = list(str(total).split('.')[0][::-1])
        decimal = str(total).split('.')[1]
        for i in range(len(total_spt)):
            if i > 0 and i % 3 == 0:
                total_spt.insert(i, '.')
        total = ''
        for n in total_spt[::-1]:
            total += f'{n}'
        return total+','+decimal
    
    def get_nome_categoria(self):
        if not self.categoria:
            return "Sem categoria"
        cat = ProductCategory.query.filter_by(id=self.categoria).first()
        return cat.name

    @classmethod
    def price_number_to_str(clas, value):
        total = round(float(value), 2)
        total_spt = list(str(total).split('.')[0][::-1])
        decimal = str(total).split('.')[1]
        for i in range(len(total_spt)):
            if i > 0 and i % 3 == 0:
                total_spt.insert(i, '.')
        total = ''
        for n in total_spt[::-1]:
            total += f'{n}'
        return f'{total},{decimal}'


class ProductForm(FlaskForm):
    cod = StringField("Código do Produto:", validators=[DataRequired()])
    desc = StringField("Descrição do produto: ", validators=[DataRequired()])
    preco = DecimalField("Preço Produto: ", validators=[DataRequired()])
    quant = IntegerField("Quantidade: ", validators=[DataRequired()])


class ProductCategory(db.Model):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    altered_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.active = True

    def __repr__(self):
        return f'Categoria: {self.name}; ativa: {self.active}'
