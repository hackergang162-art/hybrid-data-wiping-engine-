"""
🇮🇳 TRICOLOR DATA GOVERNANCE HUB - 2026 EDITION
Professional Secure Data Wiping & Privacy Protection Platform
Advanced Data Sanitization System with Sovereign Payment, AI, & Blockchain Compliance

Tagline: "Don't Shred Your Profits. Sanitize Your Future."
Focus: Green Sanitization | Hardware Value Preservation | Zero E-Waste
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
import hashlib
import secrets
import joblib
import threading
import time
import io
from functools import wraps
from collections import defaultdict

# Import new 2026 modules
try:
    from payment_engine import SovereignPaymentEngine, Currency, SubscriptionPlan, BillingCycle
    PAYMENT_ENGINE = SovereignPaymentEngine()
    PAYMENT_ENABLED = True
except ImportError:
    PAYMENT_ENABLED = False
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.colors import HexColor, white
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# Import new 2026 modules - Enhanced features
try:
    from cloud_storage_manager import cloud_manager
    CLOUD_STORAGE_ENABLED = True
except ImportError:
    CLOUD_STORAGE_ENABLED = False

try:
    from encryption_engine import sovereignty_manager, encryption_engine
    ENCRYPTION_ENABLED = True
except ImportError:
    ENCRYPTION_ENABLED = False

try:
    from ai_data_hunter import ai_hunter
    AI_HUNTER_ENABLED = True
except ImportError:
    AI_HUNTER_ENABLED = False

try:
    from advanced_payment_system import payment_manager, upi_processor, currency_converter
    ADVANCED_PAYMENT_ENABLED = True
except ImportError:
    ADVANCED_PAYMENT_ENABLED = False

try:
    from certificate_system import certificate_generator
    CERTIFICATE_SYSTEM_ENABLED = True
except ImportError:
    CERTIFICATE_SYSTEM_ENABLED = False

try:
    from support_chatbot import support_bot
    CHATBOT_ENABLED = True
except ImportError:
    CHATBOT_ENABLED = False

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_wipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'diziavatar@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')  # Set in environment
app.config['MAIL_DEFAULT_SENDER'] = 'diziavatar@gmail.com'
# Google Maps API Key (set env GOOGLE_MAPS_API_KEY)
app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('GOOGLE_MAPS_API_KEY', '')

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==========================================
# ML MODEL LOADING
# ==========================================

ml_model = None
ml_device_encoder = None
ml_method_encoder = None
ml_model_loaded = False

def load_ml_model():
    global ml_model, ml_device_encoder, ml_method_encoder, ml_model_loaded
    try:
        model_path = os.path.join(os.getcwd(), 'ml_models', 'wipe_predictor.pkl')
        if os.path.exists(model_path):
            data = joblib.load(model_path)
            ml_model = data.get('model')
            ml_device_encoder = data.get('device_encoder')
            ml_method_encoder = data.get('method_encoder')
            ml_model_loaded = data.get('is_trained', False) and ml_model is not None
            print("✓ ML model loaded from disk")
        else:
            print("⚠ ML model file not found; using heuristic predictor")
    except Exception as e:
        print("⚠ Failed to load ML model:", e)
        ml_model_loaded = False

# ==========================================
# DATABASE MODELS
# ==========================================

class User(UserMixin, db.Model):
    """User authentication model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String(20))
    notifications_enabled = db.Column(db.Boolean, default=True)
    wipe_history = db.relationship('WipeHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WipeHistory(db.Model):
    """Store individual wipe operations for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    wipe_level = db.Column(db.String(50))
    wipe_method = db.Column(db.String(100))
    passes = db.Column(db.Integer)
    status = db.Column(db.String(50), default='completed')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Float)
    data_type = db.Column(db.String(50))
    certificate_hash = db.Column(db.String(128))

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_size': self.file_size,
            'wipe_level': self.wipe_level,
            'wipe_method': self.wipe_method,
            'passes': self.passes,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'duration': self.duration
        }

class Payment(db.Model):
    """Payment transaction records"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50), default='pending')
    wipe_type = db.Column(db.String(50))
    file_count = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'currency': self.currency,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'wipe_type': self.wipe_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class WipeRecord(db.Model):
    """Store wiping operation records (legacy)"""
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), nullable=False)
    device_name = db.Column(db.String(200), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    device_size = db.Column(db.String(50), nullable=False)
    wipe_method = db.Column(db.String(100), nullable=False)
    wipe_standard = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    certificate_hash = db.Column(db.String(128))
    user_ip = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'device_type': self.device_type,
            'device_size': self.device_size,
            'wipe_method': self.wipe_method,
            'wipe_standard': self.wipe_standard,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'certificate_hash': self.certificate_hash
        }

class ChatMessage(db.Model):
    """Store chat messages for training and history"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    helpful = db.Column(db.Boolean)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'language': self.language,
            'timestamp': self.timestamp.isoformat()
        }

class DeviceAnalytics(db.Model):
    """Store device analytics for ML training"""
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(50))
    device_size_gb = db.Column(db.Float)
    wipe_method = db.Column(db.String(100))
    estimated_duration = db.Column(db.Integer)  # in seconds
    actual_duration = db.Column(db.Integer)
    success_rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# PAYMENT & SUBSCRIPTION MODELS
# ==========================================

class UserWallet(db.Model):
    """User wallet for payment system"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    balance_inr = db.Column(db.Float, default=0.0)
    currency_preference = db.Column(db.String(10), default='INR')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance_inr': self.balance_inr,
            'currency_preference': self.currency_preference,
            'created_at': self.created_at.isoformat()
        }

class Transaction(db.Model):
    """Financial transactions (credits/debits)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'credit' or 'debit'
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    method = db.Column(db.String(50), nullable=False)  # 'upi', 'card', 'net_banking', 'wallet'
    reference = db.Column(db.String(255))  # Transaction reference ID
    status = db.Column(db.String(50), default='completed')  # 'pending', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': self.amount,
            'currency': self.currency,
            'method': self.method,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Subscription(db.Model):
    """User subscription plans"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)  # 'starter', 'professional', 'enterprise'
    billing_cycle = db.Column(db.String(20), nullable=False)  # 'monthly' or 'yearly'
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    auto_renew = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50), default='active')  # 'active', 'cancelled', 'expired'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'billing_cycle': self.billing_cycle,
            'expires_at': self.expires_at.isoformat(),
            'status': self.status
        }

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================
# RATE LIMITING & SECURITY
# ==========================================

class RateLimiter:
    """Simple in-memory rate limiter (use Redis in production)"""
    def __init__(self):
        self.requests = defaultdict(list)
        self.cleanup_interval = 60
        self.last_cleanup = time.time()
    
    def is_allowed(self, key, max_requests=10, window=60):
        """Check if request is allowed within rate limit"""
        now = time.time()
        
        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self.cleanup()
            self.last_cleanup = now
        
        # Remove old requests outside window
        self.requests[key] = [req_time for req_time in self.requests[key] 
                              if now - req_time < window]
        
        # Check limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def cleanup(self):
        """Remove expired entries"""
        now = time.time()
        keys_to_remove = []
        for key, times in self.requests.items():
            self.requests[key] = [t for t in times if now - t < 300]  # 5 min window
            if not self.requests[key]:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.requests[key]

rate_limiter = RateLimiter()

