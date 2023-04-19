from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.book_model import Book


class Author:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.list_of_favorites = []

    @classmethod
    def add_book_to_favorites(cls, data):
        query = """ 
        INSERT INTO favorites (author_id, book_id)
        VALUES (%(author_id)s, %(book_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """ 
        SELECT *
        FROM authors;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        list_of_authors = []

        for row in results:
            list_of_authors.append(cls(row))

        return list_of_authors

    @classmethod
    def get_one(cls, data):
        query = """ 
        SELECT *
        FROM authors
        WHERE id = %(id)s
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        return cls(result[0])

    @classmethod
    def get_one_by_name(cls, data):
        query = """ 
        SELECT *
        FROM authors
        WHERE name = %(name)s
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) == 0:
            return None

        return cls(result[0])

    @classmethod
    def get_one_with_favorites(cls, data):
        query = """ 
        SELECT * FROM authors a
        LEFT JOIN favorites f ON f.author_id = a.id
        LEFT JOIN books b ON f.book_id = b.id
        WHERE a.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        current_author = cls(results[0])

        for row in results:
            if row["b.id"] != None:
                current_favorite = {
                    "id": row["b.id"],
                    "title": row["title"],
                    "total_pages": row["total_pages"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                current_author.list_of_favorites.append(Book(current_favorite))
        return current_author

    @classmethod
    def create_one(cls, data):
        query = """ 
        INSERT INTO authors (name)
        VALUES (%(name)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)
