#!/usr/bin/env python3
"""
Demo Data Creator for JKWI Cloud System
Creates realistic demo members, directors, and divisions for testing
"""

import json
import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class JKWIDemoDataGenerator:
    def __init__(self):
        self.demo_data = {
            "members": [],
            "directors": [],
            "divisions": [],
            "company": {},
            "partnerships": []
        }
        
        # South African names and surnames for realistic demo data
        self.first_names = [
            "Sipho", "Nomsa", "Thabo", "Lindiwe", "Mandla", "Zanele", "Bongani", "Naledi",
            "Tshepo", "Nonhlanhla", "Kagiso", "Palesa", "Lerato", "Sizani", "Mpho", "Ntombi",
            "Dumisani", "Precious", "Lucky", "Beauty", "Justice", "Faith", "Hope", "Grace",
            "John", "Mary", "David", "Sarah", "Michael", "Elizabeth", "James", "Jennifer"
        ]
        
        self.surnames = [
            "Mthembu", "Nkomo", "Dlamini", "Mokoena", "Maluleke", "Mbeki", "Zulu", "Xhosa",
            "Ndlovu", "Molefe", "Mokone", "Mashaba", "Mabaso", "Makhubo", "Mohlala", "Motsepe",
            "Ramaphosa", "Mabuza", "Sisulu", "Maimane", "Steenhuisen", "Malema", "Zuma", "Mandela",
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"
        ]
        
        self.divisions = [
            {
                "name": "Finance Division",
                "description": "Managing financial operations, investments, and treasury functions",
                "head": "",
                "budget": 5000000,
                "color": "#27ae60"
            },
            {
                "name": "Mining Division", 
                "description": "Overseeing mining operations, exploration, and mineral rights",
                "head": "",
                "budget": 15000000,
                "color": "#8b4513"
            },
            {
                "name": "Infrastructure Division",
                "description": "Managing construction, development, and infrastructure projects",
                "head": "",
                "budget": 12000000,
                "color": "#3498db"
            },
            {
                "name": "Farming Division",
                "description": "Agricultural operations, livestock, and sustainable farming practices",
                "head": "",
                "budget": 8000000,
                "color": "#2ecc71"
            },
            {
                "name": "Legal Division",
                "description": "Legal compliance, contracts, and regulatory affairs",
                "head": "",
                "budget": 3000000,
                "color": "#9b59b6"
            },
            {
                "name": "Media Division",
                "description": "Communications, public relations, and media management",
                "head": "",
                "budget": 2500000,
                "color": "#e74c3c"
            },
            {
                "name": "Service Division",
                "description": "Customer service, support operations, and member relations",
                "head": "",
                "budget": 4000000,
                "color": "#f39c12"
            },
            {
                "name": "Social Division",
                "description": "Community outreach, CSR programs, and social development",
                "head": "",
                "budget": 3500000,
                "color": "#1abc9c"
            }
        ]
        
        self.statuses = ["Active", "Pending", "Inactive"]
        self.member_types = ["Regular", "Premium", "Executive", "Founder"]
        
    def generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())[:8]
    
    def generate_email(self, first_name: str, surname: str) -> str:
        """Generate realistic email address"""
        domains = ["jkwi.co.za", "gmail.com", "outlook.com", "yahoo.com", "webmail.co.za"]
        clean_first = first_name.lower().replace(" ", "")
        clean_surname = surname.lower().replace(" ", "")
        
        patterns = [
            f"{clean_first}.{clean_surname}",
            f"{clean_first}{clean_surname}",
            f"{clean_first[0]}{clean_surname}",
            f"{clean_first}_{clean_surname}",
        ]
        
        pattern = random.choice(patterns)
        domain = random.choice(domains)
        return f"{pattern}@{domain}"
    
    def generate_phone(self) -> str:
        """Generate South African phone number"""
        area_codes = ["011", "021", "031", "012", "041", "051", "053", "054", "058"]
        area_code = random.choice(area_codes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"+27-{area_code}-{number[:3]}-{number[3:]}"
    
    def generate_address(self) -> Dict[str, str]:
        """Generate South African address"""
        streets = [
            "Main Road", "Church Street", "Market Street", "Long Street", "Loop Street",
            "Commissioner Street", "Pritchard Street", "Fox Street", "Anderson Street",
            "Mandela Avenue", "Jan Smuts Avenue", "Barry Hertzog Avenue", "William Nicol Drive"
        ]
        
        cities = [
            "Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth",
            "Bloemfontein", "East London", "Pietermaritzburg", "Rustenburg", "Nelspruit"
        ]
        
        provinces = [
            "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Free State",
            "Northern Cape", "North West", "Mpumalanga", "Limpopo"
        ]
        
        return {
            "street": f"{random.randint(1, 999)} {random.choice(streets)}",
            "city": random.choice(cities),
            "province": random.choice(provinces),
            "postal_code": f"{random.randint(1000, 9999)}",
            "country": "South Africa"
        }
    
    def generate_join_date(self) -> str:
        """Generate realistic join date"""
        start_date = datetime.now() - timedelta(days=365*3)  # 3 years ago
        end_date = datetime.now() - timedelta(days=30)       # At least 30 days ago
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        
        join_date = start_date + timedelta(days=random_days)
        return join_date.strftime("%Y-%m-%d")
    
    def create_demo_members(self, count: int = 50) -> List[Dict[str, Any]]:
        """Create demo members"""
        members = []
        
        for i in range(count):
            first_name = random.choice(self.first_names)
            surname = random.choice(self.surnames)
            full_name = f"{first_name} {surname}"
            
            member = {
                "id": self.generate_id(),
                "username": f"{first_name.lower()}.{surname.lower()}{random.randint(1, 999)}",
                "fullName": full_name,
                "firstName": first_name,
                "surname": surname,
                "email": self.generate_email(first_name, surname),
                "phone": self.generate_phone(),
                "address": self.generate_address(),
                "division": random.choice([d["name"] for d in self.divisions]),
                "memberType": random.choice(self.member_types),
                "status": random.choice(self.statuses),
                "joinDate": self.generate_join_date(),
                "lastActive": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "membershipNumber": f"JKWI-{2024}-{str(i+1).zfill(4)}",
                "emergencyContact": {
                    "name": f"{random.choice(self.first_names)} {random.choice(self.surnames)}",
                    "phone": self.generate_phone(),
                    "relationship": random.choice(["Spouse", "Parent", "Sibling", "Friend"])
                },
                "skills": random.sample([
                    "Leadership", "Project Management", "Financial Analysis", "Mining Operations",
                    "Construction", "Agriculture", "Legal Compliance", "Marketing", "IT",
                    "Human Resources", "Logistics", "Quality Control", "Safety Management"
                ], k=random.randint(2, 5)),
                "notes": f"Demo member created for testing purposes. Member #{i+1}",
                "dateCreated": datetime.now().isoformat(),
                "lastModified": datetime.now().isoformat()
            }
            
            members.append(member)
        
        return members
    
    def create_demo_directors(self, count: int = 12) -> List[Dict[str, Any]]:
        """Create demo directors"""
        directors = []
        
        # Ensure we have directors for each division
        division_names = [d["name"] for d in self.divisions]
        
        for i in range(count):
            first_name = random.choice(self.first_names)
            surname = random.choice(self.surnames)
            full_name = f"{first_name} {surname}"
            
            # Assign division (ensure each division has at least one director)
            if i < len(division_names):
                division = division_names[i]
            else:
                division = random.choice(division_names)
            
            director = {
                "id": self.generate_id(),
                "fullName": full_name,
                "firstName": first_name,
                "surname": surname,
                "email": self.generate_email(first_name, surname),
                "phone": self.generate_phone(),
                "division": division,
                "position": random.choice([
                    "Division Director", "Deputy Director", "Senior Manager", 
                    "Operations Manager", "Strategic Advisor"
                ]),
                "experience": random.randint(5, 25),
                "qualifications": random.sample([
                    "MBA", "BCom", "BSc Engineering", "LLB", "CA(SA)", "CPA", "PMP",
                    "Mining Engineering", "Civil Engineering", "Agricultural Science"
                ], k=random.randint(1, 3)),
                "startDate": self.generate_join_date(),
                "salary": random.randint(500000, 2000000),
                "status": random.choice(["Active", "On Leave", "Active"]),  # Bias towards Active
                "achievements": [
                    f"Led successful project worth R{random.randint(1, 50)}M",
                    f"Increased division efficiency by {random.randint(10, 40)}%",
                    f"Managed team of {random.randint(15, 100)} people"
                ],
                "address": self.generate_address(),
                "emergencyContact": {
                    "name": f"{random.choice(self.first_names)} {random.choice(self.surnames)}",
                    "phone": self.generate_phone(),
                    "relationship": random.choice(["Spouse", "Parent", "Sibling"])
                },
                "notes": f"Demo director for {division}. Created for testing purposes.",
                "dateCreated": datetime.now().isoformat(),
                "lastModified": datetime.now().isoformat()
            }
            
            directors.append(director)
        
        return directors
    
    def create_demo_partnerships(self, count: int = 8) -> List[Dict[str, Any]]:
        """Create demo partnerships"""
        partnerships = []
        
        company_names = [
            "Sasol Limited", "Anglo American", "Gold Fields", "Harmony Gold",
            "Standard Bank", "FirstRand Bank", "Woolworths Holdings", "Shoprite Holdings",
            "MTN Group", "Vodacom Group", "Tiger Brands", "Naspers Limited",
            "African Rainbow Minerals", "Kumba Iron Ore", "Exxaro Resources"
        ]
        
        partnership_types = [
            "Strategic Alliance", "Joint Venture", "Supplier Partnership", 
            "Technology Partnership", "Investment Partnership", "Service Partnership"
        ]
        
        for i in range(count):
            partnership = {
                "id": self.generate_id(),
                "companyName": random.choice(company_names),
                "partnershipType": random.choice(partnership_types),
                "description": f"Strategic partnership focusing on {random.choice(['mining operations', 'financial services', 'technology solutions', 'infrastructure development', 'agricultural projects'])}",
                "startDate": self.generate_join_date(),
                "endDate": None if random.random() > 0.3 else (datetime.now() + timedelta(days=random.randint(365, 1095))).strftime("%Y-%m-%d"),
                "value": random.randint(1000000, 50000000),
                "status": random.choice(["Active", "Under Review", "Pending", "Active", "Active"]),  # Bias towards Active
                "contactPerson": {
                    "name": f"{random.choice(self.first_names)} {random.choice(self.surnames)}",
                    "email": f"contact{i+1}@{random.choice(company_names).lower().replace(' ', '').replace('limited', '')}.co.za",
                    "phone": self.generate_phone(),
                    "position": random.choice(["Partnership Manager", "Business Development", "CEO", "Director"])
                },
                "benefits": [
                    "Access to new markets",
                    "Technology sharing",
                    "Cost reduction opportunities",
                    "Risk sharing",
                    "Enhanced capabilities"
                ][:random.randint(2, 5)],
                "requirements": [
                    "Monthly progress reports",
                    "Quarterly reviews",
                    "Annual audits",
                    "Compliance monitoring"
                ][:random.randint(1, 4)],
                "notes": f"Demo partnership #{i+1} for testing purposes",
                "dateCreated": datetime.now().isoformat(),
                "lastModified": datetime.now().isoformat()
            }
            
            partnerships.append(partnership)
        
        return partnerships
    
    def create_company_info(self) -> Dict[str, Any]:
        """Create company information"""
        return {
            "name": "JK Winners Investment",
            "registrationNumber": "2019/123456/07",
            "taxNumber": "9876543210",
            "vatNumber": "4567890123",
            "founded": "2019",
            "description": "JK Winners Investment is a diversified investment company focused on mining, agriculture, infrastructure, and financial services across South Africa.",
            "vision": "To be the leading investment company driving sustainable economic growth and community development in South Africa.",
            "mission": "Empowering communities through strategic investments, creating value for stakeholders, and contributing to South Africa's economic transformation.",
            "address": {
                "street": "123 Sandton Drive, Sandton City",
                "city": "Johannesburg",
                "province": "Gauteng",
                "postal_code": "2196",
                "country": "South Africa"
            },
            "contact": {
                "phone": "+27-11-784-5000",
                "fax": "+27-11-784-5001",
                "email": "info@jkwi.co.za",
                "website": "https://www.jkwinnersinvestment.co.za"
            },
            "bankDetails": {
                "bank": "Standard Bank of South Africa",
                "accountNumber": "12345678901",
                "branchCode": "051001",
                "swiftCode": "SBZAZAJJ"
            },
            "directors": [
                "Board of Directors as per company records"
            ],
            "totalEmployees": 500,
            "totalMembers": 1250,
            "establishedYear": 2019,
            "lastUpdated": datetime.now().isoformat()
        }
    
    def generate_all_demo_data(self) -> Dict[str, Any]:
        """Generate all demo data"""
        print("🚀 Generating demo data for JKWI system...")
        
        # Generate company info
        print("📋 Creating company information...")
        self.demo_data["company"] = self.create_company_info()
        
        # Generate divisions (use predefined ones)
        print("🏢 Setting up divisions...")
        self.demo_data["divisions"] = self.divisions
        
        # Generate directors
        print("👥 Creating demo directors...")
        self.demo_data["directors"] = self.create_demo_directors(12)
        
        # Assign division heads
        for division in self.demo_data["divisions"]:
            division_directors = [d for d in self.demo_data["directors"] if d["division"] == division["name"]]
            if division_directors:
                division["head"] = division_directors[0]["fullName"]
        
        # Generate members
        print("👤 Creating demo members...")
        self.demo_data["members"] = self.create_demo_members(50)
        
        # Generate partnerships
        print("🤝 Creating demo partnerships...")
        self.demo_data["partnerships"] = self.create_demo_partnerships(8)
        
        # Add metadata
        self.demo_data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "generated_by": "JKWI Demo Data Generator",
            "version": "1.0",
            "total_records": {
                "members": len(self.demo_data["members"]),
                "directors": len(self.demo_data["directors"]),
                "divisions": len(self.demo_data["divisions"]),
                "partnerships": len(self.demo_data["partnerships"])
            }
        }
        
        print("✅ Demo data generation complete!")
        return self.demo_data
    
    def save_to_file(self, filename: str = "jkwi_demo_data.json"):
        """Save demo data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.demo_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Demo data saved to: {filename}")
    
    def create_sql_inserts(self, filename: str = "jkwi_demo_data.sql"):
        """Create SQL insert statements for demo data"""
        sql_content = """
