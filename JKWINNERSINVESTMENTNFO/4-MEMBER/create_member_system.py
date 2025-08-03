import os
import json
import datetime
from pathlib import Path

def create_member_template():
    """Create the standard member template"""
    template = {
        "member_info": {
            "member_id": "",
            "template_id": "",
            "full_name": "",
            "first_name": "",
            "last_name": "",
            "date_of_birth": "",
            "gender": "",
            "nationality": "",
            "id_number": "",
            "passport_number": ""
        },
        "contact_info": {
            "email": "",
            "phone_primary": "",
            "phone_secondary": "",
            "address": {
                "street": "",
                "city": "",
                "province_state": "",
                "postal_code": "",
                "country": ""
            }
        },
        "jkwi_info": {
            "username": "",
            "registration_date": "",
            "status": "Pending",
            "division": "",
            "position": "",
            "supervisor": "",
            "employee_id": ""
        },
        "financial_info": {
            "bank_name": "",
            "account_number": "",
            "account_type": "",
            "swift_code": "",
            "tax_number": ""
        },
        "emergency_contact": {
            "name": "",
            "relationship": "",
            "phone": "",
            "email": "",
            "address": ""
        },
        "documents": {
            "id_document": "",
            "passport": "",
            "birth_certificate": "",
            "bank_statement": "",
            "proof_of_address": "",
            "cv_resume": ""
        },
        "system_info": {
            "created_date": "",
            "last_updated": "",
            "created_by": "",
            "updated_by": "",
            "version": "1.0",
            "backup_count": 0
        },
        "notes": "",
        "status_history": []
    }
    return template

def create_country_municipality_structure():
    """Create the folder structure for countries and municipalities"""
    
    # Sample countries with their codes (you can expand this list)
    countries = [
        ("001", "South-Africa"),
        ("002", "Botswana"),
        ("003", "Zimbabwe"),
        ("004", "Namibia"),
        ("005", "Lesotho"),
        ("006", "Swaziland"),
        ("007", "Mozambique"),
        ("008", "Zambia"),
        ("009", "Malawi"),
        ("010", "Tanzania")
    ]
    
    # Sample municipalities for South Africa (001)
    sa_municipalities = [
        ("00100001", "Amahlathi"),
        ("00100002", "Buffalo-City"),
        ("00100003", "Great-Kei"),
        ("00100004", "King-Sabata-Dalindyebo"),
        ("00100005", "Kouga"),
        ("00100006", "Makana"),
        ("00100007", "Mandela-Bay"),
        ("00100008", "Ndlambe"),
        ("00100009", "Raymond-Mhlaba"),
        ("00100010", "Sunday-River-Valley")
    ]
    
    # Sample municipalities for other countries
    other_municipalities = [
        ("00200001", "Gaborone"),
        ("00200002", "Francistown"),
        ("00300001", "Harare"),
        ("00300002", "Bulawayo"),
        ("00400001", "Windhoek"),
        ("00400002", "Swakopmund"),
        ("00500001", "Maseru"),
        ("00500002", "Teyateyaneng"),
        ("00600001", "Mbabane"),
        ("00600002", "Manzini"),
        ("00700001", "Maputo"),
        ("00700002", "Beira"),
        ("00800001", "Lusaka"),
        ("00800002", "Ndola"),
        ("00900001", "Lilongwe"),
        ("00900002", "Blantyre"),
        ("01000001", "Dar-es-Salaam"),
        ("01000002", "Arusha")
    ]
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    
    # Create countries folders
    for country_code, country_name in countries:
        country_folder = base_path / f"{country_code}-{country_name}"
        country_folder.mkdir(parents=True, exist_ok=True)
        
        # Create municipalities based on country
        if country_code == "001":  # South Africa
            municipalities = sa_municipalities
        else:
            # Filter municipalities for current country
            municipalities = [m for m in other_municipalities if m[0].startswith(country_code)]
        
        # Create municipality folders and templates
        for muni_code, muni_name in municipalities:
            muni_folder = country_folder / f"{muni_code}-{muni_name}"
            muni_folder.mkdir(parents=True, exist_ok=True)
            
            # Create template file
            template_file = muni_folder / f"{muni_code}.json"
            template_data = create_member_template()
            template_data["member_info"]["template_id"] = muni_code
            template_data["system_info"]["created_date"] = datetime.datetime.now().isoformat()
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=4, ensure_ascii=False)
            
            print(f"Created template: {template_file}")

def create_member_script(municipality_code, member_number=1):
    """Create a new member script from template"""
    
    # Find the municipality folder
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    
    # Search for the municipality folder
    municipality_folder = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    municipality_folder = muni_folder
                    break
            if municipality_folder:
                break
    
    if not municipality_folder:
        print(f"Municipality folder for code {municipality_code} not found!")
        return None
    
    # Load template
    template_file = municipality_folder / f"{municipality_code}.json"
    if not template_file.exists():
        print(f"Template file {template_file} not found!")
        return None
    
    with open(template_file, 'r', encoding='utf-8') as f:
        template_data = json.load(f)
    
    # Generate member ID
    member_id = f"{municipality_code}{member_number:06d}"
    
    # Create member file
    member_file = municipality_folder / f"{member_id}.json"
    
    # Update template with member-specific info
    template_data["member_info"]["member_id"] = member_id
    template_data["system_info"]["created_date"] = datetime.datetime.now().isoformat()
    template_data["system_info"]["last_updated"] = datetime.datetime.now().isoformat()
    
    with open(member_file, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=4, ensure_ascii=False)
    
    print(f"Created member file: {member_file}")
    return member_file

