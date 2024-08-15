from faker import Faker
from flask_seeder import Seeder
from blog import bcrypt, db, cfg
from blog.models.UserModel import User
from blog.models.ArticalModel import Article
from blog.models.BookModel import Book, CATEGORY
from blog.models.BookModel import AudioBook
import random
from datetime import timedelta
from blog.utils.BookUtils import create_stripe_product
fake = Faker("ar_AA")

class SeedDb(Seeder):
        
    def add_user(self):
        # لاعطاء معلومات وهمية fake.unique.first_name()
        # cfg.ACCOUNT_COUNT عدد المستخدمين من الاعدادات
        names = [fake.unique.first_name() + " " + fake.unique. last_name() for _ in range(cfg.ACCOUNT_COUNT)]
        emails = [fake.unique. email() for _ in range(cfg.ACCOUNT_COUNT)]
        for name, email in zip(names, emails):
            user = User(
                username = name,
                email = email,
                password = bcrypt.generate_password_hash(cfg.FAKER_USER_PASSWORD).decode('utf-8'),
                is_admin = fake.boolean(chance_of_getting_true = cfg.ADMIN_PERCENTAGE),# نسبة الادمن
                # يفضل الغائ هذه الخانة لكي لا ترسل رسائل لتلك الاليميلات وستعين القيمة فولس يعني كلهم غير مشتركين
                # is_subscribe = fake.boolean(chance_of_getting_true = cfg.ADMIN_PERCENTAGE),# نسبة المشتركين
                join_date = fake.date_this_year()
            )
            print(user)
            db.session.add(user)
            db.session.commit()
            
    def add_article(self):
        titles = [fake.sentence(nb_words=7) for _ in range(cfg.ARTICLE_COUNT)]
        contents = [fake.paragraph(nb_sentences=110) for _ in range(cfg.ARTICLE_COUNT)]
        for title, content in zip(titles, contents):
            article = Article(
                title = title,
                content = content,
                created_date = fake.date_this_year(),
                author_id = random.choice(User.query.filter_by(is_admin=True).all()).id
            )
            print(article)
            db.session.add(article)
            db.session.commit()
    
    def add_book(self):
        titles = [fake.sentence(nb_words=7) for _ in range(cfg.BOOK_COUNT)]
        descriptions = [fake.paragraph(nb_sentences=110) for _ in range(cfg.BOOK_COUNT)]
        for title, description in zip(titles, descriptions):
            price = random.randint(*cfg.BOOK_PRICE)
            # """""""" stripe """"""""""
            # إنشاء منتج
            
            stripe_product_id = create_stripe_product(title, description, price, CATEGORY.Fiction)
            # لانشاء قيم افتراضية استخدم
            # stripe_product_id = "prod_#############"
            
            book = Book(
                title = title,
                description = description,
                pages = random.randint(*cfg.BOOK_PAGES),
                price = price,
                category = random.choice(cfg.BOOKS_CATEGORYS)[0],
                include_date = fake.date_this_year(),
                book_name = cfg.DEFAULT_BOOK_NAME,
                author_id = random.choice(User.query.filter_by(is_admin=True).all()).id,
                stripe_id = stripe_product_id
            )

            
            print(book)
            db.session.add(book)
            db.session.commit()
                # duration = timedelta(hours=random.randint(cfg.BOOK_COUNT), minutes=),
    def add_audio_book(self):
        titles = [fake.sentence(nb_words=7) for _ in range(cfg.AUDIO_BOOK_COUNT)]
        descriptions = [fake.paragraph(nb_sentences=110) for _ in range(cfg.AUDIO_BOOK_COUNT)]
        for title, description in zip(titles, descriptions):
            price = random.randint(*cfg.BOOK_PRICE)
            # """""""" stripe """"""""""
            # إنشاء منتج
            stripe_product_id = create_stripe_product(title, description, price)
            
            book = AudioBook(
                title = title,
                description = description,
                duration = timedelta(hours=random.randint(*cfg.AUDIO_BOOK_HOUERS), minutes=random.randint(*cfg.AUDIO_BOOK_MINUTES)),
                include_date = fake.date_this_year(),
                audio_name = cfg.DEFAULT_AUDIO_NAME,
                category = random.choice(cfg.BOOKS_CATEGORYS)[0],
                price = random.randint(*cfg.AUDIO_BOOK_PRICE),
                author_id = random.choice(User.query.filter_by(is_admin=True).all()).id,
                stripe_id = stripe_product_id
            )
            print(book)
            db.session.add(book)
            db.session.commit()
    def run(self):
        self.add_user()
        self.add_article()
        self.add_book()
        self.add_audio_book()