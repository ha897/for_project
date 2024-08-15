from flask_wtf import FlaskForm
from wtforms. validators import DataRequired, Length
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from blog import cfg

class AddArticle(FlaskForm):
    title = StringField("عنوان المقاله", validators=[DataRequired(), Length(min=5, max=255)])
    content = CKEditorField("محتوى المقاله", validators=[DataRequired(), Length(min=20, max=10000)])
    article_img = FileField("صورة المقالة", validators=[FileAllowed(cfg.ALLOW_EXTENTION_IMG)])
    # author_id يضاف بالباك اند
    submit = SubmitField("اضف المقاله")