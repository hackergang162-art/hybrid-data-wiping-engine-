# API Documentation - Tricolor Governance Hub 2026

**Base URL:** `http://localhost:5000` (Development)  
**API Version:** 2.0.0  
**Authentication:** Flask-Login (Session-based)

---

## Authentication Endpoints

### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "phone": "+91-9876543210"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Registration successful"
}
```

---

### Login User
```http
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "is_admin": false,
  "redirect": "/dashboard"
}
```

---

## Wallet Management APIs

### Create Wallet
```http
POST /api/wallet/create
Authorization: Required (Login)
Content-Type: application/json

{
  "initial_balance_inr": 0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Wallet created successfully",
  "wallet_id": 1,
  "balance": 0,
  "currency": "INR"
}
```

---

### Get Wallet Balance
```http
GET /api/wallet/balance?currency=INR
Authorization: Required (Login)
```

**Response:**
```json
{
  "success": true,
  "balance_inr": 50000,
  "balance_converted": 50000,
  "currency": "INR",
  "symbol": "₹",
  "user_id": 1
}
```

**Supported Currencies:** INR, USD, EUR, GBP, JPY, AUD, CAD, SGD, HKD, AED

---

### Add Funds (UPI)
```http
POST /api/wallet/add-funds
Authorization: Required (Login)
Content-Type: application/json

{
  "amount_inr": 5000,
  "payment_method": "upi",
  "upi_id": "yourname@bank"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully added ₹5000 to wallet",
  "new_balance": 55000,
  "transaction_id": 42,
  "reference": "UPI-yourname@bank-a1b2c3d4"
}
```

---

### Add Funds (Card)
```http
POST /api/wallet/add-funds
Authorization: Required (Login)
Content-Type: application/json

{
  "amount_inr": 10000,
  "payment_method": "card",
  "card_token": "tok_visa_1234567890"
}
```

---

## Currency Conversion APIs

### Convert Currency
```http
POST /api/payment/convert
Authorization: Required (Login)
Content-Type: application/json

{
  "amount": 1000,
  "from": "INR",
  "to": "USD"
}
```

**Response:**
```json
{
  "success": true,
  "original_amount": 1000,
  "original_currency": "INR",
  "converted_amount": 12.0,
  "target_currency": "USD",
  "exchange_rate": 0.012
}
```

---

## Subscription APIs

### Subscribe to Plan
```http
POST /api/subscription/subscribe
Authorization: Required (Login)
Content-Type: application/json

{
  "plan": "professional",
  "cycle": "yearly"
}
```

**Available Plans:** starter, professional, enterprise  
**Billing Cycles:** monthly, yearly (20% discount)

**Response:**
```json
{
  "success": true,
  "message": "Successfully subscribed to PROFESSIONAL plan",
  "subscription_id": 1,
  "plan": "professional",
  "cycle": "yearly",
  "expires_at": "2027-01-15T10:30:45.123456",
  "amount_charged": 155988,
  "new_wallet_balance": 45000
}
```

---

### Get Subscription Status
```http
GET /api/subscription/status
Authorization: Required (Login)
```

**Response (Active Subscription):**
```json
{
  "success": true,
  "subscribed": true,
  "plan": "professional",
  "cycle": "yearly",
  "started_at": "2025-01-15T10:30:45.123456",
  "expires_at": "2026-01-15T10:30:45.123456",
  "days_remaining": 365,
  "auto_renew": true
}
```

**Response (No Active Subscription):**
```json
{
  "success": true,
  "subscribed": false,
  "plan": null,
  "message": "No active subscription"
}
```

---

## Invoice & Billing APIs

### Generate Invoice
```http
POST /api/invoice/generate
Authorization: Required (Login)
Content-Type: application/json

{
  "type": "wipe"
}
```

**Response:**
```json
{
  "success": true,
  "invoice_id": "INV-1-20260115101030",
  "user": "john_doe",
  "email": "john@example.com",
  "issued_at": "2026-01-15T10:10:30.123456",
  "wipe_summary": {
    "total_wipes": 25,
    "total_data_destroyed_gb": 847.5,
    "total_wipes_completed": 25
  },
  "esg_impact": {
    "carbon_saved_kg": 12.71,
    "co2_equivalent_trees": 0.61,
    "ewaste_prevented_kg": 10.17,
    "impact_message": "You've saved 12.71kg of CO₂ emissions by securely wiping 847.5GB of data instead of destroying hardware!"
  },
  "sustainability_score": 84,
  "compliance": {
    "nist_800_88_verified": true,
    "gdpr_compliant": true,
    "iso_27001_certified": true,
    "government_verified": true
  }
}
```

---

## Audit Trail APIs

### Get Audit Timeline
```http
GET /api/audit/timeline?limit=20
Authorization: Required (Login)
```

**Response:**
```json
{
  "success": true,
  "timeline": [
    {
      "id": 1,
      "filename": "sensitive_data.zip",
      "wipe_level": "military",
      "timestamp": "2026-01-15T10:30:45.123456",
      "certificate_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
      "status": "completed",
      "passes": 7,
      "file_size": 1024000000,
      "duration": 3600.5
    }
  ],
  "total_count": 25
}
```

---

## Data Wiping APIs

### Start Wipe Operation
```http
POST /api/wipe/start
Authorization: Required (Login)
Content-Type: application/json

