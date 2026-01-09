from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes here
from app.routes import users, collections

