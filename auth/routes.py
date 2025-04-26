from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, current_user
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Temporary storage for OTPs
otp_storage = {}


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        # Generate and store OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[phone] = {
            'otp': otp,
            'expires': datetime.now() + timedelta(minutes=5)
        }

        # Send OTP via Twilio
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        client.messages.create(
            body=f'Your verification code is: {otp}',
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=phone
        )

        return redirect(url_for('auth.verify_otp', phone=phone))

    return render_template('login.html')


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    phone = request.args.get('phone')

    if request.method == 'POST':
        user_otp = request.form['otp']
        stored_otp = otp_storage.get(phone)

        if not stored_otp or datetime.now() > stored_otp['expires']:
            flash('OTP expired. Please request a new one.', 'error')
            return redirect(url_for('auth.login'))

        if user_otp == stored_otp['otp']:
            # In a real app, you would create/load a user here
            login_user(user)  # You'll need a User model
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Please try again.', 'error')

    return render_template('otp_verify.html', phone=phone)