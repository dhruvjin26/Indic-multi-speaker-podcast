import os  
from flask import Flask  
from flask_cors import CORS  
from flask_jwt_extended import JWTManager  
from config import Config  
from models import db  
import routes  

app = Flask(__name__)  
app.config.from_object(Config)  

CORS(app)  
db.init_app(app)  
jwt = JWTManager(app)  

# Ensure upload folder exists  
if not os.path.exists(app.config['UPLOAD_FOLDER']):  
    os.makedirs(app.config['UPLOAD_FOLDER'])  

with app.app_context():  
    db.create_all()  # Create database tables if they don't exist  

app.register_blueprint(routes.api)  

if __name__ == "__main__":  
    app.run(debug=True)