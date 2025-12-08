from app import app
from models import db, User

with app.app_context():
    # Check users
    users = User.query.limit(5).all()
    print(f"Total users in database: {User.query.count()}\n")
    
    for user in users:
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        print(f"Role: {user.role}")
        print(f"Has password hash: {bool(user.password_hash)}")
        
        # Test password check
        test_result = user.check_password('password123')
        print(f"Password 'password123' works: {test_result}")
        print("-" * 50)