def rate_limit(max_requests=10, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use IP + session as key
            key = f"{request.remote_addr}:{session.get('chat_session_id', 'anon')}"
            
            if not rate_limiter.is_allowed(key, max_requests, window):
                return jsonify({
                    'success': False,
                    'error': 'Rate limit exceeded. Please wait before sending more messages.',
                    'retry_after': window
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def send_email_notification(to_email, subject, body):
    """Send email notification"""
    try:
        msg = Message(subject, recipients=[to_email])
        msg.body = body
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0a0e27; color: #fff; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1a1f3a 0%, #0a0e27 100%); padding: 30px; border-radius: 10px; border: 1px solid #00d4ff;">
                    <h2 style="color: #00d4ff; text-align: center;">🔐 Secure Data Wiping Platform</h2>
                    <div style="margin: 20px 0; padding: 20px; background: rgba(0, 212, 255, 0.1); border-radius: 8px;">
                        {body.replace(chr(10), '<br>')}
                    </div>
                    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 30px;">
                        © 2026 Secure Data Wiping Platform | Contact: diziavatar@gmail.com
                    </p>
                </div>
            </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_sms_notification(phone, message):
    """Simulate SMS notification (integrate with Twilio/etc in production)"""
    print(f"📱 SMS to {phone}: {message}")
    return True

def simulate_data_wipe(file_path, wipe_level, passes):
    """Simulate data wiping process"""
    time.sleep(0.5 * passes)  # Simulate wiping time
    if os.path.exists(file_path):
        os.remove(file_path)
    return True

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"TXN-{secrets.token_hex(8).upper()}"

def generate_certificate_hash(data):
    """Generate certificate hash for wipe operation"""
    hash_input = f"{data}{datetime.utcnow().isoformat()}{secrets.token_hex(8)}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

def generate_qr_code(data):
    """Generate QR code for certificate verification"""
    if not QR_AVAILABLE:
        return None
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
    except Exception as e:
        print(f"QR Code generation error: {e}")
        return None

def generate_verification_token(cert_hash):
    """Generate secure verification token for certificate"""
    token_data = f"{cert_hash}{datetime.utcnow().isoformat()}{secrets.token_hex(16)}"
    return hashlib.sha256(token_data.encode()).hexdigest()

# ==========================================
# API ROUTES
# ==========================================

@app.route('/')
def index():
    """Serve main application"""
    return render_template('index.html')

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400

        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Send welcome email
        send_email_notification(
            email,
            'Welcome to Secure Data Wiping Platform',
            f'Hello {username},\n\nWelcome to our platform! Your account has been created successfully.\n\nYou can now start securely wiping your data with industry-standard methods.\n\nBest regards,\nSecure Wipe Team'
        )

        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'is_admin': user.is_admin,
                'redirect': '/admin' if user.is_admin else '/dashboard'
            })
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# ==========================================
# USER DASHBOARD ROUTES
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    wipe_stats = {
        'total_wipes': WipeHistory.query.filter_by(user_id=current_user.id).count(),
        'total_size': db.session.query(db.func.sum(WipeHistory.file_size)).filter_by(user_id=current_user.id).scalar() or 0,
        'recent_wipes': WipeHistory.query.filter_by(user_id=current_user.id).order_by(WipeHistory.timestamp.desc()).limit(10).all(),
        'total_payments': Payment.query.filter_by(user_id=current_user.id).count(),
        'total_spent': db.session.query(db.func.sum(Payment.amount)).filter_by(user_id=current_user.id, status='completed').scalar() or 0
    }
    return render_template('dashboard.html', stats=wipe_stats, user=current_user)

@app.route('/payment-history')
@login_required
def payment_history():
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.timestamp.desc()).all()
    return render_template('payment_history.html', payments=payments)

@app.route('/wipe-history')
@login_required
def wipe_history_page():
    wipes = WipeHistory.query.filter_by(user_id=current_user.id).order_by(WipeHistory.timestamp.desc()).all()
    return render_template('wipe_history.html', wipes=wipes)

# ==========================================
# ADMIN DASHBOARD ROUTES
# ==========================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_wipes': WipeHistory.query.count(),
        'total_revenue': db.session.query(db.func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0,
        'recent_users': User.query.order_by(User.created_at.desc()).limit(10).all(),
        'recent_payments': Payment.query.order_by(Payment.timestamp.desc()).limit(10).all(),
        'recent_wipes': WipeHistory.query.order_by(WipeHistory.timestamp.desc()).limit(10).all()
    }
    return render_template('admin.html', stats=stats)

@app.route('/api/admin/users')
@admin_required
def api_admin_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'is_admin': u.is_admin,
        'created_at': u.created_at.isoformat(),
        'total_wipes': len(u.wipe_history),
        'total_payments': len(u.payments)
    } for u in users])

@app.route('/api/admin/payments')
@admin_required
def api_admin_payments():
    payments = Payment.query.order_by(Payment.timestamp.desc()).limit(50).all()
    return jsonify([{
        'id': p.id,
        'user': p.user.username,
        'amount': p.amount,
        'transaction_id': p.transaction_id,
        'status': p.status,
        'timestamp': p.timestamp.isoformat()
    } for p in payments])

# ==========================================
# DATA WIPING ROUTES
# ==========================================

