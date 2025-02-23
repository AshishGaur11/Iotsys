from flask import Blueprint, render_template, jsonify, flash, redirect, url_for  # Added missing imports
from flask_login import login_required, current_user
from app.forms import DeviceForm
from app.models import Device, DataPoint
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(
            name=form.name.data,
            broker=form.broker.data,
            topic=form.topic.data,
            mqtt_user=form.mqtt_user.data,
            mqtt_password=form.mqtt_password.data,
            owner=current_user
        )
        db.session.add(device)
        db.session.commit()
        flash('Device added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    devices = current_user.devices
    return render_template('dashboard.html', form=form, devices=devices)

@main_bp.route('/data/<int:device_id>')
@login_required
def device_data(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        return jsonify([])
    
    data = device.data_points.order_by(DataPoint.timestamp.desc()).limit(50).all()
    
    # Updated return statement with correct fields
    return jsonify([{
        'timestamp': point.timestamp.isoformat(),
        'temperature_c': point.temperature_c,
        'temperature_f': point.temperature_f
    } for point in data])