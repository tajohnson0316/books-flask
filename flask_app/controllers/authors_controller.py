from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.author_model import Author
from flask_app.models.book_model import Book


@app.route("/", methods=["GET"])
@app.route("/authors", methods=["GET"])
def display_all_authors():
    return render_template("display_all_authors.html", list_of_authors=Author.get_all())


@app.route("/authors/<int:id>", methods=["GET"])
def display_one_author(id):
    current_author = Author.get_one_with_favorites({"id": id})

    list_of_books = Book.get_all()
    list_of_favorites = current_author.list_of_favorites

    for book in list_of_books:
        for favorite in list_of_favorites:
            if book.title == favorite.title:
                list_of_books.remove(book)

    return render_template(
        "display_author_page.html",
        current_author=current_author,
        len=len(list_of_favorites),
        list_of_books=list_of_books,
    )


@app.route("/authors/new", methods=["POST"])
def create_author():
    Author.create_one({**request.form})
    return redirect("/authors")


@app.route("/authors/<int:id>/add/favorite", methods=["POST"])
def add_book_to_favorites(id):
    if request.form["title"] == "None":
        return redirect(f"/authors/{id}")

    new_favorite = Book.get_one_by_title({**request.form})
    Author.add_book_to_favorites({"author_id": id, "book_id": new_favorite.id})
    return redirect(f"/authors/{id}")
