from app import app
from models import db, User

def create_users():
    with app.app_context():
        # Check if user exists
        if not User.query.filter_by(email='student@iomp.com').first():
            student = User(
                name='Student User',
                email='student@iomp.com',
                role='student',
                profile_picture='https://ui-avatars.com/api/?name=Student+User&background=random'
            )
            student.set_password('password123')
            db.session.add(student)
            print("Created student@iomp.com")

        if not User.query.filter_by(email='teacher@iomp.com').first():
            teacher = User(
                name='Teacher User',
                email='teacher@iomp.com',
                role='teacher',
                profile_picture='https://ui-avatars.com/api/?name=Teacher+User&background=random'
            )
            teacher.set_password('password123')
            db.session.add(teacher)
            print("Created teacher@iomp.com")
            
        db.session.commit()
        print("Test users created successfully.")

if __name__ == '__main__':
    create_users()
