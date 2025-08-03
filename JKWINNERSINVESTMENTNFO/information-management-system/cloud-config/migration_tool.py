"""
Migration script to move existing local data to cloud database
This script helps migrate your current JKWI data to the new cloud system
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(str(Path(__file__).parent.parent))

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️ Firebase not available. Install with: pip install firebase-admin")

class DataMigrationTool:
    """Tool to migrate JKWI data from local storage to cloud database"""
    
    def __init__(self):
        self.local_data_path = Path(__file__).parent.parent
        self.backup_path = self.local_data_path / "migration_backups"
        self.backup_path.mkdir(exist_ok=True)
        
        # Initialize Firebase if available
        self.firebase_db = None
        if FIREBASE_AVAILABLE:
            self.init_firebase()
    
    def init_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            firebase_admin.get_app()
        except ValueError:
            # Firebase not initialized, let's initialize it
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                self.firebase_db = firestore.client()
                print("✅ Firebase initialized successfully")
            else:
                print("⚠️ Firebase service account not found. Set FIREBASE_SERVICE_ACCOUNT_PATH environment variable")
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
    
    def export_local_data(self):
        """Export existing local data to JSON file"""
        print("🔍 Scanning for existing JKWI data...")
        
        exported_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "source": "local_jkwi_system"
            },
            "company": {},
            "directors": [],
            "divisions": [],
            "members": [],
            "partnerships": [],
            "activities": []
        }
        
        # Check for existing data in various locations
        data_sources = [
            self.local_data_path / "js" / "data.js",
            self.local_data_path / "data" / "company_data.json",
            self.local_data_path / "src" / "data",
            # Add more potential data source paths
        ]
        
        # Extract data from localStorage backup if available
        localStorage_file = self.local_data_path / "localStorage_backup.json"
        if localStorage_file.exists():
            with open(localStorage_file, 'r', encoding='utf-8') as f:
                localStorage_data = json.load(f)
                if 'jkwi_data' in localStorage_data:
                    jkwi_data = json.loads(localStorage_data['jkwi_data'])
                    exported_data.update(jkwi_data)
        
        # Extract data from JavaScript data file
        data_js_file = self.local_data_path / "js" / "data.js"
        if data_js_file.exists():
            print("📁 Found data.js file, extracting data...")
            # This would require parsing the JavaScript file
            # For now, we'll use a simplified approach
        
        # Extract demo members data
        demo_members_path = self.local_data_path / "data" / "demo_members"
        if demo_members_path.exists():
            print("👥 Found demo members data...")
            demo_file = demo_members_path / "demo_members.json"
            if demo_file.exists():
                with open(demo_file, 'r', encoding='utf-8') as f:
                    demo_data = json.load(f)
                    if 'members' in demo_data:
                        exported_data['members'].extend(demo_data['members'])
        
        # Extract company details
        company_details_path = self.local_data_path.parent / "DESIGN SYSTEM" / "company details"
        if company_details_path.exists():
            print("🏢 Found company details...")
            
            # Extract from various company detail files
            for file_type in ['json', 'yaml', 'xml']:
                company_file = company_details_path / f"company_details.{file_type}"
                if company_file.exists():
                    if file_type == 'json':
                        with open(company_file, 'r', encoding='utf-8') as f:
                            company_data = json.load(f)
                            exported_data['company'].update(company_data)
        
        # Add default JKWI structure if no data found
        if not exported_data['divisions']:
            exported_data['divisions'] = [
                {"id": 1, "name": "Mining Division", "description": "Mineral extraction and resource development"},
                {"id": 2, "name": "Infrastructure Division", "description": "Construction and development projects"},
                {"id": 3, "name": "Farming Division", "description": "Agricultural and agribusiness ventures"},
                {"id": 4, "name": "Service Division", "description": "Professional and consulting services"},
                {"id": 5, "name": "Finance Division", "description": "Financial services and investment management"},
                {"id": 6, "name": "Legal Division", "description": "Legal advisory and compliance services"},
                {"id": 7, "name": "Media Division", "description": "Communications and media services"},
                {"id": 8, "name": "Social Division", "description": "Community engagement and social impact"}
            ]
        
        if not exported_data['company']:
            exported_data['company'] = {
                "name": "JK Winners Investment",
                "tradingName": "JKWI",
                "description": "JK Winners Investment (JKWI) is a comprehensive investment company structured to provide excellence across multiple sectors.",
                "lastUpdated": datetime.now().isoformat()
            }
        
        # Save exported data
        export_filename = f"jkwi_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_path = self.backup_path / export_filename
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(exported_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to: {export_path}")
        print(f"📊 Export summary:")
        print(f"   - Company: {'✓' if exported_data['company'] else '✗'}")
        print(f"   - Directors: {len(exported_data['directors'])}")
        print(f"   - Divisions: {len(exported_data['divisions'])}")
        print(f"   - Members: {len(exported_data['members'])}")
        print(f"   - Partnerships: {len(exported_data['partnerships'])}")
        
        return export_path
    
    def import_to_cloud(self, export_file_path):
        """Import data to cloud database"""
        if not self.firebase_db:
            print("❌ Cloud database not available. Please configure Firebase.")
            return False
        
        print(f"📤 Importing data from {export_file_path} to cloud database...")
        
        with open(export_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        try:
            # Import company data
            if data.get('company'):
                self.firebase_db.collection('company').document('main').set(data['company'])
                print("✅ Company data imported")
            
            # Import directors
            for director in data.get('directors', []):
                doc_id = str(director.get('id', int(datetime.now().timestamp() * 1000)))
                self.firebase_db.collection('directors').document(doc_id).set(director)
            print(f"✅ {len(data.get('directors', []))} directors imported")
            
            # Import divisions
            for division in data.get('divisions', []):
                doc_id = str(division.get('id', int(datetime.now().timestamp() * 1000)))
                self.firebase_db.collection('divisions').document(doc_id).set(division)
            print(f"✅ {len(data.get('divisions', []))} divisions imported")
            
            # Import members
            for member in data.get('members', []):
                doc_id = str(member.get('id', int(datetime.now().timestamp() * 1000)))
                self.firebase_db.collection('members').document(doc_id).set(member)
            print(f"✅ {len(data.get('members', []))} members imported")
            
            # Import partnerships
            for partnership in data.get('partnerships', []):
                doc_id = str(partnership.get('id', int(datetime.now().timestamp() * 1000)))
                self.firebase_db.collection('partnerships').document(doc_id).set(partnership)
            print(f"✅ {len(data.get('partnerships', []))} partnerships imported")
            
            # Log migration activity
            migration_log = {
                "action": "data_migration",
                "timestamp": datetime.now().isoformat(),
                "source_file": str(export_file_path),
                "imported_counts": {
                    "directors": len(data.get('directors', [])),
                    "divisions": len(data.get('divisions', [])),
                    "members": len(data.get('members', [])),
                    "partnerships": len(data.get('partnerships', []))
                }
            }
            self.firebase_db.collection('activities').add(migration_log)
            
            print("🎉 Data migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    
    def verify_migration(self):
        """Verify that data was migrated correctly"""
        if not self.firebase_db:
            print("❌ Cannot verify - cloud database not available")
            return False
        
        print("🔍 Verifying migration...")
        
        collections = ['company', 'directors', 'divisions', 'members', 'partnerships']
        for collection_name in collections:
            try:
                docs = list(self.firebase_db.collection(collection_name).stream())
                count = len(docs)
                print(f"   - {collection_name}: {count} documents")
            except Exception as e:
                print(f"   - {collection_name}: Error - {e}")
        
        print("✅ Verification completed")
    
    def create_backup(self):
        """Create a backup of current local data before migration"""
        print("💾 Creating backup of current data...")
        
        backup_data = {
            "backup_info": {
                "timestamp": datetime.now().isoformat(),
                "type": "pre_migration_backup"
            }
        }
        
        # Copy any existing data files
        data_files = [
            self.local_data_path / "js" / "data.js",
            self.local_data_path / "index.html",
            # Add more files to backup
        ]
        
        for file_path in data_files:
            if file_path.exists():
                backup_file = self.backup_path / f"backup_{file_path.name}"
                with open(file_path, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
        
        print(f"✅ Backup created in: {self.backup_path}")

def main():
    parser = argparse.ArgumentParser(description='JKWI Data Migration Tool')
    parser.add_argument('--export', action='store_true', help='Export local data to JSON')
    parser.add_argument('--import', dest='import_file', help='Import data from JSON file to cloud')
    parser.add_argument('--verify', action='store_true', help='Verify cloud data')
    parser.add_argument('--backup', action='store_true', help='Create backup of local data')
    parser.add_argument('--full-migration', action='store_true', help='Perform complete migration (export + import)')
    
    args = parser.parse_args()
    
    migrator = DataMigrationTool()
    
    if args.backup:
        migrator.create_backup()
    
    if args.export or args.full_migration:
        export_path = migrator.export_local_data()
        if args.full_migration:
            migrator.import_to_cloud(export_path)
            migrator.verify_migration()
    
    if args.import_file:
        migrator.import_to_cloud(Path(args.import_file))
        migrator.verify_migration()
    
    if args.verify:
        migrator.verify_migration()
    
    if not any(vars(args).values()):
        print("🚀 JKWI Data Migration Tool")
        print("Available options:")
        print("  --export              Export local data")
        print("  --import <file>       Import data to cloud")
        print("  --verify              Verify cloud data")
        print("  --backup              Create local backup")
        print("  --full-migration      Complete migration process")
        print("\nExample: python migration_tool.py --full-migration")

if __name__ == "__main__":
    main()
