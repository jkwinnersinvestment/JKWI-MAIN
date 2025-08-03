import json
import os
from pathlib import Path
from datetime import datetime
import uuid

class DemoMemberService:
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = "c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/information-management-system"
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data" / "demo_members"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # JKWI divisions for demo members
        self.divisions = [
            'Mining Division',
            'Infrastructure Division', 
            'Farming Division',
            'Service Division',
            'Finance Division',
            'Legal Division',
            'Media Division',
            'Social Division'
        ]
        
        # Load existing demo members
        self.demo_members = self.load_demo_members()

    def load_demo_members(self):
        """Load existing demo members from local storage"""
        demo_file = self.data_path / "demo_members.json"
        if demo_file.exists():
            try:
                with open(demo_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"members": [], "total_count": 0, "last_updated": None}

    def save_demo_members(self):
        """Save demo members to local storage"""
        demo_file = self.data_path / "demo_members.json"
        self.demo_members["last_updated"] = datetime.now().isoformat()
        self.demo_members["total_count"] = len(self.demo_members["members"])
        
        with open(demo_file, 'w', encoding='utf-8') as f:
            json.dump(self.demo_members, f, indent=2, ensure_ascii=False)

    def create_demo_member(self, municipality_code, municipality_name, country, division_index=0):
        """Create a single demo member"""
        timestamp = datetime.now().isoformat()
        member_id = f"{municipality_code}_{str(uuid.uuid4()).split('-')[0]}"
        
        demo_member = {
            "id": len(self.demo_members["members"]) + 1,
            "member_id": member_id,
            "username": f"demo_{municipality_code.lower()}",
            "fullName": f"Demo Member {municipality_name}",
            "email": f"demo.{municipality_code.lower()}@jkwi.com",
            "division": self.divisions[division_index % len(self.divisions)],
            "status": "Active",
            "registrationDate": timestamp,
            "municipality": {
                "code": municipality_code,
                "name": municipality_name,
                "country": country.replace('_', ' ').title()
            },
            "contact_info": {
                "phone": f"+27{municipality_code[2:5] if len(municipality_code) > 4 else '123'}000001",
                "address": f"Demo Address, {municipality_name}"
            },
            "is_demo": True,
            "demo_credentials": {
                "username": f"demo_{municipality_code.lower()}",
                "password": "demo123"
            }
        }
        
        return demo_member

    def generate_demo_members_for_municipalities(self, municipalities_data):
        """Generate demo members for all municipalities"""
        division_counter = 0
        created_count = 0
        
        for country, country_data in municipalities_data.items():
            for municipality_code, municipality_info in country_data.get('MUNICIPALITIES', {}).items():
                # Check if demo member already exists
                existing = next((m for m in self.demo_members["members"] 
                               if m.get("municipality", {}).get("code") == municipality_code), None)
                
                if not existing:
                    demo_member = self.create_demo_member(
                        municipality_code,
                        municipality_info['name'],
                        country,
                        division_counter
                    )
                    
                    self.demo_members["members"].append(demo_member)
                    created_count += 1
                    division_counter += 1
        
        if created_count > 0:
            self.save_demo_members()
        
        return created_count

    def get_all_demo_members(self):
        """Get all demo members"""
        return self.demo_members["members"]

    def get_demo_member_by_municipality(self, municipality_code):
        """Get demo member for specific municipality"""
        return next((m for m in self.demo_members["members"] 
                    if m.get("municipality", {}).get("code") == municipality_code), None)

    def export_for_webapp(self):
        """Export demo members in format compatible with webapp"""
        webapp_format = []
        
        for member in self.demo_members["members"]:
            webapp_member = {
                "id": member["id"],
                "username": member["username"],
                "fullName": member["fullName"],
                "email": member["email"],
                "division": member["division"],
                "status": member["status"],
                "registrationDate": member["registrationDate"]
            }
            webapp_format.append(webapp_member)
        
        # Save to webapp data directory
        webapp_data_file = self.base_path / "js" / "demo_members.js"
        
        js_content = f"""// Auto-generated demo members data
const demoMembers = {json.dumps(webapp_format, indent=2)};

// Add demo members to dataManager if it exists
if (typeof dataManager !== 'undefined') {{
    demoMembers.forEach(member => {{
        const existing = dataManager.getMembers().find(m => m.username === member.username);
        if (!existing) {{
            dataManager.addMember(member);
        }}
    }});
}}
"""
        
        with open(webapp_data_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return webapp_data_file

    def create_summary_report(self):
        """Create a summary report of demo members"""
        summary = {
            "report_info": {
                "title": "JKWI Demo Members Local Summary",
                "generated_at": datetime.now().isoformat(),
                "total_members": len(self.demo_members["members"]),
                "divisions_covered": len(set(m["division"] for m in self.demo_members["members"]))
            },
            "by_division": {},
            "by_country": {},
            "demo_credentials": {
                "pattern": "demo_{municipality_code}",
                "password": "demo123",
                "access_level": "Demo User"
            }
        }
        
        # Group by division
        for member in self.demo_members["members"]:
            division = member["division"]
            if division not in summary["by_division"]:
                summary["by_division"][division] = 0
            summary["by_division"][division] += 1
        
        # Group by country
        for member in self.demo_members["members"]:
            country = member["municipality"]["country"]
            if country not in summary["by_country"]:
                summary["by_country"][country] = []
            summary["by_country"][country].append({
                "municipality": member["municipality"]["name"],
                "member_id": member["member_id"],
                "username": member["username"]
            })
        
        # Save summary report
        summary_file = self.data_path / "demo_summary_report.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return summary