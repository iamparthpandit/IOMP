from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        print(f"Login attempt - Email: {email}")  # Debug
        
        # Validate fields
        errors = []
        if not email:
            errors.append({'field': 'email', 'message': 'Email is required'})
        elif not validate_email(email):
            errors.append({'field': 'email', 'message': 'Please provide a valid email'})
        if not password:
            errors.append({'field': 'password', 'message': 'Password is required'})
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        print(f"User found: {user is not None}")  # Debug
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        password_valid = user.check_password(password)
        print(f"Password valid: {password_valid}")  # Debug
        
        if not password_valid:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        import traceback
        print(f'Login error: {str(e)}')
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': 'Server error during login'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f'Auth error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Not authorized'
        }), 401

@auth_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Sample notifications (in production, fetch from database)
        notifications = [
            {
                'id': 1,
                'type': 'event',
                'title': 'New Event: Tech Fest 2025',
                'message': 'Annual Tech & Culture Fest is coming up on Jan 15, 2025',
                'timestamp': '2 hours ago',
                'read': False,
                'icon': 'fa-calendar'
            },
            {
                'id': 2,
                'type': 'assignment',
                'title': 'Assignment Due',
                'message': 'Data Structures assignment due in 3 days',
                'timestamp': '5 hours ago',
                'read': False,
                'icon': 'fa-file-alt'
            },
            {
                'id': 3,
                'type': 'message',
                'title': 'New Message from Dr. Smith',
                'message': 'Please check your email for project feedback',
                'timestamp': '1 day ago',
                'read': True,
                'icon': 'fa-envelope'
            },
            {
                'id': 4,
                'type': 'announcement',
                'title': 'Campus Update',
                'message': 'Library hours extended during exam week',
                'timestamp': '2 days ago',
                'read': True,
                'icon': 'fa-bullhorn'
            }
        ]
        
        unread_count = sum(1 for n in notifications if not n['read'])
        
        return jsonify({
            'success': True,
            'notifications': notifications,
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        print(f'Error fetching notifications: {str(e)}')
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """Get user settings"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Sample settings (in production, fetch from database)
        settings = {
            'profile': {
                'email': user.email,
                'name': user.first_name + ' ' + user.last_name,
                'role': user.role,
                'department': user.department_id
            },
            'notifications': {
                'email_notifications': True,
                'push_notifications': True,
                'event_reminders': True,
                'assignment_alerts': True
            },
            'privacy': {
                'profile_visibility': 'public',
                'show_email': False,
                'show_department': True
            },
            'appearance': {
                'theme': 'light',
                'language': 'en'
            }
        }
        
        return jsonify({
            'success': True,
            'settings': settings
        }), 200
        
    except Exception as e:
        print(f'Error fetching settings: {str(e)}')
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user settings"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json()
        
        # In production, save to database
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully',
            'settings': data
        }), 200
        
    except Exception as e:
        print(f'Error updating settings: {str(e)}')
        return jsonify({'success': False, 'message': 'Server error'}), 500