from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///iomp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Import models and routes (after initializing db and bcrypt)
import models
from routes import auth_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Serve static HTML files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/profile')
def profile_page():
    return send_from_directory('.', 'profile.html')

# Create database tables
with app.app_context():
    db.create_all()
    print('✓ Database tables created')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f'✓ Server running on http://localhost:{port}')
    app.run(debug=True, port=port)
