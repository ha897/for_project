from flask import render_template, flash, redirect, url_for, abort, request
from blog.models.BookModel import Book, AudioBook
from blog import cfg, db
from blog.utils.SearshUtils import get_pagination
from blog.forms.BookForm import AddBook, AddAudioBook
from flask_login import current_user, login_required
from datetime import timedelta
from blog.utils.BookUtils import create_stripe_product, update_stripe_product
from blog.utils.BookUtils import create_file, create_image, delete_image, delete_file

import os
class BookController:
    def books():
        books = Book.query.all()
        start, end, pagination = get_pagination(books)
        return render_template("items.jinja",title="الكتب", books=books[start:end], pagination=pagination)
    
    def audioBooks():
        books = AudioBook.query.all()
        start, end, pagination = get_pagination(books)
        return render_template("items.jinja",title="الكتب", audioBooks=books[start:end], pagination=pagination)
    
    @login_required
    def book(id):
        book = Book.query.get(id)
        return render_template("book.jinja", title=book.title, book=book)
    
    @login_required
    def audioBook(id):
        audio_book = AudioBook.query.get(id)
        return render_template("book.jinja", title=audio_book.title, audio_book=audio_book)
    
    @login_required
    def add_book():
        if current_user.is_admin:
            form = AddBook()
            if form.validate_on_submit():
                book_cover = form.book_cover.data 
                book_file = form.book_file.data
                
                # static/files/book/file
                book_random_name = create_file(book_file, cfg.ALLOW_EXTENTION_BOOK, "book")
                # static/image/book/file
                img_random_name = create_image(book_cover, cfg.ALLOW_EXTENTION_IMG, "book")
                if book_random_name == None:
                    flash("الملف غير صحيح","warning")
                    return render_template("admin/add_book.jinja", title="اضافة كتاب", form=form)
                if img_random_name == None:
                    flash("امتداد الصورة غير صحيح","warning")
                    return render_template("admin/add_book.jinja", title="اضافة كتاب", form=form)
                
                
                title = form.title.data
                description = form.description.data
                price = form.price.data
                category = form.category.data
                stripe_product_id = create_stripe_product(title, description, price, category)
                new_book = Book(title=title ,
                                description=description ,
                                pages=form.pages.data ,
                                book_cover=img_random_name ,
                                category=category ,
                                price=price ,
                                author_id=current_user.id,
                                book_name = book_random_name ,
                                stripe_id = stripe_product_id)
                db.session.add(new_book)
                db.session.commit()
                
                flash("تم اضافة الكتاب بنجاح", "success")
                return redirect(url_for('user_controller.user_profile'))
            
            # الميثود بوست معناها ان البيانات ارسلت لكن الفورم قال انها خاطئة
            elif request.method == "POST":
                flash("هناك خطا بالمدخلات حاول مرة اخرى", "error")                   
            return render_template("admin/add_book.jinja", title="اضافة كتاب", form=form)
        # عند محاولة مستخدم الوصول لصفحة وهو ليس "ادمين" يضهر 404
        abort(404)
        
    @login_required
    def add_audio_book():
        if current_user.is_admin:
            form = AddAudioBook()
            if form.validate_on_submit():
                book_cover = form.book_cover.data
                audio_file = form.audio_file.data
                # static/files/audio/file
                audio_random_name = create_file(audio_file, cfg.ALLOW_EXTENTION_SOUND, "audio")

                # static/image/audio/file
                img_random_name = create_image(book_cover, cfg.ALLOW_EXTENTION_IMG, "audio")
                if audio_random_name == None:
                    flash("امتداد الملف غير صحيح","warning")
                    return render_template("admin/add_audio_book.jinja", title="اضافة كتاب", form=form)
                if img_random_name == None:
                    flash("امتداد الصورة غير صحيح","warning")
                    return render_template("admin/add_audio_book.jinja", title="اضافة كتاب", form=form)
                

                    
                    
                title = form.title.data
                description = form.description.data
                price = form.price.data
                category = form.category.data
                stripe_product_id = create_stripe_product(title, description, price, category)
                new_book = AudioBook(title=title,
                                     description=description,
                                     book_cover=img_random_name,
                                     audio_name=audio_random_name,
                                     category=category,
                                     duration = timedelta(hours=form.duration_hours.data, minutes=form.duration_minuts.data),
                                     price=price,
                                     author_id=current_user.id,
                                     stripe_id = stripe_product_id
                                     
                                     )
                db.session.add(new_book)
                db.session.commit()
                flash("تم اضافة الكتاب بنجاح", "success")
                return redirect(url_for('user_controller.user_profile'))
            
            # الميثود بوست معناها ان البيانات ارسلت لكن الفورم قال انها خاطئة
            elif request.method == "POST":
                flash("هناك خطا بالمدخلات حاول مرة اخرى", "error")                   
            return render_template("admin/add_audio_book.jinja", title="اضافة كتاب", form=form)
        # عند محاولة مستخدم الوصول لصفحة وهو ليس "ادمين" يضهر 404
        abort(404)
        
    def delete_book():
        # اذا كان ادمن احذف واذا لا اضهر خطا
        if current_user.is_admin:
            try:
                book_id = request.form["book_id"]
            except:
                try:
                    audio_book_id = request.form["audio_book_id"]
                except:
                    pass
                else:
                    audio_book = Book.query.get(audio_book_id)
                    if audio_book.book_cover != "default.png":
                        try:
                            os.remove(str(cfg.IMAGE_DIR/"audio"/audio_book.book_cover))
                        except:
                            pass
                    if audio_book.book_cover != "default.pdf":
                        try:
                            os.remove(str(cfg.FILES_DIR/"audio"/audio_book.book_name))
                        except:
                            pass
                    db.session.delete(book)
                    db.session.commit()
                    flash("تم حذف الكتاب الصوتي بنجاح", "success")
            else:
                book = Book.query.get(book_id)
                if book.book_cover != "default.png":
                    try:
                        os.remove(str(cfg.IMAGE_DIR/"book"/book.book_cover))
                    except:
                        pass
                if book.book_name != "default.pdf":
                    try:
                        os.remove(str(cfg.FILES_DIR/"book"/book.book_name))
                    except:
                        pass
                db.session.delete(book)
                db.session.commit()
                flash("تم حذف الكتاب بنجاح", "success")
            return redirect(url_for("main_controller.home"))
        abort(404)
    def update_book(book_id):
        if current_user.is_admin:
            form = AddBook()
            if form.validate_on_submit():
                print("###########################################################################")
                # book = Book.query.get(book_id)
                new_book = Book.query.get(book_id)

                book_cover = form.book_cover.data
                book_file = form.book_file.data

                if book_file != None:
                    # static/files/book/file
                    book_random_name = create_file(book_file, cfg.ALLOW_EXTENTION_BOOK, "book")
                else:
                    book_random_name = new_book.book_name

                if book_cover  != None:
                    # static/image/book/file
                    img_random_name = create_image(book_cover, cfg.ALLOW_EXTENTION_IMG, "book")
                else:
                    img_random_name = new_book.book_cover
                
                if book_random_name == None:
                    flash("الملف غير صحيح لم يعدل الملف","warning")
                else:
                    delete_file(book_file, "book", new_book.book_name)
                    new_book.book_name  = book_random_name
                    
                if img_random_name == None:
                    flash("امتداد الصورة غير صحيح لم تعدل الصورة","warning")
                else:
                    delete_image(book_cover, "book", new_book.book_cover)
                    new_book.book_cover = img_random_name
                    

                title = form.title.data
                description = form.description.data
                price = int(form.price.data)
                category = form.category.data

                new_book.title = title
                new_book.description = description
                new_book.pages = form.pages.data
                new_book.category = category
                new_book.price = price
                new_book.author_id = current_user.id
                db.session.commit()

                update_stripe_product(new_book.stripe_id, title, description, price, category)

                flash("تم تعديل الكتاب بنجاح", "success")
                return redirect(url_for("main_controller.home"))
                

            values = Book.query.get(book_id)

            return render_template("admin/update_book.jinja", title="تعديل كتاب", form=form, values=values)
    
    def update_audio_book(book_id):
        if current_user.is_admin:
            form = AddAudioBook()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if form.validate_on_submit():
                print("###########################################################################")
                # book = Book.query.get(book_id)
                new_book = AudioBook.query.get(book_id)

                book_cover = form.book_cover.data
                audio_file = form.audio_file.data

                if audio_file != None:
                    # static/files/book/file
                    book_random_name = create_file(audio_file, cfg.ALLOW_EXTENTION_SOUND, "audio")
                else:
                    book_random_name = new_book.audio_name

                if book_cover  != None:
                    # static/image/book/file
                    img_random_name = create_image(book_cover, cfg.ALLOW_EXTENTION_IMG, "audio")
                else:
                    img_random_name = new_book.book_cover
                
                if book_random_name == None:
                    flash("الملف غير صحيح لم تعدل الصورة","warning")
                else:
                    delete_file(audio_file, "audio", new_book.audio_name)
                    new_book.audio_name  = book_random_name
                    
                    
                if img_random_name == None:
                    flash("امتداد الصورة غير صحيح لم تعدل الصورة","warning")
                else:
                    delete_image(book_cover, "audio", new_book.book_cover)
                    new_book.book_cover = img_random_name

                title = form.title.data
                description = form.description.data
                price = int(form.price.data)
                category = form.category.data


                new_book.title = title
                new_book.description = description
                new_book.duration = timedelta(hours=form.duration_hours.data, minutes=form.duration_minuts.data)
                new_book.category = category
                new_book.price = price
                new_book.author_id = current_user.id
                db.session.commit()
                
                update_stripe_product(new_book.stripe_id, title, description, price, category)
                
                flash("تم تعديل الكتاب بنجاح", "success")
                return redirect(url_for("main_controller.home"))
                

            values = AudioBook.query.get(book_id)
            total_seconds = values.duration.total_seconds()
            
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return render_template("admin/update_audio_book.jinja", title="تعديل كتاب", form=form, values=values,hours=hours,minutes=minutes)
