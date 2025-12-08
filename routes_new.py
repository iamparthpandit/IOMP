from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Event, EventRegistration, Announcement, Classroom, Material, Attendance, ChatMessage, Organization, Post, Assignment, Enrollment
from datetime import datetime
import random
import os
from werkzeug.utils import secure_filename

api_bp = Blueprint('api', __name__)

@api_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user_details():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

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

@api_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({'success': True, 'event': event.to_dict()}), 200

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
    data = request.get_json() or {}
    
    existing = EventRegistration.query.filter_by(event_id=event_id, user_id=current_user_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already registered'}), 400
        
    registration = EventRegistration(
        event_id=event_id, 
        user_id=current_user_id,
        phone=data.get('phone'),
        dietary_requirements=data.get('dietary_requirements'),
        accessibility_needs=data.get('accessibility_needs')
    )
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
# (Moved to bottom to avoid duplication)


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

# --- Classroom Endpoints ---

@api_bp.route('/classrooms', methods=['GET'])
@jwt_required()
def get_classrooms():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role == 'teacher':
        # Teachers see classrooms they teach
        classrooms = Classroom.query.filter_by(teacher_id=current_user_id).all()
    else:
        # Students see all classrooms for now (or enrolled ones if we implement that strictly)
        classrooms = Classroom.query.all()
        
    return jsonify({'success': True, 'classrooms': [c.to_dict() for c in classrooms]}), 200

@api_bp.route('/classrooms', methods=['POST'])
@jwt_required()
def create_classroom():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role != 'teacher':
        return jsonify({'success': False, 'message': 'Only teachers can create classrooms'}), 403
        
    data = request.get_json()
    
    # Check if class code already exists
    if Classroom.query.filter_by(code=data['code']).first():
        return jsonify({'success': False, 'message': f"Class code '{data['code']}' is already taken. Please use a unique code."}), 400

    try:
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
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@api_bp.route('/classrooms/<int:classroom_id>', methods=['DELETE'])
@jwt_required()
def delete_classroom(classroom_id):
    current_user_id = int(get_jwt_identity())
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if classroom.teacher_id != current_user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    try:
        # Manually delete related items if cascade is not set up in DB
        Material.query.filter_by(classroom_id=classroom_id).delete()
        Assignment.query.filter_by(classroom_id=classroom_id).delete()
        Enrollment.query.filter_by(classroom_id=classroom_id).delete()
        Attendance.query.filter_by(classroom_id=classroom_id).delete()
        
        db.session.delete(classroom)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Classroom deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/classrooms/<int:classroom_id>/details', methods=['GET'])
@jwt_required()
def get_classroom_details(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    
    materials = Material.query.filter_by(classroom_id=classroom_id).all()
    assignments = Assignment.query.filter_by(classroom_id=classroom_id).all()
    
    return jsonify({
        'success': True,
        'classroom': classroom.to_dict(),
        'materials': [m.to_dict() for m in materials],
        'assignments': [a.to_dict() for a in assignments]
    }), 200

@api_bp.route('/classrooms/<int:classroom_id>/materials', methods=['POST'])
@jwt_required()
def upload_material(classroom_id):
    current_user_id = int(get_jwt_identity())
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if classroom.teacher_id != current_user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
    file = request.files['file']
    title = request.form.get('title')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
        
    if file:
        try:
            filename = secure_filename(file.filename)
            # Ensure uploads directory exists
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Create URL (assuming static file serving is set up for root or uploads)
            file_url = f'/uploads/{filename}'
            
            new_material = Material(
                classroom_id=classroom_id,
                title=title,
                file_url=file_url,
                file_type='pdf' if filename.lower().endswith('.pdf') else 'file'
            )
            db.session.add(new_material)
            db.session.commit()
            return jsonify({'success': True, 'material': new_material.to_dict()}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/classrooms/<int:classroom_id>/assignments', methods=['POST'])
@jwt_required()
def create_assignment(classroom_id):
    current_user_id = int(get_jwt_identity())
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if classroom.teacher_id != current_user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    try:
        new_assignment = Assignment(
            classroom_id=classroom_id,
            title=data['title'],
            description=data.get('description', ''),
            due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data.get('due_date') else None
        )
        db.session.add(new_assignment)
        db.session.commit()
        return jsonify({'success': True, 'assignment': new_assignment.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
