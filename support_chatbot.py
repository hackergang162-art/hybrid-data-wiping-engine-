"""
🤖 INTELLIGENT SUPPORT CHATBOT
AI-Powered Customer Support System
Multi-language Support | Context-Aware Responses
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import random


class SupportChatbot:
    """
    Intelligent support chatbot with NLP capabilities
    Handles common questions, guides users, and provides contextual help
    """
    
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        self.language = 'en'
        self.knowledge_base = self._load_knowledge_base()
        self.intents = self._define_intents()
        
    def _load_knowledge_base(self) -> Dict:
        """Load comprehensive knowledge base"""
        return {
            'platform_info': {
                'name': 'Tricolor Data Governance Hub',
                'version': '2026 Enterprise Edition',
                'features': [
                    'Universal Cloud Integration',
                    'AI Data Hunter',
                    'Client-Side Encryption',
                    'Multi-Currency Payments',
                    'QR Certificate Verification',
                    'Advanced Analytics'
                ]
            },
            'supported_clouds': [
                'Google Drive', 'Dropbox', 'OneDrive', 'AWS S3'
            ],
            'payment_methods': [
                'UPI (India)', 'Credit/Debit Cards', 'Net Banking', 'Digital Wallets'
            ],
            'security_standards': [
                'NIST 800-88', 'DoD 5220.22-M', 'ISO/IEC 27001', 'GDPR Article 17'
            ],
            'pricing': {
                'starter': {'inr': 4999, 'usd': 59},
                'professional': {'inr': 12999, 'usd': 149},
                'enterprise': {'inr': 29999, 'usd': 349}
            }
        }
    
    def _define_intents(self) -> Dict:
        """Define user intents and response patterns"""
        return {
            'greeting': {
                'patterns': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'namaste'],
                'responses': [
                    "Hello! 👋 I'm your Tricolor Data Hub assistant. How can I help you today?",
                    "Hi there! Welcome to Tricolor Data Governance Hub. What can I assist you with?",
                    "Namaste! 🙏 I'm here to help you with secure data wiping. What would you like to know?"
                ]
            },
            'cloud_connect': {
                'patterns': [r'connect.*cloud', r'link.*drive', r'oauth', r'google drive', r'dropbox', r'onedrive', r's3'],
                'responses': [
                    "To connect your cloud storage:\n\n1. Go to Dashboard → Cloud Connections\n2. Click 'Connect' on your desired provider (Google Drive, Dropbox, OneDrive, or AWS S3)\n3. Authorize access via OAuth2\n4. Select files/folders to manage\n\nWhich cloud service would you like to connect?"
                ]
            },
            'ai_scanner': {
                'patterns': [r'ai.*scan', r'sensitive.*data', r'find.*password', r'detect.*api.*key', r'data hunter'],
                'responses': [
                    "Our AI Data Hunter can detect:\n\n🔍 Sensitive Information:\n• API Keys & Tokens\n• Passwords & Credentials\n• Credit Card Numbers\n• SSN/Aadhaar/PAN Cards\n• Private Keys\n• Email Addresses\n\nTo start scanning:\n1. Go to Analytics → AI Scanner\n2. Select files or entire directories\n3. Review detected sensitive data\n4. Choose items for secure wiping\n\nWould you like to start a scan?"
                ]
            },
            'payment': {
                'patterns': [r'payment', r'pay', r'upi', r'price', r'cost', r'subscription', r'plan'],
                'responses': [
                    "💳 Payment & Pricing:\n\n**Starter Plan**: ₹4,999/mo ($59)\n• 5 Cloud Connections\n• 100 GB/month\n• Email Support\n\n**Professional**: ₹12,999/mo ($149)\n• 20 Clouds\n• 1 TB/month\n• Priority Support + API\n\n**Enterprise**: ₹29,999/mo ($349)\n• Unlimited Everything\n• 24/7 Support\n• White-label\n\n💰 We accept:\n• UPI (India) - Instant\n• Credit/Debit Cards\n• Net Banking\n• All major currencies (INR, USD, EUR, GBP)\n\nWhich plan interests you?"
                ]
            },
            'certificate': {
                'patterns': [r'certificate', r'verification', r'qr.*code', r'verify', r'proof'],
                'responses': [
                    "📜 Certificate Verification:\n\nAfter each wipe operation, you receive:\n\n✓ PDF Certificate with unique ID\n✓ QR Code for instant verification\n✓ SHA-256 cryptographic hash\n✓ Compliance stamps (NIST, ISO, GDPR)\n\nTo verify a certificate:\n1. Visit /verify page\n2. Scan QR code OR enter certificate ID\n3. Instant authenticity verification\n\nCertificates are publicly verifiable and tamper-proof!"
                ]
            },
            'encryption': {
                'patterns': [r'encryption', r'security', r'privacy', r'data.*sovereignty', r'client.*side'],
                'responses': [
                    "🔐 Data Sovereignty & Security:\n\n**Your data stays YOURS:**\n• All encryption happens in your browser\n• We NEVER see your unencrypted data\n• Zero-knowledge architecture\n• End-to-end encryption (AES-256)\n\n**Security Standards:**\n• Client-side key generation\n• Master key never leaves your device\n• Cryptographic verification\n• DoD 5220.22-M wiping\n\nYour privacy is our #1 priority!"
                ]
            },
            'wiping_process': {
                'patterns': [r'how.*wipe', r'delete.*file', r'erase.*data', r'secure.*delete', r'data.*wiping'],
                'responses': [
                    "🗑️ Secure Data Wiping Process:\n\n**Step 1**: Connect cloud storage (OAuth2)\n**Step 2**: AI Scanner identifies sensitive files\n**Step 3**: Select files for deletion\n**Step 4**: Choose wiping method:\n   • Quick (1-pass)\n   • Standard (3-pass)\n   • DoD 5220.22-M (7-pass)\n   • Quantum-Safe Erasure\n\n**Step 5**: Confirm & Execute\n**Step 6**: Receive certificate of destruction\n\nData is unrecoverable after wiping!"
                ]
            },
            'analytics': {
                'patterns': [r'analytics', r'dashboard', r'report', r'statistics', r'chart'],
                'responses': [
                    "📊 Analytics Dashboard Features:\n\n• Real-time wiping trends (Chart.js)\n• Data volume by cloud provider\n• Sensitive data detection stats\n• Payment history\n• Carbon footprint savings\n• Cost savings calculator\n• AI-powered insights\n\nAccess: Dashboard → Analytics\n\nView your complete data lifecycle!"
                ]
            },
            'support': {
                'patterns': [r'help', r'support', r'contact', r'problem', r'issue', r'error'],
                'responses': [
                    "🆘 Need Help?\n\n**Quick Support:**\n• Email: support@tricolordatahub.com\n• Live Chat: Available 24/7\n• Phone: +91-800-DATA-HUB\n\n**Self-Service:**\n• Documentation: /docs\n• Video Tutorials: /tutorials\n• FAQ: /faq\n• Community Forum: /community\n\n**Response Times:**\n• Free: 24-48 hours\n• Starter: 12-24 hours\n• Professional: 4-8 hours\n• Enterprise: 1 hour (24/7)\n\nWhat specific issue can I help with?"
                ]
            },
            'languages': {
                'patterns': [r'language', r'hindi', r'spanish', r'french', r'german', r'multilingual'],
                'responses': [
                    "🌍 Multilingual Support:\n\nAvailable Languages:\n• 🇮🇳 Hindi (हिंदी)\n• 🇬🇧 English\n• 🇪🇸 Spanish (Español)\n• 🇫🇷 French (Français)\n• 🇩🇪 German (Deutsch)\n\nTo change language:\nSettings → Language → Select preferred language\n\nWhich language would you prefer?"
                ]
            },
            'gdpr': {
                'patterns': [r'gdpr', r'compliance', r'regulation', r'legal', r'right.*delete'],
                'responses': [
                    "⚖️ GDPR & Compliance:\n\n**We comply with:**\n• GDPR Article 17 (Right to Erasure)\n• CCPA (California Privacy)\n• NIST 800-88 Guidelines\n• ISO/IEC 27001\n\n**Your Rights:**\n✓ Right to be forgotten\n✓ Data portability\n✓ Access your data\n✓ Proof of deletion\n\nAll wipes come with verified certificates for audit trails!"
                ]
            },
            'thanks': {
                'patterns': [r'thank', r'thanks', r'appreciate', r'great', r'awesome'],
                'responses': [
                    "You're welcome! 😊 Happy to help!",
                    "My pleasure! If you need anything else, just ask! 🙏",
                    "Glad I could assist! Feel free to reach out anytime! 👍"
                ]
            },
            'goodbye': {
                'patterns': [r'bye', r'goodbye', r'see you', r'quit', r'exit'],
                'responses': [
                    "Goodbye! Stay secure! 🔐",
                    "Take care! Feel free to return anytime! 👋",
                    "See you later! Your data is in safe hands! 🛡️"
                ]
            }
        }
    
    def detect_intent(self, user_message: str) -> Optional[str]:
        """Detect user intent from message"""
        user_message_lower = user_message.lower()
        
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_message_lower):
                    return intent
        
        return None
    
    def generate_response(self, user_message: str, user_context: Dict = None) -> Dict:
        """Generate contextual response"""
        
        # Update context
        if user_context:
            self.user_context.update(user_context)
        
        # Detect intent
        intent = self.detect_intent(user_message)
        
        # Store in history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'detected_intent': intent
        })
        
        # Generate response
        if intent and intent in self.intents:
            response_text = random.choice(self.intents[intent]['responses'])
            
            # Add contextual suggestions
            suggestions = self._get_suggestions(intent)
            
            return {
                'success': True,
                'response': response_text,
                'intent': intent,
                'suggestions': suggestions,
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Fallback response with smart suggestions
            return {
                'success': True,
                'response': self._get_fallback_response(user_message),
                'intent': 'unknown',
                'suggestions': [
                    'How do I connect cloud storage?',
                    'What are the pricing plans?',
                    'How does AI scanning work?',
                    'Talk to human support'
                ],
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_suggestions(self, intent: str) -> List[str]:
        """Get contextual suggestions based on intent"""
        suggestion_map = {
            'greeting': [
                'Connect my cloud storage',
                'View pricing plans',
                'Start AI scan',
                'How does it work?'
            ],
            'cloud_connect': [
                'Connect Google Drive',
                'Connect Dropbox',
                'How is OAuth2 secure?',
                'Can I connect multiple clouds?'
            ],
            'payment': [
                'Start free trial',
                'Compare plans',
                'UPI payment process',
                'International payment options'
            ],
            'ai_scanner': [
                'Start scanning now',
                'What data is detected?',
                'Is scanning safe?',
                'Scan results explanation'
            ],
            'certificate': [
                'Verify a certificate',
                'Download my certificate',
                'Share certificate proof',
                'Certificate validity'
            ],
            'support': [
                'Email support',
                'Browse documentation',
                'Watch video tutorial',
                'Join community forum'
            ]
        }
        
        return suggestion_map.get(intent, [
            'How can I help you?',
            'Browse all features',
            'Contact support'
        ])
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Smart fallback when intent is unclear"""
        fallback_responses = [
            f"I'm not quite sure about '{user_message[:50]}...', but I can help you with:\n\n• Cloud storage connections\n• AI-powered scanning\n• Payment & pricing\n• Certificates & verification\n• Security & privacy\n\nWhat would you like to know more about?",
            
            "I want to make sure I understand correctly. Are you asking about:\n\n1. Connecting cloud storage?\n2. Data wiping process?\n3. Pricing & payments?\n4. Security features?\n5. Something else?\n\nPlease choose a number or rephrase your question!",
            
            "Let me connect you with relevant resources:\n\n📚 Documentation: Detailed guides\n🎥 Video Tutorials: Step-by-step\n💬 Live Support: Chat with expert\n📧 Email: support@tricolordatahub.com\n\nOr try asking: 'How do I connect Google Drive?' or 'What are the pricing plans?'"
        ]
        
        return random.choice(fallback_responses)
    
    def get_quick_actions(self) -> List[Dict]:
        """Get quick action buttons for common tasks"""
        return [
            {
                'icon': '☁️',
                'text': 'Connect Cloud',
                'action': 'cloud_connect',
                'description': 'Link Google Drive, Dropbox, etc.'
            },
            {
                'icon': '🤖',
                'text': 'AI Scan',
                'action': 'ai_scan',
                'description': 'Find sensitive data automatically'
            },
            {
                'icon': '💳',
                'text': 'View Plans',
                'action': 'pricing',
                'description': 'Compare subscription options'
            },
            {
                'icon': '📜',
                'text': 'Verify Certificate',
                'action': 'verify_cert',
                'description': 'Check certificate authenticity'
            },
            {
                'icon': '📊',
                'text': 'Analytics',
                'action': 'analytics',
                'description': 'View your dashboard'
            },
            {
                'icon': '🆘',
                'text': 'Help Center',
                'action': 'help',
                'description': 'Browse documentation'
            }
        ]
    
    def get_conversation_summary(self) -> Dict:
        """Get conversation analytics"""
        return {
            'total_messages': len(self.conversation_history),
            'intents_detected': [msg['detected_intent'] for msg in self.conversation_history],
            'duration': 'Active session',
            'satisfaction': 'pending'
        }


# Global chatbot instance
support_bot = SupportChatbot()
