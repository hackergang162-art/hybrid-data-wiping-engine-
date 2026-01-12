# 🔐 SecureWipe - Professional Data Wiping & Privacy Protection Platform

**Enterprise-Grade Data Sanitization System with Authentication, Payments & Notifications**

A complete full-stack web application for secure data wiping with user management, admin panel, payment processing, email/SMS notifications, and ML-powered features.

---

## ✨ Key Features

### 🔒 Data Wiping Engine
- **Multiple Wipe Methods** (Quick/Secure/Military/Custom)
- **File Upload Support** - Any file type
- **Text Data Wiping**
- **Browser Data Clearing**
- **Real-time Progress Tracking**
- **SHA-256 Certificate Generation**

### 👥 User Management
- User Registration & Login
- Secure Password Hashing (bcrypt)
- User Dashboard with Statistics
- Profile Management
- Role-Based Access Control

### 👑 Admin Panel
- Complete User Management
- Payment Tracking & Revenue Analytics
- Wipe Operation Monitoring
- System Statistics Dashboard

### 💳 Payment System
- Multiple Payment Methods (Card/PayPal/Crypto)
- Transaction ID Generation
- Payment History Tracking
- Invoice Generation

### 📧 Notifications
- **Email Notifications** (Flask-Mail)
  - Welcome emails
  - Wipe completion alerts
  - Transaction confirmations
- **SMS Notifications** (optional)
- Professional HTML email templates

### 🤖 AI & ML Features
- Multilingual AI Chatbot (EN, ES, FR, DE)
- ML-Powered Duration Prediction
- Device Analytics & Optimization
- Smart Wipe Recommendations

### 📊 Reporting
- PDF Report Generation (ReportLab)
- Wipe History Export
- Payment History Export
- Certificate Downloads
- Compliance Documentation

### 🛡️ Security & Compliance
- **Standards:** DoD 5220.22-M, NIST SP 800-88, ISO 27001, GDPR
- HTTPS/TLS Encryption
- Password Hashing
- CSRF Protection
- XSS Prevention
- Zero Data Retention Policy

### 🎨 Modern UI/UX
- Cybersecurity Dark Theme
- Animated Backgrounds
- Responsive Design
- Glassmorphism Effects
- Accessibility Support

---

## 🚀 Tech Stack

### Backend
- Flask 3.0, SQLAlchemy, Flask-Login, Flask-Mail
- SQLite Database
- ML: scikit-learn, joblib

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Responsive Design

---

## 📁 Project Structure

```
demo app/
├── app.py                      # Main Flask application
├── ml_training.py              # ML model training
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── templates/                  # HTML templates
│   ├── index.html             # Landing page
│   ├── login.html             # Login
│   ├── register.html          # Registration
│   ├── dashboard.html         # User dashboard
│   ├── admin.html             # Admin panel
│   ├── payment_history.html   # Payments
│   ├── wipe_history.html      # Wipe records
│   ├── about.html             # About page
│   ├── privacy.html           # Privacy policy
│   └── standards.html         # Security standards
└── static/
    ├── script.js              # JavaScript
    └── styles.css             # Styling
```

---

## 🔧 Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Environment Setup (Optional)
Create `.env` file:
```env
MAIL_PASSWORD=your_gmail_app_password
SECRET_KEY=your_secret_key
```

### Step 3: Run Application
```bash
python app.py
```

Server starts at: `http://localhost:5000`

---

## 👤 Default Accounts

### Admin
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `diziavatar@gmail.com`

### User
- Register at: `/register`

---

## 📋 Usage

### Users:
1. Register → Login → Dashboard
2. Upload file or enter text
3. Select wipe level
4. Choose payment method
5. Start wipe → Receive notifications
6. View history → Export reports

### Admins:
1. Login as admin
2. Access `/admin` dashboard
3. Manage users, payments, operations
4. Monitor revenue and analytics

---

## 💰 Pricing

| Level | Passes | Price |
|-------|--------|-------|
| Quick | 1 | $5.99 |
| Secure | 3 | $9.99 |
| Military | 7 | $14.99 |
| Custom | Variable | $19.99 |

---

## 🔌 API Endpoints

### Authentication
- `POST /register` - Register user
- `POST /login` - Login
- `GET /logout` - Logout

### Operations
- `POST /wipe` - Start wipe
- `GET /wipe-history` - View history
- `GET /payment-history` - View payments
- `GET /export-report` - Download PDF

### Admin
- `GET /admin` - Admin dashboard
- `GET /api/admin/users` - List users
- `GET /api/admin/payments` - List payments

---

## 📧 Contact

**Email:** diziavatar@gmail.com  
**Support:** 24/7 Available

---

## 🔒 Security

1. Change default admin password
2. Set strong SECRET_KEY
3. Use environment variables
4. Enable HTTPS in production
5. Regular backups
6. Monitor logs

---

## 🌟 Features

✅ User Authentication & Authorization  
✅ Payment Processing & History  
✅ Email & SMS Notifications  
✅ Admin Panel with Analytics  
✅ PDF Report Generation  
✅ ML-Powered Predictions  
✅ Multi-Language Support  
✅ Mobile Responsive Design  
✅ Zero Data Retention Policy  
✅ Compliance Certified  

---

## 📄 License

Educational & demonstration purposes.

**Disclaimer:** Simulation tool. Use hardware-level methods in production.

---

## 🤝 Contributing

Contact: **diziavatar@gmail.com**

---

**Built with ❤️ for cybersecurity and data privacy**

© 2026 SecureWipe Platform | All Rights Reserved
