"""
Import users from users_data.csv into the database
"""
import csv
from app import app
from models import db, User

def import_users_from_csv():
    """Import users from users_data.csv file"""
    with app.app_context():
        # Clear existing users
        print('Clearing existing users...')
        User.query.delete()
        db.session.commit()
        
        # Read CSV file
        print('Reading users_data.csv...')
        with open('users_data.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            users_added = 0
            
            for row in csv_reader:
                # Create new user
                user = User(
                    name=f"{row['first_name']} {row['last_name']}",
                    email=row['email'].strip().lower(),
                    role=row['role'].lower()  # Convert Admin/Staff/Student to lowercase
                )
                
                # Set password from CSV
                user.set_password(row['password'])
                
                db.session.add(user)
                users_added += 1
                print(f"Added user: {user.name} ({user.email}) - Role: {user.role} - Password: {row['password']}")
            
            # Commit all changes
            db.session.commit()
            print(f'\n✓ Successfully imported {users_added} users!')
            print('\n' + '='*80)
            print('LOGIN CREDENTIALS')
            print('='*80)
            
            # Display all users with credentials
            all_users = User.query.all()
            
            # Group by role
            admins = [u for u in all_users if u.role == 'admin']
            staff = [u for u in all_users if u.role == 'staff']
            students = [u for u in all_users if u.role == 'student']
            
            if admins:
                print('\n📌 ADMIN USERS:')
                print('-' * 80)
                for user in admins:
                    # Get password from CSV again for display
                    with open('users_data.csv', 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for r in reader:
                            if r['email'].strip().lower() == user.email:
                                print(f"  Email: {user.email:40} | Password: {r['password']:20} | Name: {user.name}")
                                break
            
            if staff:
                print('\n👨‍🏫 STAFF USERS:')
                print('-' * 80)
                for user in staff:
                    with open('users_data.csv', 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for r in reader:
                            if r['email'].strip().lower() == user.email:
                                print(f"  Email: {user.email:40} | Password: {r['password']:20} | Name: {user.name}")
                                break
            
            if students:
                print('\n🎓 STUDENT USERS:')
                print('-' * 80)
                for user in students:
                    with open('users_data.csv', 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for r in reader:
                            if r['email'].strip().lower() == user.email:
                                print(f"  Email: {user.email:40} | Password: {r['password']:20} | Name: {user.name}")
                                break
            
            print('\n' + '='*80)
            
            # Display first 5 users
            sample_users = User.query.limit(5).all()
            for user in sample_users:
                print(f"  - Email: {user.email} | Name: {user.name} | Role: {user.role}")

if __name__ == '__main__':
    try:
        import_users_from_csv()
    except FileNotFoundError:
        print('Error: user_id.csv file not found!')
    except Exception as e:
        print(f'Error importing users: {str(e)}')
