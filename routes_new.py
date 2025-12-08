from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Event, EventRegistration, Announcement, Classroom, Material, Attendance, ChatMessage, Organization, Post
from datetime import datetime
import random

api_bp = Blueprint('api', __name__)

# --- Posts Endpoints ---

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify({'success': True, 'posts': [p.to_dict() for p in posts]}), 200

@api_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'success': False, 'message': 'Content is required'}), 400
        
    try:
        new_post = Post(
            author_id=current_user_id,
            content=data['content'],
            image_url=data.get('image_url')
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'success': True, 'post': new_post.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# --- Events Endpoints ---

@api_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return jsonify({'success': True, 'events': [e.to_dict() for e in events]}), 200

@api_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    try:
        new_event = Event(
            title=data['title'],
            description=data.get('description', ''),
            date=datetime.fromisoformat(data['date'].replace('Z', '+00:00')),
            location=data.get('location', ''),
            image_url=data.get('image_url', ''),
            organizer_id=current_user_id,
            organization_id=user.organization_id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'success': True, 'event': new_event.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@api_bp.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_event(event_id):
    current_user_id = int(get_jwt_identity())
    
    existing = EventRegistration.query.filter_by(event_id=event_id, user_id=current_user_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already registered'}), 400
        
    registration = EventRegistration(event_id=event_id, user_id=current_user_id)
    db.session.add(registration)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Registered successfully'}), 201

# --- Announcements Endpoints ---

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify({'success': True, 'announcements': [a.to_dict() for a in announcements]}), 200

@api_bp.route('/announcements', methods=['POST'])
@jwt_required()
def create_announcement():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    new_announcement = Announcement(
        title=data['title'],
        content=data['content'],
        priority=data.get('priority', 'normal'),
        author_id=current_user_id,
        organization_id=user.organization_id
    )
    db.session.add(new_announcement)
    db.session.commit()
    return jsonify({'success': True, 'announcement': new_announcement.to_dict()}), 201

# --- Classroom & Materials Endpoints ---

@api_bp.route('/classrooms', methods=['GET'])
@jwt_required()
def get_classrooms():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    # For simplicity, return all classrooms in the org
    classrooms = Classroom.query.filter_by(organization_id=user.organization_id).all()
    return jsonify({'success': True, 'classrooms': [c.to_dict() for c in classrooms]}), 200

@api_bp.route('/classrooms', methods=['POST'])
@jwt_required()
def create_classroom():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    new_classroom = Classroom(
        name=data['name'],
        code=data['code'],
        description=data.get('description', ''),
        teacher_id=current_user_id,
        organization_id=user.organization_id
    )
    db.session.add(new_classroom)
    db.session.commit()
    return jsonify({'success': True, 'classroom': new_classroom.to_dict()}), 201

# --- Attendance Endpoints ---

@api_bp.route('/attendance/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    # Expects: classroom_id, student_id, date, status
    
    attendance = Attendance(
        classroom_id=data['classroom_id'],
        user_id=data['student_id'],
        date=datetime.fromisoformat(data['date']).date(),
        status=data['status']
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Attendance marked'}), 201

# --- AI Chatbot Endpoint ---

@api_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Mock AI Response Logic
    responses = [
        "That's an interesting question about IOMP!",
        "I can help you with your schedule and assignments.",
        "Please check the announcements for the latest updates.",
        "To register for an event, go to the Events page.",
        "I am a simulated AI assistant. How can I help you today?"
    ]
    
    ai_response = random.choice(responses)
    if "hello" in user_message.lower():
        ai_response = "Hello! How can I assist you with your academic tasks today?"
    elif "exam" in user_message.lower():
        ai_response = "Exam schedules are usually posted in the Announcements section."
    
    # Save chat history
    chat_entry = ChatMessage(
        user_id=current_user_id,
        message=user_message,
        response=ai_response
    )
    db.session.add(chat_entry)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'response': ai_response
    }), 200

# --- Organization Endpoint ---
@api_bp.route('/organizations', methods=['POST'])
def create_organization():
    data = request.get_json()
    new_org = Organization(
        name=data['name'],
        domain=data.get('domain')
    )
    db.session.add(new_org)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Organization created', 'id': new_org.id}), 201
