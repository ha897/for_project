from flask_login import current_user, login_required
from blog.models.BusketModel import Busket
from blog.models.BookModel import Book, AudioBook
from flask import request, flash, redirect, url_for, render_template
from blog import db, cfg
class BusketController:
    @login_required
    def add_to_busket():
    # تحقق مما إذا كان المستخدم لديه سلة بالفعل، إذا لم يكن لديه، قم بإنشائها
        busket = Busket.query.filter_by(user_id=current_user.id).first()
        if not busket:
            busket = Busket(user_id=current_user.id)
            db.session.add(busket)
            db.session.commit()

        # استرداد السلة المحدثة
        busket = Busket.query.filter_by(user_id=current_user.id).first()
        
        # محاولة استرداد book_id من النموذج
        try:
            book = int(request.form['book_id'])
        except:
            book = None
        
        if book is not None:
            if not busket.books_id:
                busket.books_id = [book]
            else:
                busket.books_id = [*busket.books_id, book]
    
            db.session.commit()
            flash("تم اضافة الكتاب للسلة", "success")
        
        # محاولة استرداد audio_book_id من النموذج
        try:
            audio_book = int(request.form['audio_book_id'])
        except:
            audio_book = None
        
        if audio_book is not None:
            if not busket.audio_books_id:
                busket.audio_books_id = [audio_book]
            else:
                busket.audio_books_id = [*busket.audio_books_id, audio_book]

            db.session.commit()
            flash("تم اضافة الكتاب الصوتي للسلة", "success")
        
        return redirect(url_for("busket_controller.busket"))

    @login_required
    def delete_from_busket():
        busket = Busket.query.filter_by(user_id=current_user.id).first()
        try:
            book_id = int(request.form['book_id'])
        except:
            book_id = None
            print("Error: book_id ")
        else:
            if book_id in busket.books_id:
                busket.books_id = filter(lambda x: x != book_id ,busket.books_id)
                db.session.commit()
                flash("تم الحذف بنجاح","success")
                
        try:
            audio_book_id = int(request.form['audio_book_id'])
        except:
            audio_book_id = None
            print("Error: audio_book ")
        else:
            print("#####################")
            print(audio_book_id)
            print(busket.audio_books_id)
            print(busket.books_id)
            print("#####################")
            
            if audio_book_id in busket.audio_books_id:
                busket.audio_books_id = filter(lambda x: x != audio_book_id ,list(busket.audio_books_id))
                db.session.commit()
                flash("تم الحذف بنجاح","success")
        return redirect(url_for('busket_controller.busket'))
    @login_required
    def busket():
        total_price = 0
        busket = Busket.query.filter_by(user_id=current_user.id).first()
        if busket.books_id:
            total_price += sum(map(lambda x :Book.query.get(x).price , busket.books_id))
            book_objects = map(lambda x: Book.query.get(x) ,busket.books_id)
        else:
            book_objects = None
            
        if busket.audio_books_id:
            total_price += sum(map(lambda x :AudioBook.query.get(x).price , busket.audio_books_id))
            audio_book_objects = map(lambda x: AudioBook.query.get(x) ,busket.audio_books_id)
        else:
            audio_book_objects = None
        return render_template("busket.jinja", title="سلة المشتريات", book_objects=book_objects, audio_book_objects=audio_book_objects, total_price=total_price)
    
    # صفحة الدفع
    def payment():
        stripe_publish_key = cfg.STRIPE_PUBLISHABLE_KEY
        return render_template("payment.jinja", title="صفحة الدفع", stripe_publish_key=stripe_publish_key)