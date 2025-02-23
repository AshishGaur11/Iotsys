from app import create_app, db
from flask_migrate import Migrate
import os

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    # Only run MQTT in production mode
    if os.environ.get('FLASK_ENV') == 'production':
        from app.mqtt_handler import initialize_mqtt_clients
        with app.app_context():
            initialize_mqtt_clients()
    app.run(ssl_context='adhoc')