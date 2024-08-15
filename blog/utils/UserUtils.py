from flask_mail import Message
from flask import url_for
from blog import cfg, mail
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender=cfg.RESET_MAIL, recipients=[user.email])
    msg.body = f'''{url_for("user_controller.reset_password", token=token, _external=True)}
    لاستعادة كلمة المرور اضغط الرابط التالي:'''
    mail.send(msg)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(f'''{url_for("user_controller.reset_password", token=token, _external=True)}
    لاستعادة كلمة المرور اضغط الرابط التالي:''')
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")