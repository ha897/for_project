from blog import db
from sqlalchemy.sql import func
#جدول
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime(timezone = True), server_default=func.now())
    artical_img = db.Column(db.String(255), nullable=False, default="default.png")

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    # تحل محل السترنج
    def __repr__(self):
        return f"Articale(id => '{self.id}'. title => '{self.title}')" 