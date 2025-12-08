from flask import Blueprint, request, jsonify
from models import db, User, ChatMessage
from flask_jwt_extended import jwt_required, get_jwt_identity
from openai import OpenAI
import os

chat_bp = Blueprint('chatbot', __name__)

# Initialize OpenAI client safely
api_key = os.getenv("OPENAI_API_KEY")
try:
    client = OpenAI(api_key=api_key) if api_key else None
except Exception as e:
    print(f"OpenAI init error: {e}")
    client = None

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    current_user_id = int(get_jwt_identity())
    data = request.json
    msg   = data.get("message", "")
    
    # Get user details from DB instead of trusting client
    user = User.query.get(current_user_id)
    role = user.role if user else "student"
    name = user.name if user else "User"

    system = f"""You are IOMP’s helpful teaching assistant.
The user is a {role} named {name}.
Answer concisely (max 60 words) and educationally.
If unsure, say “Please ask your teacher for clarification.”"""

    try:
        # Check if client is initialized
        if not client:
             # Fallback if no key
            reply = "I am currently in offline mode (API Key missing). But I'm here to help!"
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": msg}
                ],
                temperature=0.7,
                max_tokens=120
            )
            reply = response.choices[0].message.content.strip()
            
        # Save to DB
        chat_entry = ChatMessage(
            user_id=current_user_id,
            message=msg,
            response=reply
        )
        db.session.add(chat_entry)
        db.session.commit()

        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({"reply": "Sorry, I’m having trouble thinking right now. Please try again."}), 500