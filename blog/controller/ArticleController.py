from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from blog.forms.ArticleForm import AddArticle
from blog.models.ArticalModel import Article
from blog.utils.SearshUtils import get_pagination
from blog import cfg, db
from blog.utils.ArticleUtils import delete_article_image, create_article_image
import random
class ArticleController:
    def articles():
        articles = Article.query.all()    
        start, end, pagination = get_pagination(articles)
        return render_template("items.jinja",title="المقالات", articles=articles[start:end], pagination=pagination)
    
    def article(id):
        article = Article.query.get(id)
        return render_template("article.jinja", title=article.title, article=article)
    
    @login_required
    def add_article():
        if current_user.is_admin:
            form = AddArticle()
            
            
            
            if form.validate_on_submit():
                article_img = form.article_img.data
                if article_img != None:
                    img_ext = article_img.filename.rsplit(".")[-1]
                    if img_ext in cfg.ALLOW_EXTENTION_IMG:  
                        img_random_name = "img" + str(random.randint(1000,9999))+"."+img_ext
                        # filename = secure_filename(file.filename)
                        article_img.save(str(cfg.IMAGE_DIR/"article"/img_random_name))
                    else:
                        
                        flash("امتداد الصورة غير صالح", "warning")
                        return render_template("admin/add_article.jinja", title="اضافة مقاله", form=form)
                else:
                    img_random_name = "default.png"
                    
                new_article = Article(title = form.title.data, content = form.content.data, author_id = current_user.id, artical_img=img_random_name)
                db.session.add(new_article)
                db.session.commit()
                flash("تم اضافة المقاله بنجاح", "success")
                return redirect(url_for('main_controller.home'))
            
            # الميثود بوست معناها ان البيانات ارسلت لكن الفورم قال انها خاطئة
            elif request.method == "POST":
                flash("هناك خطا بالمدخلات حاول مرة اخرى", "error")                    
            return render_template("admin/add_article.jinja", title="اضافة مقاله", form=form)
        
        # عند محاولة مستخدم الوصول لصفحة وهو ليس "ادمين" يضهر 404
        abort(404)

    @login_required
    def ubdate_article(article_id):
        if current_user.is_admin:
            form = AddArticle()
            if form.validate_on_submit():
                article = Article.query.get(article_id)
                
                article_image = form.article_img.data
                if article_image:
                    article_image_name = create_article_image(article_image)
                    if article_image_name:
                        delete_article_image(article.article_img)
                        article.article_img = article_image_name
                    else:
                        flash("امتداد الصورة غير صالح", "warning")
                article.title = form.title.data
                article.content = form.content.data
        
                db.session.commit()
                flash("تم التعديل بنجاح", "success")
                return redirect(url_for("article_controller.article", id=article_id))
            article = Article.query.get(article_id)
            return render_template("admin/ubdate_article.jinja",title="نعديل مقاله", article=article, form=form)
        abort(404)
        
    @login_required
    def delete_article(article_id):
        if current_user.is_admin:
            article = Article.query.get(article_id)
            delete_article_image(article.article_img)   
            db.session.delete(article)
            db.session.commit()
            flash("تم الحذف بنجاح", "success")
            return redirect(url_for("main_controller.home"))
        abort(404)
        