def get_next_member_number(municipality_code):
    """Get the next available member number for a municipality"""
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    
    # Find municipality folder
    municipality_folder = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    municipality_folder = muni_folder
                    break
            if municipality_folder:
                break
    
    if not municipality_folder:
        return 1
    
    # Find existing member files
    max_number = 0
    for file in municipality_folder.glob(f"{municipality_code}*.json"):
        if file.name != f"{municipality_code}.json":  # Skip template
            try:
                member_number = int(file.stem[-6:])
                max_number = max(max_number, member_number)
            except ValueError:
                continue
    
    return max_number + 1

def update_member_info(member_id, updates):
    """Update member information"""
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    municipality_code = member_id[:8]
    
    # Find member file
    member_file = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    potential_file = muni_folder / f"{member_id}.json"
                    if potential_file.exists():
                        member_file = potential_file
                        break
            if member_file:
                break
    
    if not member_file:
        print(f"Member file for ID {member_id} not found!")
        return False
    
    # Load existing data
    with open(member_file, 'r', encoding='utf-8') as f:
        member_data = json.load(f)
    
    # Create backup
    backup_count = member_data["system_info"]["backup_count"] + 1
    backup_file = member_file.parent / f"{member_id}_backup_{backup_count}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(member_data, f, indent=4, ensure_ascii=False)
    
    # Update data
    def update_nested_dict(d, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in d:
                update_nested_dict(d[key], value)
            else:
                d[key] = value
    
    update_nested_dict(member_data, updates)
    
    # Update system info
    member_data["system_info"]["last_updated"] = datetime.datetime.now().isoformat()
    member_data["system_info"]["backup_count"] = backup_count
    
    # Save updated data
    with open(member_file, 'w', encoding='utf-8') as f:
        json.dump(member_data, f, indent=4, ensure_ascii=False)
    
    print(f"Updated member {member_id}")
    return True

def read_member_info(member_id):
    """Read member information"""
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    municipality_code = member_id[:8]
    
    # Find member file
    member_file = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    potential_file = muni_folder / f"{member_id}.json"
                    if potential_file.exists():
                        member_file = potential_file
                        break
            if member_file:
                break
    
    if not member_file:
        print(f"Member file for ID {member_id} not found!")
        return None
    
    with open(member_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_members_by_municipality(municipality_code):
    """List all members in a municipality"""
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    
    # Find municipality folder
    municipality_folder = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    municipality_folder = muni_folder
                    break
            if municipality_folder:
                break
    
    if not municipality_folder:
        print(f"Municipality folder for code {municipality_code} not found!")
        return []
    
    members = []
    for file in municipality_folder.glob(f"{municipality_code}*.json"):
        if file.name != f"{municipality_code}.json":  # Skip template
            with open(file, 'r', encoding='utf-8') as f:
                member_data = json.load(f)
                members.append({
                    'id': member_data['member_info']['member_id'],
                    'name': member_data['member_info']['full_name'],
                    'status': member_data['jkwi_info']['status'],
                    'division': member_data['jkwi_info']['division']
                })
    
    return members

def export_municipality_data(municipality_code):
    """Export all data for a municipality"""
    
    base_path = Path("c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER")
    
    # Find municipality folder
    municipality_folder = None
    for country_folder in base_path.iterdir():
        if country_folder.is_dir():
            for muni_folder in country_folder.iterdir():
                if muni_folder.is_dir() and muni_folder.name.startswith(municipality_code):
                    municipality_folder = muni_folder
                    break
            if municipality_folder:
                break
    
    if not municipality_folder:
        print(f"Municipality folder for code {municipality_code} not found!")
        return None
    
    export_data = {
        "municipality_code": municipality_code,
        "municipality_name": municipality_folder.name.split('-', 1)[1],
        "export_date": datetime.datetime.now().isoformat(),
        "members": []
    }
    
    for file in municipality_folder.glob(f"{municipality_code}*.json"):
        if file.name != f"{municipality_code}.json":  # Skip template
            with open(file, 'r', encoding='utf-8') as f:
                member_data = json.load(f)
                export_data["members"].append(member_data)
    
    # Save export file
    export_file = municipality_folder / f"export_{municipality_code}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=4, ensure_ascii=False)
    
    print(f"Exported data to: {export_file}")
    return export_file

# Example usage and testing
if __name__ == "__main__":
    print("Creating JKWI Member Management System...")
    
    # Create the folder structure and templates
    create_country_municipality_structure()
    
    print("\nSystem created successfully!")
    print("\nExample usage:")
    
    # Create a sample member
    sample_member_file = create_member_script("00100001", 1)  # Amahlathi, member 1
    
    # Update sample member with some information
    if sample_member_file:
        updates = {
            "member_info": {
                "full_name": "John Doe",
                "first_name": "John",
                "last_name": "Doe"
            },
            "contact_info": {
                "email": "john.doe@jkwi.com",
                "phone_primary": "+27123456789"
            },
            "jkwi_info": {
                "username": "johndoe",
                "status": "Active",
                "division": "Finance Division"
            }
        }
        update_member_info("001000010000001", updates)
    
    # List members in Amahlathi
    members = list_members_by_municipality("00100001")
    print(f"\nMembers in Amahlathi: {len(members)}")
    for member in members:
        print(f"  - {member['id']}: {member['name']} ({member['status']})")