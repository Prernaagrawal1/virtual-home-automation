from flask import Flask
from flask_cors import CORS

def create_app(template_folder='templates'):
    app = Flask(__name__, template_folder=template_folder)  # Add template_folder argument
    CORS(app)

# ✅ Add secret key for session management (used in login/logout)
    app.secret_key = "supersecretkey123"  # You can make this more random/secure

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
