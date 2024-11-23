from flask import Blueprint, request, jsonify  
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity  
from models import db, User, Podcast  
from werkzeug.security import generate_password_hash, check_password_hash  
from werkzeug.utils import secure_filename  
from flask_uploads import UploadSet, configure_uploads, IMAGES  
import os  


api = Blueprint('api', __name__)  
thumbnails = UploadSet('thumbnails', IMAGES)  
configure_uploads(api.app, thumbnails)  # Register the thumbnails upload set  

@api.route('/api/register', methods=['POST'])   
def register():  
    data = request.get_json()  
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required."}), 400

    # Check for existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists."}), 400

    try:
        hashed_password = generate_password_hash(data['password'])  
        new_user = User(username=data['username'])  
        new_user.set_password(data['password'])  # Use the method to hash the password
        db.session.add(new_user)  
        db.session.commit()  
        return jsonify({"message": "User created successfully."}), 201
    except Exception as e:
        db.session.rollback()  # Rollback session on error
        return jsonify({"message": "Error registering user!", "error": str(e)}), 500@api.route('/api/register', methods=['POST'])  
def register():  
    data = request.get_json()  
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required."}), 400

    # Check for existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists."}), 400

    try:
        hashed_password = generate_password_hash(data['password'])  
        new_user = User(username=data['username'])  
        new_user.set_password(data['password'])  # Use the method to hash the password
        db.session.add(new_user)  
        db.session.commit()  
        return jsonify({"message": "User created successfully."}), 201
    except Exception as e:
        db.session.rollback()  # Rollback session on error
        return jsonify({"message": "Error registering user!", "error": str(e)}), 500


@api.route('/api/login', methods=['POST'])  
def login():  
    data = request.get_json()  
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required."}), 400

    user = User.query.filter_by(username=data['username']).first()  
    if user and user.check_password(data['password']):  # Use the method to check the password
        token = create_access_token(identity=user.id)  
        return jsonify({"token": token}), 200  
    return jsonify({"message": "Invalid credentials."}), 401  

@api.route('/api/podcasts', methods=['POST'])  
@jwt_required()  
def create_podcast():
    data = request.form  
    if not data.get('title') or not data.get('description'):
        return jsonify({"message": "Title and description are required."}), 400

    thumbnail_url = None
    if 'thumbnail' in request.files:  
        thumbnail = request.files['thumbnail']  
        if thumbnail and allowed_file(thumbnail.filename):  
            if thumbnail.content_length > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({"message": "File too large. Max size is 16MB."}), 400
            try:
                thumbnail_url = thumbnails.save(thumbnail)  
            except Exception as e:
                return jsonify({"message": "Error saving thumbnail", "error": str(e)}), 500
        else:
            return jsonify({"message": "Invalid file type. Only images are allowed."}), 400

    podcast = Podcast(  
        title=data['title'],  
        description=data['description'],  
        category=data.get('category'),  
        thumbnail_url=thumbnail_url,  
        user_id=get_jwt_identity()  
    )  
    try:
        db.session.add(podcast)  
        db.session.commit()  
    except Exception as e:
        return jsonify({"message": "Error creating podcast", "error": str(e)}), 500

    return jsonify({"message": "Podcast created."}), 201  

@api.route('/api/podcasts', methods=['GET'])  
def get_podcasts():  
    podcasts = Podcast.query.all()  
    return jsonify([{'id': p.id, 'title': p.title, 'thumbnail_url': p.thumbnail_url} for p in podcasts]), 200  

def allowed_file(filename):
    """Check if the uploaded file is an allowed image type."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
