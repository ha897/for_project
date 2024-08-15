from blog import db
from sqlalchemy.dialects.postgresql import ARRAY

class Busket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, unique=True, nullable=False) 
    # اريي به الايدي لكل الكتب الموضوعة بالسلة
    books_id = db.Column(ARRAY(db.Integer), unique=True) 
    audio_books_id = db.Column(ARRAY(db.Integer), unique=True)