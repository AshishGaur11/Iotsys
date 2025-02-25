import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MQTT_TLS_CA_CERTS = os.environ.get('MQTT_TLS_CA_CERTS')
    MQTT_TLS_INSECURE = os.environ.get('MQTT_TLS_INSECURE', 'False').lower() == 'true'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-key' 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)  # Fix for Heroku
    SQLALCHEMY_TRACK_MODIFICATIONS = False