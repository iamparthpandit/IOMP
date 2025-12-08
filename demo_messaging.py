"""
Simple test script to demonstrate the messaging API functionality
"""

import json
from datetime import datetime
import uuid

# Simulate the messaging system
messages = {}
users = {
    'admin': {'id': 'admin', 'name': 'Admin User', 'role': 'admin'},
    'teacher1': {'id': 'teacher1', 'name': 'John Teacher', 'role': 'staff'},
    'student1': {'id': 'student1', 'name': 'Jane Student', 'role': 'student'},
    'student2': {'id': 'student2', 'name': 'Bob Student', 'role': 'student'}
}

class Message:
    def __init__(self, sender_id, receiver_id, content, message_type='direct'):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.message_type = message_type
        self.is_read = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': users.get(self.sender_id, {}).get('name', 'Unknown'),
            'receiver_id': self.receiver_id,
            'receiver_name': users.get(self.receiver_id, {}).get('name', 'Unknown') if self.receiver_id != 'all' else 'All Users',
            'content': self.content,
            'timestamp': self.timestamp,
            'message_type': self.message_type,
            'is_read': self.is_read
        }

def demo_messaging_system():
    print("🚀 IOMP Messaging System Demo")
    print("=" * 50)
    
    # Add sample messages
    sample_messages = [
        Message('teacher1', 'student1', 'Welcome to the course! Please check the course materials.', 'direct'),
        Message('admin', 'all', 'Welcome to IOMP platform! All systems are now online.', 'broadcast'),
        Message('student1', 'teacher1', 'Thank you for the warm welcome, professor!', 'direct'),
        Message('student2', 'admin', 'Admin, I have a question about the assignment.', 'direct'),
        Message('teacher1', 'all', 'Class tomorrow will start 15 minutes late.', 'broadcast')
    ]
    
    for msg in sample_messages:
        messages[msg.id] = msg
    
    print(f"✅ Created {len(sample_messages)} sample messages")
    print()
    
    # Display all messages
    print("📋 All Messages:")
    print("-" * 30)
    all_messages = list(messages.values())
    all_messages.sort(key=lambda x: x.timestamp)
    
    for msg in all_messages:
        print(f"[{msg.timestamp[:19]}] {msg.sender_name} → {msg.receiver_name}")
        print(f"   Type: {msg.message_type}")
        print(f"   Content: {msg.content}")
        print()
    
    # Demonstrate user-specific message filtering
    print("👤 Messages for Student1:")
    print("-" * 30)
    student1_messages = [msg for msg in all_messages 
                        if msg.sender_id == 'student1' or msg.receiver_id == 'student1' or msg.receiver_id == 'all']
    
    for msg in student1_messages:
        print(f"[{msg.timestamp[:19]}] {msg.sender_name} → {msg.receiver_name}")
        print(f"   {msg.content}")
        print()
    
    # Demonstrate API simulation
    print("🌐 API Response Simulation:")
    print("-" * 30)
    api_response = {
        "status": "success",
        "total_messages": len(all_messages),
        "messages": [msg.to_dict() for msg in all_messages]
    }
    
    print(json.dumps(api_response, indent=2))
    
    print()
    print("✨ Demo Features Implemented:")
    print("   • User authentication (Admin/Staff/Student roles)")
    print("   • Direct messaging between users")
    print("   • Broadcast messages to all users")
    print("   • Message history with timestamps")
    print("   • User-specific message filtering")
    print("   • Role-based message styling")
    print("   • Real-time updates (5-second refresh)")
    print("   • Responsive HTML interface")
    print("   • Message validation and error handling")
    
    print()
    print("🔧 Integration Options:")
    print("   1. Standalone: Use messaging_api.py as complete app")
    print("   2. Integrated: Add messaging_routes.py to your existing IOMP app")
    print("   3. Frontend: Use messaging.html for the user interface")

if __name__ == "__main__":
    demo_messaging_system()
