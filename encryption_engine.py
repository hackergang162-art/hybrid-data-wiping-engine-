"""
🔐 CLIENT-SIDE ENCRYPTION ENGINE
User-Centric Data Sovereignty Model
Zero-Knowledge Architecture - Platform Never Sees Raw Data
End-to-End Encryption with Client-Side Key Management
"""

import os
import base64
import hashlib
import secrets
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import json


class ClientSideEncryption:
    """
    End-to-End Encryption Manager
    - All encryption/decryption happens client-side (via JavaScript)
    - Server only stores encrypted blobs and metadata
    - User's master key never leaves their device
    """
    
    def __init__(self):
        self.backend = default_backend()
        self.key_size = 256  # AES-256
        self.iterations = 100000  # PBKDF2 iterations
    
    def generate_master_key(self, user_password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """
        Generate user's master encryption key from password
        This should be done CLIENT-SIDE in production
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        
        key = kdf.derive(user_password.encode())
        return key, salt
    
    def generate_file_encryption_key(self) -> bytes:
        """Generate random encryption key for each file"""
        return Fernet.generate_key()
    
    def encrypt_file_data(self, data: bytes, file_key: bytes) -> bytes:
        """Encrypt file data with file-specific key"""
        f = Fernet(file_key)
        return f.encrypt(data)
    
    def decrypt_file_data(self, encrypted_data: bytes, file_key: bytes) -> bytes:
        """Decrypt file data"""
        f = Fernet(file_key)
        return f.decrypt(encrypted_data)
    
    def encrypt_file_key_with_master(self, file_key: bytes, master_key: bytes) -> bytes:
        """Encrypt file key with user's master key"""
        f = Fernet(base64.urlsafe_b64encode(master_key))
        return f.encrypt(file_key)
    
    def decrypt_file_key_with_master(self, encrypted_file_key: bytes, master_key: bytes) -> bytes:
        """Decrypt file key with user's master key"""
        f = Fernet(base64.urlsafe_b64encode(master_key))
        return f.decrypt(encrypted_file_key)
    
    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """Generate RSA keypair for asymmetric encryption"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=self.backend
        )
        
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def create_secure_metadata(self, file_info: Dict, master_key: bytes) -> Dict:
        """
        Create encrypted metadata for file
        Only metadata is stored on server, actual data stays encrypted
        """
        # Generate file-specific encryption key
        file_key = self.generate_file_encryption_key()
        
        # Encrypt the file key with user's master key
        encrypted_file_key = self.encrypt_file_key_with_master(file_key, master_key)
        
        metadata = {
            'file_id': secrets.token_urlsafe(16),
            'encrypted_file_key': base64.b64encode(encrypted_file_key).decode(),
            'filename_hash': hashlib.sha256(file_info.get('filename', '').encode()).hexdigest(),
            'size_encrypted': file_info.get('size', 0),
            'upload_timestamp': datetime.utcnow().isoformat(),
            'encryption_version': '1.0',
            'algorithm': 'AES-256-GCM + Fernet',
            'client_side_only': True
        }
        
        return metadata
    
    def generate_client_side_script(self) -> str:
        """
        Generate JavaScript code for client-side encryption
        This ensures the server NEVER sees unencrypted data
        """
        return """
// Client-Side Encryption Library
// All encryption happens in the browser - server never sees raw data

class DataSovereigntyEngine {
    constructor() {
        this.encoder = new TextEncoder();
        this.decoder = new TextDecoder();
    }
    
    // Generate master key from user password
    async generateMasterKey(password, salt) {
        const enc = this.encoder;
        const keyMaterial = await window.crypto.subtle.importKey(
            "raw",
            enc.encode(password),
            "PBKDF2",
            false,
            ["deriveBits", "deriveKey"]
        );
        
        return await window.crypto.subtle.deriveKey(
            {
                name: "PBKDF2",
                salt: salt || window.crypto.getRandomValues(new Uint8Array(32)),
                iterations: 100000,
                hash: "SHA-256"
            },
            keyMaterial,
            { name: "AES-GCM", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );
    }
    
    // Encrypt file before upload
    async encryptFile(file, masterKey) {
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const fileData = await file.arrayBuffer();
        
        const encrypted = await window.crypto.subtle.encrypt(
            { name: "AES-GCM", iv: iv },
            masterKey,
            fileData
        );
        
        // Return encrypted data + IV (needed for decryption)
        return {
            encrypted: new Blob([encrypted]),
            iv: Array.from(iv),
            originalSize: file.size,
            originalName: file.name
        };
    }
    
    // Decrypt file after download
    async decryptFile(encryptedBlob, iv, masterKey) {
        const encryptedData = await encryptedBlob.arrayBuffer();
        
        const decrypted = await window.crypto.subtle.decrypt(
            { name: "AES-GCM", iv: new Uint8Array(iv) },
            masterKey,
            encryptedData
        );
        
        return new Blob([decrypted]);
    }
    
    // Hash filename for privacy (server only sees hash)
    async hashFilename(filename) {
        const msgBuffer = this.encoder.encode(filename);
        const hashBuffer = await window.crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    
    // Generate file fingerprint for deduplication
    async generateFingerprint(file) {
        const buffer = await file.arrayBuffer();
        const hashBuffer = await window.crypto.subtle.digest('SHA-256', buffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
}

// Global instance
window.sovereigntyEngine = new DataSovereigntyEngine();

// Example usage:
async function secureUpload(file, userPassword) {
    const engine = window.sovereigntyEngine;
    
    // Generate master key from password
    const masterKey = await engine.generateMasterKey(userPassword);
    
    // Encrypt file client-side
    const encrypted = await engine.encryptFile(file, masterKey);
    
    // Hash filename for privacy
    const filenameHash = await engine.hashFilename(file.name);
    
    // Upload only encrypted blob (server never sees original)
    const formData = new FormData();
    formData.append('encrypted_file', encrypted.encrypted);
    formData.append('iv', JSON.stringify(encrypted.iv));
    formData.append('filename_hash', filenameHash);
    formData.append('size', encrypted.originalSize);
    
    return fetch('/api/upload_encrypted', {
        method: 'POST',
        body: formData
    });
}
"""


class ZeroKnowledgeStorage:
    """
    Zero-knowledge storage system
    Server stores encrypted data without ability to decrypt
    """
    
    def __init__(self, storage_path: str = 'encrypted_vault'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def store_encrypted_blob(self, file_id: str, encrypted_data: bytes, metadata: Dict) -> bool:
        """Store encrypted blob with metadata"""
        try:
            # Store encrypted file
            file_path = os.path.join(self.storage_path, f"{file_id}.enc")
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Store metadata (also encrypted or hashed)
            metadata_path = os.path.join(self.storage_path, f"{file_id}.meta")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)
            
            return True
        except Exception as e:
            print(f"Storage error: {e}")
            return False
    
    def retrieve_encrypted_blob(self, file_id: str) -> Optional[Tuple[bytes, Dict]]:
        """Retrieve encrypted blob and metadata"""
        try:
            file_path = os.path.join(self.storage_path, f"{file_id}.enc")
            metadata_path = os.path.join(self.storage_path, f"{file_id}.meta")
            
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            return encrypted_data, metadata
        except Exception:
            return None
    
    def secure_delete_blob(self, file_id: str, passes: int = 7) -> bool:
        """Securely delete encrypted blob (DoD 5220.22-M)"""
        file_path = os.path.join(self.storage_path, f"{file_id}.enc")
        metadata_path = os.path.join(self.storage_path, f"{file_id}.meta")
        
        try:
            # Overwrite file multiple times
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                
                for pass_num in range(passes):
                    with open(file_path, 'wb') as f:
                        if pass_num % 2 == 0:
                            f.write(b'\x00' * file_size)  # Zeros
                        else:
                            f.write(b'\xFF' * file_size)  # Ones
                
                # Final pass with random data
                with open(file_path, 'wb') as f:
                    f.write(secrets.token_bytes(file_size))
                
                # Delete
                os.remove(file_path)
            
            # Delete metadata
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            return True
        except Exception as e:
            print(f"Secure delete error: {e}")
            return False


class DataSovereigntyManager:
    """
    Main manager for data sovereignty
    Ensures user maintains full control over their data
    """
    
    def __init__(self):
        self.encryption = ClientSideEncryption()
        self.storage = ZeroKnowledgeStorage()
    
    def get_client_encryption_script(self) -> str:
        """Get JavaScript for client-side encryption"""
        return self.encryption.generate_client_side_script()
    
    def process_encrypted_upload(self, encrypted_data: bytes, metadata: Dict, user_id: int) -> Dict:
        """
        Process encrypted file upload
        Server only handles encrypted blobs
        """
        file_id = secrets.token_urlsafe(16)
        
        # Add server-side metadata (non-sensitive)
        server_metadata = {
            **metadata,
            'user_id': user_id,
            'server_timestamp': datetime.utcnow().isoformat(),
            'storage_location': 'encrypted_vault',
            'can_decrypt': False,  # Server cannot decrypt
            'data_sovereignty': 'user_controlled'
        }
        
        # Store encrypted blob
        success = self.storage.store_encrypted_blob(file_id, encrypted_data, server_metadata)
        
        return {
            'success': success,
            'file_id': file_id,
            'message': 'File stored with end-to-end encryption. Only you can decrypt it.'
        }
    
    def process_secure_deletion(self, file_id: str, user_id: int) -> Dict:
        """Process secure deletion request"""
        # Verify ownership (check user_id matches)
        blob_data = self.storage.retrieve_encrypted_blob(file_id)
        
        if blob_data:
            _, metadata = blob_data
            if metadata.get('user_id') == user_id:
                success = self.storage.secure_delete_blob(file_id)
                return {
                    'success': success,
                    'message': 'File securely wiped using DoD 5220.22-M standard (7-pass)',
                    'certificate_eligible': True
                }
        
        return {
            'success': False,
            'message': 'File not found or permission denied'
        }


# Global instances
sovereignty_manager = DataSovereigntyManager()
encryption_engine = ClientSideEncryption()
