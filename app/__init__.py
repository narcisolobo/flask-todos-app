from os import environ
from dotenv import load_dotenv
from flask import Flask, render_template


def create_app():

    app = Flask(__name__)

    load_dotenv()
    app.secret_key = environ.get("SECRET_KEY")

    @app.get("/")
    def index():
        return render_template("index.html")

    from . import auth
    app.register_blueprint(auth.bp)
    auth.bcrypt.init_app(app)

    from . import todos
    app.register_blueprint(todos.bp)

    return app
