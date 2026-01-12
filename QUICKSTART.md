# ⚡ SecureWipe - Quick Start Guide

## 🚀 Get Started in 3 Minutes!

### Step 1: Install Dependencies
Open terminal in project folder:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
==================================================
DOCWIPING Professional Data Wiping Platform
==================================================
✓ Database initialized
✓ AI Chatbot ready (Multilingual: EN, ES, FR, DE)
✓ ML Model loaded
✓ Authentication system active
✓ Payment system integrated
✓ Email notifications enabled
✓ Admin Panel: /admin (username: admin, password: admin123)
==================================================
 * Running on http://0.0.0.0:5000
```

### Step 3: Access the Platform
Open your browser and visit:
- **Main Site:** http://localhost:5000
- **Login Page:** http://localhost:5000/login
- **Admin Panel:** http://localhost:5000/admin

---

## 👤 Login Credentials

### Admin Account
```
Username: admin
Password: admin123
Email: diziavatar@gmail.com
```
**⚠️ Change this password immediately for production use!**

### Create User Account
1. Go to http://localhost:5000/register
2. Fill in:
   - Username
   - Email
   - Password
   - Phone (optional for SMS notifications)
3. Click "Create Account"
4. Login at http://localhost:5000/login

---

## 🎯 Quick Feature Tour

### For Users:

#### 1. **Dashboard** (http://localhost:5000/dashboard)
- View your statistics
- See total wipes, data wiped, payments
- Access recent wipe history

#### 2. **Start Wiping Data**
- Select wipe type: File Upload or Text Data
- Choose wipe level:
  - Quick (1-Pass) - $5.99
  - Secure (3-Pass) - $9.99
  - Military (7-Pass) - $14.99
- Pick payment method
- Click "Start Secure Wipe"
- Receive instant email notification!

#### 3. **View History**
- **Wipe History:** http://localhost:5000/wipe-history
- **Payment History:** http://localhost:5000/payment-history

#### 4. **Export Reports**
- Click "Export Report" button
- Download PDF certificate with all wipe operations

### For Admins:

#### 1. **Admin Dashboard** (http://localhost:5000/admin)
- Total users count
- Total wipes performed
- Total revenue generated
- System status

#### 2. **Manage Users**
- View all registered users
- See their wipe counts
- Monitor user activity

#### 3. **Track Payments**
- All transaction records
- Revenue analytics
- Payment method breakdown

#### 4. **Monitor Operations**
- System-wide wipe history
- Performance metrics
- Success rates

---

## 📧 Email Notifications Setup (Optional)

To enable email notifications:

### Step 1: Get Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Go to "App passwords"
4. Select "Mail" and "Windows Computer"
5. Click "Generate"
6. Copy the 16-character password

### Step 2: Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:MAIL_PASSWORD="your-app-password-here"
```

**Windows (CMD):**
```cmd
set MAIL_PASSWORD=your-app-password-here
```

**Linux/Mac:**
```bash
export MAIL_PASSWORD="your-app-password-here"
```

### Step 3: Restart Application
```bash
python app.py
```

Now emails will be sent on:
- User registration
- Wipe completion
- Payment confirmation

---

## 🎨 Website Pages

### Public Pages
- **Home:** http://localhost:5000/
- **About:** http://localhost:5000/about
- **Privacy Policy:** http://localhost:5000/privacy
- **Security Standards:** http://localhost:5000/standards

### User Pages (Login Required)
- **Dashboard:** http://localhost:5000/dashboard
- **Wipe History:** http://localhost:5000/wipe-history
- **Payment History:** http://localhost:5000/payment-history

### Admin Pages (Admin Login Required)
- **Admin Panel:** http://localhost:5000/admin

---

## 💡 Common Tasks

### Change Admin Password
1. Login as admin
2. Go to database: `instance/secure_wipe.db`
3. Or create new admin via code:
```python
from app import app, db, User
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('new_secure_password')
    db.session.commit()
```

### Test Wipe Operation
1. Login as user
2. Go to Dashboard
3. Upload a test file (any file)
4. Select "Quick Wipe"
5. Choose "Credit/Debit Card"
6. Click "Start Secure Wipe"
7. Confirm the dialog
8. Check your email for confirmation!

### View Database
```bash
# Windows
sqlite3 instance\secure_wipe.db
# Linux/Mac
sqlite3 instance/secure_wipe.db

# Inside SQLite:
.tables                    # List all tables
SELECT * FROM user;        # View users
SELECT * FROM payment;     # View payments
SELECT * FROM wipe_history; # View wipes
.exit                      # Exit
```

### Clear All Data (Reset)
```bash
# Delete database
rm instance/secure_wipe.db   # Linux/Mac
del instance\secure_wipe.db  # Windows

# Restart app (recreates database)
python app.py
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Module Not Found Error
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Email Not Sending
**Issue:** No email received after wipe

**Solution:**
1. Check MAIL_PASSWORD is set
2. Verify Gmail App Password is correct
3. Check spam folder
4. Ensure internet connection

### Database Locked
**Error:** `database is locked`

**Solution:**
```bash
# Close all connections and restart
python app.py
```

---

## 📊 Test Data

### Sample Test Files
Create test files to wipe:
```bash
# Windows
echo "Test data to wipe" > test.txt

# Linux/Mac
echo "Test data to wipe" > test.txt
```

### Sample Text Data
Use this in "Text Data Wipe":
```
This is sensitive data that needs to be securely wiped.
Credit Card: 1234-5678-9012-3456
Social Security: 123-45-6789
```

---

## 🎓 Learning Path

1. ✅ **Day 1:** Setup & Login
   - Install dependencies
   - Run application
   - Login as admin
   - Explore dashboard

2. ✅ **Day 2:** User Features
   - Create user account
   - Perform wipe operation
   - View history
   - Export report

3. ✅ **Day 3:** Admin Features
   - Access admin panel
   - Manage users
   - Track payments
   - Monitor operations

4. ✅ **Day 4:** Advanced
   - Configure email
   - Customize pricing
   - Add new features
   - Deploy to production

---

## 🌟 Next Steps

- [ ] Change default admin password
- [ ] Configure email notifications
- [ ] Test all wipe levels
- [ ] Explore admin panel
- [ ] Read security standards
- [ ] Review privacy policy
- [ ] Export your first report
- [ ] Deploy to production (see DEPLOYMENT.md)

---

## 📞 Need Help?

**Email:** diziavatar@gmail.com
**Support:** Available 24/7

---

## 🎉 You're Ready!

Your SecureWipe platform is now running. Start exploring and enjoy secure data wiping!

**Remember:** Always verify you have permission before wiping any data!

---

**Happy Wiping! 🔐**
