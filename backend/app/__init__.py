from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, origins=["http://localhost:3000"])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Import blueprint and setup authentication middleware
    from app.routes import api_bp
    from app.middleware.auth import setup_auth_middleware

    setup_auth_middleware(api_bp, exempt_routes=['/login', '/logout', '/users'])
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

