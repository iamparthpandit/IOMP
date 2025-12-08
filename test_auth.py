"""
Test authentication and database
"""
from app import app
from models import db, User

def test_authentication():
    """Test authentication for student002@techvista.edu"""
    with app.app_context():
        # Check if database has users
        total_users = User.query.count()
        print(f"Total users in database: {total_users}")
        
        if total_users == 0:
            print("\n❌ Database is empty! Need to import users.")
            print("Run: python import_users.py")
            return
        
        # Test specific user
        test_email = "student002@techvista.edu"
        test_password = "Student@2025"
        
        print(f"\nTesting login for: {test_email}")
        print(f"Password: {test_password}")
        
        # Find user
        user = User.query.filter_by(email=test_email).first()
        
        if not user:
            print(f"\n❌ User not found: {test_email}")
            print("\nSearching for similar emails...")
            all_users = User.query.all()
            for u in all_users:
                if "student002" in u.email or "maria" in u.name.lower():
                    print(f"  - {u.email} ({u.name}) - Role: {u.role}")
        else:
            print(f"\n✓ User found: {user.name} ({user.email})")
            print(f"  Role: {user.role}")
            print(f"  Password hash: {user.password_hash[:50]}...")
            
            # Test password
            password_valid = user.check_password(test_password)
            print(f"\n  Password check result: {password_valid}")
            
            if password_valid:
                print("\n✅ LOGIN SHOULD WORK!")
            else:
                print("\n❌ PASSWORD DOES NOT MATCH!")
                print("\nTesting common password variations:")
                variations = [
                    "Student@2025",
                    "student@2025",
                    "STUDENT@2025",
                ]
                for pwd in variations:
                    if user.check_password(pwd):
                        print(f"  ✓ Correct password: {pwd}")
                        break
        
        # Display all students
        print("\n" + "="*80)
        print("ALL STUDENT ACCOUNTS:")
        print("="*80)
        students = User.query.filter_by(role='student').all()
        for student in students:
            print(f"Email: {student.email:40} | Name: {student.name}")

if __name__ == '__main__':
    test_authentication()