-- JKWI Demo Data SQL Inserts
-- Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

-- Company Information
INSERT INTO company (name, registration_number, description, address, contact_info, created_at) 
VALUES (
    '""" + self.demo_data["company"]["name"] + """',
    '""" + self.demo_data["company"]["registrationNumber"] + """',
    '""" + self.demo_data["company"]["description"] + """',
    '""" + json.dumps(self.demo_data["company"]["address"]).replace("'", "''") + """',
    '""" + json.dumps(self.demo_data["company"]["contact"]).replace("'", "''") + """',
    NOW()
);

-- Divisions
"""
        for division in self.demo_data["divisions"]:
            sql_content += f"""
INSERT INTO divisions (name, description, head, budget, color, created_at) 
VALUES (
    '{division["name"]}',
    '{division["description"]}',
    '{division["head"]}',
    {division["budget"]},
    '{division["color"]}',
    NOW()
);
"""
        
        sql_content += "\n-- Directors\n"
        for director in self.demo_data["directors"]:
            sql_content += f"""
INSERT INTO directors (full_name, email, phone, division, position, experience, salary, status, created_at) 
VALUES (
    '{director["fullName"]}',
    '{director["email"]}',
    '{director["phone"]}',
    '{director["division"]}',
    '{director["position"]}',
    {director["experience"]},
    {director["salary"]},
    '{director["status"]}',
    NOW()
);
"""
        
        sql_content += "\n-- Members\n"
        for member in self.demo_data["members"]:
            sql_content += f"""
