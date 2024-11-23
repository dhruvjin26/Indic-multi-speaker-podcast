import os  

class Config:  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///podcasts.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'  
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  
