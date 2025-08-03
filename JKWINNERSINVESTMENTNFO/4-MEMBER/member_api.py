"""
JKWI Member Management API
Cross-platform compatible member management system
"""

import json
import os
import datetime
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any

class JKWIMemberManager:
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = "c:/Users/jacob/Documents/JKWINNERSINVESTMENTNFO/4-MEMBER"
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create_member(self, municipality_code: str, member_data: Dict[str, Any] = None) -> str:
        """Create a new member and return member ID"""
        
        member_number = self._get_next_member_number(municipality_code)
        member_id = f"{municipality_code}{member_number:06d}"
        
        # Load template
        template_data = self._load_template(municipality_code)
        if not template_data:
            raise ValueError(f"Template for municipality {municipality_code} not found")
        
        # Update with provided data
        if member_data:
            self._update_nested_dict(template_data, member_data)
        
        # Set member ID and timestamps
        template_data["member_info"]["member_id"] = member_id
        template_data["system_info"]["created_date"] = datetime.datetime.now().isoformat()
        template_data["system_info"]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Save member file
        municipality_folder = self._find_municipality_folder(municipality_code)
        member_file = municipality_folder / f"{member_id}.json"
        
        with open(member_file, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=4, ensure_ascii=False)
        
        return member_id
    
    def read_member(self, member_id: str) -> Optional[Dict[str, Any]]:
        """Read member information"""
        
        municipality_code = member_id[:8]
        municipality_folder = self._find_municipality_folder(municipality_code)
        
        if not municipality_folder:
            return None
        
        member_file = municipality_folder / f"{member_id}.json"
        
        if not member_file.exists():
            return None
        
        with open(member_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_member(self, member_id: str, updates: Dict[str, Any], user: str = "system") -> bool:
        """Update member information"""
        
        member_data = self.read_member(member_id)
        if not member_data:
            return False
        
        # Create backup
        self._create_backup(member_id, member_data)
        
        # Apply updates
        self._update_nested_dict(member_data, updates)
        
        # Update system info
        member_data["system_info"]["last_updated"] = datetime.datetime.now().isoformat()
        member_data["system_info"]["updated_by"] = user
        member_data["system_info"]["backup_count"] = member_data["system_info"].get("backup_count", 0) + 1
        
        # Save updated data
        municipality_code = member_id[:8]
        municipality_folder = self._find_municipality_folder(municipality_code)
        member_file = municipality_folder / f"{member_id}.json"
        
        with open(member_file, 'w', encoding='utf-8') as f:
            json.dump(member_data, f, indent=4, ensure_ascii=False)
        
        return True
    
    def delete_member(self, member_id: str, user: str = "system") -> bool:
        """Soft delete member (move to archive)"""
        
        member_data = self.read_member(member_id)
        if not member_data:
            return False
        
        municipality_code = member_id[:8]
        municipality_folder = self._find_municipality_folder(municipality_code)
        member_file = municipality_folder / f"{member_id}.json"
        
        # Create archive folder
        archive_folder = municipality_folder / "archive"
        archive_folder.mkdir(exist_ok=True)
        
        # Update member data with deletion info
        member_data["system_info"]["deleted_date"] = datetime.datetime.now().isoformat()
        member_data["system_info"]["deleted_by"] = user
        member_data["jkwi_info"]["status"] = "Deleted"
        
        # Move to archive
        archive_file = archive_folder / f"{member_id}_deleted.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(member_data, f, indent=4, ensure_ascii=False)
        
        # Remove original file
        member_file.unlink()
        
        return True
    
    def search_members(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search members based on criteria"""
        
        results = []
        
        for country_folder in self.base_path.iterdir():
            if not country_folder.is_dir():
                continue
                
            for municipality_folder in country_folder.iterdir():
                if not municipality_folder.is_dir():
                    continue
                
                municipality_code = municipality_folder.name.split('-')[0]
                
                for member_file in municipality_folder.glob(f"{municipality_code}??????.json"):
                    try:
                        with open(member_file, 'r', encoding='utf-8') as f:
                            member_data = json.load(f)
                        
                        if self._matches_query(member_data, query):
                            results.append(member_data)
                    
                    except (json.JSONDecodeError, IOError):
                        continue
        
        return results
    
    def get_municipality_stats(self, municipality_code: str) -> Dict[str, Any]:
        """Get statistics for a municipality"""
        
        municipality_folder = self._find_municipality_folder(municipality_code)
        if not municipality_folder:
            return {}
        
        stats = {
            "total_members": 0,
            "active_members": 0,
            "pending_members": 0,
            "inactive_members": 0,
            "divisions": {},
            "municipality_code": municipality_code,
            "municipality_name": municipality_folder.name.split('-', 1)[1] if '-' in municipality_folder.name else municipality_code
        }
        
        for member_file in municipality_folder.glob(f"{municipality_code}??????.json"):
            try:
                with open(member_file, 'r', encoding='utf-8') as f:
                    member_data = json.load(f)
                
                stats["total_members"] += 1
                
                status = member_data.get("jkwi_info", {}).get("status", "Unknown")
                if status == "Active":
                    stats["active_members"] += 1
                elif status == "Pending":
                    stats["pending_members"] += 1
                else:
                    stats["inactive_members"] += 1
                
                division = member_data.get("jkwi_info", {}).get("division", "Unassigned")
                stats["divisions"][division] = stats["divisions"].get(division, 0) + 1
            
            except (json.JSONDecodeError, IOError):
                continue
        
        return stats
    
    def export_data(self, municipality_code: str = None, format: str = "json") -> str:
        """Export data to file"""
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if municipality_code:
            # Export specific municipality
            municipality_folder = self._find_municipality_folder(municipality_code)
            if not municipality_folder:
                raise ValueError(f"Municipality {municipality_code} not found")
            
            export_data = {
                "municipality_code": municipality_code,
                "export_date": datetime.datetime.now().isoformat(),
                "members": []
            }
            
            for member_file in municipality_folder.glob(f"{municipality_code}??????.json"):
                with open(member_file, 'r', encoding='utf-8') as f:
                    member_data = json.load(f)
                    export_data["members"].append(member_data)
            
            export_file = municipality_folder / f"export_{municipality_code}_{timestamp}.json"
            
        else:
            # Export all data
            export_data = {
                "export_date": datetime.datetime.now().isoformat(),
                "countries": {}
            }
            
            for country_folder in self.base_path.iterdir():
                if not country_folder.is_dir():
                    continue
                
                country_name = country_folder.name
                export_data["countries"][country_name] = {
                    "municipalities": {}
                }
                
                for municipality_folder in country_folder.iterdir():
                    if not municipality_folder.is_dir():
                        continue
                    
                    municipality_code = municipality_folder.name.split('-')[0]
                    municipality_name = municipality_folder.name
                    
                    export_data["countries"][country_name]["municipalities"][municipality_name] = {
                        "members": []
                    }
                    
                    for member_file in municipality_folder.glob(f"{municipality_code}??????.json"):
                        with open(member_file, 'r', encoding='utf-8') as f:
                            member_data = json.load(f)
                            export_data["countries"][country_name]["municipalities"][municipality_name]["members"].append(member_data)
            
            export_file = self.base_path / f"full_export_{timestamp}.json"
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False)
        
        return str(export_file)
    
    def import_data(self, file_path: str) -> bool:
        """Import data from file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if "municipality_code" in import_data:
                # Single municipality import
                municipality_code = import_data["municipality_code"]
                for member_data in import_data.get("members", []):
                    member_id = member_data.get("member_info", {}).get("member_id")
                    if member_id:
                        municipality_folder = self._find_municipality_folder(municipality_code)
                        member_file = municipality_folder / f"{member_id}.json"
                        
                        with open(member_file, 'w', encoding='utf-8') as f:
                            json.dump(member_data, f, indent=4, ensure_ascii=False)
            
            elif "countries" in import_data:
                # Full data import
                for country_name, country_data in import_data["countries"].items():
                    for municipality_name, municipality_data in country_data["municipalities"].items():
                        for member_data in municipality_data.get("members", []):
                            member_id = member_data.get("member_info", {}).get("member_id")
                            if member_id:
                                municipality_code = member_id[:8]
                                municipality_folder = self._find_municipality_folder(municipality_code)
                                if municipality_folder:
                                    member_file = municipality_folder / f"{member_id}.json"
                                    
                                    with open(member_file, 'w', encoding='utf-8') as f:
                                        json.dump(member_data, f, indent=4, ensure_ascii=False)
            
            return True
        
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Import failed: {e}")
            return False
    
    # Helper methods
    def _find_municipality_folder(self, municipality_code: str) -> Optional[Path]:
        """Find municipality folder by code"""
        
        for country_folder in self.base_path.iterdir():
            if not country_folder.is_dir():
                continue
            
            for municipality_folder in country_folder.iterdir():
                if municipality_folder.is_dir() and municipality_folder.name.startswith(municipality_code):
                    return municipality_folder
        
        return None
    
    def _get_next_member_number(self, municipality_code: str) -> int:
        """Get next available member number"""
        
        municipality_folder = self._find_municipality_folder(municipality_code)
        if not municipality_folder:
            return 1
        
        max_number = 0
        for member_file in municipality_folder.glob(f"{municipality_code}??????.json"):
            try:
                member_number = int(member_file.stem[-6:])
                max_number = max(max_number, member_number)
            except ValueError:
                continue
        
        return max_number + 1
    
    def _load_template(self, municipality_code: str) -> Optional[Dict[str, Any]]:
        """Load template for municipality"""
        
        municipality_folder = self._find_municipality_folder(municipality_code)
        if not municipality_folder:
            return None
        
        template_file = municipality_folder / f"{municipality_code}.json"
        if not template_file.exists():
            return None
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_backup(self, member_id: str, member_data: Dict[str, Any]) -> None:
        """Create backup of member data"""
        
        municipality_code = member_id[:8]
        municipality_folder = self._find_municipality_folder(municipality_code)
        
        backup_folder = municipality_folder / "backups"
        backup_folder.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_folder / f"{member_id}_backup_{timestamp}.json"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(member_data, f, indent=4, ensure_ascii=False)
    
    def _update_nested_dict(self, d: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Update nested dictionary"""
        
        for key, value in updates.items():
            if isinstance(value, dict) and key in d and isinstance(d[key], dict):
                self._update_nested_dict(d[key], value)
            else:
                d[key] = value
    
    def _matches_query(self, member_data: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Check if member data matches query"""
        
        for key, value in query.items():
            if '.' in key:
                # Nested key like "member_info.full_name"
                keys = key.split('.')
                data = member_data
                for k in keys:
                    if not isinstance(data, dict) or k not in data:
                        return False
                    data = data[k]
                
                if isinstance(value, str) and isinstance(data, str):
                    if value.lower() not in data.lower():
                        return False
                elif data != value:
                    return False
            else:
                # Direct key
                if key not in member_data:
                    return False
                
                if isinstance(value, str) and isinstance(member_data[key], str):
                    if value.lower() not in member_data[key].lower():
                        return False
                elif member_data[key] != value:
                    return False
        
        return True

# Example usage
if __name__ == "__main__":
    # Initialize manager
    manager = JKWIMemberManager()
    
    # Create a member
    member_data = {
        "member_info": {
            "full_name": "Jane Smith",
            "first_name": "Jane",
            "last_name": "Smith"
        },
        "contact_info": {
            "email": "jane.smith@jkwi.com"
        },
        "jkwi_info": {
            "username": "janesmith",
            "status": "Active"
        }
    }
    
    member_id = manager.create_member("00100001", member_data)
    print(f"Created member: {member_id}")
    
    # Read member
    member = manager.read_member(member_id)
    print(f"Member name: {member['member_info']['full_name']}")
    
    # Search members
    results = manager.search_members({"jkwi_info.status": "Active"})
    print(f"Found {len(results)} active members")
    
    # Get stats
    stats = manager.get_municipality_stats("00100001")
    print(f"Municipality stats: {stats}")