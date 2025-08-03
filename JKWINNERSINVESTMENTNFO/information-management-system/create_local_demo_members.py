import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from services.demo_member_service import DemoMemberService

# Municipality data from your create_demo_members.py
MUNICIPALITIES_DATA = {
    'SOUTH_AFRICA': {
        'MUNICIPALITIES': {
            'EC101_CACADU': {'code': 'EC101', 'name': 'Cacadu District'},
            'EC102_AMATHOLE': {'code': 'EC102', 'name': 'Amathole District'},
            'EC103_CHRIS_HANI': {'code': 'EC103', 'name': 'Chris Hani District'},
            'EC104_JOE_GQABI': {'code': 'EC104', 'name': 'Joe Gqabi District'},
            'EC105_ALFRED_NZO': {'code': 'EC105', 'name': 'Alfred Nzo District'},
            'GT423_JOHANNESBURG': {'code': 'GT423', 'name': 'Johannesburg Metropolitan'},
            'GT424_TSHWANE': {'code': 'GT424', 'name': 'Tshwane Metropolitan'},
            'KZN222_ETHEKWINI': {'code': 'KZN222', 'name': 'eThekwini Metropolitan'},
            'WC011_CITY_OF_CAPE_TOWN': {'code': 'WC011', 'name': 'City of Cape Town Metropolitan'}
        }
    },
    'BOTSWANA': {
        'MUNICIPALITIES': {
            'BW001_GABORONE': {'code': 'BW001', 'name': 'Gaborone City'},
            'BW002_FRANCISTOWN': {'code': 'BW002', 'name': 'Francistown City'}
        }
    },
    'ZIMBABWE': {
        'MUNICIPALITIES': {
            'ZW001_HARARE': {'code': 'ZW001', 'name': 'Harare Metropolitan'},
            'ZW002_BULAWAYO': {'code': 'ZW002', 'name': 'Bulawayo Metropolitan'}
        }
    }
}

def main():
    print("🏆 JK WINNERS INVESTMENT - Local Demo Member Generator 🏆")
    print("=" * 60)
    
    # Initialize demo member service
    demo_service = DemoMemberService()
    
    # Generate demo members
    print("Creating demo members locally...")
    created_count = demo_service.generate_demo_members_for_municipalities(MUNICIPALITIES_DATA)
    
    print(f"✅ Created {created_count} new demo members")
    print(f"📊 Total demo members: {len(demo_service.get_all_demo_members())}")
    
    # Export for webapp
    print("\n🌐 Exporting for webapp...")
    webapp_file = demo_service.export_for_webapp()
    print(f"✅ Exported to: {webapp_file}")
    
    # Create summary report
    print("\n📋 Creating summary report...")
    summary = demo_service.create_summary_report()
    print(f"✅ Summary report created")
    
    print("\n🎉 Demo members are now available locally!")
    print("\n📝 Next Steps:")
    print("1. Demo members are stored in: data/demo_members/")
    print("2. Webapp integration file: js/demo_members.js")
    print("3. Include demo_members.js in your HTML to auto-load demo data")
    print("4. Demo credentials pattern: demo_{municipality_code} / demo123")
    
    # Show some examples
    print("\n🔑 Example Demo Credentials:")
    for i, member in enumerate(demo_service.get_all_demo_members()[:5]):
        print(f"   • {member['username']} / demo123 ({member['municipality']['name']})")
    
    if len(demo_service.get_all_demo_members()) > 5:
        print(f"   ... and {len(demo_service.get_all_demo_members()) - 5} more")

if __name__ == "__main__":
    main()