from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, template_folder='app/templates')
    CORS(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
