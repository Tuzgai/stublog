from flask import render_template, current_app
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
    
def send_password_reset_email(user):
    token = user.get_reset_token()
    send_email('[Stublog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                        user=user, token=token))
    
def send_registration_invitation_email(user):
    token = user.get_reset_token(expires_in=86400)
    send_email('[Stublog] Registration Invitation',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/registration_invitation.txt', token=token),
               html_body=render_template('email/registration_invitation.txt', token=token))