import stripe
from flask import render_template, jsonify, url_for, request, current_user
from flask_login import login_required
from blog.models.BookModel import Book ,AudioBook
from blog.models.BusketModel import Busket
from blog import cfg, db
from blog.utils.StripeUtils import send_file_email
class StripeController:
    @login_required
    def success():
        busket = Busket.query.get(current_user.id)
        filenamepaths=[]
        for bookID in busket.books_id:
            bookName = Book.query.get(bookID).book_name
            filenamepaths.append(str(cfg.FILES_DIR /"book"/ bookName))
            
        for audioID in busket.audio_books_id:
            bookName = AudioBook.query.get(audioID).audio_name
            filenamepaths.append(str(cfg.FILES_DIR /"audio"/ bookName))
            
            
        send_file_email(current_user, filenamepaths)
        db.session.delete(busket)
        db.session.commit()
        return render_template("stripe/success.jinja")

    @login_required
    def cancelled():
        return render_template("stripe/cancelled.jinja")
    
    @login_required
    def get_published_key():
        return jsonify({'public_key': cfg.STRIPE_PUBLISHABLE_KEY})

    @login_required
    def create_checkout_session():
        stripe.api_key = cfg.STRIPE_SECRET_KEY
        items = request.get_json()['items']

        line_items_list = []
        for id in items:
            book = Book.query.get_or_404(id)
            line_items_list.append({
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                        'name': book.title
                    },
                    'unit_amount': book.price * 100,
                },
                'quantity': 1})

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=url_for(
                    'stripe_controller.success', 
                    session_id='{CHECKOUT_SESSION_ID}', 
                    _external=True),
                cancel_url=url_for('stripe_controller.cancelled', _external=True),
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items_list)
            return jsonify({'sessionId': checkout_session['id']})
        except Exception as e:
            return jsonify(error=str(e)), 403
    
    def stripe_webhook():
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")
 
        print(payload)
        print(sig_header)

        try:
            event = stripe.Webhook.construct_event(
                payload=payload, 
                sig_header=sig_header, 
                secret=cfg.STRIPE_ENDPOINT_SECRET
                )

        except ValueError as e:
            return "Invalid payload", 400
        except stripe.error.SignatureVerificationError as e:
            return "Invalid signature", 400

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            print("Payment was successful.")

        return "Success", 200
