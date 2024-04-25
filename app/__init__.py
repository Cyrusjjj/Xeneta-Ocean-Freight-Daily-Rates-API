from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

# Import the routes module
from app import routes
