from flask import render_template, request, flash
from blog.models.ArticalModel import Article
from blog.models.BookModel import Book, AudioBook
from blog import cfg
from blog.utils.SearshUtils import get_pagination
# from sqlalchemy import in_
class MainController:
    def home():
        items_home = cfg.ITEMS_HOME_PAGE
        articles = Article.query.all()[:items_home]
        books = Book.query.all()[:items_home]
        audioBooks = AudioBook.query.all()[:items_home]
        return render_template("home.jinja", title="الصفحة الرئيسية", articles=articles, books=books, audioBooks=audioBooks)
    
    def searsh():
        if request.method == "POST":
            try:
                searsh_word = request.form["searsh"]
                
            except:
                return render_template("searsh.jinja", title="بحث")
            try:
                selected = request.form["selected"]
            except:
                # selected = "كتاب"
                books = Book.query.filter_by(title = searsh_word).all()
                start, end, pagination = get_pagination(books)
                return render_template("searsh.jinja", title="بحث", books=books[start:end], pagination=pagination)
            else:
                if selected == "مقاله":
                    articles = Article.query.filter_by(title = searsh_word).all()
                    start, end, pagination = get_pagination(articles)

                    return render_template("searsh.jinja", title="بحث", articles=articles[start:end], pagination=pagination)
                elif selected == "كتاب":
                    books = Book.query.filter_by(title = searsh_word).all()
                    start, end, pagination = get_pagination(books)
                    return render_template("searsh.jinja", title="بحث", books=books[start:end], pagination=pagination)
                
                elif selected == "كتاب صوتي":
                    audioBooks = AudioBook.query.filter_by(title = searsh_word).all()
                    start, end, pagination = get_pagination(audioBooks)
                    return render_template("searsh.jinja", title="بحث", audioBooks=audioBooks[start:end], pagination=pagination)
                else:
                    flash("ادخلت قيمة غير موجودة بالخيارات", "error")
        books = Book.query.all()
        start, end, pagination = get_pagination(books)
        return render_template("searsh.jinja", title="بحث", books=books[start:end], pagination=pagination)
