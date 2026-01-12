"""
💳 ADVANCED MULTI-CURRENCY PAYMENT GATEWAY
UPI Integration (Razorpay/Cashfree) + International Payment Support
Real-time Currency Conversion + Subscription Management
"""

import os
import json
import hashlib
import secrets
from enum import Enum
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import requests


class Currency(Enum):
    """Global currency support with live exchange rates"""
    INR = {'symbol': '₹', 'name': 'Indian Rupee', 'rate': 1.0}
    USD = {'symbol': '$', 'name': 'US Dollar', 'rate': 0.012}
    EUR = {'symbol': '€', 'name': 'Euro', 'rate': 0.011}
    GBP = {'symbol': '£', 'name': 'British Pound', 'rate': 0.0095}
    JPY = {'symbol': '¥', 'name': 'Japanese Yen', 'rate': 1.75}
    AUD = {'symbol': 'A$', 'name': 'Australian Dollar', 'rate': 0.018}
    CAD = {'symbol': 'C$', 'name': 'Canadian Dollar', 'rate': 0.016}
    SGD = {'symbol': 'S$', 'name': 'Singapore Dollar', 'rate': 0.016}
    AED = {'symbol': 'د.إ', 'name': 'UAE Dirham', 'rate': 0.044}
    CNY = {'symbol': '¥', 'name': 'Chinese Yuan', 'rate': 0.086}


class PaymentGateway(Enum):
    """Supported payment gateways"""
    RAZORPAY = {
        'name': 'Razorpay',
        'supports_upi': True,
        'supports_international': True,
        'fee_percentage': 2.0,
        'countries': ['IN', 'US', 'UK', 'SG']
    }
    CASHFREE = {
        'name': 'Cashfree',
        'supports_upi': True,
        'supports_international': False,
        'fee_percentage': 1.8,
        'countries': ['IN']
    }
    STRIPE = {
        'name': 'Stripe',
        'supports_upi': False,
        'supports_international': True,
        'fee_percentage': 2.9,
        'countries': ['US', 'UK', 'EU', 'AU', 'CA']
    }
    PAYPAL = {
        'name': 'PayPal',
        'supports_upi': False,
        'supports_international': True,
        'fee_percentage': 3.5,
        'countries': ['GLOBAL']
    }


class SubscriptionTier(Enum):
    """Subscription plans with features"""
    FREE = {
        'name': 'Free Trial',
        'price_inr': 0,
        'price_usd': 0,
        'features': ['1 Cloud Connection', '10 GB/month', 'Basic Support'],
        'max_clouds': 1,
        'data_limit_gb': 10,
        'ai_scans': 5,
        'duration_days': 30
    }
    STARTER = {
        'name': 'Starter',
        'price_inr': 4999,
        'price_usd': 59,
        'features': ['5 Cloud Connections', '100 GB/month', 'Email Support', 'AI Scanner'],
        'max_clouds': 5,
        'data_limit_gb': 100,
        'ai_scans': 50,
        'certificates': True
    }
    PROFESSIONAL = {
        'name': 'Professional',
        'price_inr': 12999,
        'price_usd': 149,
        'features': ['20 Clouds', '1 TB/month', 'Priority Support', 'Advanced AI', 'Custom Reports'],
        'max_clouds': 20,
        'data_limit_gb': 1024,
        'ai_scans': 500,
        'certificates': True,
        'api_access': True
    }
    ENTERPRISE = {
        'name': 'Enterprise',
        'price_inr': 29999,
        'price_usd': 349,
        'features': ['Unlimited Clouds', 'Unlimited Data', '24/7 Support', 'White-label', 'Custom Integration'],
        'max_clouds': float('inf'),
        'data_limit_gb': float('inf'),
        'ai_scans': float('inf'),
        'certificates': True,
        'api_access': True,
        'white_label': True
    }


