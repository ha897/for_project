from blog import db, cfg
from blog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous.url_safe import URLSafeTimedSerializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




#جدول
# تخليعها ترث من يوزر ميكسن لمعرفة اذا كان مسجل ام لا سابقا (داله داخل المتحكم)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime(timezone = True), server_default=func.now())
    username = db.Column(db.String(100), unique=False, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_subscribe = db.Column(db.Boolean, nullable=False, default=False)
    # عند حذف المؤلف تحذف الكتب الخاصة به
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")
    articles = db.relationship('Article', backref='author', lazy=True, cascade="all, delete-orphan")

    # تحل محل السترنج
    def __repr__(self):
        return f"User('username => {self.username}'. 'email => {self.email}')" 
    
    # انشائ التوقيع الفريد لاستعادة كلمات المرور
    def get_reset_token(self):
        sign = URLSafeTimedSerializer(cfg.SECRET_KEY, salt="PasswordReset")
        return sign.dumps({"user_id":self.id})
    
    @staticmethod
    def verify_reset_token(token):
        sign = URLSafeTimedSerializer(cfg.SECRET_KEY, salt="PasswordReset")
        try:
            # المفتاح الذي يرسله المستخدم token
            # عمر المفتاح بالثانية max_age (المفتاح مفعل لساعة واحدة فقط)
            user_id = sign.loads(token, max_age=3600)["user_id"]
            # يضهر خطا عند انهائ المدة
        except:
            return None
        return User.query.get(user_id)
