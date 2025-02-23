# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import Config
# import os  # Add this import
# from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect()
# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.update(
#         WTF_CSRF_ENABLED=True,
#         WTF_CSRF_SECRET_KEY=app.config['SECRET_KEY']
#     )


#     app.config.from_object(config_class)

#     # Initialize extensions
#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'

#     # Register blueprints
#     from app.routes import auth_bp, main_bp
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(main_bp)

#     # Only initialize MQTT when not in migration context
#     if not os.environ.get('FLASK_DB_COMMAND'):
#         with app.app_context():
#             from app.mqtt_handler import initialize_mqtt_clients
#             try:
#                 initialize_mqtt_clients()
#             except Exception as e:
#                 app.logger.error(f"MQTT init error: {str(e)}")

#     return app



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
import os

# Initialize extensions
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    # Create and configure app
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    csrf.init_app(app)  # Proper CSRF initialization
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Initialize MQTT only in normal operation
    if not os.environ.get('FLASK_DB_COMMAND'):
        with app.app_context():
            try:
                from app.mqtt_handler import initialize_mqtt_clients
                if db.engine.dialect.has_table(db.engine.connect(), "device"):
                    initialize_mqtt_clients()
            except Exception as e:
                app.logger.error(f"MQTT initialization failed: {str(e)}")
                if app.debug:
                    raise e

    return app