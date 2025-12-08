from flask import Flask, request, jsonify, send_from_directory
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

# Import db and bcrypt from models and initialize with app
from models import db, bcrypt

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Import routes after app initialization
from routes import auth_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Serve static HTML files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/profile')
def profile_page():
    return send_from_directory('.', 'profile.html')

@app.route('/events')
def events_page():
    return send_from_directory('.', 'events.html')

# Serve static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Create database tables
with app.app_context():
    db.create_all()
    print('✓ Database tables created')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f'✓ Server running on http://localhost:{port}')
    app.run(debug=True, port=port)
