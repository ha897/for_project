from flask_wtf import FlaskForm
from wtforms. validators import DataRequired, Length, Email, EqualTo
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from blog import cfg

class Login(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField("تسجيل الدخول")

class Register(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=5, max=255)])
    email = StringField("البريد الالكتروني",validators=[DataRequired(), Email(message="البريد الالكتروني غير صالح")])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    config_password = PasswordField("تاكيد كلمة السر", validators=[DataRequired(), EqualTo("password",message="كلمة المرور غير متطابقة")])
    login = BooleanField('سجل دخول؟')
    submit = SubmitField("انشائ حساب")

class ToResetPassword(FlaskForm):
    email = StringField("البريد الالكتروني",validators=[DataRequired(), Email(message="البريد الالكتروني غير صالح")])
    submit = SubmitField("استعادة كلمة المرور")
    
class ResetPassword(FlaskForm):
    password = PasswordField("كلمة السر الجديدة", validators=[DataRequired()])
    config_password = PasswordField("تاكيد كلمة السر", validators=[DataRequired(), EqualTo("password",message="كلمة المرور غير متطابقة")])
    submit = SubmitField("تغيير كلمة المرور")
class ProfileResetPassword(FlaskForm):
    old_password = PasswordField("كلمة السر", validators=[DataRequired()])
    new_password = PasswordField("كلمة السر الجديدة", validators=[DataRequired()])
    config_password = PasswordField("تاكيد كلمة السر", validators=[DataRequired(), EqualTo("new_password",message="كلمة المرور غير متطابقة")])
    submit = SubmitField("تغيير كلمة المرور")