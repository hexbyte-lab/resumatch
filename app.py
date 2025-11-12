from flask import Flask
from flask_cors import CORS
from src.api.routes import api
from src.config import Config


def create_app():
    """
    Application factory pattern
    """
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()

    print(f"Starting ResuMatch API on http://{Config.HOST}:{Config.PORT}")

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
