from flask_mail import Message
from blog import cfg, mail
import mimetypes

def send_file_email(user, filenamepaths):
    token = user.get_reset_token()
    msg = Message("books", sender=cfg.RESET_MAIL, recipients=[user.email])
    msg.body = "التكتب التي اشتريتها من الموقع:"
    
    for filenamepath in filenamepaths:
        with open(filenamepath, 'rb') as file:
            filename = filenamepath.split("/")[-1]
            mime_type = mimetypes.guess_type(filename)[0]
            msg.attach(filename, mime_type, file.read())
    
    mail.send(msg)