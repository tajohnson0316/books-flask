from flask import Flask

app = Flask(__name__)
app.secret_key = "This is my secret key - there are many like it, but this one is mine"

DATABASE = "books_db"
