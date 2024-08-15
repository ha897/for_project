from flask import Flask, render_template
from blog.config import DevelopmantCfg
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_seeder import FlaskSeeder


cfg = DevelopmantCfg
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
mail = Mail()
seeder = FlaskSeeder()

# تخصيص تسجيل الدخول
# ارسال المستخدم الغير مصادق عليه لصفحة تسجيل الدخول
login_manager.login_view = "user_controller.user_login"
# رساله تضهر لمستخدم مجهول عند محاولة دخول صفحة محمية
login_manager.login_message = cfg.LOGIN_MSG
# نوع رسائل فللش الافتراضية
login_manager.login_message_category = "warning" #  تحزيرية تاخت تنسيقات التحذيرية مثل اللون الاحمر الخ


def create_app():
    app = Flask(__name__, template_folder=cfg.TEMPLATE_DIR, static_folder=cfg.STATIC_DIR)
    app.config.from_object(cfg)
    

            
    with app.app_context():
        regester_extention(app)
        regester_blueprint(app)
        with app.app_context():
            populate_database()
        # before_first_request is deprecated since version 2.2 and removed in Flask 2.3
        # app.before_first_request(populate_database)
        register_errorhandlers(app)

    return app

def regester_extention(app):
        bcrypt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        ckeditor.init_app(app)
        mail.init_app(app)
        seeder.init_app(app, db)

        
def regester_blueprint(app):
    from .routes.ArticleRoute import article_bp
    from .routes.UserRoute import login_bp
    from .routes.MainRoute import main_bp
    from .routes.BookRoute import book_bp
    from .routes.AiRoute import gbt_bp
    from .routes.BusketRoute import busket_bp
    from .routes.StripeRoute import stripe_bp

    app.register_blueprint(article_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(gbt_bp)
    app.register_blueprint(busket_bp)
    app.register_blueprint(stripe_bp)
    
from blog.models.ArticalModel import Article
from blog.models.UserModel import User
from blog.models.BookModel import Book
from blog.models.BookModel import AudioBook
from blog.models.BusketModel import Busket


# داله ملئ قاعدة البيانات
def populate_database():
    # التاكد من وجود الجداول اذا موجودة زين اذا لا انشاها
    # db.create_all()
    
    if not User.query.filter_by(username=cfg.OWNER_USERNAME).first():
        owner = User(
            username=cfg.OWNER_USERNAME, 
            email=cfg.OWNER_EMAIL, 
            password=bcrypt.generate_password_hash(
                cfg.OWNER_PASSWORD).decode("UTF-8"), 
            is_admin=True)
        db.session.add(owner)
        db.session.commit()

# ملفات الاخطاء
def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, "code", 404)
    # اسم الملف 404
        return render_template(f"errors/{error_code}.jinja", error_code= error_code,
                title="غير متوفر")
    for errcode in [404]:
            app.errorhandler(errcode)(render_error)
            