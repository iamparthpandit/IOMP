from app import app
from models import db, Event, User
from datetime import datetime, timedelta
import random

with app.app_context():
    print("🌱 Seeding Calendar Events...")
    
    # Reset Database
    print("♻️ Resetting database schema...")
    db.drop_all()
    db.create_all()

    # Ensure we have at least one user to be the organizer
    organizer = User.query.first()
    if not organizer:
        print("⚠️ No users found. Creating a default admin user...")
        organizer = User(
            name="Admin User", 
            email="admin@iomp.com", 
            role="admin"
        )
        organizer.set_password("password123")
        db.session.add(organizer)
        db.session.commit()
        print(f"✅ Created user: {organizer.email} (ID: {organizer.id})")

    # Clear old events
    deleted_count = Event.query.delete()
    print(f"🧹 Cleared {deleted_count} old events.")
    
    # Base date: Today
    today = datetime.now()
    
    # Generate dummy events for current month and next month
    events_data = [
        {
            "title": "Project Kickoff",
            "description": "Initial meeting to discuss project scope and timeline.",
            "date": today.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1),
            "location": "Conference Room A",
            "organizer_id": organizer.id
        },
        {
            "title": "Design Review",
            "description": "Reviewing the new UI mockups with the design team.",
            "date": today.replace(hour=14, minute=30, second=0, microsecond=0) + timedelta(days=3),
            "location": "Design Lab",
            "organizer_id": organizer.id
        },
        {
            "title": "Client Presentation",
            "description": "Presenting the Q4 progress report to the client.",
            "date": today.replace(hour=11, minute=0, second=0, microsecond=0) + timedelta(days=5),
            "location": "Zoom Meeting",
            "organizer_id": organizer.id
        },
        {
            "title": "Team Lunch",
            "description": "Monthly team bonding lunch.",
            "date": today.replace(hour=12, minute=30, second=0, microsecond=0) + timedelta(days=8),
            "location": "Cafeteria",
            "organizer_id": organizer.id
        },
        {
            "title": "Code Freeze",
            "description": "No new features to be merged after this point.",
            "date": today.replace(hour=17, minute=0, second=0, microsecond=0) + timedelta(days=12),
            "location": "Remote",
            "organizer_id": organizer.id
        },
        {
            "title": "Release Day",
            "description": "Deploying version 2.0 to production.",
            "date": today.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=15),
            "location": "War Room",
            "organizer_id": organizer.id
        },
        {
            "title": "Retrospective",
            "description": "Analyzing what went well and what didn't.",
            "date": today.replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=18),
            "location": "Room 101",
            "organizer_id": organizer.id
        }
    ]
    
    for event_info in events_data:
        event = Event(**event_info)
        db.session.add(event)
    
    db.session.commit()
    print(f"✅ Successfully added {len(events_data)} events for {today.strftime('%B %Y')}.")