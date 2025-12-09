from flask import Blueprint, request, jsonify
from models import db, User, ChatMessage, Event, EventRegistration, Announcement, Classroom, Material, Attendance
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from groq import Groq
import os
import json

chat_bp = Blueprint('chatbot', __name__)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
        print("✓ Groq AI client initialized successfully")
    else:
        client = None
        print("⚠️ GROQ_API_KEY not found in environment variables")
except Exception as e:
    print(f"❌ Groq init error: {e}")
    client = None

def get_user_context(user_id):
    """Fetch comprehensive user context from database"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {}
        
        context = {
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'user_id': user.id
        }
        
        # Get attendance data
        if user.role == 'student':
            try:
                attendance_records = Attendance.query.filter_by(user_id=user_id).all()
                total = len(attendance_records)
                present = sum(1 for a in attendance_records if a.status == 'present')
                context['attendance'] = {
                    'total': total,
                    'present': present,
                    'percentage': round((present / total * 100) if total > 0 else 0, 2)
                }
            except Exception:
                context['attendance'] = {'total': 0, 'present': 0, 'percentage': 0}
            
            # Get enrolled classrooms
            try:
                classrooms = Classroom.query.all()  # In real app, filter by user enrollment
                context['classrooms'] = [{'id': c.id, 'name': c.name, 'teacher': c.teacher_name} for c in classrooms[:5]]
            except Exception:
                context['classrooms'] = []
            
        # Get registered events - handle schema mismatch
        try:
            registrations = EventRegistration.query.filter_by(user_id=user_id).all()
            event_ids = [r.event_id for r in registrations]
            events = Event.query.filter(Event.id.in_(event_ids)).all() if event_ids else []
            context['registered_events'] = [{'id': e.id, 'title': e.title, 'date': e.date.isoformat() if e.date else None} for e in events[:5]]
        except Exception:
            context['registered_events'] = []
        
        # Get upcoming events
        try:
            upcoming_events = Event.query.filter(Event.date >= datetime.now().date()).order_by(Event.date).limit(5).all()
            context['upcoming_events'] = [{'id': e.id, 'title': e.title, 'date': e.date.isoformat() if e.date else None} for e in upcoming_events]
        except Exception:
            context['upcoming_events'] = []
        
        # Get recent announcements
        try:
            announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
            context['recent_announcements'] = [{'id': a.id, 'title': a.title, 'content': a.content[:100]} for a in announcements]
        except Exception:
            context['recent_announcements'] = []
        
        return context
    except Exception as e:
        print(f"Error getting user context: {e}")
        return {}

def build_system_prompt(user, context):
    """Build comprehensive system prompt based on user role and context"""
    
    base_prompt = f"""You are IOMP AI Assistant - an intelligent, helpful, and context-aware chatbot for an Integrated Organizational Management Platform.

**User Information:**
- Name: {user.name}
- Role: {user.role.upper()}
- Email: {user.email}

**Your Capabilities:**

1. **General Queries**: Answer questions about the institution, campus policies, timings, contacts
2. **Academic Help**: Explain topics, provide definitions, offer study guidance
3. **Event Information**: List events, provide details, check registration status
4. **Attendance**: Show attendance records and percentages
5. **Announcements**: Fetch latest notices and important updates
6. **Classroom Info**: List enrolled classes, materials, and teacher details
7. **AI Assistance**: Summarize content, simplify explanations, provide study tips

**Current Context Data:**"""

    if user.role == 'student':
        attendance = context.get('attendance', {})
        base_prompt += f"""
- **Attendance**: {attendance.get('present', 0)}/{attendance.get('total', 0)} classes ({attendance.get('percentage', 0)}%)
- **Enrolled Classes**: {len(context.get('classrooms', []))} classrooms
- **Registered Events**: {len(context.get('registered_events', []))} events"""
    
    if context.get('upcoming_events'):
        base_prompt += f"\n- **Upcoming Events**: {len(context['upcoming_events'])} events scheduled"
    
    if context.get('recent_announcements'):
        base_prompt += f"\n- **Recent Announcements**: {len(context['recent_announcements'])} new notices"
    
    base_prompt += """

