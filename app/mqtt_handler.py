import json  # Added missing json import
import paho.mqtt.client as mqtt
import ssl
from flask import current_app
from app import db
from app.models import DataPoint

clients = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        current_app.logger.info(f"Connected to MQTT Broker")
        client.subscribe(userdata['topic'])
    else:
        current_app.logger.error(f"Connection failed with code {rc}")

# def on_message(client, userdata, msg):
#     try:
#         data = json.loads(msg.payload)
#         new_point = DataPoint(
#             temperature=data.get('temp'),
#             humidity=data.get('humidity'),
#             device_id=userdata['device_id']
#         )
#         db.session.add(new_point)
#         db.session.commit()
#     except Exception as e:
#         current_app.logger.error(f"Error processing MQTT message: {str(e)}")

# def create_mqtt_client(device):
#     client = mqtt.Client()
#     client.username_pw_set(device.mqtt_user, device.mqtt_password)
#     client.tls_set(ca_certs=current_app.config['MQTT_TLS_CA_CERTS'], 
#                   cert_reqs=ssl.CERT_REQUIRED)
#     client.user_data_set({'device_id': device.id, 'topic': device.topic})
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect(device.broker, 8883, 60)
#     client.loop_start()
#     clients[device.id] = client
def create_mqtt_client(device):
    client = mqtt.Client()
    client.username_pw_set(device.mqtt_user, device.mqtt_password)
    
    # Secure connection handling
    try:
        client.tls_set(
            ca_certs=current_app.config['MQTT_TLS_CA_CERTS'],
            cert_reqs=ssl.CERT_REQUIRED if not current_app.config['MQTT_TLS_INSECURE'] else ssl.CERT_NONE
        )
        client.connect(device.broker, 8883, 60)
    except Exception as e:
        current_app.logger.error(f"MQTT connection failed: {str(e)}")
        return
    
    client.loop_start()
    clients[device.id] = client
# def initialize_mqtt_clients():
#     from app.models import Device
#     for device in Device.query.all():
#         create_mqtt_client(device)


# def initialize_mqtt_clients():
#     from app.models import Device
#     try:
#         # Check if table exists first
#         if not Device.__table__.exists(db.engine):
#             return
            
#         for device in Device.query.all():
#             create_mqtt_client(device)
#     except Exception as e:
#         current_app.logger.error(f"MQTT initialization error: {str(e)}")

# def initialize_mqtt_clients():
#     from app.models import Device
#     try:
#         # Check if table exists using proper SQLAlchemy method
#         if not db.engine.dialect.has_table(db.engine, Device.__tablename__):
#             return
            
#         for device in Device.query.all():
#             create_mqtt_client(device)
#     except Exception as e:
#         current_app.logger.error(f"MQTT initialization error: {str(e)}")

def initialize_mqtt_clients():
    from app.models import Device
    try:
        # Use proper table existence check
        inspector = db.inspect(db.engine)
        if not inspector.has_table(Device.__tablename__):
            return
            
        for device in Device.query.all():
            create_mqtt_client(device)
    except Exception as e:
        current_app.logger.error(f"MQTT initialization error: {str(e)}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        new_point = DataPoint(
            temperature_c=data['tempC'],  # Changed from temp to tempC
            temperature_f=data['tempF'],  # Added Fahrenheit field
            device_id=userdata['device_id']
        )
        db.session.add(new_point)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error processing MQTT message: {str(e)}")