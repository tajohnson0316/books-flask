from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import author_model


class Book:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.total_pages = data["total_pages"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.list_of_favorites = []

    @classmethod
    def get_all(cls):
        query = """ 
        SELECT *
        FROM books;
        """

        list_of_books = []

        results = connectToMySQL(DATABASE).query_db(query)

        for row in results:
            list_of_books.append(cls(row))

        return list_of_books

    @classmethod
    def get_one(cls, data):
        query = """ 
        SELECT *
        FROM books
        WHERE id = %(id)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        return cls(result[0])

    @classmethod
    def get_one_with_favorites(cls, data):
        query = """ 
        SELECT * FROM books b
        LEFT JOIN favorites f ON f.book_id = b.id
        LEFT JOIN authors a ON f.author_id = a.id
        WHERE b.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        current_book = cls(results[0])
        for row in results:
            if row["a.id"] != None:
                current_author = {
                    "id": row["a.id"],
                    "name": row["name"],
                    "created_at": row["a.created_at"],
                    "updated_at": row["a.updated_at"],
                }
                current_book.list_of_favorites.append(
                    author_model.Author(current_author)
                )
        return current_book

    @classmethod
    def get_one_by_title(cls, data):
        query = """ 
        SELECT *
        FROM books
        WHERE title = %(title)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        return cls(result[0])

    @classmethod
    def create_one(cls, data):
        query = """ 
        INSERT INTO books (title, total_pages)
        VALUES (%(title)s, %(total_pages)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)
