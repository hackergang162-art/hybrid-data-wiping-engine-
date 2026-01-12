"""
🤖 AI DATA HUNTER
Intelligent Sensitive Data Discovery & Classification
ML-Powered Pattern Recognition for Privacy Protection
"""

import re
import os
import json
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime
import hashlib
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib


class SensitiveDataPatterns:
    """Patterns for identifying sensitive data"""
    
    # Credit Card Patterns
    CREDIT_CARD_PATTERNS = [
        r'\b(?:4[0-9]{12}(?:[0-9]{3})?)\b',  # Visa
        r'\b(?:5[1-5][0-9]{14})\b',  # MasterCard
        r'\b(?:3[47][0-9]{13})\b',  # American Express
        r'\b(?:6(?:011|5[0-9]{2})[0-9]{12})\b',  # Discover
    ]
    
    # SSN Pattern (US)
    SSN_PATTERN = r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b'
    
    # Indian Aadhaar Pattern
    AADHAAR_PATTERN = r'\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b'
    
    # PAN Card Pattern (India)
    PAN_PATTERN = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    
    # Email Pattern
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Phone Pattern (International)
    PHONE_PATTERN = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'
    
    # API Keys / Tokens
    API_KEY_PATTERNS = [
        r'(?i)api[_-]?key["\']?\s*[:=]\s*["\']?([a-z0-9]{32,})',
        r'(?i)access[_-]?token["\']?\s*[:=]\s*["\']?([a-z0-9]{32,})',
        r'(?i)secret[_-]?key["\']?\s*[:=]\s*["\']?([a-z0-9]{32,})',
        r'AKIA[0-9A-Z]{16}',  # AWS Access Key
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub Token
    ]
    
    # Password Patterns
    PASSWORD_PATTERNS = [
        r'(?i)password\s*[:=]\s*["\']?([^\s"\']+)',
        r'(?i)pwd\s*[:=]\s*["\']?([^\s"\']+)',
        r'(?i)passwd\s*[:=]\s*["\']?([^\s"\']+)',
    ]
    
    # Bank Account Pattern
    BANK_ACCOUNT_PATTERN = r'\b\d{9,18}\b'
    
    # IP Address Pattern
    IP_ADDRESS_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    # Private Key Pattern
    PRIVATE_KEY_PATTERN = r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----'


