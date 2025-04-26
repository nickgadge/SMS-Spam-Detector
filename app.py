from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import joblib
import os
from dotenv import load_dotenv

# Initialize app
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Mock User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Mock user database
users = {'1': User('1')}

# Configure Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Load ML models
MODELS_LOADED = False
try:
    sms_model = joblib.load('models/sms_model.pkl')
    sms_vectorizer = joblib.load('models/sms_vectorizer.pkl')
    MODELS_LOADED = True
except Exception as e:
    print(f"Model loading error: {e}")

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users['1']
        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', models_loaded=MODELS_LOADED)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# SMS Spam Detection
@app.route('/sms', methods=['GET', 'POST'])
@login_required
def sms():
    if not MODELS_LOADED:
        flash('Model not loaded. Try again later.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            # Transform and predict
            vector = sms_vectorizer.transform([message])
            prediction = sms_model.predict(vector)[0]
            probs = sms_model.predict_proba(vector)[0]

            result = {
                'message': message,
                'is_spam': bool(prediction),
                'spam_prob': round(probs[1] * 100, 2),
                'ham_prob': round(probs[0] * 100, 2)
            }
            return render_template('result.html', result=result)

    return render_template('sms.html')

# Email Spam Detection (upload file)
@app.route('/email', methods=['GET', 'POST'])
@login_required
def email():
    if not MODELS_LOADED:
        flash('Model not loaded. Try again later.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            vector = sms_vectorizer.transform([content])
            prediction = sms_model.predict(vector)[0]
            probs = sms_model.predict_proba(vector)[0]

            result = {
                'message': content,
                'is_spam': bool(prediction),
                'spam_prob': round(probs[1] * 100, 2),
                'ham_prob': round(probs[0] * 100, 2)
            }
            return render_template('result.html', result=result)
        else:
            flash('Invalid file type. Please upload a .txt file.', 'danger')
            return redirect(url_for('email'))

    return render_template('email.html')

# Run
if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    app.run(debug=True)
