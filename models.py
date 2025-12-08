from datetime import datetime

# Import db and bcrypt from app module
# This works because app.py imports models AFTER initializing db and bcrypt
def init_model():
    from app import db, bcrypt
    return db, bcrypt

db, bcrypt = init_model()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, teacher, admin
    profile_picture = db.Column(db.String(500), default='https://lh3.googleusercontent.com/aida-public/AB6AXuDJ7alwZ4VtU9QjSG7VKafpieuWwNgPDgp2Y4KxAjlKwzhLF9QwtgPuE_RxEueIXjzAiJU3DrN2mg8myDX5Rfxgw2ifFs1p5OCij9LY2ZGhTKIh0kYMHHC3Mtg1ufz4cR_l1c73jMMIalIAWIrN_SQWZVBn-C9kHQB0yE-qHi9Fo1cK2mGRyJk9nbq4IFvGPJGk4WnaxiN08atgc4Ee_rrBwEKGkl90Fub5d2GJsgmGbs3F0VpIEi4oxFCGFJO761a2Q4R5x811WzyZ')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