class AIDataHunter:
    """
    AI-powered sensitive data discovery engine
    Uses ML and pattern matching to identify sensitive information
    """
    
    def __init__(self):
        self.patterns = SensitiveDataPatterns()
        self.sensitivity_keywords = self._load_sensitivity_keywords()
        self.ml_model = None
        self.vectorizer = None
        self._initialize_ml_model()
    
    def _load_sensitivity_keywords(self) -> Set[str]:
        """Load keywords that indicate sensitive data"""
        return {
            # Personal Information
            'ssn', 'social security', 'passport', 'driver license', 'birth certificate',
            'aadhaar', 'pan card', 'voter id', 'national id',
            
            # Financial
            'credit card', 'debit card', 'bank account', 'routing number', 'swift code',
            'payment', 'invoice', 'salary', 'tax', 'financial statement',
            
            # Health
            'medical', 'health record', 'prescription', 'diagnosis', 'patient',
            'hospital', 'clinic', 'doctor', 'insurance',
            
            # Credentials
            'password', 'passphrase', 'secret', 'token', 'api key', 'private key',
            'certificate', 'credential', 'authentication',
            
            # Legal
            'confidential', 'proprietary', 'classified', 'restricted', 'nda',
            'contract', 'agreement', 'legal', 'lawsuit',
            
            # Personal
            'personal', 'private', 'sensitive', 'internal', 'do not share',
        }
    
    def _initialize_ml_model(self):
        """Initialize ML model for classification"""
        try:
            # Try to load pre-trained model
            self.ml_model = joblib.load('ml_models/sensitivity_classifier.pkl')
            self.vectorizer = joblib.load('ml_models/sensitivity_vectorizer.pkl')
        except:
            # Create and train a simple model
            self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self._train_initial_model()
    
    def _train_initial_model(self):
        """Train initial model with sample data"""
        # Sample training data
        sensitive_samples = [
            "credit card number 4532-1234-5678-9010",
            "SSN: 123-45-6789",
            "password: MySecretP@ss123",
            "API Key: sk_live_abcdef123456",
            "confidential financial report",
            "medical records patient data",
            "bank account routing number",
        ]
        
        non_sensitive_samples = [
            "meeting agenda for tomorrow",
            "grocery shopping list",
            "vacation photos 2023",
            "project documentation",
            "public announcement",
            "general information",
            "weather forecast",
        ]
        
        X_train = sensitive_samples + non_sensitive_samples
        y_train = [1] * len(sensitive_samples) + [0] * len(non_sensitive_samples)
        
        X_vectorized = self.vectorizer.fit_transform(X_train)
        self.ml_model.fit(X_vectorized, y_train)
        
        # Save model
        os.makedirs('ml_models', exist_ok=True)
        joblib.dump(self.ml_model, 'ml_models/sensitivity_classifier.pkl')
        joblib.dump(self.vectorizer, 'ml_models/sensitivity_vectorizer.pkl')
    
    def scan_text_content(self, text: str) -> Dict:
        """Scan text content for sensitive data"""
        findings = {
            'credit_cards': [],
            'ssn': [],
            'aadhaar': [],
            'pan_card': [],
            'emails': [],
            'phones': [],
            'api_keys': [],
            'passwords': [],
            'bank_accounts': [],
            'ip_addresses': [],
            'private_keys': [],
            'sensitivity_score': 0.0,
            'risk_level': 'low'
        }
        
        # Check credit cards
        for pattern in self.patterns.CREDIT_CARD_PATTERNS:
            matches = re.findall(pattern, text)
            findings['credit_cards'].extend(matches)
        
        # Check SSN
        ssn_matches = re.findall(self.patterns.SSN_PATTERN, text)
        findings['ssn'].extend(ssn_matches)
        
        # Check Aadhaar
        aadhaar_matches = re.findall(self.patterns.AADHAAR_PATTERN, text)
        findings['aadhaar'].extend(aadhaar_matches)
        
        # Check PAN
        pan_matches = re.findall(self.patterns.PAN_PATTERN, text)
        findings['pan_card'].extend(pan_matches)
        
        # Check emails
        email_matches = re.findall(self.patterns.EMAIL_PATTERN, text)
        findings['emails'].extend(email_matches)
        
        # Check phones
        phone_matches = re.findall(self.patterns.PHONE_PATTERN, text)
        findings['phones'].extend(['-'.join(m) for m in phone_matches])
        
        # Check API keys
        for pattern in self.patterns.API_KEY_PATTERNS:
            api_matches = re.findall(pattern, text)
            findings['api_keys'].extend(api_matches)
        
        # Check passwords
        for pattern in self.patterns.PASSWORD_PATTERNS:
            pwd_matches = re.findall(pattern, text)
            findings['passwords'].extend(pwd_matches)
        
        # Check bank accounts
        bank_matches = re.findall(self.patterns.BANK_ACCOUNT_PATTERN, text)
        findings['bank_accounts'].extend(bank_matches)
        
        # Check IP addresses
        ip_matches = re.findall(self.patterns.IP_ADDRESS_PATTERN, text)
        findings['ip_addresses'].extend(ip_matches)
        
        # Check private keys
        if re.search(self.patterns.PRIVATE_KEY_PATTERN, text):
            findings['private_keys'].append('Found private key')
        
        # Calculate sensitivity score using ML
        if self.ml_model and self.vectorizer:
            try:
                X = self.vectorizer.transform([text[:1000]])  # First 1000 chars
                sensitivity_prob = self.ml_model.predict_proba(X)[0][1]
                findings['sensitivity_score'] = float(sensitivity_prob)
            except:
                findings['sensitivity_score'] = 0.0
        
        # Calculate overall findings count
        total_findings = sum(len(v) if isinstance(v, list) else 0 for k, v in findings.items() if k not in ['sensitivity_score', 'risk_level'])
        
        # Determine risk level
        if total_findings > 10 or findings['sensitivity_score'] > 0.8:
            findings['risk_level'] = 'critical'
        elif total_findings > 5 or findings['sensitivity_score'] > 0.6:
            findings['risk_level'] = 'high'
        elif total_findings > 0 or findings['sensitivity_score'] > 0.4:
            findings['risk_level'] = 'medium'
        else:
            findings['risk_level'] = 'low'
        
        return findings
    
    def scan_filename(self, filename: str) -> Dict:
        """Analyze filename for sensitivity indicators"""
        filename_lower = filename.lower()
        
        sensitive_indicators = []
        for keyword in self.sensitivity_keywords:
            if keyword in filename_lower:
                sensitive_indicators.append(keyword)
        
        return {
            'filename': filename,
            'sensitive_indicators': sensitive_indicators,
            'is_sensitive': len(sensitive_indicators) > 0,
            'sensitivity_level': 'high' if len(sensitive_indicators) > 2 else 'medium' if len(sensitive_indicators) > 0 else 'low'
        }
    
    def scan_file_metadata(self, file_info: Dict) -> Dict:
        """Scan file metadata for sensitivity"""
        metadata_scan = {
            'file_path': file_info.get('path', ''),
            'file_size': file_info.get('size', 0),
            'file_type': file_info.get('type', ''),
            'sensitivity_indicators': [],
            'recommendations': []
        }
        
        # Check file type
        sensitive_extensions = {
            '.pdf': 'May contain documents with sensitive information',
            '.doc': 'Word documents often contain personal/business data',
            '.docx': 'Word documents often contain personal/business data',
            '.xls': 'Spreadsheets may contain financial data',
            '.xlsx': 'Spreadsheets may contain financial data',
            '.csv': 'CSV files may contain database exports',
            '.sql': 'Database files may contain sensitive records',
            '.db': 'Database files may contain sensitive records',
            '.key': 'Potential cryptographic key file',
            '.pem': 'Potential certificate/key file',
            '.p12': 'Potential certificate file',
            '.env': 'Environment variables may contain secrets',
            '.config': 'Configuration files may contain credentials',
        }
        
        file_ext = os.path.splitext(file_info.get('path', ''))[1].lower()
        if file_ext in sensitive_extensions:
            metadata_scan['sensitivity_indicators'].append(sensitive_extensions[file_ext])
            metadata_scan['recommendations'].append(f'Review {file_ext} file for sensitive content before wiping')
        
        # Check file size (very large files might be backups)
        if metadata_scan['file_size'] > 1_000_000_000:  # > 1GB
            metadata_scan['sensitivity_indicators'].append('Large file - may be backup or archive')
            metadata_scan['recommendations'].append('Verify contents before deletion')
        
        return metadata_scan
    
    def comprehensive_scan(self, file_path: str, content: Optional[str] = None) -> Dict:
        """Perform comprehensive sensitivity scan"""
        results = {
            'file_path': file_path,
            'scan_timestamp': datetime.utcnow().isoformat(),
            'filename_analysis': {},
            'content_analysis': {},
            'metadata_analysis': {},
            'overall_risk': 'low',
            'recommendations': []
        }
        
        # Scan filename
        results['filename_analysis'] = self.scan_filename(os.path.basename(file_path))
        
        # Scan metadata
        file_info = {
            'path': file_path,
            'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            'type': os.path.splitext(file_path)[1]
        }
        results['metadata_analysis'] = self.scan_file_metadata(file_info)
        
        # Scan content if provided
        if content:
            results['content_analysis'] = self.scan_text_content(content)
        
        # Determine overall risk
        risks = [
            results['filename_analysis'].get('sensitivity_level', 'low'),
            results['content_analysis'].get('risk_level', 'low') if content else 'low'
        ]
        
        if 'critical' in risks or 'high' in risks:
            results['overall_risk'] = 'high'
        elif 'medium' in risks:
            results['overall_risk'] = 'medium'
        else:
            results['overall_risk'] = 'low'
        
        # Generate recommendations
        if results['overall_risk'] == 'high':
            results['recommendations'].append('⚠️ HIGH RISK: This file contains sensitive data')
            results['recommendations'].append('Consider secure wiping with multiple passes')
            results['recommendations'].append('Generate certificate of destruction for compliance')
        elif results['overall_risk'] == 'medium':
            results['recommendations'].append('⚡ MEDIUM RISK: Review file before deletion')
            results['recommendations'].append('Use secure wiping method')
        else:
            results['recommendations'].append('✓ LOW RISK: Standard deletion recommended')
        
        return results
    
    def batch_scan_directory(self, directory_path: str, recursive: bool = True) -> Dict:
        """Scan entire directory for sensitive files"""
        scan_results = {
            'directory': directory_path,
            'total_files': 0,
            'sensitive_files': [],
            'high_risk_files': [],
            'medium_risk_files': [],
            'low_risk_files': [],
            'scan_summary': {}
        }
        
        # Walk through directory
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                scan_results['total_files'] += 1
                
                # Quick scan (filename only for performance)
                filename_scan = self.scan_filename(filename)
                
                file_result = {
                    'path': file_path,
                    'filename': filename,
                    'sensitivity': filename_scan['sensitivity_level']
                }
                
                if filename_scan['is_sensitive']:
                    scan_results['sensitive_files'].append(file_result)
                
                if filename_scan['sensitivity_level'] == 'high':
                    scan_results['high_risk_files'].append(file_result)
                elif filename_scan['sensitivity_level'] == 'medium':
                    scan_results['medium_risk_files'].append(file_result)
                else:
                    scan_results['low_risk_files'].append(file_result)
            
            if not recursive:
                break
        
        # Generate summary
        scan_results['scan_summary'] = {
            'total_scanned': scan_results['total_files'],
            'sensitive_count': len(scan_results['sensitive_files']),
            'high_risk_count': len(scan_results['high_risk_files']),
            'medium_risk_count': len(scan_results['medium_risk_files']),
            'low_risk_count': len(scan_results['low_risk_files']),
            'recommendation': self._generate_directory_recommendation(scan_results)
        }
        
        return scan_results
    
    def _generate_directory_recommendation(self, scan_results: Dict) -> str:
        """Generate recommendation based on directory scan"""
        high_count = len(scan_results['high_risk_files'])
        medium_count = len(scan_results['medium_risk_files'])
        
        if high_count > 10:
            return '🚨 CRITICAL: Multiple sensitive files detected. Review carefully before wiping.'
        elif high_count > 0:
            return '⚠️ WARNING: Sensitive files detected. Verify before deletion.'
        elif medium_count > 5:
            return '⚡ CAUTION: Some potentially sensitive files found.'
        else:
            return '✓ SAFE: No major sensitive data detected.'
    
    def generate_wipe_report(self, scan_results: Dict) -> str:
        """Generate human-readable wipe report"""
        report = []
        report.append("=" * 60)
        report.append("AI DATA HUNTER - SENSITIVITY SCAN REPORT")
        report.append("=" * 60)
        report.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Location: {scan_results.get('file_path', scan_results.get('directory', 'N/A'))}")
        report.append("")
        
        if 'scan_summary' in scan_results:
            summary = scan_results['scan_summary']
            report.append("SUMMARY:")
            report.append(f"  Total Files Scanned: {summary['total_scanned']}")
            report.append(f"  High Risk Files: {summary['high_risk_count']}")
            report.append(f"  Medium Risk Files: {summary['medium_risk_count']}")
            report.append(f"  Low Risk Files: {summary['low_risk_count']}")
            report.append(f"\n  Recommendation: {summary['recommendation']}")
        
        if 'content_analysis' in scan_results and scan_results['content_analysis']:
            analysis = scan_results['content_analysis']
            report.append("\nCONTENT ANALYSIS:")
            report.append(f"  Sensitivity Score: {analysis['sensitivity_score']:.2%}")
            report.append(f"  Risk Level: {analysis['risk_level'].upper()}")
            
            if analysis['credit_cards']:
                report.append(f"  ⚠️ Credit Cards Found: {len(analysis['credit_cards'])}")
            if analysis['ssn']:
                report.append(f"  ⚠️ SSN Found: {len(analysis['ssn'])}")
            if analysis['api_keys']:
                report.append(f"  ⚠️ API Keys Found: {len(analysis['api_keys'])}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)


# Global instance
ai_hunter = AIDataHunter()
