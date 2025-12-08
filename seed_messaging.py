from app import app
from models import db, User, Message
from datetime import datetime

def seed_messaging_data():
    with app.app_context():
        print("🌱 Seeding Messaging Data...")
        
        # 1. Create Users
        users_data = [
            {'email': 'admin@iomp.com', 'name': 'Admin User', 'role': 'admin', 'password': 'password123'},
            {'email': 'teacher1@iomp.com', 'name': 'John Teacher', 'role': 'teacher', 'password': 'password123'},
            {'email': 'student1@iomp.com', 'name': 'Jane Student', 'role': 'student', 'password': 'password123'},
            {'email': 'student2@iomp.com', 'name': 'Bob Student', 'role': 'student', 'password': 'password123'}
        ]
        
        user_map = {} # Map email to User object
        
        for u_data in users_data:
            user = User.query.filter_by(email=u_data['email']).first()
            if not user:
                user = User(
                    name=u_data['name'],
                    email=u_data['email'],
                    role=u_data['role'],
                    profile_picture=f"https://ui-avatars.com/api/?name={u_data['name'].replace(' ', '+')}&background=random"
                )
                user.set_password(u_data['password'])
                db.session.add(user)
                print(f"   Created user: {u_data['name']}")
            else:
                print(f"   User exists: {u_data['name']}")
            
            # We need to commit to get the ID
            db.session.commit()
            user_map[u_data['email']] = user

        # 2. Create Messages
        # Map demo IDs to emails for easy translation
        demo_id_map = {
            'admin': 'admin@iomp.com',
            'teacher1': 'teacher1@iomp.com',
            'student1': 'student1@iomp.com',
            'student2': 'student2@iomp.com'
        }

        sample_messages = [
            ('teacher1', 'student1', 'Welcome to the course! Please check the course materials.', 'direct'),
            ('admin', 'all', 'Welcome to IOMP platform! All systems are now online.', 'broadcast'),
            ('student1', 'teacher1', 'Thank you for the warm welcome, professor!', 'direct'),
            ('student2', 'admin', 'Admin, I have a question about the assignment.', 'direct'),
            ('teacher1', 'all', 'Class tomorrow will start 15 minutes late.', 'broadcast')
        ]

        count = 0
        for sender_key, receiver_key, content, msg_type in sample_messages:
            sender = user_map[demo_id_map[sender_key]]
            
            receiver_id = None
            if receiver_key != 'all':
                receiver = user_map[demo_id_map[receiver_key]]
                receiver_id = receiver.id
            
            # Check if message already exists to avoid duplicates (simple check)
            exists = Message.query.filter_by(
                sender_id=sender.id, 
                receiver_id=receiver_id, 
                content=content
            ).first()
            
            if not exists:
                msg = Message(
                    sender_id=sender.id,
                    receiver_id=receiver_id,
                    content=content,
                    message_type=msg_type,
                    timestamp=datetime.utcnow()
                )
                db.session.add(msg)
                count += 1
        
        db.session.commit()
        print(f"✅ Added {count} sample messages.")
        print("✨ Messaging data seeded successfully!")

if __name__ == '__main__':
    seed_messaging_data()
