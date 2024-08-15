from flask import Blueprint
from blog.controller.UserController import UserController
login_bp = Blueprint("user_controller",__name__)

login_bp.route("/login", methods=["GET", "POST"])(UserController.user_login)
login_bp.route("/logout", methods=["POST"])(UserController.user_logout)
login_bp.route("/regester", methods=["GET", "POST"])(UserController.user_regester)
login_bp.route("/profile")(UserController.user_profile)
login_bp.route("/to-reset-password", methods=["GET", "POST"])(UserController.to_reset_password)
login_bp.route("/reset-password/<string:token>", methods=["GET", "POST"])(UserController.reset_password)
login_bp.route("/reset-password", methods=["GET", "POST"])(UserController.profile_reset_password)
login_bp.route("/subscriber", methods=["POST"])(UserController.subscriber)
