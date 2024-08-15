from flask import Blueprint
from blog.controller.BookController import BookController
book_bp = Blueprint("book_controller",__name__)

book_bp.route("/books")(BookController.books)
book_bp.route("/books/<int:id>")(BookController.book)
book_bp.route("/add-book", methods=["POST", "GET"])(BookController.add_book)
book_bp.route("/update-book/<int:book_id>", methods=["POST"])(BookController.update_book)

book_bp.route("/audio-books")(BookController.audioBooks)
book_bp.route("/audio-books/<int:id>")(BookController.audioBook)
book_bp.route("/add-audio-book", methods=["POST", "GET"])(BookController.add_audio_book)
book_bp.route("/update-audio-book/<int:book_id>", methods=["POST"])(BookController.update_audio_book)


book_bp.route("/delete-book", methods=["POST"])(BookController.delete_book) #لحذف الكتب العادية والصوتية