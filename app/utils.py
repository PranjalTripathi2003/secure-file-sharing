from itsdangerous import URLSafeTimedSerializer
from app import app, mail
from flask_mail import Message
from functools import wraps
from flask import request, jsonify
from flask_login import current_user

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def generate_confirmation_token(email):
    return s.dumps(email, salt='email-confirm')


def confirm_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='email-confirm', max_age=expiration)
    except:
        return False
    return email


def send_email(subject, recipient, html_body):
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    mail.send(msg)


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            email = s.loads(token, salt='token')
            current_user = User.query.filter_by(email=email).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)

    return decorated


def generate_download_token(file_id):
    return s.dumps(file_id, salt='file-download')
