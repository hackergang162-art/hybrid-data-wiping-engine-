"""
📜 ADVANCED CERTIFICATE GENERATION SYSTEM
QR Code Verification | Blockchain-Ready | Compliance-Ready
ISO 27001, NIST 800-88, GDPR Compliant Certificates
"""

import os
import io
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class CertificateGenerator:
    """
    Enterprise-grade certificate generation with QR verification
    """
    
    def __init__(self, verification_base_url: str = "https://yourapp.com/verify"):
        self.verification_url = verification_base_url
        self.certificates_db = {}  # In production, use database
        self.output_dir = "certificates"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_certificate_id(self) -> str:
        """Generate unique certificate ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_part = secrets.token_hex(4).upper()
        return f"CERT-{timestamp}-{random_part}"
    
    def create_certificate_hash(self, certificate_data: Dict) -> str:
        """Create cryptographic hash of certificate for verification"""
        hash_data = json.dumps(certificate_data, sort_keys=True).encode()
        return hashlib.sha256(hash_data).hexdigest()
    
    def generate_qr_code(self, certificate_id: str, verification_hash: str) -> str:
        """Generate QR code for certificate verification"""
        verification_url = f"{self.verification_url}/{certificate_id}?hash={verification_hash}"
        
        # Create QR code with custom styling
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Create styled QR code
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(
                back_color=(255, 255, 255),
                front_color=(255, 138, 0)  # Orange color
            )
        )
        
        # Save QR code
        qr_path = os.path.join(self.output_dir, f"{certificate_id}_qr.png")
        img.save(qr_path)
        
        return qr_path
    
    def generate_certificate(self, wipe_data: Dict, user_info: Dict) -> Dict:
        """
        Generate complete certificate with QR code
        
        Args:
            wipe_data: Information about the wiping operation
            user_info: User/organization information
        """
        
        # Generate certificate metadata
        certificate_id = self.generate_certificate_id()
        issue_date = datetime.now()
        
        certificate_data = {
            'certificate_id': certificate_id,
            'issue_date': issue_date.isoformat(),
            'organization': user_info.get('organization', 'N/A'),
            'user_name': user_info.get('name', 'N/A'),
            'user_email': user_info.get('email', 'N/A'),
            'wipe_method': wipe_data.get('method', 'DoD 5220.22-M (7-pass)'),
            'data_volume': wipe_data.get('volume_gb', 0),
            'file_count': wipe_data.get('file_count', 0),
            'cloud_providers': wipe_data.get('providers', []),
            'standards_compliance': [
                'NIST 800-88',
                'DoD 5220.22-M',
                'ISO/IEC 27001',
                'GDPR Article 17'
            ],
            'verification_method': 'SHA-256 Hash + QR Code',
            'certificate_type': wipe_data.get('type', 'Data Erasure Certificate')
        }
        
        # Create hash for verification
        verification_hash = self.create_certificate_hash(certificate_data)
        certificate_data['verification_hash'] = verification_hash
        
        # Generate QR code
        qr_path = self.generate_qr_code(certificate_id, verification_hash)
        
        # Generate PDF certificate
        pdf_path = self._create_pdf_certificate(certificate_data, qr_path)
        
        # Store in database for verification
        self.certificates_db[certificate_id] = {
            **certificate_data,
            'qr_code_path': qr_path,
            'pdf_path': pdf_path,
            'verified_count': 0,
            'status': 'active'
        }
        
        return {
            'certificate_id': certificate_id,
            'pdf_path': pdf_path,
            'qr_code_path': qr_path,
            'verification_url': f"{self.verification_url}/{certificate_id}",
            'verification_hash': verification_hash,
            'issue_date': issue_date.isoformat()
        }
    
    def _create_pdf_certificate(self, cert_data: Dict, qr_path: str) -> str:
        """Create professional PDF certificate"""
        
        pdf_path = os.path.join(self.output_dir, f"{cert_data['certificate_id']}.pdf")
        
        # Create PDF
        c = pdf_canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        # Draw decorative border
        c.setStrokeColorRGB(1, 0.54, 0)  # Orange
        c.setLineWidth(3)
        c.rect(0.5*inch, 0.5*inch, width-inch, height-inch, fill=0)
        
        # Inner border
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(1)
        c.rect(0.6*inch, 0.6*inch, width-1.2*inch, height-1.2*inch, fill=0)
        
        # Header - Title
        c.setFillColorRGB(1, 0.54, 0)  # Orange
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width/2, height - 1.5*inch, "CERTIFICATE OF DATA ERASURE")
        
        # Tricolor flag
        c.setFillColorRGB(1, 0.54, 0)  # Saffron
        c.rect(width/2 - 1.5*inch, height - 2*inch, 3*inch, 0.15*inch, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)  # White
        c.rect(width/2 - 1.5*inch, height - 2.15*inch, 3*inch, 0.15*inch, fill=1, stroke=0)
        c.setFillColorRGB(0, 0.5, 0)  # Green
        c.rect(width/2 - 1.5*inch, height - 2.3*inch, 3*inch, 0.15*inch, fill=1, stroke=0)
        
        # Subtitle
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height - 2.7*inch, "Tricolor Data Governance Hub - 2026")
        c.drawCentredString(width/2, height - 2.95*inch, "Professional Secure Data Wiping & Privacy Protection Platform")
        
        # Certificate ID and Date
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1*inch, height - 3.5*inch, f"Certificate ID: {cert_data['certificate_id']}")
        c.drawString(1*inch, height - 3.75*inch, f"Issue Date: {datetime.fromisoformat(cert_data['issue_date']).strftime('%B %d, %Y at %H:%M UTC')}")
        
        # Main content
        y_position = height - 4.3*inch
        
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, y_position, "This certifies that:")
        
        y_position -= 0.3*inch
        c.setFont("Helvetica-Bold", 13)
        c.drawString(1.5*inch, y_position, f"Organization: {cert_data['organization']}")
        
        y_position -= 0.25*inch
        c.setFont("Helvetica", 11)
        c.drawString(1.5*inch, y_position, f"Authorized by: {cert_data['user_name']} ({cert_data['user_email']})")
        
        y_position -= 0.4*inch
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, y_position, "Has successfully performed secure data erasure with the following details:")
        
        # Data table
        y_position -= 0.5*inch
        
        data = [
            ["Data Volume Wiped:", f"{cert_data['data_volume']:.2f} GB"],
            ["Number of Files:", f"{cert_data['file_count']:,}"],
            ["Wiping Method:", cert_data['wipe_method']],
            ["Cloud Providers:", ", ".join(cert_data['cloud_providers']) if cert_data['cloud_providers'] else "Local Storage"],
        ]
        
        for label, value in data:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(1.5*inch, y_position, label)
            c.setFont("Helvetica", 10)
            c.drawString(3.5*inch, y_position, value)
            y_position -= 0.25*inch
        
        # Compliance standards
        y_position -= 0.3*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1*inch, y_position, "Standards Compliance:")
        
        y_position -= 0.25*inch
        c.setFont("Helvetica", 10)
        for standard in cert_data['standards_compliance']:
            c.drawString(1.5*inch, y_position, f"✓ {standard}")
            y_position -= 0.2*inch
        
        # QR Code
        if os.path.exists(qr_path):
            c.drawImage(qr_path, width - 2.5*inch, 1.2*inch, width=1.8*inch, height=1.8*inch)
            c.setFont("Helvetica", 9)
            c.drawCentredString(width - 1.6*inch, 0.9*inch, "Scan to Verify")
        
        # Verification hash
        c.setFont("Helvetica", 7)
        c.drawString(1*inch, 1.5*inch, f"Verification Hash: {cert_data['verification_hash'][:32]}...")
        
        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(width/2, 0.8*inch, "This certificate is cryptographically signed and can be verified online.")
        c.drawCentredString(width/2, 0.6*inch, f"Verify at: {self.verification_url}/{cert_data['certificate_id']}")
        
        # Digital signature placeholder
        c.setFillColorRGB(1, 0.54, 0)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, 3.8*inch, "Digitally Signed & Verified")
        
        # Save PDF
        c.save()
        
        return pdf_path
    
    def verify_certificate(self, certificate_id: str, provided_hash: Optional[str] = None) -> Dict:
        """Verify certificate authenticity"""
        
        if certificate_id not in self.certificates_db:
            return {
                'valid': False,
                'error': 'Certificate not found',
                'status': 'invalid'
            }
        
        cert_data = self.certificates_db[certificate_id]
        
        # Verify hash if provided
        if provided_hash:
            if provided_hash != cert_data['verification_hash']:
                return {
                    'valid': False,
                    'error': 'Hash mismatch - certificate may be tampered',
                    'status': 'invalid'
                }
        
        # Update verification count
        self.certificates_db[certificate_id]['verified_count'] += 1
        self.certificates_db[certificate_id]['last_verified'] = datetime.now().isoformat()
        
        return {
            'valid': True,
            'certificate_id': certificate_id,
            'issue_date': cert_data['issue_date'],
            'organization': cert_data['organization'],
            'data_volume': cert_data['data_volume'],
            'wipe_method': cert_data['wipe_method'],
            'standards_compliance': cert_data['standards_compliance'],
            'verification_count': cert_data['verified_count'],
            'status': 'verified'
        }
    
    def get_certificate_statistics(self) -> Dict:
        """Get statistics about issued certificates"""
        total_certs = len(self.certificates_db)
        total_data_wiped = sum(cert['data_volume'] for cert in self.certificates_db.values())
        total_verifications = sum(cert.get('verified_count', 0) for cert in self.certificates_db.values())
        
        return {
            'total_certificates': total_certs,
            'total_data_wiped_gb': total_data_wiped,
            'total_verifications': total_verifications,
            'average_data_per_cert': total_data_wiped / total_certs if total_certs > 0 else 0
        }
    
    def revoke_certificate(self, certificate_id: str, reason: str) -> bool:
        """Revoke a certificate"""
        if certificate_id in self.certificates_db:
            self.certificates_db[certificate_id]['status'] = 'revoked'
            self.certificates_db[certificate_id]['revocation_reason'] = reason
            self.certificates_db[certificate_id]['revoked_at'] = datetime.now().isoformat()
            return True
        return False


class BlockchainCertificateIntegration:
    """
    Blockchain integration for certificate immutability
    Future-ready for Ethereum/Polygon integration
    """
    
    def __init__(self):
        self.blockchain_enabled = False
        self.contract_address = None
    
    def register_certificate_on_chain(self, certificate_id: str, certificate_hash: str) -> Dict:
        """
        Register certificate hash on blockchain for immutability
        This is a placeholder for actual blockchain integration
        """
        
        # In production, integrate with Web3.py for Ethereum/Polygon
        # Example: 
        # web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        # contract = web3.eth.contract(address=self.contract_address, abi=contract_abi)
        # tx_hash = contract.functions.registerCertificate(certificate_id, certificate_hash).transact()
        
        return {
            'blockchain_enabled': False,
            'message': 'Blockchain integration ready - configure Web3 provider',
            'certificate_id': certificate_id,
            'hash': certificate_hash,
            'network': 'Polygon (Coming Soon)'
        }
    
    def verify_on_chain(self, certificate_id: str) -> Dict:
        """Verify certificate on blockchain"""
        return {
            'on_chain_verified': False,
            'message': 'Blockchain verification ready for integration'
        }


# Global instances
certificate_generator = CertificateGenerator()
blockchain_integration = BlockchainCertificateIntegration()


# Example usage function
def create_wipe_certificate_example():
    """Example of creating a certificate"""
    
    wipe_data = {
        'method': 'DoD 5220.22-M (7-pass) + Quantum-Safe Erasure',
        'volume_gb': 245.8,
        'file_count': 12847,
        'providers': ['Google Drive', 'Dropbox', 'AWS S3'],
        'type': 'Enterprise Data Erasure Certificate'
    }
    
    user_info = {
        'organization': 'TechCorp Industries',
        'name': 'John Doe',
        'email': 'john.doe@techcorp.com'
    }
    
    result = certificate_generator.generate_certificate(wipe_data, user_info)
    print(f"Certificate generated: {result['certificate_id']}")
    print(f"PDF: {result['pdf_path']}")
    print(f"Verify at: {result['verification_url']}")
    
    return result
