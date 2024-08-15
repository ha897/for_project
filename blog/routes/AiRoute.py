from flask import Blueprint
from blog.controller.AiController import AiController
# from flask_cors import CORS
gbt_bp = Blueprint("ai_controller",__name__)

# جعل التطبيق يعمل بالمصادر الغير موثوقة
# CORS(ai_bp) 

gbt_bp.route("/app-gbt", methods=["POST"])(AiController.get_gbt_request)
gbt_bp.route("/app-orign-gbt", methods=["POST"])(AiController.get_orign_gbt_request)
gbt_bp.route("/ai-page")(AiController.gbt_page)
