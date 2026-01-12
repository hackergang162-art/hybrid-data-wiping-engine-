# 🚀 SecureWipe Deployment Guide

## Quick Start (Local Development)

### 1. Install Dependencies
```bash
cd "c:\Users\snmeh\Desktop\demo app"
pip install -r requirements.txt
```

### 2. Configure Email (Optional)
Create `.env` file:
```env
MAIL_PASSWORD=your_gmail_app_password
```

**To get Gmail App Password:**
1. Go to Google Account Settings
2. Security → 2-Step Verification
3. App Passwords → Generate
4. Copy password to `.env`

### 3. Run Application
```bash
python app.py
```

### 4. Access Application
- **Main Site:** http://localhost:5000
- **Login:** http://localhost:5000/login
- **Admin Panel:** http://localhost:5000/admin

### 5. Default Admin Credentials
- Username: `admin`
- Password: `admin123`
- **⚠️ CHANGE IN PRODUCTION!**

---

## 🌐 Production Deployment

### Option 1: Vercel (Recommended for Demo)

#### Prerequisites
```bash
npm install -g vercel
```

#### Deploy
```bash
vercel
```

#### Environment Variables (Vercel Dashboard)
```
MAIL_PASSWORD=your_app_password
SECRET_KEY=random_secret_key
```

### Option 2: Heroku

#### Prerequisites
```bash
heroku login
```

#### Deploy
```bash
git init
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku master
```

#### Set Environment Variables
```bash
heroku config:set MAIL_PASSWORD=your_password
heroku config:set SECRET_KEY=your_secret_key
```

### Option 3: AWS EC2

#### 1. Launch EC2 Instance
- Ubuntu 22.04 LTS
- t2.micro (free tier)
- Open ports: 22, 80, 443, 5000

#### 2. SSH into Instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 3. Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

#### 4. Upload Application
```bash
scp -r -i your-key.pem . ubuntu@your-ec2-ip:~/securewipe
```

#### 5. Setup Virtual Environment
```bash
cd ~/securewipe
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/securewipe
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 7. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/securewipe /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### 8. Run with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 9. Setup Systemd Service
```bash
sudo nano /etc/systemd/system/securewipe.service
```

Add:
```ini
[Unit]
Description=SecureWipe Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/securewipe
Environment="PATH=/home/ubuntu/securewipe/venv/bin"
ExecStart=/home/ubuntu/securewipe/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

#### 10. Start Service
```bash
sudo systemctl enable securewipe
sudo systemctl start securewipe
```

### Option 4: Docker

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Build & Run
```bash
docker build -t securewipe .
docker run -p 5000:5000 -e MAIL_PASSWORD=your_pass securewipe
```

---

## 🔐 Production Security Checklist

### ✅ Pre-Deployment
- [ ] Change admin password
- [ ] Set strong SECRET_KEY
- [ ] Configure environment variables
- [ ] Enable HTTPS/SSL
- [ ] Update CORS settings
- [ ] Configure firewall rules
- [ ] Setup database backups
- [ ] Test email notifications
- [ ] Review security headers

### ✅ Post-Deployment
- [ ] Monitor logs
- [ ] Test all features
- [ ] Verify payment processing
- [ ] Check email delivery
- [ ] Test admin panel
- [ ] Verify SSL certificate
- [ ] Setup monitoring alerts
- [ ] Create backup schedule

---

## 📊 Database Migration

### SQLite to PostgreSQL (Production)

#### 1. Install PostgreSQL
```bash
pip install psycopg2-binary
```

#### 2. Update Configuration
```python
# In app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/securewipe'
```

#### 3. Migrate Data
```bash
python migrate_db.py
```

---

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-Factor Authentication
2. Generate App Password
3. Add to environment:
```bash
export MAIL_PASSWORD="your-app-password"
```

### Payment Integration

#### Stripe
```python
STRIPE_PUBLIC_KEY = "pk_test_..."
STRIPE_SECRET_KEY = "sk_test_..."
```

#### PayPal
```python
PAYPAL_CLIENT_ID = "your-client-id"
PAYPAL_SECRET = "your-secret"
```

---

## 📈 Monitoring

### Application Logs
```bash
tail -f logs/securewipe.log
```

### Database Backup
```bash
sqlite3 instance/secure_wipe.db .dump > backup.sql
```

### Health Check Endpoint
```bash
curl http://localhost:5000/
```

---

## 🐛 Troubleshooting

### Email Not Sending
- Check MAIL_PASSWORD is set
- Verify Gmail App Password
- Check firewall allows port 587
- Enable "Less secure app access" (if needed)

### Database Errors
```bash
rm instance/secure_wipe.db
python app.py  # Recreates database
```

### Permission Errors
```bash
chmod -R 755 uploads/
chmod -R 755 instance/
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux
lsof -ti:5000 | xargs kill -9
```

---

## 📞 Support

For deployment issues, contact:
**Email:** diziavatar@gmail.com

---

## 🎯 Performance Optimization

### Production Settings
```python
DEBUG = False
SQLALCHEMY_ECHO = False
SEND_FILE_MAX_AGE_DEFAULT = 31536000
```

### Caching (Redis)
```bash
pip install redis flask-caching
```

### CDN Integration
- Upload static files to CDN
- Update static file URLs

---

## 🔄 Updates & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Database Backup Schedule
```bash
0 0 * * * /usr/bin/sqlite3 /path/to/db .dump > /backups/$(date +\%Y\%m\%d).sql
```

---

**Deployment Complete! 🎉**

Access your application and change the default admin password immediately.
