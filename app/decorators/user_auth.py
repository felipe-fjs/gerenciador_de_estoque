from functools import wraps
from flask import session, redirect, url_for, flash, request
from CONFIG import SALT_FOR_TOKEN_2
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError


def reset_token_required(f):
    @wraps(f)
    def decored_function(*args, **kwargs):
        if not session.get('token_for_reset') or not request.args.get('token'):
            flash('Você precisa ter um token de nova-senha para acessar essa página!')
            return redirect(url_for('user.reset_pwd'))

        try:
            token = session['token_for_reset'] if session.get('token_for_reset') else request.args.get('token')
            decode = jwt.decode(token, SALT_FOR_TOKEN_2, algorithmds='HS256')

        except ExpiredSignatureError:
            flash(f'Seu link para redefinição de senha expirou!')
            return redirect(url_for('user.login'))
        except DecodeError:
            flash('Token inválido ou corrompido<br>Tenha certeza que copiou e colou corretamente!')
            return redirect(url_for('user.login'))
        except InvalidTokenError:
            flash('Token inválido!')
            return redirect(url_for('user.login'))
        
        else:
            if not decode['allow_reset']:
                flash('A redefinição de senha não foi permitida!')
                return redirect(url_for('user.login'))

        return f(*args, **kwargs)
    return decored_function

