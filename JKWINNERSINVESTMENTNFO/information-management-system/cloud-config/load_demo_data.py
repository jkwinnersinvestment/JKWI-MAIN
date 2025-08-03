#!/usr/bin/env python3
"""
Demo Data Loader for JKWI Cloud System
Loads demo members and data into the cloud system for testing
"""

import json
import requests
import sys
import time
from datetime import datetime

class JKWIDemoDataLoader:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.auth_token = None
        self.admin_user = {
            "username": "jkwi_admin",
            "password": "Admin123!",
            "email": "admin@jkwi.co.za",
            "division": "Executive"
        }
    
    def load_demo_data(self, filename="jkwi_demo_data.json"):
        """Load demo data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Demo data file not found: {filename}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error reading demo data: {e}")
            return None
    
    def register_admin_user(self):
        """Register admin user for loading data"""
        try:
            response = requests.post(
                f"{self.base_url}/api/register",
                json=self.admin_user,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get('access_token')
                print("✅ Admin user registered successfully")
                return True
            else:
                print(f"❌ Admin registration failed: {response.status_code}")
                # Try to login instead
                return self.login_admin_user()
        except Exception as e:
            print(f"❌ Admin registration error: {str(e)}")
            return False
    
    def login_admin_user(self):
        """Login admin user"""
        try:
            login_data = {
                "username": self.admin_user["username"],
                "password": self.admin_user["password"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                print("✅ Admin user logged in successfully")
                return True
            else:
                print(f"❌ Admin login failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Admin login error: {str(e)}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def load_company_data(self, company_data):
        """Load company information"""
        try:
            response = requests.put(
                f"{self.base_url}/api/company",
                json=company_data,
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Company data loaded successfully")
                return True
            else:
                print(f"❌ Company data load failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Company data load error: {str(e)}")
            return False
    
    def load_divisions(self, divisions_data):
        """Load divisions"""
        success_count = 0
        
        for division in divisions_data:
            try:
                response = requests.post(
                    f"{self.base_url}/api/divisions",
                    json=division,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 201:
                    success_count += 1
                    print(f"✅ Division loaded: {division['name']}")
                else:
                    print(f"❌ Division load failed: {division['name']} ({response.status_code})")
            except Exception as e:
                print(f"❌ Division load error: {division['name']} - {str(e)}")
            
            time.sleep(0.5)  # Small delay to avoid overwhelming the server
        
        print(f"📊 Divisions loaded: {success_count}/{len(divisions_data)}")
        return success_count > 0
    
    def load_directors(self, directors_data):
        """Load directors"""
        success_count = 0
        
        for director in directors_data:
            try:
                response = requests.post(
                    f"{self.base_url}/api/directors",
                    json=director,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 201:
                    success_count += 1
                    print(f"✅ Director loaded: {director['fullName']}")
                else:
                    print(f"❌ Director load failed: {director['fullName']} ({response.status_code})")
            except Exception as e:
                print(f"❌ Director load error: {director['fullName']} - {str(e)}")
            
            time.sleep(0.5)
        
        print(f"📊 Directors loaded: {success_count}/{len(directors_data)}")
        return success_count > 0
    
    def load_members(self, members_data):
        """Load members"""
        success_count = 0
        
        for member in members_data:
            try:
                response = requests.post(
                    f"{self.base_url}/api/members",
                    json=member,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 201:
                    success_count += 1
                    print(f"✅ Member loaded: {member['fullName']}")
                else:
                    print(f"❌ Member load failed: {member['fullName']} ({response.status_code})")
            except Exception as e:
                print(f"❌ Member load error: {member['fullName']} - {str(e)}")
            
            time.sleep(0.5)
        
        print(f"📊 Members loaded: {success_count}/{len(members_data)}")
        return success_count > 0
    
    def load_partnerships(self, partnerships_data):
        """Load partnerships"""
        success_count = 0
        
        for partnership in partnerships_data:
            try:
                response = requests.post(
                    f"{self.base_url}/api/partnerships",
                    json=partnership,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 201:
                    success_count += 1
                    print(f"✅ Partnership loaded: {partnership['companyName']}")
                else:
                    print(f"❌ Partnership load failed: {partnership['companyName']} ({response.status_code})")
            except Exception as e:
                print(f"❌ Partnership load error: {partnership['companyName']} - {str(e)}")
            
            time.sleep(0.5)
        
        print(f"📊 Partnerships loaded: {success_count}/{len(partnerships_data)}")
        return success_count > 0
    
    def check_server_health(self):
        """Check if the server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy")
                return True
            else:
                print(f"❌ Server health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Server not reachable: {str(e)}")
            return False
    
    def load_all_demo_data(self, filename="jkwi_demo_data.json"):
        """Load all demo data into the system"""
        print("🚀 JKWI Demo Data Loader")
        print("=" * 40)
        
        # Check server health
        if not self.check_server_health():
            print("❌ Server is not running. Please start the JKWI cloud system first.")
            return False
        
        # Load demo data from file
        demo_data = self.load_demo_data(filename)
        if not demo_data:
            return False
        
        # Register/login admin user
        if not self.register_admin_user():
            print("❌ Failed to authenticate admin user")
            return False
        
        print("\n📥 Loading demo data...")
        
        # Load company data
        if 'company' in demo_data:
            self.load_company_data(demo_data['company'])
        
        # Load divisions
        if 'divisions' in demo_data:
            self.load_divisions(demo_data['divisions'])
        
        # Load directors
        if 'directors' in demo_data:
            self.load_directors(demo_data['directors'])
        
        # Load members
        if 'members' in demo_data:
            self.load_members(demo_data['members'])
        
        # Load partnerships
        if 'partnerships' in demo_data:
            self.load_partnerships(demo_data['partnerships'])
        
        print("\n🎉 Demo data loading completed!")
        print(f"You can now access the system at: {self.base_url}")
        print("Admin credentials:")
        print(f"  Username: {self.admin_user['username']}")
        print(f"  Password: {self.admin_user['password']}")
        
        return True

def main():
    """Main function"""
    # Get base URL from command line or use default
    base_url = "http://localhost:5000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    # Get demo data filename
    filename = "jkwi_demo_data.json"
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    
    print(f"🔗 Loading demo data into: {base_url}")
    print(f"📁 Using demo data file: {filename}")
    
    # Load demo data
    loader = JKWIDemoDataLoader(base_url)
    success = loader.load_all_demo_data(filename)
    
    if success:
        print("\n✅ Demo data loaded successfully!")
        print("🎯 You can now test the system with realistic member data")
    else:
        print("\n❌ Demo data loading failed!")
        print("💡 Make sure the JKWI cloud system is running first")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
