from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.book_model import Book
from flask_app.models.author_model import Author


@app.route("/books", methods=["GET"])
def display_all_books():
    return render_template("display_all_books.html", list_of_books=Book.get_all())


@app.route("/books/<int:id>", methods=["GET"])
def display_one_book(id):
    current_book = Book.get_one_with_favorites({"id": id})
    list_of_authors = Author.get_all()

    for author in list_of_authors:
        for favorite in current_book.list_of_favorites:
            if author.name == favorite.name:
                list_of_authors.remove(author)

    return render_template(
        "display_book_page.html",
        current_book=current_book,
        list_of_authors=list_of_authors,
    )


@app.route("/books/<int:id>/add/favorite", methods=["POST"])
def add_author_to_favorites(id):
    if request.form["name"] == "None":
        return redirect(f"/books/{id}")

    current_book = Book.get_one({"id": id})

    new_author = Author.get_one_by_name({**request.form})
    Author.add_book_to_favorites(
        {"author_id": new_author.id, "book_id": current_book.id}
    )
    return redirect(f"/books/{id}")


@app.route("/books/new", methods=["POST"])
def create_book():
    book_id = Book.create_one({**request.form})
    return redirect("/books")
