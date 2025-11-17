from flask import Flask, send_from_directory
from flask_cors import CORS # type: ignore
from src.api.routes import api
from src.config import Config


def create_app():
    """
    Application factory pattern
    """
    app = Flask(__name__, static_folder="static")

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(api, url_prefix="/api")

    # Serve static files
    @app.route("/")
    def index():
        return send_from_directory("static", "index.html")

    return app


if __name__ == "__main__":
    app = create_app()

    print(f"Starting ResuMatch API on http://{Config.HOST}:{Config.PORT}")
    print(
        f"Open http://localhost:{Config.PORT} in your browser to access the frontend."
    )

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