class UPIPaymentProcessor:
    """
    UPI Payment Integration using Razorpay/Cashfree
    Handles QR codes, intent flows, and payment verification
    """
    
    def __init__(self, gateway: str = 'razorpay'):
        self.gateway = gateway
        
        if gateway == 'razorpay':
            self.api_key = os.getenv('RAZORPAY_KEY_ID', '')
            self.api_secret = os.getenv('RAZORPAY_KEY_SECRET', '')
            self.base_url = 'https://api.razorpay.com/v1'
        elif gateway == 'cashfree':
            self.api_key = os.getenv('CASHFREE_APP_ID', '')
            self.api_secret = os.getenv('CASHFREE_SECRET_KEY', '')
            self.base_url = 'https://api.cashfree.com/pg'
    
    def create_upi_payment_link(self, amount_inr: float, order_id: str, customer_info: Dict) -> Dict:
        """Generate UPI payment link/QR code"""
        
        if self.gateway == 'razorpay':
            return self._razorpay_create_order(amount_inr, order_id, customer_info)
        elif self.gateway == 'cashfree':
            return self._cashfree_create_order(amount_inr, order_id, customer_info)
    
    def _razorpay_create_order(self, amount_inr: float, order_id: str, customer_info: Dict) -> Dict:
        """Create Razorpay payment order"""
        try:
            auth = (self.api_key, self.api_secret)
            
            data = {
                'amount': int(amount_inr * 100),  # Razorpay expects paise
                'currency': 'INR',
                'receipt': order_id,
                'notes': {
                    'customer_name': customer_info.get('name', ''),
                    'customer_email': customer_info.get('email', ''),
                    'purpose': 'Data Wiping Subscription'
                }
            }
            
            response = requests.post(
                f'{self.base_url}/orders',
                json=data,
                auth=auth,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                order = response.json()
                
                # Generate UPI payment details
                upi_details = {
                    'order_id': order['id'],
                    'amount': amount_inr,
                    'currency': 'INR',
                    'payment_link': f"https://rzp.io/l/{order['id']}",
                    'upi_id': 'razorpay@upi',
                    'qr_code': self._generate_upi_qr(amount_inr, order['id']),
                    'status': 'created',
                    'gateway': 'razorpay'
                }
                
                return upi_details
            
            return {'error': 'Failed to create order', 'details': response.text}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _cashfree_create_order(self, amount_inr: float, order_id: str, customer_info: Dict) -> Dict:
        """Create Cashfree payment order"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'x-client-id': self.api_key,
                'x-client-secret': self.api_secret
            }
            
            data = {
                'order_id': order_id,
                'order_amount': amount_inr,
                'order_currency': 'INR',
                'customer_details': {
                    'customer_id': customer_info.get('user_id', ''),
                    'customer_name': customer_info.get('name', ''),
                    'customer_email': customer_info.get('email', ''),
                    'customer_phone': customer_info.get('phone', '')
                },
                'order_meta': {
                    'return_url': 'https://yourapp.com/payment/callback',
                    'notify_url': 'https://yourapp.com/payment/webhook'
                }
            }
            
            response = requests.post(
                f'{self.base_url}/orders',
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                order = response.json()
                return {
                    'order_id': order_id,
                    'amount': amount_inr,
                    'currency': 'INR',
                    'payment_link': order.get('payment_link', ''),
                    'upi_id': 'cashfree@upi',
                    'status': 'created',
                    'gateway': 'cashfree'
                }
            
            return {'error': 'Failed to create order', 'details': response.text}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_upi_qr(self, amount: float, order_id: str) -> str:
        """Generate UPI QR code data"""
        # UPI QR format: upi://pay?pa=<UPI_ID>&pn=<Name>&am=<Amount>&tr=<TxnID>&tn=<Note>
        upi_string = f"upi://pay?pa=tricolor@razorpay&pn=Tricolor%20Data%20Hub&am={amount}&tr={order_id}&tn=Data%20Wiping%20Service"
        return upi_string
    
    def verify_payment(self, payment_id: str, order_id: str, signature: str) -> bool:
        """Verify UPI payment signature"""
        if self.gateway == 'razorpay':
            # Razorpay signature verification
            expected_signature = hashlib.sha256(
                f"{order_id}|{payment_id}".encode() + self.api_secret.encode()
            ).hexdigest()
            return expected_signature == signature
        
        return False
    
    def get_payment_status(self, payment_id: str) -> Dict:
        """Check payment status"""
        try:
            if self.gateway == 'razorpay':
                auth = (self.api_key, self.api_secret)
                response = requests.get(f'{self.base_url}/payments/{payment_id}', auth=auth)
                
                if response.status_code == 200:
                    return response.json()
            
            return {'status': 'unknown'}
        
        except Exception as e:
            return {'error': str(e)}


class MultiCurrencyConverter:
    """Real-time currency conversion"""
    
    def __init__(self):
        self.base_currency = 'INR'
        self.rates = {c.name: c.value['rate'] for c in Currency}
        self.last_update = datetime.now()
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert between currencies"""
        # Convert to INR first
        amount_in_inr = amount / self.rates.get(from_currency, 1.0)
        
        # Convert to target currency
        converted_amount = amount_in_inr * self.rates.get(to_currency, 1.0)
        
        return round(converted_amount, 2)
    
    def format_price(self, amount: float, currency_code: str) -> str:
        """Format price with currency symbol"""
        currency = Currency[currency_code]
        symbol = currency.value['symbol']
        return f"{symbol}{amount:,.2f}"
    
    def get_subscription_price(self, tier: SubscriptionTier, currency_code: str) -> Dict:
        """Get subscription price in any currency"""
        tier_data = tier.value
        base_price_inr = tier_data['price_inr']
        
        converted_price = self.convert(base_price_inr, 'INR', currency_code)
        
        return {
            'tier': tier_data['name'],
            'price': converted_price,
            'currency': currency_code,
            'symbol': Currency[currency_code].value['symbol'],
            'formatted': self.format_price(converted_price, currency_code)
        }
    
    def update_exchange_rates(self):
        """Fetch live exchange rates (requires API)"""
        # In production, use a service like exchangerate-api.com
        try:
            api_key = os.getenv('EXCHANGE_RATE_API_KEY', '')
            if api_key:
                url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/INR"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    self.rates = data.get('conversion_rates', self.rates)
                    self.last_update = datetime.now()
        except:
            pass  # Use default rates if API fails


class AdvancedPaymentManager:
    """
    Complete payment management system
    Handles UPI, cards, subscriptions, invoicing
    """
    
    def __init__(self):
        self.upi_processor = UPIPaymentProcessor('razorpay')
        self.currency_converter = MultiCurrencyConverter()
        self.transactions = []
        self.subscriptions = {}
    
    def create_subscription_payment(self, user_id: str, tier: SubscriptionTier, 
                                   currency: str = 'INR', payment_method: str = 'UPI') -> Dict:
        """Create subscription payment"""
        
        # Get price in user's currency
        price_info = self.currency_converter.get_subscription_price(tier, currency)
        
        # Generate order ID
        order_id = f"SUB_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(4)}"
        
        # Customer info
        customer_info = {
            'user_id': user_id,
            'name': 'Customer Name',  # Get from user profile
            'email': 'user@example.com',  # Get from user profile
        }
        
        # Create payment based on method
        if payment_method == 'UPI' and currency == 'INR':
            payment_details = self.upi_processor.create_upi_payment_link(
                price_info['price'],
                order_id,
                customer_info
            )
        else:
            # For international payments, use Stripe/PayPal
            payment_details = {
                'order_id': order_id,
                'amount': price_info['price'],
                'currency': currency,
                'payment_method': payment_method,
                'status': 'pending_gateway_integration'
            }
        
        # Store transaction
        transaction = {
            'order_id': order_id,
            'user_id': user_id,
            'tier': tier.value['name'],
            'amount': price_info['price'],
            'currency': currency,
            'payment_method': payment_method,
            'created_at': datetime.now().isoformat(),
            'status': 'created',
            'payment_details': payment_details
        }
        
        self.transactions.append(transaction)
        
        return transaction
    
    def activate_subscription(self, user_id: str, tier: SubscriptionTier, payment_id: str) -> Dict:
        """Activate subscription after successful payment"""
        
        tier_data = tier.value
        
        subscription = {
            'user_id': user_id,
            'tier': tier.value['name'],
            'payment_id': payment_id,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=30),
            'features': tier_data['features'],
            'max_clouds': tier_data['max_clouds'],
            'data_limit_gb': tier_data['data_limit_gb'],
            'ai_scans_remaining': tier_data.get('ai_scans', 0),
            'status': 'active'
        }
        
        self.subscriptions[user_id] = subscription
        
        return subscription
    
    def verify_subscription(self, user_id: str) -> Dict:
        """Check if user has active subscription"""
        subscription = self.subscriptions.get(user_id)
        
        if not subscription:
            return {'active': False, 'tier': 'FREE'}
        
        # Check expiry
        if datetime.now() > subscription['end_date']:
            subscription['status'] = 'expired'
            return {'active': False, 'tier': subscription['tier'], 'expired': True}
        
        return {
            'active': True,
            'tier': subscription['tier'],
            'features': subscription['features'],
            'data_remaining_gb': subscription['data_limit_gb'],
            'expires_at': subscription['end_date'].isoformat()
        }
    
    def get_invoice(self, transaction_id: str) -> Dict:
        """Generate invoice for transaction"""
        transaction = next((t for t in self.transactions if t['order_id'] == transaction_id), None)
        
        if not transaction:
            return {'error': 'Transaction not found'}
        
        invoice = {
            'invoice_number': f"INV-{transaction['order_id']}",
            'date': transaction['created_at'],
            'customer_id': transaction['user_id'],
            'items': [{
                'description': f"{transaction['tier']} Subscription",
                'amount': transaction['amount'],
                'currency': transaction['currency']
            }],
            'total': transaction['amount'],
            'currency': transaction['currency'],
            'payment_method': transaction['payment_method'],
            'status': transaction['status']
        }
        
        return invoice


# Global instances
payment_manager = AdvancedPaymentManager()
upi_processor = UPIPaymentProcessor()
currency_converter = MultiCurrencyConverter()
