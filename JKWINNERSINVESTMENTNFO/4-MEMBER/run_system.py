"""
JKWI Member Management System Runner
Execute this file to set up the complete system
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from create_member_system import create_country_municipality_structure, create_member_script
from member_api import JKWIMemberManager

def main():
    """Main system setup and demonstration"""
    
    print("=" * 60)
    print("JKWI MEMBER MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Step 1: Create folder structure
    print("\n1. Creating folder structure...")
    create_country_municipality_structure()
    print("✓ Folder structure created successfully!")
    
    # Step 2: Initialize API manager
    print("\n2. Initializing API manager...")
    manager = JKWIMemberManager()
    print("✓ API manager initialized!")
    
    # Step 3: Create sample members
    print("\n3. Creating sample members...")
    
    sample_members = [
        {
            "municipality": "00100001",  # Amahlathi
            "data": {
                "member_info": {
                    "full_name": "John Winner Doe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1990-05-15",
                    "gender": "Male",
                    "nationality": "South African"
                },
                "contact_info": {
                    "email": "john.doe@jkwi.com",
                    "phone_primary": "+27123456789",
                    "address": {
                        "city": "King Williams Town",
                        "province_state": "Eastern Cape",
                        "country": "South Africa"
                    }
                },
                "jkwi_info": {
                    "username": "johndoe",
                    "status": "Active",
                    "division": "Finance Division",
                    "position": "Financial Analyst"
                }
            }
        },
        {
            "municipality": "00100001",  # Amahlathi
            "data": {
                "member_info": {
                    "full_name": "Jane Winner Smith",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "date_of_birth": "1988-08-22",
                    "gender": "Female",
                    "nationality": "South African"
                },
                "contact_info": {
                    "email": "jane.smith@jkwi.com",
                    "phone_primary": "+27987654321",
                    "address": {
                        "city": "Stutterheim",
                        "province_state": "Eastern Cape",
                        "country": "South Africa"
                    }
                },
                "jkwi_info": {
                    "username": "janesmith",
                    "status": "Active",
                    "division": "Mining Division",
                    "position": "Mining Engineer"
                }
            }
        },
        {
            "municipality": "00100002",  # Buffalo City
            "data": {
                "member_info": {
                    "full_name": "Michael Winner Johnson",
                    "first_name": "Michael",
                    "last_name": "Johnson",
                    "date_of_birth": "1985-12-10",
                    "gender": "Male",
                    "nationality": "South African"
                },
                "contact_info": {
                    "email": "michael.johnson@jkwi.com",
                    "phone_primary": "+27111222333",
                    "address": {
                        "city": "East London",
                        "province_state": "Eastern Cape",
                        "country": "South Africa"
                    }
                },
                "jkwi_info": {
                    "username": "michaeljohnson",
                    "status": "Pending",
                    "division": "Infrastructure Division",
                    "position": "Project Manager"
                }
            }
        }
    ]
    
    created_members = []
    for member in sample_members:
        member_id = manager.create_member(member["municipality"], member["data"])
        created_members.append(member_id)
        print(f"   ✓ Created member: {member_id}")
    
    # Step 4: Demonstrate system capabilities
    print("\n4. System demonstration...")
    
    # Show member information
    print("\n   Member Information:")
    for member_id in created_members:
        member = manager.read_member(member_id)
        print(f"   - {member_id}: {member['member_info']['full_name']} ({member['jkwi_info']['status']})")
    
    # Show municipality stats
    print("\n   Municipality Statistics:")
    for municipality_code in ["00100001", "00100002"]:
        stats = manager.get_municipality_stats(municipality_code)
        if stats:
            print(f"   - {stats['municipality_name']}: {stats['total_members']} members")
            print(f"     Active: {stats['active_members']}, Pending: {stats['pending_members']}")
    
    # Search functionality
    print("\n   Search Results:")
    active_members = manager.search_members({"jkwi_info.status": "Active"})
    print(f"   - Active members: {len(active_members)}")
    
    mining_members = manager.search_members({"jkwi_info.division": "Mining Division"})
    print(f"   - Mining division members: {len(mining_members)}")
    
    # Export data
    print("\n5. Creating data exports...")
    export_file = manager.export_data("00100001")
    print(f"   ✓ Exported Amahlathi data to: {export_file}")
    
    full_export = manager.export_data()
    print(f"   ✓ Full system export to: {full_export}")
    
    print("\n" + "=" * 60)
    print("SYSTEM SETUP COMPLETE!")
    print("=" * 60)
    print("\nNow you can:")
    print("- Use member_api.py to manage members programmatically")
    print("- Access member files directly in the folder structure")
    print("- Import/export data as needed")
    print("- Integrate with the web interface")
    
    print(f"\nBase folder: {manager.base_path}")
    print("Structure:")
    print("├── [Country Code]-[Country Name]/")
    print("│   ├── [Municipality Code]-[Municipality Name]/")
    print("│   │   ├── [Municipality Code].json (template)")
    print("│   │   ├── [Municipality Code][Member Number].json (members)")
    print("│   │   ├── backups/ (member backups)")
    print("│   │   └── archive/ (deleted members)")
    
    return manager, created_members

if __name__ == "__main__":
    manager, members = main()
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print("You can now use the 'manager' object to interact with the system.")
    print("Example commands:")
    print("- manager.read_member('001000010000001')")
    print("- manager.search_members({'jkwi_info.status': 'Active'})")
    print("- manager.get_municipality_stats('00100001')")
    print("- manager.create_member('00100001', member_data)")