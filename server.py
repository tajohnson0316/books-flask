from flask_app import app
from flask_app.controllers import authors_controller
from flask_app.controllers import books_controller

if __name__ == "__main__":
    app.run(debug=True, port=5002)
