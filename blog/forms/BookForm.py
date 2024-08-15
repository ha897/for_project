from flask_wtf import FlaskForm
from wtforms. validators import DataRequired, Length
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from blog import cfg
class AddBook(FlaskForm):
    title = StringField("عنوان الكتاب", validators=[DataRequired(), Length(min=5, max=255)])
    description = TextAreaField("وصف الكتاب", validators=[DataRequired(), Length(min=20, max=10000)])
    pages = IntegerField("عدد الصفحات", validators=[DataRequired()])
    book_cover = FileField("غلاف الكتاب", validators=[FileAllowed(cfg.ALLOW_EXTENTION_IMG)])
    book_file = FileField("الكتاب", validators=[FileAllowed(cfg.ALLOW_EXTENTION_BOOK)])
    
    category = SelectField('تصنيف الكتاب', choices=cfg.BOOKS_CATEGORYS, validators=[DataRequired()])
    price = IntegerField("السعر", validators=[DataRequired()])
    submit = SubmitField("اضف الكتاب")
    
class AddAudioBook(FlaskForm):
    title = StringField("عنوان الكتاب", validators=[DataRequired(), Length(min=5, max=255)])
    description = TextAreaField("وصف الكتاب", validators=[DataRequired(), Length(min=20, max=10000)])
    book_cover = FileField("غلاف الكتاب", validators=[FileAllowed(cfg.ALLOW_EXTENTION_IMG)])
    audio_file = FileField("الملف الصوتي", validators=[FileAllowed(cfg.ALLOW_EXTENTION_SOUND)])
    category = SelectField('تصنيف الكتاب', choices=cfg.BOOKS_CATEGORYS, validators=[DataRequired()])
    price = IntegerField("السعر", validators=[DataRequired()])
    duration_hours = IntegerField('الساعات', validators=[DataRequired()])
    duration_minuts = IntegerField('الدقائق', validators=[DataRequired()])
    submit = SubmitField("اضف الكتاب")