INSERT INTO members (username, full_name, email, phone, division, member_type, status, membership_number, created_at) 
VALUES (
    '{member["username"]}',
    '{member["fullName"]}',
    '{member["email"]}',
    '{member["phone"]}',
    '{member["division"]}',
    '{member["memberType"]}',
    '{member["status"]}',
    '{member["membershipNumber"]}',
    NOW()
);
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print(f"📄 SQL inserts saved to: {filename}")

def main():
    """Main function to generate and save demo data"""
    print("🎯 JKWI Demo Data Generator")
    print("=" * 40)
    
    generator = JKWIDemoDataGenerator()
    
    # Generate all demo data
    demo_data = generator.generate_all_demo_data()
    
    # Save to JSON file
    generator.save_to_file("jkwi_demo_data.json")
    
    # Create SQL inserts
    generator.create_sql_inserts("jkwi_demo_data.sql")
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   Members: {len(demo_data['members'])}")
    print(f"   Directors: {len(demo_data['directors'])}")
    print(f"   Divisions: {len(demo_data['divisions'])}")
    print(f"   Partnerships: {len(demo_data['partnerships'])}")
    
    print("\n🎉 Demo data generation complete!")
    print("Files created:")
    print("   - jkwi_demo_data.json (JSON format)")
    print("   - jkwi_demo_data.sql (SQL inserts)")
    
    return demo_data

if __name__ == "__main__":
    main()
