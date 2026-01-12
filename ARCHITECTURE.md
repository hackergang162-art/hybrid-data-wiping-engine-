# Aura-X AI Assistant - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer (Browser)                    │
├─────────────────────────────────────────────────────────────┤
│  • HTML5 + CSS3 (Tailwind CDN)                              │
│  • Vanilla JavaScript (No framework dependencies)            │
│  • AuraXRobot Animation Engine (GPU-accelerated)            │
│  • ChatManager (Debouncing, Queue, Session)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                   Nginx Reverse Proxy                        │
├─────────────────────────────────────────────────────────────┤
│  • SSL/TLS Termination                                       │
│  • Gzip Compression                                          │
│  • Static File Serving (CDN-ready)                          │
│  • Rate Limiting (IP-based)                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Gunicorn WSGI Server (Multi-worker)             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Flask Application                          │
├─────────────────────────────────────────────────────────────┤
│  API Endpoints:                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ /api/chat  → AI Assistant (Rate Limited)             │  │
│  │ /api/wipe/* → Data Sanitization Operations           │  │
│  │ /api/wallet/* → Payment Engine                        │  │
│  │ /api/ml/* → ML Prediction                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  Middleware:                                                 │
│  • RateLimiter (in-memory, upgradeable to Redis)           │
│  • CORS Handler                                             │
│  • Session Management                                        │
│  • Input Sanitization                                        │
│  • Security Headers                                          │
└─────────────────────────────────────────────────────────────┘
              ↓                    ↓                    ↓
    ┌─────────────────┐  ┌──────────────────┐  ┌─────────────┐
    │   PostgreSQL    │  │   ML Models      │  │  Email SMTP │
    │   (Primary DB)  │  │   (Joblib)       │  │  Service    │
    └─────────────────┘  └──────────────────┘  └─────────────┘
```

---

## Component Breakdown

### 1. **Frontend Components**

#### A. AuraXRobot Animation Engine
```javascript
class AuraXRobot {
    - State Machine: idle, listening, thinking, speaking
    - GPU Acceleration: CSS transforms + requestAnimationFrame
    - Mobile Optimized: Reduced motion support
    - Lazy Loading: Animation starts on interaction
}
```

**Performance Features:**
- `transform: translateZ(0)` for GPU layer
- `will-change` properties for smooth animations
- `requestAnimationFrame` for 60fps rendering
- Debounced state transitions

#### B. ChatManager
```javascript
class ChatManager {
    - Message Queue: Prevents API spam
    - Session Persistence: localStorage + server sync
    - Debouncing: 1s typing delay detection
    - State Synchronization: Robot animation triggers
}
```

---

### 2. **Backend Components**

#### A. Rate Limiter
```python
class RateLimiter:
    Strategy: Token bucket (in-memory)
    Limits: 20 requests/minute per IP+Session
    Cleanup: Automatic garbage collection
    Upgrade Path: Redis for distributed deployment
```

#### B. Chat API Endpoint
```
POST /api/chat
├── Input Validation (max 1000 chars)
├── XSS Sanitization
├── Rate Limit Check
├── AI Response Generation (get_ai_response)
├── Database Logging (ChatMessage)
└── JSON Response + Session ID
```

**Security Measures:**
- HTML entity encoding
- Session-based tracking
- IP-based rate limiting
- Error message sanitization
- HTTPS-only cookies

---

### 3. **Database Schema**

```sql
-- Chat Sessions
CREATE TABLE chat_message (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    helpful BOOLEAN
);

-- User Management
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wipe History
CREATE TABLE wipe_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    filename VARCHAR(255),
    wipe_method VARCHAR(100),
    certificate_hash VARCHAR(128),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Performance Optimizations

### Client-Side
1. **Lazy Loading**: Robot animation initializes on first chat open
2. **Debouncing**: Typing indicators throttled to 1s
3. **Message Queue**: Prevents API flooding
4. **GPU Acceleration**: All animations use `transform` and `opacity`
5. **Reduced Motion**: Respects user preference

### Server-Side
1. **Rate Limiting**: 20 req/min prevents abuse
2. **Connection Pooling**: SQLAlchemy manages DB connections
3. **Gunicorn Workers**: Multi-process for concurrency
4. **Nginx Caching**: Static assets served with 30d cache
5. **Gzip Compression**: 70% bandwidth reduction

### Network
1. **CDN-Ready**: Static files can be offloaded to CloudFlare
2. **HTTP/2**: Multiplexed connections via Nginx
3. **Minification**: CSS/JS compressed in production
4. **Preload Headers**: Critical resources prioritized

---

## Security Architecture

### Defense Layers

```
┌─────────────────────────────────────────┐
│  Layer 1: Network (Firewall + DDoS)    │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 2: Nginx (Rate Limit + SSL)     │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 3: App Rate Limiter              │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 4: Input Validation/Sanitization │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 5: Session + CSRF Protection     │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  Layer 6: Database (Parameterized SQL)  │
└─────────────────────────────────────────┘
```

### Security Headers (Automatic)
```http
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'...
```

---

## Scalability Path

### Current (Single Server)
- Handles: ~100 concurrent users
- Response Time: <200ms (API)
- Database: PostgreSQL (local)
- Session: In-memory

### Stage 1: Vertical Scaling
- Upgrade server specs (4→8 cores)
- Add Redis for sessions + rate limiting
- Enable database connection pooling
- Expected: ~500 concurrent users

### Stage 2: Horizontal Scaling
```
         Load Balancer (HAProxy/Nginx)
           /        |        \
      App1       App2       App3
           \        |        /
        Shared PostgreSQL + Redis
```
- Multiple Gunicorn instances
- Sticky sessions via Redis
- Database read replicas
- Expected: ~2000 concurrent users

### Stage 3: Cloud Native
- Kubernetes deployment
- Auto-scaling pods
- Managed PostgreSQL (AWS RDS/Google Cloud SQL)
- CDN for static assets (CloudFlare/Fastly)
- Serverless functions for ML predictions
- Expected: 10,000+ concurrent users

---

## Monitoring Stack

### Application Metrics
```python
# Add prometheus_flask_exporter
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

# Monitored automatically:
- Request count by endpoint
- Response time percentiles (p50, p95, p99)
- Error rates
- Active sessions
```

### Infrastructure Monitoring
- **Nginx**: Access logs → Loki/ELK
- **Database**: pg_stat_activity monitoring
- **System**: CPU, Memory, Disk (Prometheus + Grafana)
- **Alerts**: PagerDuty/Slack integration

---

## API Response Times (Target)

| Endpoint | Avg | p95 | p99 | Max |
|----------|-----|-----|-----|-----|
| /api/chat | 150ms | 300ms | 500ms | 1s |
| /api/wipe/start | 50ms | 100ms | 200ms | 500ms |
| /api/wallet/balance | 30ms | 60ms | 100ms | 200ms |
| Static Files (CDN) | 10ms | 20ms | 30ms | 50ms |

---

## Tech Stack Summary

**Frontend:**
- HTML5, CSS3 (Tailwind CDN)
- Vanilla JavaScript (ES6+)
- No build tools (dev simplicity)

**Backend:**
- Flask 3.0 (Python 3.8+)
- Gunicorn WSGI server
- PostgreSQL database
- Redis (optional, for scaling)

**Infrastructure:**
- Nginx reverse proxy
- Let's Encrypt SSL
- Systemd service management
- Ubuntu/Debian Linux

**Future Integrations:**
- OpenAI API (LLM responses)
- Stripe/Razorpay (payments)
- AWS S3 (file storage)
- Twilio (SMS notifications)

---

**Architecture designed for: Production readiness, Easy maintenance, Clear upgrade path** 🚀
