from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
    
        from app.models.user import User
        from app.models.complaint import Complaint
        
      
        db.create_all()
    
  
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.complaints import complaints
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(complaints)
    
    return app