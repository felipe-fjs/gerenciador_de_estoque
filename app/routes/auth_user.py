from app import login_manager, bcrypt, db, app
from app.models.user import User, SignupForm
from app.decoratos.user_auth import reset_token_required
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from smtplib import SMTPException
from flask_login import current_user, login_user, logout_user, login_required
from flask_mailman import EmailMessage
from sqlalchemy.exc import OperationalError
import sqlalchemy.exc as exc
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import datetime
from CONFIG import SALT_FOR_TOKEN_2

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
            new_user = User(request.form['name'],
                            request.form['email'],
                            request.form['pwd'])
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

                    message = EmailMessage(subject=subject, 
                                           body=body, 
                                           from_email=app.config['MAIL_USERNAME'], 
                                           to=[new_user.email])
                    message.send()
                    
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


@app.route('/')
@app.route('/login')
@user_route.route('/')
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
            login_user(user, remember=True)
            return redirect(url_for('stock.home'))
        
        flash('Senha incorreta!')

    return render_template('auth/login.html')


@user_route.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso!')
    return redirect(url_for('user.login'))


@user_route.route('/redefinir-senha/', methods=['GET', 'POST'])
def reset_pwd():
    if request.method == 'POST':
        print('GERAR TOKEN')
        # GERAR O LINK COM TOKEN PARA REDEFINIR SENHA
        if not User.query.filter_by(email=request.form['email']).first():
            flash('Email não cadastrado!')
            return redirect(url_for('user.reset_pwd'))

        user = User.query.filter_by(email=request.form['email']).first()
        payload = {
            'allow_reset': True,
            'id': user.id,
            'email': user.email,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
        }
        
        code = jwt.encode(payload, SALT_FOR_TOKEN_2, algorithm='HS256')

        link = url_for('user.new_pwd', token=code, _external=True, _method='GET')
        subject = f'Link para redefinição de senha de {user.name}!'
        body = f'Olá, {user.name}! O link a seguir é para a redefinição de senha solicitada para a sua conta no Gerenciador De Estoque e tem um duração de 60 MINUTOS! <br> {link}'
        message = EmailMessage(subject=subject, body=body, from_email=app.config['MAIL_USERNAME'], to=[user.email])
        try:
            message.send()
        except SMTPException as e:
            flash(f'ocorreu um erro ao enviar o email com o link!<br>erro: {e}')
        else:
            flash(f'Email enviado com sucesso!')
        finally:
            return redirect(url_for('user.reset_pwd'))
        
    # if request.args.get("token"):  
    #     token = request.args.get("token")
    #     # FAZ DECODE DO TOKEN E redirect para rota de nova_senha
    #     print("REDIRECT PARA NOVA_SENHA")
    #     try:
    #         decode = jwt.decode(token, SALT_FOR_TOKEN_1, algorithms='HS256')
    #     except ExpiredSignatureError:
    #         flash("Seu Token para nova senha EXPIROU!")
    #         return redirect(url_for('user.reset_pwd'))
    #     except InvalidSignatureError:
    #         flash('Seu Token está CORROMPIDO!')
    #         return redirect(url_for('user.reset_pwd'))
    #     # Entendo que não é necessário verificar existência de cadastro
    #     # pois para haver link para redefinição deve haver um cadastro antes        
    #     user = User.query.filter_by(id=decode['id']).first()
    #     payload = {
    #         'allow_reset': True,
    #         'id': user.id,
    #         'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1)
    #     }
    #     token = jwt.encode(payload, SALT_FOR_TOKEN_2, algorithm='HS256')
    #     session['token_for_reset'] = token
    #     return redirect(url_for('user.new_pwd'))
    # print('não entrou em nada')       
    return render_template('auth/reset_pwd.html')


@user_route.route('/nova-senha/', defaults={'token': None}, methods=['POST'])
@user_route.route('/nova-senha/<token>', methods=['GET'])
def new_pwd(token):
    if request.method == 'POST':
        user_info = jwt.decode(session['token'], SALT_FOR_TOKEN_2, algorithms='HS256')
        new_pwd = request.form['pwd']
        try:
            user = User.query.filter_by(email=user_info['email']).first()
            user.pwd = bcrypt.generate_password_hash(new_pwd)
            db.session.commit()
        except OperationalError:
            flash('ocorreu um erro ao salvar sua nova senha... tente novamente.')
            db.session.close()
            return redirect(url_for('user.new_pwd'))
        else:
            session.pop('token')

        return redirect(url_for('user.login'))

    try:
        decode = jwt.decode(token, SALT_FOR_TOKEN_2, algorithms='HS256')

    except ExpiredSignatureError:
        flash('Seu token expirou!')
        return redirect(url_for('user.login'))
    
    except InvalidSignatureError:
        flash('Seu Token está CORROMPIDO!')
        return redirect(url_for('user.login'))
    
    if not User.query.filter_by(email=decode['email']):
        flash('O Email deste token não foi encontrado no banco de dados!')
        return redirect(url_for('user.login'))

    session['token'] = token

    return render_template('auth/new_pwd.html')
