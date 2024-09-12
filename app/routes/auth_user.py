from app import login_manager, bcrypt, db, app, mail
from app.models.user import User, SignupForm
from flask import Blueprint, request, render_template, redirect, url_for, flash
from smtplib import SMTPException
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import OperationalError
import sqlalchemy.exc as exc
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import datetime

user_route = Blueprint('user', __name__)


@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


@app.route('/')
@app.route('/login')
def redirect_login():
    if current_user.is_authenticated:
        return redirect(url_for('stock.home'))
    return redirect(url_for('user.login'))


@user_route.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('stock.home'))
    
    form = SignupForm()
    if request.method == 'POST':
        if not User.query.filter_by(email=request.form['email']).first():
            pwd = bcrypt.generate_password_hash(request.form['pwd'])
            new_user = User(request.form['name'],
                            request.form['email'],
                            pwd)
            try:
                # realiza a tentativa de cadastrar o usuário
                db.session.add(new_user)
                db.session.commit()
            except OperationalError as e:
                link = "https://github.com/felipe-fjs"
                error = f'''ocorreu algum erro no seu cadastro.... {e}.
                Tente novamente, se o erro persistir entre em contato com o <a href='{link}' target='_blank'>desenvolvedor</a> para corrigir o erro'''
                flash(error)
            else:
                flash(f'Usuário "{new_user.name}" cadastrado com sucesso!')
                try:
                    # Realiza envio de e-mail para confirmação do email
                    token = jwt.encode(
                                        payload={
                                            'email':new_user.email, 
                                            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=15)
                                            },
                                        key=app.config['SECRET_KEY'],
                                        algorithm='HS256')
                    subject = 'Link para confirmação do seu Email!'
                    link = url_for('user.confirmation', token=token, _external=True)
                    body = (f'Olá {new_user.name}, logo abaixo estará o link para a confirmação do seu email, clique '
                            f'ou copie e cole-o em seu navegador para acessá-lo\n {link}')

                    mail.send_mail(subject=subject, message=body, from_email=app.config['MAIL_USERNAME'],
                                   recipient_list=[new_user.email], auth_user=app.config['MAIL_USERNAME'],
                                   auth_password=app.config['MAIL_PASSWORD'])
                    
                except SMTPException as e:
                    flash(f'Ocorreu algum erro ao enviar o email para confirmação: {e}.'
                          '</br>Faça login para solicitar um novo link!')

                return redirect(url_for('user.login'))
            finally:
                db.session.close()

            return redirect(url_for('user.signup'))
        
        flash("Email já cadastrado!")
        return redirect(url_for('user.signup'))
        
    return render_template('auth/signup.html', form=form)


@user_route.route('/email-confirmation/<token>')
def confirmation(token):
    try:
        decode = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

    except ExpiredSignatureError as e:
        message = f"""Token Expirado! ERROR: {e}
Faça login novamente para solicitar um nove token de autenticação!"""
        return message
    except InvalidSignatureError as e:
        message = f"""Token Corronpido! ERROR: {e}
Faça login novamente para solicitar um nove token de autenticação!"""
        return message
    else:
            # Não foi testado se existia um cadastro, 
            # pois entendo que para haver o token deve haver um cadastro antes
            user = User.query.filter_by(email=decode['email']).first()
            user.email_confirmed = True
            try:
                db.session.commit()
            except OperationalError as e:
                link = "https://github.com/felipe-fjs"
                error = f"""Ocorreu algum erro ao confirmar seu email...
                Erro: {e}. 
                Faça login para gerar um nove e se persistir consulte o <a href="{link}" target="_blank">desenvolvedor</a> para informar erro!"""
                return error
            except exc as e:
                link = "https://github.com/felipe-fjs"
                error = f"""Ocorreu algum erro ao confirmar seu email...
                Erro: {e}. 
                Faça login para gerar um nove e se persistir consulte o <a href="{link}" target="_blank">desenvolvedor</a> para informar erro!"""
                return error
            else:

                return redirect(url_for('stock.home'))


@user_route.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('stock.home'))
    
    if request.method == 'POST':
        if not User.query.filter_by(email=request.form['email']).first():
            flash(f'Email não cadastrado!')
            return redirect(url_for('user.login'))

        user = User.query.filter_by(email=request.form['email']).first()
        if user.verify_pwd(request.form['pwd']):
            login_user(user)
            return redirect(url_for('stock.home'))
        
        flash('Senha incorreta!')

    return render_template('auth/login.html')


@user_route.route('/logout')
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso!')
    return redirect(url_for('user.login'))


@user_route.route('/redefinir-senha')
def reset_pwd():
    pass
