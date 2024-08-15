from flask import Blueprint
from blog.controller.ArticleController import ArticleController
article_bp = Blueprint("article_controller",__name__)

article_bp.route("/articles")(ArticleController.articles)
article_bp.route("/articles/<int:id>")(ArticleController.article)
article_bp.route("/add-article", methods=["GET", "POST"])(ArticleController.add_article)
article_bp.route("/ubdate-article/<int:article_id>", methods=["POST"])(ArticleController.ubdate_article)
article_bp.route("/delete-article/<int:article_id>", methods=["POST"])(ArticleController.delete_article)