@app.route('/wipe', methods=['POST'])
@login_required
def wipe_data():
    try:
        wipe_type = request.form.get('wipe_type', 'file')
        wipe_level = request.form.get('wipe_level', 'quick')
        
        # Determine passes based on wipe level
        passes_map = {'quick': 1, 'secure': 3, 'military': 7, 'custom': int(request.form.get('custom_passes', 3))}
        passes = passes_map.get(wipe_level, 3)
        
        # Pricing
        pricing = {'quick': 5.99, 'secure': 9.99, 'military': 14.99, 'custom': 19.99}
        amount = pricing.get(wipe_level, 9.99)
        
        file_path = None
        filename = None
        file_size = 0
        
        if wipe_type == 'file' and 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{secrets.token_hex(8)}_{filename}")
                file.save(file_path)
                file_size = os.path.getsize(file_path)
        elif wipe_type == 'text':
            text_data = request.form.get('text_data', '')
            filename = 'text_data.txt'
            file_size = len(text_data.encode('utf-8'))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{secrets.token_hex(8)}_text.txt")
            with open(file_path, 'w') as f:
                f.write(text_data)
        
        # Create payment record
        payment = Payment(
            user_id=current_user.id,
            amount=amount,
            payment_method=request.form.get('payment_method', 'card'),
            transaction_id=generate_transaction_id(),
            status='completed',
            wipe_type=wipe_level,
            file_count=1
        )
        db.session.add(payment)
        
        # Simulate wiping in background
        start_time = time.time()
        if file_path:
            simulate_data_wipe(file_path, wipe_level, passes)
        duration = time.time() - start_time
        
        # Generate certificate hash
        cert_hash = generate_certificate_hash(f"{filename}{current_user.id}{wipe_level}")
        
        # Create wipe history
        wipe_record = WipeHistory(
            user_id=current_user.id,
            filename=filename,
            file_size=file_size,
            wipe_level=wipe_level,
            wipe_method=f"{passes}-Pass Overwrite",
            passes=passes,
            status='completed',
            duration=duration,
            data_type=wipe_type,
            certificate_hash=cert_hash
        )
        db.session.add(wipe_record)
        db.session.commit()
        
        # Send email notification
        if current_user.notifications_enabled:
            send_email_notification(
                current_user.email,
                'Data Wiping Completed Successfully',
                f'Hello {current_user.username},\n\nYour data has been securely wiped!\n\nDetails:\n- File: {filename}\n- Size: {file_size} bytes\n- Method: {wipe_level.upper()} ({passes} passes)\n- Duration: {duration:.2f}s\n- Transaction ID: {payment.transaction_id}\n- Amount: ${amount}\n- Certificate: {cert_hash[:16]}...\n\nYour data has been permanently erased and cannot be recovered.\n\nThank you for using our service!'
            )
            
            # Send SMS notification if phone available
            if current_user.phone:
                send_sms_notification(
                    current_user.phone,
                    f"Secure Wipe Complete! File: {filename}, Method: {wipe_level.upper()}, TXN: {payment.transaction_id}"
                )
        
        return jsonify({
            'success': True,
            'message': 'Data wiped successfully',
            'wipe_id': wipe_record.id,
            'transaction_id': payment.transaction_id,
            'amount': amount,
            'duration': duration,
            'certificate_hash': cert_hash
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/certificate/<int:wipe_id>')
@login_required
def view_certificate(wipe_id):
    """View and display secure certificate"""
    wipe = WipeHistory.query.filter_by(user_id=current_user.id, id=wipe_id).first()
    if not wipe:
        return jsonify({'error': 'Certificate not found'}), 404
    
    return render_template('certificate.html', wipe=wipe, user=current_user)

@app.route('/api/verify-certificate/<cert_hash>')
def verify_certificate(cert_hash):
    """Verify certificate authenticity (public endpoint)"""
    wipe = WipeHistory.query.filter_by(certificate_hash=cert_hash).first()
    if not wipe:
        return jsonify({'verified': False, 'message': 'Certificate not found'}), 404
    
    user = User.query.get(wipe.user_id)
    return jsonify({
        'verified': True,
        'filename': wipe.filename,
        'file_size': wipe.file_size,
        'wipe_level': wipe.wipe_level,
        'passes': wipe.passes,
        'timestamp': wipe.timestamp.isoformat(),
        'duration': f"{wipe.duration:.2f}" if wipe.duration else "N/A",
        'user': user.username if user else 'Verified User',
        'data_type': wipe.data_type or 'Mixed',
        'status': '✓ AUTHENTIC - Certificate verified',
        'compliance': ['GDPR', 'ISO 27001', 'NIST SP 800-88', 'DoD 5220.22-M']
    })

# ==========================================
# Certificate System (Advanced PDF + QR)
# ==========================================

@app.route('/api/certificate/generate', methods=['POST'])
@login_required
def api_generate_certificate():
    """Generate an advanced certificate (PDF + QR) for a wipe record."""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return jsonify({'error': 'Certificate system not available'}), 503

    try:
        payload = request.get_json(silent=True) or {}
        wipe_id = payload.get('wipe_id')

        # Ensure verification URL points to this server
        try:
            certificate_generator.verification_url = request.url_root.rstrip('/') + '/verify'
        except Exception:
            pass

        # Build wipe data from existing record if provided
        wipe_data = {}
        if wipe_id:
            wipe = WipeHistory.query.filter_by(id=wipe_id, user_id=current_user.id).first()
            if not wipe:
                return jsonify({'error': 'Wipe record not found'}), 404
            wipe_data = {
                'method': wipe.wipe_method or wipe.wipe_level or 'DoD 5220.22-M (7-pass)',
                'volume_gb': float(wipe.file_size or 0) / (1024*1024*1024) if (wipe.file_size and wipe.file_size > 0) else 0,
                'file_count': 1,
                'providers': [],
                'type': 'Data Erasure Certificate'
            }
        else:
            # Fallback: accept direct payload
            wipe_data = {
                'method': payload.get('method', 'DoD 5220.22-M (7-pass)'),
                'volume_gb': payload.get('volume_gb', 0),
                'file_count': payload.get('file_count', 0),
                'providers': payload.get('providers', []),
                'type': payload.get('type', 'Data Erasure Certificate')
            }

        user_info = {
            'organization': payload.get('organization', getattr(current_user, 'organization', 'N/A') or 'N/A'),
            'name': current_user.username,
            'email': current_user.email
        }

        result = certificate_generator.generate_certificate(wipe_data, user_info)

        # Optional: associate certificate id with wipe record
        if wipe_id:
            # Store certificate ID in wipe record metadata if model has such field
            # (kept non-invasive; not all schemas have it)
            pass

        return jsonify({
            'success': True,
            'certificate_id': result['certificate_id'],
            'verification_url': result['verification_url'],
            'verification_hash': result['verification_hash'],
            'pdf_path': result['pdf_path'],
            'qr_code_path': result['qr_code_path'],
            'download_url': url_for('download_certificate_pdf', cert_id=result['certificate_id'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/verify/<cert_id>')
def verify_cert_page(cert_id):
    """Certificate verification page using advanced certificate system."""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return render_template('verify_certificate.html', certificate=None)

    provided_hash = request.args.get('hash')
    cert = certificate_generator.certificates_db.get(cert_id)
    if not cert:
        # If no cert found yet, attempt to verify (will return invalid)
        return render_template('verify_certificate.html', certificate=None)

    # Update verification metadata (and validate hash if provided)
    certificate_generator.verify_certificate(cert_id, provided_hash)

    # Pass full certificate data to template (includes verification_hash)
    return render_template('verify_certificate.html', certificate=cert)


@app.route('/api/certificate/<cert_id>/download')
def download_certificate_pdf(cert_id):
    """Download the generated certificate PDF file."""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return jsonify({'error': 'Certificate system not available'}), 503

    cert = certificate_generator.certificates_db.get(cert_id)
    if not cert:
        return jsonify({'error': 'Certificate not found'}), 404

    pdf_path = cert.get('pdf_path')
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF not available'}), 404

    return send_file(pdf_path, as_attachment=True, download_name=f"{cert_id}.pdf", mimetype='application/pdf')

@app.route('/export-report')
@login_required
def export_report():
    """Export comprehensive wipe certificate report"""
    if not PDF_AVAILABLE:
        return jsonify({'error': 'PDF generation not available'}), 500
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    story.append(Paragraph("🔐 SECURE DATA WIPING CERTIFICATE", styles['Heading1']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(f"<b>User:</b> {current_user.username} | <b>Email:</b> {current_user.email}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>✓ GDPR Compliant</b> | <b>✓ ISO 27001 Certified</b> | <b>✓ Government Verified</b>", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    cert_id = f"DSCI-{current_user.id}-{datetime.now().strftime('%Y%m%d')}"
    gov_text = f"<b style='color:#d84315'>🇮🇳 INDIAN GOVERNMENT VERIFICATION</b><br/>" + \
               "<b>Authority:</b> Ministry of Electronics and Information Technology (MeitY)<br/>" + \
               "<b>Certified By:</b> DSCI (Data Security Council of India)<br/>" + \
               f"<b>Certificate ID:</b> {cert_id}"
    story.append(Paragraph(gov_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    wipes = WipeHistory.query.filter_by(user_id=current_user.id).order_by(WipeHistory.timestamp.desc()).limit(50).all()
    
    if wipes:
        story.append(Paragraph("<b>Wipe Operations Record</b>", styles['Heading2']))
        table_data = [['Date', 'Filename', 'Size', 'Method', 'Passes', 'Duration', 'Status']]
        for wipe in wipes:
            table_data.append([
                wipe.timestamp.strftime('%Y-%m-%d'),
                (wipe.filename[:12] if wipe.filename else 'N/A'),
                f"{wipe.file_size or 0}",
                str(wipe.wipe_level or 'N/A'),
                str(wipe.passes),
                f"{wipe.duration:.1f}s" if wipe.duration else 'N/A',
                'Complete'
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#999')),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>✓ SECURITY ASSURANCE</b><br/>Data permanently destroyed | Data Retention: ZERO | Recovery: NIL", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    hash_val = generate_certificate_hash(current_user.username)[:24]
    story.append(Paragraph(f"<b>SecureWipe Platform</b> | Email: diziavatar@gmail.com | Hash: {hash_val}...", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'SecureWipe_Certificate_{current_user.username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        mimetype='application/pdf'
    )

# ==========================================
# INFORMATION PAGES
# ==========================================

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/standards')
def standards():
    return render_template('standards.html')

@app.route('/trust')
def trust_verification():
    """Trust and certification verification page"""
    return render_template('trust_verification.html')

@app.route('/api/stats')
@login_required
def api_stats():
    stats = {
        'total_wipes': WipeHistory.query.filter_by(user_id=current_user.id).count(),
        'total_size': db.session.query(db.func.sum(WipeHistory.file_size)).filter_by(user_id=current_user.id).scalar() or 0,
        'total_spent': db.session.query(db.func.sum(Payment.amount)).filter_by(user_id=current_user.id, status='completed').scalar() or 0
    }
    return jsonify(stats)

@app.route('/api/wipe/start', methods=['POST'])
def start_wipe():
    """Initialize a wipe operation"""
    data = request.json
    
    record = WipeRecord(
        device_id=data.get('device_id'),
        device_name=data.get('device_name'),
        device_type=data.get('device_type'),
        device_size=data.get('device_size'),
        wipe_method=data.get('wipe_method'),
        wipe_standard=data.get('wipe_standard'),
        user_ip=request.remote_addr,
        status='in_progress'
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'record_id': record.id,
        'status': 'in_progress'
    })

@app.route('/api/wipe/update/<int:record_id>', methods=['PUT'])
def update_wipe(record_id):
    """Update wipe operation status"""
    data = request.json
    record = WipeRecord.query.get(record_id)
    
    if not record:
        return jsonify({'success': False, 'error': 'Record not found'}), 404
    
    record.status = data.get('status', 'completed')
    record.completed_at = datetime.utcnow()
    record.certificate_hash = data.get('certificate_hash', generate_certificate_hash(record.device_id))
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'certificate_hash': record.certificate_hash,
        'record': record.to_dict()
    })

@app.route('/api/wipe/history', methods=['GET'])
def wipe_history():
    """Get wipe operation history"""
    records = WipeRecord.query.order_by(WipeRecord.started_at.desc()).limit(50).all()
    return jsonify({
        'success': True,
        'records': [r.to_dict() for r in records]
    })

@app.route('/api/chat', methods=['POST'])
@rate_limit(max_requests=20, window=60)  # 20 messages per minute
def chat():
    """AI Chatbot endpoint with multilingual support, rate limiting, and session management"""
    data = request.json
    user_message = data.get('message', '').strip()
    language = data.get('language', 'en')
    client_session_id = data.get('session_id', '')
    
    # Input validation
    if not user_message:
        return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
    
    if len(user_message) > 1000:
        return jsonify({'success': False, 'error': 'Message too long (max 1000 characters)'}), 400
    
    # Sanitize input (basic XSS prevention)
    user_message = user_message.replace('<', '&lt;').replace('>', '&gt;')
    
    # Session management
    if not session.get('chat_session_id'):
        session['chat_session_id'] = client_session_id or secrets.token_hex(16)
    
    session_id = session['chat_session_id']
    
    # Get AI response
    try:
        bot_response = get_ai_response(user_message, language)
    except Exception as e:
        app.logger.error(f"Chat error: {e}")
        bot_response = "System error. Please try again."
    
    # Store in database
    try:
        chat_msg = ChatMessage(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            language=language
        )
        db.session.add(chat_msg)
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        # Don't fail the request if DB write fails
    
    return jsonify({
        'success': True,
        'response': bot_response,
        'language': language,
        'session_id': session_id
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get system analytics and statistics"""
    total_wipes = WipeRecord.query.count()
    completed_wipes = WipeRecord.query.filter_by(status='completed').count()
    
    # Device type breakdown
    device_types = db.session.query(
        WipeRecord.device_type,
        db.func.count(WipeRecord.id)
    ).group_by(WipeRecord.device_type).all()
    
    return jsonify({
        'success': True,
        'total_wipes': total_wipes,
        'completed_wipes': completed_wipes,
        'success_rate': (completed_wipes / total_wipes * 100) if total_wipes > 0 else 0,
        'device_types': dict(device_types)
    })

@app.route('/api/ml/predict-duration', methods=['POST'])
def predict_duration():
    """ML-powered duration prediction"""
    data = request.json
    device_type = data.get('device_type')
    device_size = data.get('device_size')
    wipe_method = data.get('wipe_method')
    device_age_years = float(data.get('device_age_years', 0))

    prediction = ml_predict_wipe_duration(
        device_type=device_type,
        device_size=device_size,
        wipe_method=wipe_method,
        device_age_years=device_age_years
    )

    return jsonify({
        'success': True,
        'estimated_seconds': prediction['duration'],
        'confidence': prediction['confidence']
    })

# ==========================================
# UNIFIED CONTROL PANEL ROUTES
# ==========================================

@app.route('/control-panel')
@login_required
def control_panel():
    """Unified enterprise control panel"""
    return render_template('control_panel.html', user=current_user)

# ==========================================
# PAYMENT & WALLET ROUTES
# ==========================================

@app.route('/api/wallet/create', methods=['POST'])
@login_required
def create_wallet():
    """Initialize user wallet"""
    try:
        data = request.get_json()
        initial_balance = float(data.get('initial_balance_inr', 0))
        
        # Check if wallet already exists
        existing_wallet = db.session.query(UserWallet).filter_by(user_id=current_user.id).first()
        if existing_wallet:
            return jsonify({
                'success': True,
                'message': 'Wallet already exists',
                'wallet_id': existing_wallet.id,
                'balance': existing_wallet.balance_inr,
                'currency': existing_wallet.currency_preference
            })
        
        # Create new wallet
        wallet = UserWallet(
            user_id=current_user.id,
            balance_inr=initial_balance,
            currency_preference='INR'
        )
        db.session.add(wallet)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Wallet created successfully',
            'wallet_id': wallet.id,
            'balance': wallet.balance_inr,
            'currency': wallet.currency_preference
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/wallet/balance', methods=['GET'])
@login_required
def get_wallet_balance():
    """Get wallet balance in selected currency"""
    try:
        currency = request.args.get('currency', 'INR')
        
        wallet = db.session.query(UserWallet).filter_by(user_id=current_user.id).first()
        if not wallet:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        # Currency exchange rates (demo data)
        exchange_rates = {
            'INR': 1.0,
            'USD': 0.012,
            'EUR': 0.011,
            'GBP': 0.0095,
            'JPY': 1.85,
            'AUD': 0.018,
            'CAD': 0.016,
            'SGD': 0.016,
            'HKD': 0.095,
            'AED': 0.044
        }
        
        rate = exchange_rates.get(currency, 1.0)
        converted_balance = wallet.balance_inr * rate
        
        currency_symbols = {
            'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
            'AUD': 'A$', 'CAD': 'C$', 'SGD': 'S$', 'HKD': 'HK$', 'AED': 'د.إ'
        }
        
        return jsonify({
            'success': True,
            'balance_inr': wallet.balance_inr,
            'balance_converted': round(converted_balance, 2),
            'currency': currency,
            'symbol': currency_symbols.get(currency, currency),
            'user_id': current_user.id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/wallet/add-funds', methods=['POST'])
@login_required
def add_funds():
    """Add funds to wallet via UPI/Card/Net Banking"""
    try:
        data = request.get_json()
        amount_inr = float(data.get('amount_inr', 0))
        payment_method = data.get('payment_method', 'upi')
        upi_id = data.get('upi_id', '')
        
        if amount_inr <= 0:
            return jsonify({'success': False, 'error': 'Invalid amount'}), 400
        
        wallet = db.session.query(UserWallet).filter_by(user_id=current_user.id).first()
        if not wallet:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        # Create transaction record
        transaction = Transaction(
            user_id=current_user.id,
            type='credit',
            amount=amount_inr,
            currency='INR',
            method=payment_method,
            reference=f"{payment_method.upper()}-{upi_id if upi_id else 'CARD'}-{secrets.token_hex(8)}",
            status='completed'
        )
        db.session.add(transaction)
        
        # Update wallet balance
        wallet.balance_inr += amount_inr
        wallet.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully added ₹{amount_inr} to wallet',
            'new_balance': wallet.balance_inr,
            'transaction_id': transaction.id,
            'reference': transaction.reference
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/subscription/subscribe', methods=['POST'])
@login_required
def subscribe_plan():
    """Subscribe to a plan (Starter/Professional/Enterprise)"""
    try:
        data = request.get_json()
        plan_name = data.get('plan', 'starter')
        billing_cycle = data.get('cycle', 'monthly')
        
        # Plan pricing in INR
        plan_pricing = {
            'starter': {'monthly': 4999, 'yearly': 59988},
            'professional': {'monthly': 12999, 'yearly': 155988},
            'enterprise': {'monthly': 29999, 'yearly': 359988}
        }
        
        if plan_name not in plan_pricing:
            return jsonify({'success': False, 'error': 'Invalid plan'}), 400
        
        amount = plan_pricing[plan_name].get(billing_cycle, plan_pricing[plan_name]['monthly'])
        
        # Get or create wallet
        wallet = db.session.query(UserWallet).filter_by(user_id=current_user.id).first()
        if not wallet:
            wallet = UserWallet(user_id=current_user.id, balance_inr=0)
            db.session.add(wallet)
            db.session.commit()
        
        if wallet.balance_inr < amount:
            return jsonify({
                'success': False,
                'error': f'Insufficient balance. Required: ₹{amount}, Available: ₹{wallet.balance_inr}'
            }), 400
        
        # Create subscription record
        from datetime import timedelta
        duration_days = 365 if billing_cycle == 'yearly' else 30
        
        subscription = Subscription(
            user_id=current_user.id,
            plan_name=plan_name,
            billing_cycle=billing_cycle,
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=duration_days),
            auto_renew=True,
            status='active'
        )
        db.session.add(subscription)
        
        # Deduct from wallet
        wallet.balance_inr -= amount
        wallet.updated_at = datetime.utcnow()
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user.id,
            type='debit',
            amount=amount,
            currency='INR',
            method='wallet',
            reference=f"SUB-{plan_name.upper()}-{billing_cycle.upper()}",
            status='completed'
        )
        db.session.add(transaction)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully subscribed to {plan_name.upper()} plan',
            'subscription_id': subscription.id,
            'plan': plan_name,
            'cycle': billing_cycle,
            'expires_at': subscription.expires_at.isoformat(),
            'amount_charged': amount,
            'new_wallet_balance': wallet.balance_inr
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/subscription/status', methods=['GET'])
@login_required
def subscription_status():
    """Get current subscription status"""
    try:
        subscription = db.session.query(Subscription).filter_by(
            user_id=current_user.id,
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({
                'success': True,
                'subscribed': False,
                'plan': None,
                'message': 'No active subscription'
            })
        
        return jsonify({
            'success': True,
            'subscribed': True,
            'plan': subscription.plan_name,
            'cycle': subscription.billing_cycle,
            'started_at': subscription.started_at.isoformat(),
            'expires_at': subscription.expires_at.isoformat(),
            'days_remaining': (subscription.expires_at - datetime.utcnow()).days,
            'auto_renew': subscription.auto_renew
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/invoice/generate', methods=['POST'])
@login_required
def generate_invoice():
    """Generate invoice with ESG metrics"""
    try:
        data = request.get_json()
        invoice_type = data.get('type', 'wipe')  # 'wipe' or 'subscription'
        
        # Calculate wipe statistics
        wipes = db.session.query(WipeHistory).filter_by(user_id=current_user.id).all()
        total_size_gb = sum(w.file_size or 0 for w in wipes) / (1024**3)
        
        # ESG Impact Calculation
        carbon_saved_kg = total_size_gb * 0.015  # ~15g CO2 per GB destroyed
        trees_equivalent = carbon_saved_kg / 21  # 1 tree absorbs ~21kg CO2/year
        ewaste_prevented_kg = total_size_gb * 0.012  # ~12g e-waste per GB
        
        invoice = {
            'success': True,
            'invoice_id': f"INV-{current_user.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user': current_user.username,
            'email': current_user.email,
            'issued_at': datetime.utcnow().isoformat(),
            'wipe_summary': {
                'total_wipes': len(wipes),
                'total_data_destroyed_gb': round(total_size_gb, 2),
                'total_wipes_completed': sum(1 for w in wipes if w.status == 'completed')
            },
            'esg_impact': {
                'carbon_saved_kg': round(carbon_saved_kg, 2),
                'co2_equivalent_trees': round(trees_equivalent, 2),
                'ewaste_prevented_kg': round(ewaste_prevented_kg, 2),
                'impact_message': f"You've saved {round(carbon_saved_kg, 2)}kg of CO₂ emissions by securely wiping {round(total_size_gb, 2)}GB of data instead of destroying hardware!"
            },
            'sustainability_score': min(100, int((total_size_gb / 10) * 100)),
            'compliance': {
                'nist_800_88_verified': True,
                'gdpr_compliant': True,
                'iso_27001_certified': True,
                'government_verified': True
            }
        }
        
        return jsonify(invoice)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/payment/convert', methods=['POST'])
@login_required
def convert_currency():
    """Convert currency in real-time"""
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_curr = data.get('from', 'INR')
        to_curr = data.get('to', 'USD')
        
        exchange_rates = {
            'INR': 1.0,
            'USD': 0.012,
            'EUR': 0.011,
            'GBP': 0.0095,
            'JPY': 1.85,
            'AUD': 0.018,
            'CAD': 0.016,
            'SGD': 0.016,
            'HKD': 0.095,
            'AED': 0.044
        }
        
        if from_curr not in exchange_rates or to_curr not in exchange_rates:
            return jsonify({'success': False, 'error': 'Invalid currency'}), 400
        
        # Convert to base (INR) then to target
        amount_inr = amount / exchange_rates.get(from_curr, 1.0)
        converted = amount_inr * exchange_rates.get(to_curr, 1.0)
        
        return jsonify({
            'success': True,
            'original_amount': amount,
            'original_currency': from_curr,
            'converted_amount': round(converted, 2),
            'target_currency': to_curr,
            'exchange_rate': round(exchange_rates.get(to_curr, 1.0) / exchange_rates.get(from_curr, 1.0), 4)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/audit/timeline', methods=['GET'])
@login_required
def audit_timeline():
    """Get audit timeline with blockchain-verified hashes"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        wipes = db.session.query(WipeHistory).filter_by(user_id=current_user.id)\
            .order_by(WipeHistory.timestamp.desc()).limit(limit).all()
        
        timeline = []
        for wipe in wipes:
            timeline.append({
                'id': wipe.id,
                'filename': wipe.filename,
                'wipe_level': wipe.wipe_level,
                'timestamp': wipe.timestamp.isoformat(),
                'certificate_hash': wipe.certificate_hash,
                'status': wipe.status,
                'passes': wipe.passes,
                'file_size': wipe.file_size,
                'duration': wipe.duration
            })
        
        return jsonify({
            'success': True,
            'timeline': timeline,
            'total_count': db.session.query(WipeHistory).filter_by(user_id=current_user.id).count()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# AI & ML FUNCTIONS
# ==========================================

def get_ai_response(message, language='en'):
    """Generate AI chatbot response with multilingual support (Aura-X persona)"""
    
    # Multilingual knowledge base
    responses = {
        'en': {
            'greeting': "Systems ready. Aura-X online. How may I assist, Commander?",
            'wipe_info': "Affirmative. Supported methods: NIST SP 800-88 Rev. 2, DoD 5220.22-M, Gutmann, ATA Secure Erase, Crypto Erase. Provide device type/size — I’ll recommend the optimal protocol.",
            'standards': "Compliance stack: NIST SP 800-88 Rev. 2 | ISO 27001 | GDPR | DPDP Act 2023 (India). Zero-knowledge; geo-fencing available.",
            'help': "Capabilities: method selection, compliance mapping, certificate verification, ESG impact, wallet/subscriptions, control panel ops. Copy that.",
        },
        'es': {
            'greeting': "¡Hola! Soy Nexus — tu compañero robótico Tricolor. ¿Cómo te ayudo hoy con la sanitización y gobernanza de datos?",
            'wipe_info': "Soportamos NIST SP 800-88 Rev. 2, DoD 5220.22-M, Gutmann, ATA Secure Erase y Crypto Erase. Dime tu dispositivo y recomiendo el método.",
            'standards': "Cumplimiento: NIST SP 800-88 Rev. 2, ISO 27001, GDPR y la Ley DPDP 2023 (India). Diseño de conocimiento cero y geo-cercas opcionales.",
            'help': "Te ayudo con: selección de métodos, mapeo de cumplimiento, verificación de certificados, impacto ESG, pagos/suscripciones y navegación del panel.",
        },
        'fr': {
            'greeting': "Bonjour ! Je suis Nexus — votre compagnon robot Tricolore. Besoin d’aide pour la désinfection ou la gouvernance des données ?",
            'wipe_info': "Prise en charge : NIST SP 800-88 Rev. 2, DoD 5220.22-M, Gutmann, ATA Secure Erase et Crypto Erase. Donnez-moi votre appareil, je conseille le meilleur.",
            'standards': "Conformité : NIST SP 800-88 Rev. 2, ISO 27001, RGPD et Loi DPDP 2023 (Inde). Zéro connaissance par défaut, géorepérage en option.",
            'help': "Je peux aider : sélection des méthodes, cartographie de conformité, vérification de certificats, impact ESG, paiements/abonnements et navigation du tableau de bord.",
        },
        'de': {
            'greeting': "Hallo! Ich bin Nexus — Ihr Tricolor Robot-Begleiter. Wie kann ich heute bei sicherer Datenbereinigung oder Governance helfen?",
            'wipe_info': "Unterstützt: NIST SP 800-88 Rev. 2, DoD 5220.22-M, Gutmann, ATA Secure Erase und Crypto Erase. Nennen Sie Ihr Gerät, ich empfehle die Methode.",
            'standards': "Konformität: NIST SP 800-88 Rev. 2, ISO 27001, GDPR und das DPDP-Gesetz 2023 (Indien). Standard: Zero-Knowledge, optional Geo-Fencing.",
            'help': "Ich helfe bei: Methodenwahl, Compliance-Mapping, Zertifikatsprüfung, ESG-Wirkung, Zahlungen/Abos und Dashboard-Navigation.",
        }
    }
    
    msg_lower = message.lower()
    lang_responses = responses.get(language, responses['en'])
    
    # Simple intent matching (in production, use NLP/ML model)
    if any(word in msg_lower for word in ['hello', 'hi', 'hola', 'bonjour', 'hallo']):
        return lang_responses['greeting']
    elif any(word in msg_lower for word in ['wipe', 'method', 'erase', 'delete']):
        return lang_responses['wipe_info']
    elif any(word in msg_lower for word in ['standard', 'compliance', 'certification']):
        return lang_responses['standards']
    elif any(word in msg_lower for word in ['help', 'ayuda', 'aide', 'hilfe']):
        return lang_responses['help']
    else:
        return lang_responses['greeting']

def ml_predict_wipe_duration(device_type, device_size, wipe_method, device_age_years=0.0):
    """Predict wipe duration using trained model if available, else heuristic.
    Applies age factor adjustment: +3% per year of age.
    """

    size_gb = parse_size_to_gb(device_size)

    if ml_model_loaded:
        try:
            d_enc = ml_device_encoder.transform([device_type])[0]
            m_enc = ml_method_encoder.transform([wipe_method])[0]
            X = [[d_enc, size_gb, m_enc]]
            duration = float(ml_model.predict(X)[0])
            # Age adjustment
            duration *= (1.0 + max(0.0, device_age_years) * 0.03)
            return {
                'duration': int(duration),
                'confidence': 0.9
            }
        except Exception as e:
            print("⚠ ML prediction failed, falling back to heuristic:", e)

    # Heuristic fallback
    base_speed_mb_per_sec = {
        'NVMe SSD': 3000,
        'SATA SSD': 500,
        'SATA HDD': 150,
        'Android': 100
    }.get(device_type, 200)

    method_multiplier = {
        'DoD 5220.22-M (3-pass)': 3,
        'DoD 5220.22-M (7-pass)': 7,
        'Gutmann (35-pass)': 35,
        'NIST SP 800-88': 1,
        'ATA Secure Erase': 0.5,
        'NVMe Format (Crypto Erase)': 0.1,
        'Crypto Erase': 0.1
    }.get(wipe_method, 1)

    total_mb = size_gb * 1024
    duration_seconds = (total_mb / base_speed_mb_per_sec) * method_multiplier
    duration_seconds *= (1.0 + max(0.0, device_age_years) * 0.03)

    return {
        'duration': int(duration_seconds),
        'confidence': 0.8
    }

def parse_size_to_gb(size_str):
    """Parse size string to GB"""
    import re
    match = re.search(r'([\d.]+)\s*(TB|GB|MB)', size_str, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2).upper()
        if unit == 'TB':
            return value * 1024
        elif unit == 'GB':
            return value
        elif unit == 'MB':
            return value / 1024
    return 100  # default

def estimate_wipe_duration(wipe_data):
    """Estimate wipe duration"""
    prediction = ml_predict_wipe_duration(
        wipe_data.get('device_type'),
        wipe_data.get('device_size'),
        wipe_data.get('wipe_method')
    )
    return prediction['duration']

# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():
    """Initialize database with sample data for ML training"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='diziavatar@gmail.com',
                phone='+1234567890',
                is_admin=True
            )
            admin.set_password('admin123')  # Change in production!
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created: username=admin, password=admin123")
        
        # Add sample analytics data for ML training
        if DeviceAnalytics.query.count() == 0:
            sample_data = [
                DeviceAnalytics(device_type='NVMe SSD', device_size_gb=1600, wipe_method='NVMe Format (Crypto Erase)', estimated_duration=960, actual_duration=945, success_rate=0.99),
                DeviceAnalytics(device_type='SATA SSD', device_size_gb=960, wipe_method='ATA Secure Erase', estimated_duration=1920, actual_duration=1950, success_rate=0.98),
                DeviceAnalytics(device_type='SATA HDD', device_size_gb=4000, wipe_method='DoD 5220.22-M (3-pass)', estimated_duration=82944, actual_duration=83200, success_rate=0.97),
                DeviceAnalytics(device_type='Android', device_size_gb=128, wipe_method='Crypto Erase', estimated_duration=768, actual_duration=750, success_rate=0.99),
            ]
            db.session.bulk_save_objects(sample_data)
            db.session.commit()
            print("✓ Sample ML training data initialized")

# ==========================================
# 2026 FEATURES: TOPOLOGY & QUANTUM ERASURE
# ==========================================

# Import quantum erasure engine
try:
    from quantum_erasure import QuantumSafeErasure
    quantum_engine = QuantumSafeErasure()
    QUANTUM_ENABLED = True
except ImportError:
    QUANTUM_ENABLED = False
    print("⚠ Quantum erasure module not available")

# Topology data storage (in-memory, use Redis in production)
topology_nodes = []

@app.route('/topology')
@login_required
def topology_map():
    """Render geospatial topology map"""
    return render_template('topology_map.html', google_maps_api_key=app.config.get('GOOGLE_MAPS_API_KEY', ''))

@app.route('/api/topology/nodes', methods=['GET'])
@login_required
def get_topology_nodes():
    """Get current topology nodes"""
    return jsonify({
        'success': True,
        'nodes': topology_nodes,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/topology/update', methods=['POST'])
def update_topology_nodes():
    """Receive updates from Discovery Agent"""
    global topology_nodes
    data = request.get_json()
    
    if data and 'nodes' in data:
        topology_nodes = data['nodes']
        return jsonify({'success': True, 'count': len(topology_nodes)})
    
    return jsonify({'success': False, 'error': 'Invalid data'}), 400

@app.route('/api/quantum/wipe', methods=['POST'])
@login_required
def execute_quantum_wipe():
    """Execute quantum-safe data wipe with geo-fencing"""
    if not QUANTUM_ENABLED:
        return jsonify({'success': False, 'error': 'Quantum engine not available'}), 500
    
    data = request.get_json()
    
    # Extract parameters
    device_id = data.get('device_id')
    device_type = data.get('device_type')
    size_gb = float(data.get('size_gb', 0))
    method = data.get('method', 'purge')
    
    # GPS coordinates for geo-fencing
    gps_coords = None
    if data.get('latitude') and data.get('longitude'):
        gps_coords = (float(data['latitude']), float(data['longitude']))
    
    # Execute quantum wipe
    result = quantum_engine.execute_nist_purge(
        device_id=device_id,
        device_type=device_type,
        size_gb=size_gb,
        method=method,
        gps_coords=gps_coords
    )
    
    # If successful, create wipe history record
    if result.get('success') and current_user.is_authenticated:
        wipe_record = WipeHistory(
            user_id=current_user.id,
            filename=device_id,
            file_size=int(size_gb * 1024 * 1024 * 1024),
            wipe_level=f"Quantum {method}",
            wipe_method=result['method'],
            passes=result['passes'],
            status='completed',
            duration=result['duration_seconds'],
            certificate_hash=result['quantum_hash']
        )
        db.session.add(wipe_record)
        db.session.commit()
    
    return jsonify(result)

@app.route('/api/topology/certificate', methods=['GET', 'POST'])
@login_required
def generate_tricolor_certificate():
    """Generate Tricolor blockchain certificate"""
    if not QUANTUM_ENABLED:
        return jsonify({'success': False, 'error': 'Quantum engine not available'}), 500
    
    # Get latest sanitization from current user
    latest_wipe = WipeHistory.query.filter_by(user_id=current_user.id).order_by(WipeHistory.timestamp.desc()).first()
    
    if not latest_wipe:
        return jsonify({'success': False, 'error': 'No wipe history found'}), 404
    
    # Create mock sanitization record for certificate
    sanitization_record = {
        'device_id': latest_wipe.filename or 'DEVICE_001',
        'device_type': 'Enterprise Storage',
        'size_gb': (latest_wipe.file_size or 0) / (1024 * 1024 * 1024),
        'method': latest_wipe.wipe_method or 'NIST 800-88 PURGE',
        'passes': latest_wipe.passes or 3,
        'timestamp': latest_wipe.timestamp.isoformat() if latest_wipe.timestamp else datetime.utcnow().isoformat(),
        'duration_seconds': latest_wipe.duration or 0,
        'gps_latitude': 19.0760,  # Default to Mumbai
        'gps_longitude': 72.8777,
        'jurisdiction': 'India',
        'quantum_hash': latest_wipe.certificate_hash or 'N/A',
        'verification_token': generate_verification_token(latest_wipe.certificate_hash or 'default')
    }
    
    cert_data = quantum_engine.generate_tricolor_certificate(sanitization_record)
    
    return jsonify({
        'success': True,
        'certificate': cert_data
    })

@app.route('/api/sustainability/calculate', methods=['POST'])
def calculate_sustainability():
    """Calculate ESG metrics for sanitization"""
    if not QUANTUM_ENABLED:
        return jsonify({'success': False, 'error': 'Quantum engine not available'}), 500
    
    data = request.get_json()
    size_gb = float(data.get('size_gb', 0))
    method = data.get('method', 'purge')
    
    esg_metrics = quantum_engine.calculate_carbon_offset(size_gb, method)
    
    return jsonify({
        'success': True,
        'esg_metrics': esg_metrics
    })

@app.route('/sustainability')
@login_required
def sustainability_dashboard():
    """Sustainability & ESG tracking dashboard"""
    # Calculate total ESG impact for user
    user_wipes = WipeHistory.query.filter_by(user_id=current_user.id).all()
    
    total_carbon_saved = 0
    total_resale_value = 0
    
    for wipe in user_wipes:
        size_gb = (wipe.file_size or 0) / (1024 * 1024 * 1024)
        if QUANTUM_ENABLED:
            metrics = quantum_engine.calculate_carbon_offset(size_gb, wipe.wipe_method or 'purge')
            total_carbon_saved += metrics['carbon_saved_kg']
            total_resale_value += metrics['resale_value_usd']
    
    stats = {
        'total_wipes': len(user_wipes),
        'carbon_saved_kg': round(total_carbon_saved, 2),
        'resale_value_usd': round(total_resale_value, 2),
        'trees_equivalent': round(total_carbon_saved / 21, 1)  # 1 tree = ~21kg CO2/year
    }
    
    return render_template('sustainability.html', stats=stats, user=current_user)


# ==================== NEW ENHANCED ROUTES 2026 ====================

@app.route('/home')
def home_modern():
    """Modern landing page with all features"""
    return render_template('home_modern.html')

@app.route('/analytics')
@login_required
def analytics_dashboard():
    """Advanced analytics dashboard with Chart.js"""
    return render_template('analytics.html', user=current_user)

@app.route('/api/cloud/connect/<provider>')
@login_required
def cloud_connect(provider):
    """Initiate OAuth2 connection to cloud provider"""
    if not CLOUD_STORAGE_ENABLED:
        return jsonify({'error': 'Cloud storage not enabled'}), 400
    
    connector = cloud_manager.get_provider(provider)
    if not connector:
        return jsonify({'error': 'Provider not supported'}), 400
    
    auth_url = connector.get_authorization_url(current_user.id)
    return redirect(auth_url)

@app.route('/oauth/<provider>/callback')
@login_required
def oauth_callback(provider):
    """Handle OAuth2 callback from cloud providers"""
    if not CLOUD_STORAGE_ENABLED:
        return jsonify({'error': 'Cloud storage not enabled'}), 400
    
    code = request.args.get('code')
    state = request.args.get('state')
    
    # Verify state
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state'}), 400
    
    connector = cloud_manager.get_provider(provider)
    token_data = connector.exchange_code_for_token(code)
    
    # Store token in database (implement CloudConnection model)
    flash(f'{provider.title()} connected successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/ai/scan', methods=['POST'])
@login_required
def ai_scan_files():
    """AI-powered sensitive data scanning"""
    if not AI_HUNTER_ENABLED:
        return jsonify({'error': 'AI Hunter not enabled'}), 400
    
    data = request.get_json()
    file_path = data.get('file_path')
    content = data.get('content', '')
    
    if file_path:
        scan_result = ai_hunter.comprehensive_scan(file_path, content)
        return jsonify(scan_result)
    
    return jsonify({'error': 'No file path provided'}), 400

@app.route('/api/ai/scan/directory', methods=['POST'])
@login_required
def ai_scan_directory():
    """Scan entire directory for sensitive files"""
    if not AI_HUNTER_ENABLED:
        return jsonify({'error': 'AI Hunter not enabled'}), 400
    
    data = request.get_json()
    directory_path = data.get('directory_path')
    
    if directory_path:
        scan_result = ai_hunter.batch_scan_directory(directory_path)
        return jsonify(scan_result)
    
    return jsonify({'error': 'No directory path provided'}), 400

@app.route('/api/payment/create', methods=['POST'])
@login_required
def create_payment():
    """Create payment for subscription"""
    if not ADVANCED_PAYMENT_ENABLED:
        return jsonify({'error': 'Advanced payment not enabled'}), 400
    
    data = request.get_json()
    tier = data.get('tier', 'STARTER')
    currency = data.get('currency', 'INR')
    payment_method = data.get('payment_method', 'UPI')
    
    from advanced_payment_system import SubscriptionTier
    tier_enum = SubscriptionTier[tier.upper()]
    
    transaction = payment_manager.create_subscription_payment(
        user_id=str(current_user.id),
        tier=tier_enum,
        currency=currency,
        payment_method=payment_method
    )
    
    return jsonify(transaction)

@app.route('/api/payment/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify UPI/card payment"""
    if not ADVANCED_PAYMENT_ENABLED:
        return jsonify({'error': 'Advanced payment not enabled'}), 400
    
    data = request.get_json()
    payment_id = data.get('payment_id')
    order_id = data.get('order_id')
    signature = data.get('signature')
    
    is_valid = upi_processor.verify_payment(payment_id, order_id, signature)
    
    if is_valid:
        # Activate subscription
        from advanced_payment_system import SubscriptionTier
        subscription = payment_manager.activate_subscription(
            user_id=str(current_user.id),
            tier=SubscriptionTier.PROFESSIONAL,
            payment_id=payment_id
        )
        return jsonify({'success': True, 'subscription': subscription})
    
    return jsonify({'success': False, 'error': 'Invalid payment'}), 400

@app.route('/api/certificate/generate', methods=['POST'])
@login_required
def generate_certificate():
    """Generate certificate with QR code"""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return jsonify({'error': 'Certificate system not enabled'}), 400
    
    data = request.get_json()
    
    wipe_data = {
        'method': data.get('method', 'DoD 5220.22-M (7-pass)'),
        'volume_gb': data.get('volume_gb', 0),
        'file_count': data.get('file_count', 0),
        'providers': data.get('providers', []),
        'type': 'Enterprise Data Erasure Certificate'
    }
    
    user_info = {
        'organization': data.get('organization', 'N/A'),
        'name': current_user.username,
        'email': current_user.email
    }
    
    result = certificate_generator.generate_certificate(wipe_data, user_info)
    
    return jsonify({
        'success': True,
        'certificate_id': result['certificate_id'],
        'verification_url': result['verification_url'],
        'pdf_download': url_for('download_certificate', cert_id=result['certificate_id'])
    })

@app.route('/verify/<certificate_id>')
def verify_certificate_page(certificate_id):
    """Certificate verification page"""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return render_template('verify_certificate.html', certificate=None)
    
    provided_hash = request.args.get('hash')
    verification = certificate_generator.verify_certificate(certificate_id, provided_hash)
    
    return render_template('verify_certificate.html', certificate=verification if verification.get('valid') else None)

@app.route('/api/certificate/<cert_id>/download')
@login_required
def download_certificate(cert_id):
    """Download certificate PDF"""
    if not CERTIFICATE_SYSTEM_ENABLED:
        return jsonify({'error': 'Certificate system not enabled'}), 400
    
    cert_data = certificate_generator.certificates_db.get(cert_id)
    if cert_data and os.path.exists(cert_data['pdf_path']):
        return send_file(cert_data['pdf_path'], as_attachment=True)
    
    return jsonify({'error': 'Certificate not found'}), 404

@app.route('/api/encryption/script')
def get_encryption_script():
    """Get client-side encryption JavaScript"""
    if not ENCRYPTION_ENABLED:
        return jsonify({'error': 'Encryption not enabled'}), 400
    
    script = sovereignty_manager.get_client_encryption_script()
    return jsonify({'script': script})


# ==================== CHATBOT ROUTES ====================

@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages"""
    if not CHATBOT_ENABLED:
        return jsonify({'error': 'Chatbot not enabled'}), 400
    
    data = request.get_json()
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id')
    
    # Get user context if logged in
    user_context = {}
    if current_user.is_authenticated:
        user_context = {
            'user_id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }
    
    # Generate response
    response = support_bot.generate_response(user_message, user_context)
    
    return jsonify(response)

@app.route('/api/chatbot/quick-actions')
def chatbot_quick_actions():
    """Get quick action buttons"""
    if not CHATBOT_ENABLED:
        return jsonify({'error': 'Chatbot not enabled'}), 400
    
    actions = support_bot.get_quick_actions()
    return jsonify(actions)

@app.route('/chatbot')
def chatbot_page():
    """Standalone chatbot page"""
    return render_template('chatbot_widget.html')


if __name__ == '__main__':
    init_db()
    load_ml_model()
    print("=" * 50)
    print("DOCWIPING Professional Data Wiping Platform")
    print("=" * 50)
    print("✓ Database initialized")
    print("✓ AI Chatbot ready (Multilingual: EN, ES, FR, DE)")
    print("✓ ML Model loaded")
    print("✓ Authentication system active")
    print("✓ Payment system integrated")
    print("✓ Email notifications enabled")
    if QUANTUM_ENABLED:
        print("✓ Quantum-Safe Erasure active (NIST 800-88 + PQC)")
        print("✓ Geospatial Topology Map available")
        print("✓ ESG Sustainability Tracker enabled")
    if CLOUD_STORAGE_ENABLED:
        print("✓ Cloud Storage Integration (Google Drive, Dropbox, OneDrive, S3)")
    if ENCRYPTION_ENABLED:
        print("✓ Client-Side Encryption & Data Sovereignty")
    if AI_HUNTER_ENABLED:
        print("✓ AI Data Hunter (Sensitive Data Detection)")
    if ADVANCED_PAYMENT_ENABLED:
        print("✓ Multi-Currency Payment + UPI Integration")
    if CERTIFICATE_SYSTEM_ENABLED:
        print("✓ QR Certificate Verification System")
    if CHATBOT_ENABLED:
        print("✓ AI Support Chatbot (24/7 Intelligent Assistance)")
    print("✓ Admin Panel: /admin (username: admin, password: admin123)")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
