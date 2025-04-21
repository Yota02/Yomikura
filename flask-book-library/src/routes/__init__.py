# filepath: flask-book-library/src/routes/__init__.py
from flask import Blueprint

# Initialiser le blueprint pour les routes
routes_bp = Blueprint('routes', __name__)

# Importer les routes
from .books import *
from .series import *