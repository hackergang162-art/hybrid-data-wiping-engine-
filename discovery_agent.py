"""
Discovery Agent - AWS/Azure/On-Prem Scanner
Autonomous Data Discovery with Sovereign Compliance
"""

import boto3
import requests
import json
import time
import os
from datetime import datetime

# Configuration
DASHBOARD_API_URL = "http://localhost:5000/api/topology/update"
ORG_ID = "TRICOLOR_INDIA_001"
SCAN_INTERVAL = 300  # 5 minutes

class DataDiscoveryAgent:
    """
    Autonomous agent that scans hybrid infrastructure
    for shadow data and compliance risks
    """
    
    def __init__(self):
        self.aws_enabled = False
        self.azure_enabled = False
        
        # Try to initialize AWS
        try:
            self.s3 = boto3.client('s3')
            self.macie = boto3.client('macie2')
            self.aws_enabled = True
            print("✓ AWS SDK initialized")
        except Exception as e:
            print(f"⚠ AWS not configured: {e}")
        
        # Mock Azure connector (replace with actual Azure SDK)
        self.azure_enabled = False
        
    def scan_s3_buckets(self):
        """Scan AWS S3 for unencrypted or sensitive 'Shadow Data'"""
        if not self.aws_enabled:
            return []
        
        results = []
        try:
            buckets = self.s3.list_buckets()['Buckets']
            
            for bucket in buckets:
                name = bucket['Name']
                region = self.s3.get_bucket_location(Bucket=name)['LocationConstraint'] or 'us-east-1'
                
                # Check if bucket is in India (ap-south-1)
                in_india = 'south-1' in region or 'south' in region
                
                # Check encryption status
                try:
                    enc = self.s3.get_bucket_encryption(Bucket=name)
                    status = "verified"  # Green - Encrypted
                    risk = "Zero"
                except:
                    status = "pending"  # Saffron - Risk Detected
                    risk = "High"
                
                # Check for public access
                try:
                    acl = self.s3.get_bucket_acl(Bucket=name)
                    is_public = any(grant['Permission'] == 'READ' for grant in acl['Grants'])
                    if is_public:
                        status = "pending"
                        risk = "Critical"
                except:
                    pass
                
                results.append({
                    "node_id": name,
                    "name": f"{name} ({region})",
                    "type": "AWS_S3",
                    "status": status,
                    "location": self._get_region_location(region),
                    "lat": self._get_region_lat(region),
                    "lng": self._get_region_lng(region),
                    "risk_score": 0.8 if status == "pending" else 0.1,
                    "risk": risk,
                    "co2": self._estimate_carbon_offset(name),
                    "in_india": in_india
                })
        except Exception as e:
            print(f"Error scanning S3: {e}")
        
        return results
    
    def scan_onprem_servers(self):
        """Scan on-premise servers (mock implementation)"""
        # In production, this would connect to internal APIs
        mock_servers = [
            {
                "node_id": "ONPREM_BLR_01",
                "name": "Bangalore Data Center",
                "type": "On-Premise",
                "status": "verified",
                "location": "Bangalore, India",
                "lat": 12.9716,
                "lng": 77.5946,
                "risk": "Low",
                "co2": 65,
                "in_india": True
            },
            {
                "node_id": "ONPREM_DEL_01",
                "name": "Delhi Data Center",
                "type": "On-Premise",
                "status": "verified",
                "location": "Delhi, India",
                "lat": 28.7041,
                "lng": 77.1025,
                "risk": "Zero",
                "co2": 85,
                "in_india": True
            }
        ]
        return mock_servers
    
    def scan_azure_blobs(self):
        """Scan Azure Blob Storage (mock implementation)"""
        # In production, use Azure SDK
        mock_azure = [
            {
                "node_id": "AZURE_CHN_01",
                "name": "Chennai Azure Node",
                "type": "Azure Blob",
                "status": "verified",
                "location": "Chennai, India",
                "lat": 13.0827,
                "lng": 80.2707,
                "risk": "Zero",
                "co2": 120,
                "in_india": True
            }
        ]
        return mock_azure
    
    def detect_shadow_data(self, nodes):
        """
        Use AI to detect sensitive data patterns
        This is where you'd integrate with AWS Macie, Azure Purview, etc.
        """
        for node in nodes:
            # Mock AI detection logic
            if node['status'] == 'pending':
                node['shadow_data_detected'] = True
                node['pii_types'] = ['Aadhaar', 'PAN Card', 'Email', 'Phone']
            else:
                node['shadow_data_detected'] = False
                node['pii_types'] = []
        
        return nodes
    
    def push_to_dashboard(self, data):
        """Send discovered telemetry to the React Topology Map"""
        payload = {
            "org_id": ORG_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "nodes": data
        }
        
        try:
            response = requests.post(DASHBOARD_API_URL, json=payload, timeout=5)
            return response.status_code
        except Exception as e:
            print(f"Error pushing to dashboard: {e}")
            return 500
    
    def _get_region_location(self, region):
        """Map AWS region to location name"""
        region_map = {
            'ap-south-1': 'Mumbai, India',
            'us-east-1': 'Virginia, USA',
            'eu-west-1': 'Ireland, EU',
            'ap-southeast-1': 'Singapore'
        }
        return region_map.get(region, region)
    
    def _get_region_lat(self, region):
        """Get latitude for region"""
        coords = {
            'ap-south-1': 19.0760,
            'us-east-1': 37.4316,
            'eu-west-1': 53.3498,
            'ap-southeast-1': 1.3521
        }
        return coords.get(region, 20.5937)
    
    def _get_region_lng(self, region):
        """Get longitude for region"""
        coords = {
            'ap-south-1': 72.8777,
            'us-east-1': -78.6569,
            'eu-west-1': -6.2603,
            'ap-southeast-1': 103.8198
        }
        return coords.get(region, 78.9629)
    
    def _estimate_carbon_offset(self, resource_name):
        """Estimate carbon offset from software sanitization"""
        # Mock calculation: 1TB = 50kg CO2 saved
        import random
        return random.randint(30, 150)
    
    def run_scan_cycle(self):
        """Execute a complete scan cycle"""
        print(f"\n{'='*50}")
        print(f"🚀 Discovery Agent - Scan Cycle Started")
        print(f"{'='*50}")
        
        all_nodes = []
        
        # Scan AWS
        print("📡 Scanning AWS infrastructure...")
        aws_nodes = self.scan_s3_buckets()
        all_nodes.extend(aws_nodes)
        print(f"   Found {len(aws_nodes)} AWS nodes")
        
        # Scan Azure
        print("📡 Scanning Azure infrastructure...")
        azure_nodes = self.scan_azure_blobs()
        all_nodes.extend(azure_nodes)
        print(f"   Found {len(azure_nodes)} Azure nodes")
        
        # Scan On-Prem
        print("📡 Scanning On-Premise infrastructure...")
        onprem_nodes = self.scan_onprem_servers()
        all_nodes.extend(onprem_nodes)
        print(f"   Found {len(onprem_nodes)} On-Prem nodes")
        
        # AI Shadow Data Detection
        print("🤖 Running AI Shadow Data Detection...")
        all_nodes = self.detect_shadow_data(all_nodes)
        
        # Filter nodes outside India
        india_nodes = [n for n in all_nodes if n.get('in_india', False)]
        foreign_nodes = [n for n in all_nodes if not n.get('in_india', False)]
        
        print(f"\n📊 Scan Results:")
        print(f"   Total Nodes: {len(all_nodes)}")
        print(f"   India Nodes: {len(india_nodes)} ✅")
        print(f"   Foreign Nodes: {len(foreign_nodes)} ⚠️")
        print(f"   Risk Nodes: {len([n for n in all_nodes if n['status'] == 'pending'])}")
        
        # Push to dashboard
        status = self.push_to_dashboard(all_nodes)
        print(f"\n✓ Dashboard Update Status: {status}")
        
        return all_nodes


def main():
    """Main execution loop"""
    agent = DataDiscoveryAgent()
    
    print("\n" + "="*50)
    print("🇮🇳 TRICOLOR DISCOVERY AGENT - 2026")
    print("   Sovereign Data Compliance Scanner")
    print("="*50)
    
    if '--once' in os.sys.argv:
        # Run once and exit
        agent.run_scan_cycle()
    else:
        # Continuous monitoring
        print(f"\n⏰ Running continuous monitoring (every {SCAN_INTERVAL}s)")
        print("   Press Ctrl+C to stop\n")
        
        while True:
            try:
                agent.run_scan_cycle()
                print(f"\n💤 Waiting {SCAN_INTERVAL}s for next scan...")
                time.sleep(SCAN_INTERVAL)
            except KeyboardInterrupt:
                print("\n\n👋 Discovery Agent stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Error in scan cycle: {e}")
                time.sleep(60)  # Wait 1 min before retry


if __name__ == "__main__":
    import sys
    os.sys = sys
    main()
