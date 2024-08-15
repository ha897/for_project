from flask import Blueprint
from blog.controller.StripeController import StripeController

stripe_bp = Blueprint("stripe_controller", __name__)

stripe_bp.route("/get-key")(StripeController.get_published_key)
stripe_bp.route("/create-checkout-session", methods=['POST'])(StripeController.create_checkout_session)
stripe_bp.route("/success")(StripeController.success)
stripe_bp.route("/cancelled")(StripeController.cancelled)
stripe_bp.route("/webhook", methods=['POST'])(StripeController.stripe_webhook)
