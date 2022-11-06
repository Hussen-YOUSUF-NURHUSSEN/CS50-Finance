from flask import Flask
from flask_session import Session
from .helpers import usd, apology
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from tempfile import mkdtemp
import os


"""  Return create_app() that will
                        ===> create application + register_blueprint + configure session + handle error ... """

def create_app():
    app = Flask(__name__)

    # Make sure API key is set
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Ensure responses aren't cached
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from .auth import auth
    from .views import views
    from .actions import actions
    from .content import content

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(actions, url_prefix='/')
    app.register_blueprint(content, url_prefix="/")


    def errorhandler(e):
        """Handle error"""
        if not isinstance(e, HTTPException):
            e = InternalServerError()
        return apology(e.name, e.code)


    # Listen for errors
    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)

    return app

