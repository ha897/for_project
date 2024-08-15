from flask import Blueprint
from blog.controller.BusketController import BusketController
busket_bp = Blueprint("busket_controller",__name__)

busket_bp.route("/add-to-busket", methods=["POST"])(BusketController.add_to_busket)
busket_bp.route("/busket")(BusketController.busket)
busket_bp.route("/delete-from-busket", methods=["POST"])(BusketController.delete_from_busket)
busket_bp.route("/payment", methods=["GET","POST"])(BusketController.payment)