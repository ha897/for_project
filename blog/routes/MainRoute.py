from flask import Blueprint
from blog.controller.MainController import MainController
main_bp = Blueprint("main_controller",__name__)

main_bp.route("/")(MainController.home)
main_bp.route("/searsh", methods=["GET", "POST"])(MainController.searsh)