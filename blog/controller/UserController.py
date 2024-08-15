from flask import render_template, redirect, url_for, flash, request, abort
from blog.forms.UserForm import Login, Register, ToResetPassword, ResetPassword, ProfileResetPassword
from flask_login import current_user, login_user, logout_user, login_required
from blog.models.UserModel import User
from blog.utils.UserUtils import send_reset_email
from blog import bcrypt, db, cfg
import random
class UserController:
    def user_login():
        if current_user.is_authenticated:
            flash("انت مسجل الدخول بالفعل", "info")
            return redirect(url_for('main_controller.home'))
        form = Login()   
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                
                login_user(user, remember=form.remember.data)
                flash("تم تسجيل الدخول بنجاح", "success")
                try:
                    return redirect(url_for(request.args.get("next")))
                except:
                    return redirect(url_for("main_controller.home"))
        elif request.method == "POST":
            flash("البيانات غير صحيحة", "danger")
        return render_template("user/login.jinja", title="تسجيل الدخول", form=form)
    def user_logout():
        logout_user()
        flash("تم تسجيل الخروج بنجاح", "success")
        return redirect(url_for('main_controller.home'))
    
    def user_regester():
        if current_user.is_authenticated:
            flash("انت مسجل الدخول بالفعل", "info")
            return redirect(url_for('main_controller.home'))
        
        form = Register()   
        if form.validate_on_submit():
            last_username = User.query.filter_by(username= form.username.data).first()
            last_email = User.query.filter_by(email= form.email.data).first()
            if last_email or last_email:
                if last_username:
                    flash("اسم المستخدم مسجل مسبقا حاول استخدام اسم مستخدم مختلف", "danger")
                if last_email:
                    flash("الايمل مسجل مسبقا حاول استخدام ايميل مختلف", "danger")
            else:
                
                user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode("UTF-8"))
                db.session.add(user)
                db.session.commit()
                flash("تم انشاء الحساب بنجاح", "success")

                if form.login.data == True:
                    login_user(user, remember=True)
                    flash("تم تسجيل الدخول بنجاح", "success")
                return redirect(url_for("main_controller.home"))
        elif request.method == "POST":
            flash("البيانات غير صحيحة", "danger")
        return render_template("user/register.jinja", title="انشاء حساب", form=form)
    
    @login_required
    def user_profile():
        return render_template("user/profile.jinja", title="الملف الشخصي")
    
    
    def to_reset_password():
        if  current_user.is_authenticated:
            flash("انت مسجل الدخول بالفعل", "info")
            return redirect(url_for('main_controller.home'))
        form = ToResetPassword()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user == None:
                flash("لا يوجد مستخدم بهذا الاليميل", "error")
                return render_template("user/reset_password.jinja", title="اعادة تعيين كلمة المرور", form=form)
            send_reset_email(user)
            flash("تم ارسال رابط تعيين كلمة المرور بنجاح", "success")
            return redirect(url_for('main_controller.home'))
            
        return render_template("user/reset_password.jinja", title="اعادة تعيين كلمة المرور", form=form)
    
    def reset_password(token):
        if  current_user.is_authenticated:
            flash("انت مسجل الدخول بالفعل", "info")
            return redirect(url_for('main_controller.home'))
        user = User.verify_reset_token(token)
        if user == None:
            flash("رابط اعادة تعيين كلمة المرور غير صحيح حاول مرة اخرى", "danger")
            return redirect(url_for('user_controller.to_reset_password'))

        resetForm = ResetPassword()
        if resetForm.validate_on_submit():
            password_hash = bcrypt.generate_password_hash(resetForm.password.data).decode("UTF-8")
            user.password = password_hash
            db.session.commit()
            flash("تم تعيين كلمة المرور", "success")
            return redirect(url_for('user_controller.user_login'))
        
        return render_template("user/reset_password.jinja", title="اعادة تعيين كلمة المرور", resetForm=resetForm)
    
    @login_required
    def profile_reset_password():
        profileResetForm = ProfileResetPassword()
        if profileResetForm.validate_on_submit():
            user = User.query.get(current_user.id)

            if user != None and bcrypt.check_password_hash(user.password, profileResetForm.old_password.data):
                user.password = bcrypt.generate_password_hash(profileResetForm.new_password.data).decode("UTF-8")
                db.session.commit()
                logout_user()
                flash("تم تغيير كلمة المرور بنجاح", "success")
                return redirect(url_for("user_controller.user_login"))
            else:
                flash("كلمة المرور غير صحيحة", "error")
        return render_template("user/reset_password.jinja", title="اعادة تعيين كلمة المرور", profileResetForm=profileResetForm)
    
    
    @login_required
    def subscriber():
        user = User.query.get_or_404(current_user.id)
        if user.is_subscribe:
            flash("تم الغاء الاشتراك بنجاح", "success")
        else:
            flash("تم الاشتراك بنجاح", "success")
        user.is_subscribe = not user.is_subscribe    
        db.session.commit()
        return redirect(url_for('user_controller.user_profile'))