{
  "device_id": "nvme_001",
  "device_name": "Samsung 980 Pro",
  "device_type": "NVMe SSD",
  "device_size": "2TB",
  "wipe_method": "NVMe Format (Crypto Erase)",
  "wipe_standard": "NIST 800-88 Rev 2"
}
```

**Response:**
```json
{
  "success": true,
  "record_id": 1,
  "status": "in_progress"
}
```

---

### Update Wipe Status
```http
PUT /api/wipe/update/1
Authorization: Required (Login)
Content-Type: application/json

{
  "status": "completed",
  "certificate_hash": "x1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6"
}
```

**Response:**
```json
{
  "success": true,
  "certificate_hash": "x1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6",
  "record": {
    "id": 1,
    "device_id": "nvme_001",
    "device_name": "Samsung 980 Pro",
    "status": "completed",
    "timestamp": "2026-01-15T10:30:45.123456"
  }
}
```

---

### Get Wipe History
```http
GET /api/wipe/history
Authorization: Required (Login)
```

**Response:**
```json
{
  "success": true,
  "records": [
    {
      "id": 1,
      "device_id": "nvme_001",
      "device_name": "Samsung 980 Pro",
      "device_type": "NVMe SSD",
      "device_size": "2TB",
      "wipe_method": "NVMe Format (Crypto Erase)",
      "status": "completed",
      "started_at": "2026-01-15T10:00:00",
      "completed_at": "2026-01-15T10:30:00",
      "certificate_hash": "x1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6"
    }
  ]
}
```

---

## ML Duration Prediction APIs

### Predict Wipe Duration
```http
POST /api/ml/predict-duration
Authorization: Required (Login)
Content-Type: application/json

{
  "device_type": "SATA HDD",
  "device_size": "4TB",
  "wipe_method": "DoD 5220.22-M (3-pass)",
  "device_age_years": 3
}
```

**Response:**
```json
{
  "success": true,
  "estimated_seconds": 85500,
  "confidence": 0.9
}
```

**Duration Calculation:**
- Base Speed: 150 MB/s for HDD
- Method Multiplier: 3 passes = 3×
- Age Adjustment: +3% per year
- **Result:** (4000 GB × 1024 MB/GB ÷ 150 MB/s) × 3 × 1.09 ≈ 85,500 seconds (≈23.75 hours)

---

## Statistics & Analytics APIs

### Get User Statistics
```http
GET /api/stats
Authorization: Required (Login)
```

**Response:**
```json
{
  "total_wipes": 25,
  "total_size": 1073741824000,
  "total_spent": 125000
}
```

---

### Get System Analytics
```http
GET /api/analytics
```

**Response:**
```json
{
  "success": true,
  "total_wipes": 1250,
  "completed_wipes": 1200,
  "success_rate": 96,
  "device_types": {
    "NVMe SSD": 450,
    "SATA SSD": 380,
    "HDD": 300,
    "Android": 70
  }
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Login required"
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid amount or currency"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Rate Limiting

**Current Limits (Demo Mode):**
- 100 requests per minute per IP
- 1000 requests per hour per user

**Production Limits:**
- 500 requests per minute per IP
- 10,000 requests per hour per user
- 100 concurrent connections per user

---

## Pagination

All list endpoints support pagination:

```http
GET /api/audit/timeline?limit=20&offset=0
```

**Parameters:**
- `limit`: Number of records (default: 20, max: 100)
- `offset`: Number of records to skip (default: 0)

---

## SDKs & Libraries

### JavaScript/TypeScript
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true  // Include session cookies
});

// Create wallet
const response = await api.post('/api/wallet/create', {
  initial_balance_inr: 0
});

// Get balance
const balance = await api.get('/api/wallet/balance', {
  params: { currency: 'INR' }
});
```

### Python
```python
import requests

session = requests.Session()

# Login
response = session.post('http://localhost:5000/login', json={
    'username': 'john_doe',
    'password': 'secure_password'
})

# Get wallet balance
response = session.get('http://localhost:5000/api/wallet/balance', 
    params={'currency': 'INR'})
balance = response.json()
```

---

## Webhook Events (Future)

**Planned for Q2 2026:**
- `wipe.started`
- `wipe.completed`
- `wipe.failed`
- `payment.received`
- `subscription.renewed`
- `subscription.expired`

---

**Documentation Version:** 2.0.0  
**Last Updated:** January 2026  
**Status:** Production Ready ✅
