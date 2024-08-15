from blog import db
from sqlalchemy import Enum
from enum import Enum as Eman1
from sqlalchemy.sql import func

class CATEGORY(Eman1):
    Fiction = "fiction" # كتب خيالي
    Adventure = "adventure" # كتب مغامرة
    History = "history" # كتب تاريخ
    Psychology = "psychology" # كتب علم نفس
    Romance = "romance" # كتب رومانسية
    Fantasy = "fantasy" # كتب فنتازيا
    Mystery = "mystery" # كتب غموض
    Thriller = "thriller" # كتب الاثارة
    Physiognomy = "physiognomy" # كتب علم الفراسة
    Finance = "finance" # كتب المال
    
#جدول
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    include_date = db.Column(db.DateTime(timezone = True), server_default=func.now())
    book_cover = db.Column(db.String(255), nullable=False, default="default.png")
    # نوع الكتاب
    category = db.Column(Enum(CATEGORY), nullable=False)
    # السعر
    price = db.Column(db.Integer, nullable=False)
    # المؤلف
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripe_id = db.Column(db.String(20), nullable=False)

    book_name = db.Column(db.String(255), nullable=False)
    # تحل محل السترنج
    def __repr__(self):
        return f"Book( title => '{self.title}')" 


class AudioBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    include_date = db.Column(db.DateTime(timezone = True), server_default=func.now())
    book_cover = db.Column(db.String(255), nullable=False, default="default.png")
    audio_name = db.Column(db.String(255), nullable=False)
    category = db.Column(Enum(CATEGORY), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripe_id = db.Column(db.String(20), nullable=False)


    # تحل محل السترنج
    def __repr__(self):
        return f"AudioBook(title => '{self.title}')" 