**Instructions:**
- Be helpful, friendly, and professional
- Provide accurate information based on the database context
- If data is not available, suggest the user check with admin/teacher
- Keep responses clear and concise (max 150 words)
- For specific data requests, use the context provided above
- Maintain conversation context across messages
- For admin/teacher roles, offer additional management capabilities
- Never share confidential information
- Reject inappropriate or unsafe queries politely

**Safety Rules:**
- Role-based access: Students cannot access admin functions
- No confidential data disclosure
- Academic integrity maintained
- Professional and educational responses only"""

    return base_prompt

def generate_data_response(user, context, query):
    """Generate responses with real database data"""
    query_lower = query.lower()
    
    # Attendance queries
    if any(word in query_lower for word in ['attendance', 'present', 'absent', 'percentage']):
        if user.role == 'student':
            att = context.get('attendance', {})
            return f"📊 Your Attendance:\n\nTotal Classes: {att.get('total', 0)}\nPresent: {att.get('present', 0)}\nAttendance: {att.get('percentage', 0)}%\n\n" + (
                "⚠️ Your attendance is below 75%. Please improve!" if att.get('percentage', 0) < 75 else "✅ Great attendance! Keep it up!"
            )
    
    # Event queries
    if any(word in query_lower for word in ['event', 'fest', 'upcoming', 'register']):
        events = context.get('upcoming_events', [])
        if events:
            response = "📅 Upcoming Events:\n\n"
            for e in events[:3]:
                response += f"• {e['title']} - {e['date']}\n"
            return response
        return "📅 No upcoming events at the moment. Check back later!"
    
    # Announcement queries
    if any(word in query_lower for word in ['announcement', 'notice', 'update', 'news']):
        announcements = context.get('recent_announcements', [])
        if announcements:
            response = "📢 Recent Announcements:\n\n"
            for a in announcements:
                response += f"• {a['title']}\n{a['content'][:80]}...\n\n"
            return response
        return "📢 No recent announcements."
    
    # Classroom queries
    if any(word in query_lower for word in ['classroom', 'class', 'subject', 'teacher']) and user.role == 'student':
        classrooms = context.get('classrooms', [])
        if classrooms:
            response = "📚 Your Classrooms:\n\n"
            for c in classrooms[:5]:
                response += f"• {c['name']} - Teacher: {c['teacher']}\n"
            return response
        return "📚 No classrooms enrolled yet."
    
    return None

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    current_user_id = int(get_jwt_identity())
    data = request.json
    msg = data.get("message", "").strip()
    
    if not msg:
        return jsonify({"reply": "Please ask me something!"}), 400
    
    # Get user and context
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"reply": "User not found."}), 404
    
    context = get_user_context(current_user_id)
    
    try:
        # First check if this is a direct data query
        data_response = generate_data_response(user, context, msg)
        
        if data_response:
            reply = data_response
        elif not client:
            reply = "I am currently in offline mode. But I can help with:\n• Attendance\n• Events\n• Announcements\n• Classrooms\nWhat would you like to know?"
        else:
            # Use Groq AI for intelligent responses
            system_prompt = build_system_prompt(user, context)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq's powerful model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": msg}
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content.strip()
        
        # Save to database
        chat_entry = ChatMessage(
            user_id=current_user_id,
            message=msg,
            response=reply
        )
        db.session.add(chat_entry)
        db.session.commit()
        
        return jsonify({"reply": reply, "success": True})
        
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "reply": "Sorry, I'm having trouble right now. Please try again in a moment.",
            "success": False
        }), 500

@chat_bp.route('/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get user's chat history"""
    current_user_id = int(get_jwt_identity())
    
    history = ChatMessage.query.filter_by(user_id=current_user_id).order_by(ChatMessage.created_at.desc()).limit(20).all()
    
    return jsonify({
        'success': True,
        'history': [{
            'id': h.id,
            'message': h.message,
            'response': h.response,
            'created_at': h.created_at.isoformat()
        } for h in history]
    })
