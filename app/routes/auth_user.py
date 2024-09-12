from app import login_manager, bcrypt, db, app, mail
from app.models.user import User, SignupForm
from flask import Blueprint, request, render_template, redirect, url_for, flash
from smtplib import SMTPException
from flask_login import current_user
from sqlalchemy.exc import OperationalError
import sqlalchemy.exc as exc
import jwt
from jwt.exceptions import ExpiredSignatureError
import datetime

user_route = Blueprint('user', __name__)


@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


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
        message = 'Token Expirado!' +  f'ERROR: {e}'
    else:
        message = f'Token NÃO expirado {decode}'
        
        if User.query.filter_by(email=decode['email']).first():
            user = User.query.filter_by(email=decode['email']).first()
            user.email_confirmed = True
            try:
                db.session.commit()
            except OperationalError as e:
                link = "https://github.com/felipe-fjs"
                flash(f'Ocorreu algum erro ao confirmar seu email...</br>'
                      f'Erro: {e}. Consulte o <a href="{link}" target="_blank">desenvolvedor</a> para informar erro')
            except exc as e:
                link = "https://github.com/felipe-fjs"
                flash(f'Ocorreu algum erro ao confirmar seu email...</br>'
                      f'Erro: {e}. Consulte o <a href="{link}" target="_blank">desenvolvedor</a> para informar erro')
            else:

                return redirect(url_for('stock.home'))

    return f"<h1>{message}</h1>"


@user_route.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('stock.home'))
    
    return "<h1> Login page </h1>"


@user_route.route('/redefinir-senha')
def forget_pwd():
    pass
