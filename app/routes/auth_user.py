from app import login_manager, bcrypt, db
from app.models.user import User, SignupForm
from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError

user_route = Blueprint('user', __name__)


@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


@user_route.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if not User.query.filter_by(email=request.form['email']).first():
            pwd = bcrypt.generate_password_hash(request.form['pwd'])
            new_user = User(request.form['name'],
                            request.form['email'],
                            pwd)
            try:
                db.session.add(new_user)
                db.session.commit()
            except OperationalError as e:
                error = f'ocorreu algum erro no seu cadastro....\n{e}'
                flash(error)
            else:
                flash(f'Usuário "{new_user.name}" cadastrado com sucesso!')
                return redirect(url_for('user.login'))
            finally:
                db.session.close()

            return redirect(url_for('user.signup'))
        
        flash("Email já cadastrado!")
        return redirect(url_for('user.signup'))
        
    return render_template('auth/signup.html', form=form)


@user_route.route('/login')
def login():
    return "<h1> Login page </h1>"


@user_route.route('/redefinir-senha')
def forget_pwd():
    pass
