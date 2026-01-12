# DOCWIPING - Advanced Data Sanitization System

**Neon Blue Edition with AI & ML Features**

A professional-grade data destruction simulator with Flask backend, SQL database, AI chatbot, and machine learning predictions.

## 🚀 Features

### Core Features
- ✅ **Multi-OS Support**: Windows, Linux, Android
- ✅ **Multiple Wipe Methods**: DoD 5220.22-M, NIST SP 800-88, Gutmann, ATA Secure Erase, Crypto Erase
- ✅ **Real-time Data Meters**: Visual GB wiped & MB/s speed tracking
- ✅ **Certificate Generation**: PDF certificates with quantum-grade verification
- ✅ **Device Information**: Display device names and specifications

### Backend & Database
- 🔥 **Flask Backend**: RESTful API for wipe operations
- 🔥 **SQL Database**: SQLite database with 3 models (WipeRecord, ChatMessage, DeviceAnalytics)
- 🔥 **API Endpoints**: 
  - `/api/wipe/start` - Initialize wipe operations
  - `/api/wipe/complete` - Complete wipe and generate certificate
  - `/api/wipe/history` - View wipe history
  - `/api/chat` - AI chatbot interface
  - `/api/analytics` - System analytics
  - `/api/ml/predict-duration` - ML-powered duration prediction

### AI & Machine Learning
- 🤖 **Multilingual AI Chatbot**: Support for English, Spanish, French, German
- 🤖 **ML Duration Predictor**: Random Forest model trained on 1000+ samples
- 🤖 **Smart Predictions**: Device-specific wipe time estimation
- 🤖 **Continuous Learning**: Database stores all operations for model improvement

### New Design
- 🎨 **Purple-Blue Gradient Background**: Dynamic radial gradients
- 🎨 **Enhanced Neon Effects**: Cyan, purple, pink accents
- 🎨 **Animated Chatbot Widget**: Floating AI assistant
- 🎨 **Responsive Design**: Works on desktop and mobile

## 📦 Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train ML Model
```bash
python ml_training.py
```

### 3. Initialize Database & Start Flask Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Tailwind CSS
- jsPDF for certificate generation

### Backend
- Python 3.14
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0

### Machine Learning
- scikit-learn 1.8.0
- NumPy 2.4.1
- Pandas 2.3.3
- Joblib 1.5.3

### Database
- SQLite (Development)
- SQLAlchemy ORM

## 📁 Project Structure

```
demo app/
├── app.py                 # Flask backend server
├── ml_training.py         # ML model training script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── styles.css        # CSS with new gradient backgrounds
│   └── script.js         # JavaScript with API integration
├── ml_models/
│   └── wipe_predictor.pkl # Trained ML model
└── instance/
    └── docwiping.db      # SQLite database
```

## 🎯 Usage

1. **Start the Server**:
   ```bash
   python app.py
   ```

2. **Access the Application**:
   - Open browser to `http://localhost:5000`

3. **Select Operating System**:
   - Choose Windows, Linux, or Android

4. **Select Device & Wipe Method**:
   - View detected drives
   - Analyze device specifications
   - Choose appropriate wipe standard

5. **Monitor Wipe Progress**:
   - Real-time data meters show GB wiped
   - Speed indicators show MB/s
   - Live console logs

6. **Use AI Chatbot**:
   - Click purple chat button (bottom right)
   - Ask questions in English, Spanish, French, or German
   - Get help with wipe methods, standards, troubleshooting

7. **Download Certificate**:
   - Quantum-grade verification certificate
   - SHA-512 digital signature
   - Compliance standards included

## 🔒 Security Standards

- **NIST SP 800-88 Rev. 1**: Guidelines for Media Sanitization
- **DoD 5220.22-M**: Department of Defense standard
- **ISO 27001**: Information security management
- **AES-256-GCM**: Quantum-safe encryption engine

## 🌐 Multilingual Support

Chatbot available in:
- 🇬🇧 English
- 🇪🇸 Español (Spanish)
- 🇫🇷 Français (French)
- 🇩🇪 Deutsch (German)

## 🧠 Machine Learning Model

The ML model predicts wipe duration based on:
- Device type (NVMe SSD, SATA SSD, HDD, Android)
- Storage size (GB)
- Wipe method complexity

**Model Performance**:
- Training R² score: ~0.99
- Testing R² score: ~0.98
- Average confidence: 85%

## 📊 Database Schema

### WipeRecord
- Device information
- Wipe method & standard
- Timestamps
- Certificate hash
- Status tracking

### ChatMessage
- User messages
- Bot responses
- Language preference
- Session tracking
- Feedback (helpful rating)

### DeviceAnalytics
- Performance metrics
- Duration predictions vs actual
- Success rates
- Training data for ML model

## 🎨 Color Palette

```css
--neon-blue: #00d4ff
--accent-cyan: #00ffff
--gradient-purple: #8b5cf6
--gradient-pink: #ec4899
--gradient-orange: #f97316
```

## 📝 API Documentation

### POST `/api/wipe/start`
Start a new wipe operation.

**Request Body**:
```json
{
  "device_id": "NVME01",
  "device_name": "Enterprise NVMe Drive",
  "device_type": "NVMe SSD",
  "device_size": "1.6 TB",
  "wipe_method": "NVMe Format (Crypto Erase)",
  "wipe_standard": "NIST SP 800-88"
}
```

**Response**:
```json
{
  "success": true,
  "wipe_id": 1,
  "estimated_duration": 960
}
```

### POST `/api/chat`
Send message to AI chatbot.

**Request Body**:
```json
{
  "message": "What is DoD 5220.22-M?",
  "language": "en"
}
```

**Response**:
```json
{
  "success": true,
  "response": "DoD 5220.22-M is a Department of Defense standard...",
  "language": "en"
}
```

## 🚀 Future Enhancements

- [ ] PostgreSQL support for production
- [ ] User authentication & authorization
- [ ] Advanced ML models (Neural Networks)
- [ ] Real hardware integration
- [ ] Cloud backup of certificates
- [ ] Mobile app (React Native)
- [ ] Enterprise dashboard
- [ ] Scheduled wipe operations

## 📄 License

This is a demonstration/educational project for data sanitization workflows.

## 👨‍💻 Developer

DOCWIPING v2.1 Neon Edition
Advanced Data Sanitization & Destruction System

---

**Note**: This is a simulation tool for educational purposes. For actual data destruction, use certified hardware-based solutions compliant with your organization's security policies.
