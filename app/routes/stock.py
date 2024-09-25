from app import db
from app.models.product import Product, ProductForm, ProductCategory
from flask import Blueprint, url_for, render_template, flash, request, redirect, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import OperationalError

stock_route = Blueprint('stock', __name__)

""" Rotas do estoque
    * /estoque/inicio (GET): realiza renderização de template com os produtos do estoque
    
    * /estoque/produto/novo (GET - POST):
        - GET: renderizar formulário para inserção de informações
        - POST: realiza o envio das informações do produto

    * /estoque/produto/novos (GET - POST): futuramente será criada rota para adição de produtos via foto
        - GET: carrega o template
        - GET 2 : retorna um lista com os produtos identificados em foto
        - POST: realiza o envio dos dados para o DB

    * /estoque/produto/<id> (GET): carrega as informações de acordo com um produto

    * /estoque/produto/<id>/edit (GET - PUT):
        - GET: carrega as informações do produto para edição num formulário
        - PUT: envia as informações para o back-end

    * /estoque/produto/<id>/delete (DELETE): realiza a "suspensão" do produto no estoque, pois o produto ainda pode ser informado futuramente em notas fiscais

    
    * /estoque/exportar (GET): será retornado um template com opções para formatos que o estoque pode ser retornado (PDF, EXCEL, CSV)
"""

@stock_route.route('/')
@stock_route.route('/home')
@stock_route.route('/inicio')
@login_required
def home():
    try:
        products = Product.query.filter_by(user_id=current_user.id, active=True).all()
    except OperationalError:
        products = []
        flash('Ocorreu algum erro ao recuperar os produtos em seu estoque no banco de dados....')
    else:
        total = 0
        total_produtos = 0
        for product in products:
            total +=  product.get_total()
            total_produtos += product.quant

        total = Product.price_number_to_str(total)
        db.session.close()
        
    return render_template('stock/product/home.html', products=products, total=total, total_produtos=total_produtos)


@stock_route.route('/produto/novo', methods=['POST', 'GET'])
@login_required
def new_product():
    form = ProductForm()
    if request.method == 'POST':
        if not Product.query.filter_by(cod=form.cod.data).first():
            # caso o produto não esteja cadastrado
            product = Product(form.cod.data, form.desc.data, form.preco.data, form.quant.data, current_user.id)

            try:
                db.session.add(product)
                db.session.commit()
            except OperationalError:
                flash(f"Ocorreu algum erro ao tentar salvar o Produto de código {product.cod}")
            else:
                flash(f'Produto "{product.desc}" foi adicionado com sucesso!')
            finally:
                db.session.close()
    
            return redirect(url_for('stock.new_product'))
        
        # parte destinada caso o produto já esteja cadastrado
        
    return render_template('stock/product/new_product.html', form=form)


@stock_route.route('/produto/', defaults={'id': None}, methods=['GET'])
@stock_route.route('/produto/<id>')
@login_required
def get_product(id):
    if not id:
        id = request.args.get('id')

    if not Product.query.filter_by(id=id).first():
        flash(f'Nenhum produto foi encontrado com esse id.')
        return redirect(url_for('stock.home'))
    
    try:
        product = Product.query.filter_by(id=id).first()
    except OperationalError:
        flash(f'ocorreu um erro ao carregar o produto de id {id}')
    finally:
        db.session.close()
    return render_template('stock/product/get_product.html', product=product)


@stock_route.route('/produto/edit/', defaults={'id':None}, methods=['GET', 'PUT'])
@stock_route.route('/produto/edit/<id>', methods=['PUT', 'GET'])
@login_required
def edit_product(id):
    if not id:
        id = request.args.get('id')

    if request.method == 'PUT':
        try:
            update_product= request.json
            product = Product.query.filter_by(id=id).first()
            product.cod = update_product['cod']
            product.desc = update_product['desct']
            product.preco = update_product['preco']
            product.quant = update_product['quant']
            db.session.commit()
        except OperationalError:
            flash(f'Ocorreu algum erro ao atualizar o produto de id {id}.')
            db.session.close()
            return jsonify(ok=False)
        else:
            flash(f'produto de id {id} foi atualizado com sucesso!')
        finally:
            db.session.close()
            return jsonify(ok=True, url=url_for('stock.get_product', id=id))

    product = Product.query.filter_by(id=id).first()
    return render_template('stock/product/edit_product.html', product=product)


@stock_route.route('produto/desativar/', defaults={'id':None}, methods=['PUT'])
@stock_route.route('produto/desativar/<id>')
@login_required
def deactivate_product(id):
    if not id:
        id = request.args.get('id')

    try:
        # acessando produto
        product = Product.query.filter_by(id=id).first()
    except OperationalError:
        flash(f'Ocorreu um erro ao acessar o produto de id {id}. Reportar erro ao desenvolvedor do sistema!')
    else:
        # desativando produto
        product.active = False
        try:
            db.session.commit()
        except OperationalError:
            flash(f'ocorreu um erro ao desativar o produto {product.desc[:21]}. Reportar erro ao desenvolvedor do sistema!')
        else:
            flash(f'Produto "{product.desc[:21]}" foi desativado com sucesso!')
    finally:
        db.session.close()

    return redirect(url_for('stock.get_product', id=id))


@stock_route.route('produto/ativar/', defaults={'id':None})
@stock_route.route('produto/ativar/<id>')
@login_required
def activate_product(id):
    if not id:
        id = request.args.get('id')

    try:
        # acessando produto
        product = Product.query.filter_by(id=id).first()
    except OperationalError:
        flash(f'Ocorreu um erro ao acessar o produto de id {id}. Reportar erro ao desenvolvedor do sistema!')
    else:
        # desativando produto
        product.active = True
        try:
            db.session.commit()
        except OperationalError:
            flash(f'ocorreu um erro ao desativar o produto {product.desc[:21]}. Reportar erro ao desenvolvedor do sistema!')
        else:
            flash(f'Produto "{product.desc[:21]}" foi desativado com sucesso!')
    finally:
        db.session.close()

    return redirect(url_for('stock.get_product', id=id))


@stock_route.route('/categorias')
@login_required
def categorias():
    try:
        categorias = ProductCategory.query.filter_by(user_id=current_user.id).all()
    except:
        flash("Ocorreu um erro ao acessar as categorias de produtos!")
        return redirect(url_for('stock.home'))
    
    return render_template('stock/category/categorias.html', categorias=categorias)


@stock_route.route('/categoria', defaults={'id': None})
@stock_route.route('/categoria/<id>')
def get_categoria(id):
    
    return


@stock_route.route('/nova-categoria', methods=['GET', 'POST'])
@login_required
def new_category():
    if request.method == 'POST':
        new_cat = ProductCategory(request.form['cat'], current_user.id)
        try:
            db.session.add(new_cat)
            db.session.commit()
        except OperationalError:
            flash(f"Ocorreu um erro ao cadastrar a categoria {new_cat.name}")
            return redirect(url_for('stock.new_category'))
        
        flash(f'Categoria {new_cat.name} registrada com sucesso!')
        db.session.close()
        return redirect(url_for("stock.new_category"))
    return render_template('stock/category/new-category.html')


@stock_route.route('/exportar')
def export():
    # retorna ao usuario um arquivo contendo as informações do estoque  
    return
