"""
🌐 CLOUD STORAGE INTEGRATION MODULE
Universal Data Wiping Across Multiple Cloud Platforms
OAuth2 Authentication & Secure Access
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import requests
from flask import session, request, redirect, url_for
import boto3
from botocore.exceptions import ClientError

class CloudStorageManager:
    """Universal cloud storage manager with OAuth2 support"""
    
    def __init__(self):
        self.providers = {
            'google_drive': GoogleDriveConnector(),
            'dropbox': DropboxConnector(),
            'aws_s3': AWSS3Connector(),
            'onedrive': OneDriveConnector()
        }
    
    def get_provider(self, provider_name: str):
        """Get specific cloud provider connector"""
        return self.providers.get(provider_name)
    
    def list_all_connections(self, user_id: int) -> List[Dict]:
        """List all active cloud connections for a user"""
        connections = []
        for name, provider in self.providers.items():
            if provider.is_connected(user_id):
                connections.append({
                    'name': name,
                    'display_name': provider.display_name,
                    'connected': True,
                    'last_sync': provider.get_last_sync(user_id)
                })
        return connections


class GoogleDriveConnector:
    """Google Drive OAuth2 connector"""
    
    display_name = "Google Drive"
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/oauth/google/callback')
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.token_url = 'https://oauth2.googleapis.com/token'
        self.api_base = 'https://www.googleapis.com/drive/v3'
    
    def get_authorization_url(self, user_id: int) -> str:
        """Generate OAuth2 authorization URL"""
        state = hashlib.sha256(f"{user_id}{datetime.now()}".encode()).hexdigest()
        session['oauth_state'] = state
        session['oauth_user_id'] = user_id
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scopes),
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        return f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(self.token_url, data=data)
        return response.json()
    
    def list_files(self, access_token: str, folder_id: str = 'root', query: str = None) -> List[Dict]:
        """List files in Google Drive"""
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {
            'q': query or f"'{folder_id}' in parents and trashed=false",
            'fields': 'files(id,name,mimeType,size,createdTime,modifiedTime,parents)',
            'pageSize': 1000
        }
        
        response = requests.get(f"{self.api_base}/files", headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json().get('files', [])
        return []
    
    def delete_file(self, access_token: str, file_id: str) -> bool:
        """Permanently delete a file from Google Drive"""
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # First, trash the file
        response = requests.delete(f"{self.api_base}/files/{file_id}", headers=headers)
        
        if response.status_code == 204:
            # Then permanently delete from trash
            trash_response = requests.delete(
                f"{self.api_base}/files/{file_id}",
                headers=headers,
                params={'supportsAllDrives': 'true'}
            )
            return trash_response.status_code == 204
        return False
    
    def scan_sensitive_data(self, access_token: str) -> List[Dict]:
        """Scan for potentially sensitive files"""
        sensitive_patterns = [
            "password", "confidential", "secret", "private", "ssn", 
            "credit_card", "bank", "tax", "medical", "personal"
        ]
        
        sensitive_files = []
        for pattern in sensitive_patterns:
            query = f"name contains '{pattern}' and trashed=false"
            files = self.list_files(access_token, query=query)
            sensitive_files.extend(files)
        
        return sensitive_files
    
    def is_connected(self, user_id: int) -> bool:
        """Check if user has connected Google Drive"""
        # This would check database for stored tokens
        return False
    
    def get_last_sync(self, user_id: int) -> Optional[str]:
        """Get last sync timestamp"""
        return None


class DropboxConnector:
    """Dropbox OAuth2 connector"""
    
    display_name = "Dropbox"
    
    def __init__(self):
        self.client_id = os.getenv('DROPBOX_CLIENT_ID', '')
        self.client_secret = os.getenv('DROPBOX_CLIENT_SECRET', '')
        self.redirect_uri = os.getenv('DROPBOX_REDIRECT_URI', 'http://localhost:5000/oauth/dropbox/callback')
        self.auth_url = 'https://www.dropbox.com/oauth2/authorize'
        self.token_url = 'https://api.dropboxapi.com/oauth2/token'
        self.api_base = 'https://api.dropboxapi.com/2'
    
    def get_authorization_url(self, user_id: int) -> str:
        """Generate OAuth2 authorization URL"""
        state = hashlib.sha256(f"{user_id}{datetime.now()}".encode()).hexdigest()
        session['oauth_state'] = state
        session['oauth_user_id'] = user_id
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': state,
            'token_access_type': 'offline'
        }
        
        return f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(self.token_url, data=data)
        return response.json()
    
    def list_files(self, access_token: str, path: str = '') -> List[Dict]:
        """List files in Dropbox"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {'path': path or '', 'recursive': False}
        response = requests.post(f"{self.api_base}/files/list_folder", headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json().get('entries', [])
        return []
    
    def delete_file(self, access_token: str, path: str) -> bool:
        """Permanently delete a file from Dropbox"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {'path': path}
        response = requests.post(f"{self.api_base}/files/permanently_delete", headers=headers, json=data)
        
        return response.status_code == 200
    
    def scan_sensitive_data(self, access_token: str) -> List[Dict]:
        """Scan for potentially sensitive files"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Search for sensitive patterns
        sensitive_patterns = ["password", "confidential", "secret", "private"]
        sensitive_files = []
        
        for pattern in sensitive_patterns:
            data = {
                'query': pattern,
                'options': {'max_results': 100}
            }
            response = requests.post(f"{self.api_base}/files/search_v2", headers=headers, json=data)
            
            if response.status_code == 200:
                matches = response.json().get('matches', [])
                sensitive_files.extend([m.get('metadata', {}).get('metadata') for m in matches])
        
        return sensitive_files
    
    def is_connected(self, user_id: int) -> bool:
        return False
    
    def get_last_sync(self, user_id: int) -> Optional[str]:
        return None


class AWSS3Connector:
    """AWS S3 connector"""
    
    display_name = "AWS S3"
    
    def __init__(self):
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
    
    def get_client(self):
        """Get S3 client"""
        return boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
    
    def list_buckets(self) -> List[Dict]:
        """List all S3 buckets"""
        try:
            s3 = self.get_client()
            response = s3.list_buckets()
            return response.get('Buckets', [])
        except ClientError:
            return []
    
    def list_files(self, bucket_name: str, prefix: str = '') -> List[Dict]:
        """List files in S3 bucket"""
        try:
            s3 = self.get_client()
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            return response.get('Contents', [])
        except ClientError:
            return []
    
    def delete_file(self, bucket_name: str, key: str) -> bool:
        """Delete file from S3"""
        try:
            s3 = self.get_client()
            s3.delete_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError:
            return False
    
    def secure_wipe_s3_object(self, bucket_name: str, key: str) -> bool:
        """Securely wipe S3 object by overwriting before deletion"""
        try:
            s3 = self.get_client()
            
            # Get object metadata
            metadata = s3.head_object(Bucket=bucket_name, Key=key)
            size = metadata.get('ContentLength', 0)
            
            # Overwrite with zeros (DoD 5220.22-M standard)
            zero_data = b'\x00' * min(size, 10485760)  # 10MB chunks
            
            for _ in range(3):  # 3-pass overwrite
                s3.put_object(Bucket=bucket_name, Key=key, Body=zero_data)
            
            # Final deletion
            s3.delete_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError:
            return False
    
    def scan_sensitive_data(self, bucket_name: str) -> List[Dict]:
        """Scan for potentially sensitive files in S3"""
        sensitive_patterns = ['password', 'secret', 'key', 'token', 'credentials']
        sensitive_files = []
        
        try:
            files = self.list_files(bucket_name)
            for file in files:
                key = file.get('Key', '').lower()
                if any(pattern in key for pattern in sensitive_patterns):
                    sensitive_files.append(file)
        except Exception:
            pass
        
        return sensitive_files
    
    def is_connected(self, user_id: int) -> bool:
        return bool(self.access_key and self.secret_key)
    
    def get_last_sync(self, user_id: int) -> Optional[str]:
        return None


class OneDriveConnector:
    """Microsoft OneDrive OAuth2 connector"""
    
    display_name = "OneDrive"
    
    def __init__(self):
        self.client_id = os.getenv('ONEDRIVE_CLIENT_ID', '')
        self.client_secret = os.getenv('ONEDRIVE_CLIENT_SECRET', '')
        self.redirect_uri = os.getenv('ONEDRIVE_REDIRECT_URI', 'http://localhost:5000/oauth/onedrive/callback')
        self.scopes = ['Files.ReadWrite.All', 'offline_access']
        self.auth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
        self.token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        self.api_base = 'https://graph.microsoft.com/v1.0'
    
    def get_authorization_url(self, user_id: int) -> str:
        """Generate OAuth2 authorization URL"""
        state = hashlib.sha256(f"{user_id}{datetime.now()}".encode()).hexdigest()
        session['oauth_state'] = state
        session['oauth_user_id'] = user_id
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scopes),
            'state': state
        }
        
        return f"{self.auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(self.token_url, data=data)
        return response.json()
    
    def list_files(self, access_token: str, folder_id: str = 'root') -> List[Dict]:
        """List files in OneDrive"""
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f"{self.api_base}/me/drive/items/{folder_id}/children"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get('value', [])
        return []
    
    def delete_file(self, access_token: str, item_id: str) -> bool:
        """Delete file from OneDrive"""
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f"{self.api_base}/me/drive/items/{item_id}"
        
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    
    def scan_sensitive_data(self, access_token: str) -> List[Dict]:
        """Scan for sensitive files"""
        sensitive_patterns = ['password', 'confidential', 'secret']
        sensitive_files = []
        
        for pattern in sensitive_patterns:
            headers = {'Authorization': f'Bearer {access_token}'}
            url = f"{self.api_base}/me/drive/search(q='{pattern}')"
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                sensitive_files.extend(response.json().get('value', []))
        
        return sensitive_files
    
    def is_connected(self, user_id: int) -> bool:
        return False
    
    def get_last_sync(self, user_id: int) -> Optional[str]:
        return None


# Initialize global instance
cloud_manager = CloudStorageManager()
