from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime  
from werkzeug.security import generate_password_hash, check_password_hash  

db = SQLAlchemy()  

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False)  
    podcasts = db.relationship('Podcast', backref='user', lazy=True)  

    def set_password(self, password):  
        self.password = generate_password_hash(password)  

    def check_password(self, password):  
        return check_password_hash(self.password, password)  

class Podcast(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(120), nullable=False)  
    description = db.Column(db.Text, nullable=True)  
    category = db.Column(db.String(50), nullable=True)  
    thumbnail_url = db.Column(db.String(255), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
