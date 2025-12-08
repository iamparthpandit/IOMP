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
from models import db, bcrypt, Message, User, Post

# Initialize extensions with app
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Import routes after app initialization
from routes import auth_bp
from routes_new import api_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(api_bp, url_prefix='/api')

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

@app.route('/calendar')
def calendar_page():
    return send_from_directory('.', 'calander.html')

@app.route('/settings')
def settings_page():
    return send_from_directory('.', 'settings.html')

@app.route('/messages')
def messages_page():
    return send_from_directory('.', 'messages.html')

# --- Messaging API Endpoints ---

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/api/messages', methods=['GET'])
@jwt_required()
def get_messages():
    current_user_id = int(get_jwt_identity())
    
    # Get messages where user is sender, receiver, or it's a broadcast
    messages = Message.query.filter(
        (Message.sender_id == current_user_id) | 
        (Message.receiver_id == current_user_id) | 
        (Message.message_type == 'broadcast')
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([m.to_dict() for m in messages])

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
        
    receiver_id = data.get('receiver_id')
    message_type = 'direct'
    
    if receiver_id == 'all':
        message_type = 'broadcast'
        receiver_id = None
    
    new_message = Message(
        sender_id=current_user_id,
        receiver_id=receiver_id,
        content=data['content'],
        message_type=message_type
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(new_message.to_dict()), 201

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