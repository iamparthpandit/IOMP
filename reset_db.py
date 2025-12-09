"""
Reset database - Drop all tables and recreate
"""
import os
from app import app
from models import db

def reset_database():
    """Drop all tables and recreate them"""
    with app.app_context():
        # Delete the database file
        db_path = 'instance/iomp.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f'✓ Deleted old database: {db_path}')
        
        # Create all tables with new schema
        db.create_all()
        print('✓ Created new database tables')
        
        print('\nDatabase reset complete!')
        print('Now run: python import_users.py')

if __name__ == '__main__':
    reset_database()
