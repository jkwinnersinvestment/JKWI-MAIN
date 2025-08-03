#!/usr/bin/env python3
"""
Simple test script to verify the JKWI cloud system is working correctly
Run this after setting up the cloud system to ensure everything is functioning
"""

import requests
import json
import time
import sys
from datetime import datetime

class JKWITestSuite:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.auth_token = None
        self.test_results = []
    
    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_health_check(self):
        """Test if the API is responding"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            test_user = {
                "username": f"test_user_{int(time.time())}",
                "password": "test_password_123",
                "email": "test@jkwi.com",
                "division": "Finance Division"
            }
            
            response = requests.post(
                f"{self.base_url}/api/register",
                json=test_user,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get('access_token')
                self.test_user = test_user
                self.log_test("User Registration", True, f"User: {test_user['username']}")
                return True
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        try:
            if not hasattr(self, 'test_user'):
                self.log_test("User Login", False, "No test user available")
                return False
            
            login_data = {
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
            
            response = requests.post(
                f"{self.base_url}/api/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                self.log_test("User Login", True, f"Token received: {'Yes' if self.auth_token else 'No'}")
                return True
            else:
                self.log_test("User Login", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Login", False, f"Error: {str(e)}")
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_company_api(self):
        """Test company API endpoints"""
        try:
            # Test GET company
            response = requests.get(
                f"{self.base_url}/api/company",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                company_data = response.json()
                self.log_test("Get Company Data", True, f"Company: {company_data.get('name', 'Unknown')}")
                
                # Test UPDATE company
                updated_data = {
                    **company_data,
                    "description": f"Updated at {datetime.now().isoformat()}"
                }
                
                update_response = requests.put(
                    f"{self.base_url}/api/company",
                    json=updated_data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if update_response.status_code == 200:
                    self.log_test("Update Company Data", True)
                    return True
                else:
                    self.log_test("Update Company Data", False, f"Status: {update_response.status_code}")
                    return False
            else:
                self.log_test("Get Company Data", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Company API", False, f"Error: {str(e)}")
            return False
    
    def test_stats_api(self):
        """Test statistics API"""
        try:
            response = requests.get(
                f"{self.base_url}/api/stats",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                stats = response.json()
                self.log_test("Get Statistics", True, 
                    f"Members: {stats.get('totalMembers')}, "
                    f"Directors: {stats.get('totalDirectors')}, "
                    f"Divisions: {stats.get('totalDivisions')}")
                return True
            else:
                self.log_test("Get Statistics", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Statistics API", False, f"Error: {str(e)}")
            return False
    
    def test_members_crud(self):
        """Test member CRUD operations"""
        try:
            # Test GET members
            response = requests.get(
                f"{self.base_url}/api/members",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                members = response.json()
                self.log_test("Get Members", True, f"Found {len(members)} members")
                
                # Test ADD member
                new_member = {
                    "username": f"test_member_{int(time.time())}",
                    "fullName": "Test Member",
                    "email": "testmember@jkwi.com",
                    "division": "Mining Division",
                    "status": "Active"
                }
                
                add_response = requests.post(
                    f"{self.base_url}/api/members",
                    json=new_member,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if add_response.status_code == 201:
                    member_data = add_response.json().get('data', {})
                    member_id = member_data.get('id')
                    self.log_test("Add Member", True, f"Member ID: {member_id}")
                    
                    # Test UPDATE member
                    if member_id:
                        updated_member = {
                            **member_data,
                            "status": "Pending"
                        }
                        
                        update_response = requests.put(
                            f"{self.base_url}/api/members/{member_id}",
                            json=updated_member,
                            headers=self.get_auth_headers(),
                            timeout=10
                        )
                        
                        if update_response.status_code == 200:
                            self.log_test("Update Member", True)
                            
                            # Test DELETE member
                            delete_response = requests.delete(
                                f"{self.base_url}/api/members/{member_id}",
                                headers=self.get_auth_headers(),
                                timeout=10
                            )
                            
                            if delete_response.status_code == 200:
                                self.log_test("Delete Member", True)
                                return True
                            else:
                                self.log_test("Delete Member", False, f"Status: {delete_response.status_code}")
                        else:
                            self.log_test("Update Member", False, f"Status: {update_response.status_code}")
                    else:
                        self.log_test("Member CRUD", False, "No member ID returned")
                else:
                    self.log_test("Add Member", False, f"Status: {add_response.status_code}")
            else:
                self.log_test("Get Members", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Members CRUD", False, f"Error: {str(e)}")
            return False
    
    def test_data_export(self):
        """Test data export functionality"""
        try:
            response = requests.get(
                f"{self.base_url}/api/export",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                export_data = response.json()
                self.log_test("Data Export", True, 
                    f"Exported collections: {list(export_data.keys())}")
                return True
            else:
                self.log_test("Data Export", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Data Export", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting JKWI Cloud System Tests")
        print("=" * 50)
        
        # Basic connectivity tests
        if not self.test_health_check():
            print("\n❌ Health check failed. Is the server running?")
            return False
        
        # Authentication tests
        if not self.test_user_registration():
            print("\n❌ User registration failed.")
            return False
        
        if not self.test_user_login():
            print("\n❌ User login failed.")
            return False
        
        # API functionality tests
        self.test_company_api()
        self.test_stats_api()
        self.test_members_crud()
        self.test_data_export()
        
        # Summary
        print("\n" + "=" * 50)
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        total_tests = len(self.test_results)
        
        print(f"📊 Test Summary: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Your JKWI cloud system is working correctly.")
            return True
        else:
            print("⚠️ Some tests failed. Check the output above for details.")
            return False
    
    def save_test_report(self, filename="jkwi_test_report.json"):
        """Save test results to file"""
        report = {
            'test_run': {
                'timestamp': datetime.now().isoformat(),
                'base_url': self.base_url,
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for r in self.test_results if r['passed'])
            },
            'results': self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Test report saved to: {filename}")

def main():
    """Main test function"""
    # Check command line arguments
    base_url = "http://localhost:5000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"🔗 Testing JKWI system at: {base_url}")
    
    # Run tests
    test_suite = JKWITestSuite(base_url)
    success = test_suite.run_all_tests()
    
    # Save report
    test_suite.save_test_report()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
