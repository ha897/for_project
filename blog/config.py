from dotenv import load_dotenv
import os
from pathlib import Path
import os
load_dotenv()
class DevelopmantCfg:
    DEBUG = True
    APP_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

    TEMPLATE_DIR="templates"
    STATIC_DIR="static"
    IMAGE_DIR=APP_DIR/Path("static")/Path("image")
    FILES_DIR=APP_DIR/Path("static")/Path("files")
    LOGIN_MSG = "يجب تسجيل الدخول"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@localhost/{os.getenv("DATABASE_NAME")}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    OWNER_USERNAME=os.getenv("OWNER_USERNAME")
    OWNER_EMAIL=os.getenv("OWNER_EMAIL")
    OWNER_PASSWORD=os.getenv("OWNER_PASSWORD")
    
    ITEMS_PER_PAGE = 6
    ITEMS_HOME_PAGE = 4
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    ALLOW_EXTENTION_IMG = ['jpg', 'png']
    ALLOW_EXTENTION_SOUND = ['mp3']
    
    BOOKS_CATEGORYS = [("Fiction", "fiction") ,("Adventure", "adventure") ,("History", "history") ,("Psychology", "psychology"),("Romance", "romance") ,("Fantasy", "fantasy") ,("Mystery", "mystery") ,("Thriller", "thriller") ,("Physiognomy", "physiognomy") ,("Finance", "finance")]
    # mail
    MAIL_SERVER='sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    RESET_MAIL = os.getenv("RESET_MAIL")
    # """seeder"""
    # user
    FAKER_USER_PASSWORD = os.getenv("FAKER_USER_PASSWORD")
    ADMIN_PERCENTAGE = 20
    # article
    ACCOUNT_COUNT = 30
    ARTICLE_COUNT = 30
    # book
    BOOK_COUNT = 30
    BOOK_PAGES = (1,140)
    BOOK_PRICE = (32,210)
    # defolt book in static/files/book/default.pdf
    DEFAULT_BOOK_NAME = "default.pdf"
    # audio
    AUDIO_BOOK_COUNT = 30
    # defolt audio in static/files/audio/default.mp3
    DEFAULT_AUDIO_NAME = "default.mp3"
    AUDIO_BOOK_PRICE = (32,210)
    AUDIO_BOOK_HOUERS = (1,3)
    AUDIO_BOOK_MINUTES = (12,43)
    
    # STRIPE_PUBLISHABLE_KEY = "pk_test_51PPSziDmKD9C7pTkil8nrKMbSNgpJjzA6xPfNzzsWskADEnF5lIgDsFuRdoL111RZgLDVcxG0rh1osu1joU7LySj00SjhB18MQ"
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET")
    ALLOW_EXTENTION_BOOK = ["pdf"]