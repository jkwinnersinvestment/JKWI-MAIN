#!/usr/bin/env python3
"""
Company Details Manager
======================

This script allows you to read, edit, and update company details across multiple file formats.
It can read from and write to JSON, YAML, INI, CSV, XML, and plain text formats.

Usage:
    python company_manager.py --read [format]     # Read company details
    python company_manager.py --edit [format]     # Edit company details
    python company_manager.py --update-all        # Update all formats
    python company_manager.py --validate          # Validate all files

Supported formats: json, yaml, ini, csv, xml, txt
"""

import json
import csv
import configparser
import xml.etree.ElementTree as ET
import os
import argparse
from pathlib import Path

class CompanyDetailsManager:
    def __init__(self, base_path=None):
        if base_path is None:
            self.base_path = Path(r"C:\Users\jacob\Documents\0 company info\company details")
        else:
            self.base_path = Path(base_path)
        
        # Ensure directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.company_data = {
            "name": "JK WINNERS INVESTMENT(PTY)Ltd",
            "registration_number": "2013/047375/07",
            "type": "Private Company",
            "street": "22 Sloane Street",
            "suburb": "Bryanston",
            "province": "GAUTENG",
            "postal_code": "1619",
            "country": "South Africa",
            "email": "info@jkwinnersinvestment.co.za",
            "phone": "010 085 3553",
            "whatsapp": "0839887569",
            "website": "",
            "account_name": "JK Winners Investment (Pty)Ltd",
            "bank": "FNB",
            "branch_code": "250655",
            "account_number": "63151527133",
            "account_type": "Business",
            "swift_code": "",
            "vat_number": "",
            "tax_reference": "",
            "default_tax_rate": 15.0,
            "industry": "Investment",
            "established_year": "2013",
            "description": "Investment Company"
        }
    
    def read_json(self):
        """Read company details from JSON file"""
        file_path = self.base_path / "company_details.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data["company"]
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return None
    
    def write_json(self, data=None):
        """Write company details to JSON file"""
        if data is None:
            data = self.company_data
        
        file_path = self.base_path / "company_details.json"
        structured_data = {
            "company": {
                "name": data["name"],
                "registration_number": data["registration_number"],
                "type": data["type"],
                "address": {
                    "street": data["street"],
                    "suburb": data["suburb"],
                    "province": data["province"],
                    "postal_code": data["postal_code"],
                    "country": data["country"],
                    "full_address": f"{data['street']}, {data['suburb']}, {data['province']} {data['postal_code']}"
                },
                "contact": {
                    "email": data["email"],
                    "phone": data["phone"],
                    "whatsapp": data["whatsapp"],
                    "website": data["website"]
                },
                "banking": {
                    "account_name": data["account_name"],
                    "bank": data["bank"],
                    "branch_code": data["branch_code"],
                    "account_number": data["account_number"],
                    "account_type": data["account_type"],
                    "swift_code": data["swift_code"]
                },
                "tax": {
                    "vat_number": data["vat_number"],
                    "tax_reference": data["tax_reference"],
                    "default_tax_rate": data["default_tax_rate"]
                },
                "business": {
                    "industry": data["industry"],
                    "established_year": data["established_year"],
                    "description": data["description"]
                }
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    def read_ini(self):
        """Read company details from INI file"""
        file_path = self.base_path / "company_details.ini"
        try:
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            
            data = {}
            for section in config.sections():
                for key, value in config[section].items():
                    data[key] = value
            return data
        except Exception as e:
            print(f"Error reading INI: {e}")
            return None
    
    def write_ini(self, data=None):
        """Write company details to INI file"""
        if data is None:
            data = self.company_data
        
        file_path = self.base_path / "company_details.ini"
        config = configparser.ConfigParser()
        
        config['company'] = {
            'name': data['name'],
            'registration_number': data['registration_number'],
            'type': data['type']
        }
        
        config['address'] = {
            'street': data['street'],
            'suburb': data['suburb'],
            'province': data['province'],
            'postal_code': data['postal_code'],
            'country': data['country'],
            'full_address': f"{data['street']}, {data['suburb']}, {data['province']} {data['postal_code']}"
        }
        
        config['contact'] = {
            'email': data['email'],
            'phone': data['phone'],
            'whatsapp': data['whatsapp'],
            'website': data['website']
        }
        
        config['banking'] = {
            'account_name': data['account_name'],
            'bank': data['bank'],
            'branch_code': data['branch_code'],
            'account_number': data['account_number'],
            'account_type': data['account_type'],
            'swift_code': data['swift_code']
        }
        
        config['tax'] = {
            'vat_number': data['vat_number'],
            'tax_reference': data['tax_reference'],
            'default_tax_rate': str(data['default_tax_rate'])
        }
        
        config['business'] = {
            'industry': data['industry'],
            'established_year': data['established_year'],
            'description': data['description']
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            config.write(f)
    
    def write_csv(self, data=None):
        """Write company details to CSV file"""
        if data is None:
            data = self.company_data
        
        file_path = self.base_path / "company_details.csv"
        
        fieldnames = [
            'company_name', 'registration_number', 'company_type', 'street_address',
            'suburb', 'province', 'postal_code', 'country', 'email', 'phone',
            'whatsapp', 'website', 'account_name', 'bank', 'branch_code',
            'account_number', 'account_type', 'vat_number', 'tax_reference',
            'default_tax_rate', 'industry', 'established_year', 'description'
        ]
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'company_name': data['name'],
                'registration_number': data['registration_number'],
                'company_type': data['type'],
                'street_address': data['street'],
                'suburb': data['suburb'],
                'province': data['province'],
                'postal_code': data['postal_code'],
                'country': data['country'],
                'email': data['email'],
                'phone': data['phone'],
                'whatsapp': data['whatsapp'],
                'website': data['website'],
                'account_name': data['account_name'],
                'bank': data['bank'],
                'branch_code': data['branch_code'],
                'account_number': data['account_number'],
                'account_type': data['account_type'],
                'vat_number': data['vat_number'],
                'tax_reference': data['tax_reference'],
                'default_tax_rate': data['default_tax_rate'],
                'industry': data['industry'],
                'established_year': data['established_year'],
                'description': data['description']
            })
    
    def write_text(self, data=None):
        """Write company details to plain text file"""
        if data is None:
            data = self.company_data
        
        file_path = self.base_path / "COMPANY DETAILS"
        
        content = f"""Company Name
    {data['name']}

Registration Number
    {data['registration_number']}

Company Type
    {data['type']}

Address
    {data['street']}
    {data['suburb']}
    {data['province']}
    {data['postal_code']}
    {data['country']}

Contact Details
    Email: {data['email']}
    Phone: {data['phone']}
    WhatsApp: {data['whatsapp']}

Banking Details
    Account Name: {data['account_name']}
    Bank: {data['bank']}
    Branch Code: {data['branch_code']}
    Account Number: {data['account_number']}
    Account Type: {data['account_type']}

Tax Information
    VAT Number: {data['vat_number'] or '[To be filled]'}
    Tax Reference: {data['tax_reference'] or '[To be filled]'}
    Default Tax Rate: {data['default_tax_rate']}%

Business Information
    Industry: {data['industry']}
    Established: {data['established_year']}
    Description: {data['description']}"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def update_all_formats(self, data=None):
        """Update all file formats with current data"""
        if data is None:
            data = self.company_data
        
        print("Updating all file formats...")
        
        self.write_json(data)
        print("✓ JSON file updated")
        
        self.write_ini(data)
        print("✓ INI file updated")
        
        self.write_csv(data)
        print("✓ CSV file updated")
        
        self.write_text(data)
        print("✓ Text file updated")
        
        print("All formats updated successfully!")
    
    def interactive_edit(self):
        """Interactive editing of company details"""
        print("=== Company Details Editor ===")
        print("Current company details:")
        self.display_data(self.company_data)
        
        print("\\nWhat would you like to edit?")
        print("1. Company Information")
        print("2. Address")
        print("3. Contact Details")
        print("4. Banking Information")
        print("5. Tax Information")
        print("6. Business Information")
        print("7. Save and Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            self.edit_company_info()
        elif choice == "2":
            self.edit_address()
        elif choice == "3":
            self.edit_contact()
        elif choice == "4":
            self.edit_banking()
        elif choice == "5":
            self.edit_tax()
        elif choice == "6":
            self.edit_business()
        elif choice == "7":
            self.update_all_formats()
            return
        
        # Ask if user wants to continue editing
        if input("Continue editing? (y/n): ").lower() == 'y':
            self.interactive_edit()
        else:
            self.update_all_formats()
    
    def edit_company_info(self):
        """Edit basic company information"""
        print("\\n--- Company Information ---")
        self.company_data['name'] = input(f"Company Name [{self.company_data['name']}]: ") or self.company_data['name']
        self.company_data['registration_number'] = input(f"Registration Number [{self.company_data['registration_number']}]: ") or self.company_data['registration_number']
        self.company_data['type'] = input(f"Company Type [{self.company_data['type']}]: ") or self.company_data['type']
    
    def edit_address(self):
        """Edit address information"""
        print("\\n--- Address Information ---")
        self.company_data['street'] = input(f"Street Address [{self.company_data['street']}]: ") or self.company_data['street']
        self.company_data['suburb'] = input(f"Suburb [{self.company_data['suburb']}]: ") or self.company_data['suburb']
        self.company_data['province'] = input(f"Province [{self.company_data['province']}]: ") or self.company_data['province']
        self.company_data['postal_code'] = input(f"Postal Code [{self.company_data['postal_code']}]: ") or self.company_data['postal_code']
        self.company_data['country'] = input(f"Country [{self.company_data['country']}]: ") or self.company_data['country']
    
    def edit_contact(self):
        """Edit contact information"""
        print("\\n--- Contact Information ---")
        self.company_data['email'] = input(f"Email [{self.company_data['email']}]: ") or self.company_data['email']
        self.company_data['phone'] = input(f"Phone [{self.company_data['phone']}]: ") or self.company_data['phone']
        self.company_data['whatsapp'] = input(f"WhatsApp [{self.company_data['whatsapp']}]: ") or self.company_data['whatsapp']
        self.company_data['website'] = input(f"Website [{self.company_data['website']}]: ") or self.company_data['website']
    
    def edit_banking(self):
        """Edit banking information"""
        print("\\n--- Banking Information ---")
        self.company_data['account_name'] = input(f"Account Name [{self.company_data['account_name']}]: ") or self.company_data['account_name']
        self.company_data['bank'] = input(f"Bank [{self.company_data['bank']}]: ") or self.company_data['bank']
        self.company_data['branch_code'] = input(f"Branch Code [{self.company_data['branch_code']}]: ") or self.company_data['branch_code']
        self.company_data['account_number'] = input(f"Account Number [{self.company_data['account_number']}]: ") or self.company_data['account_number']
        self.company_data['account_type'] = input(f"Account Type [{self.company_data['account_type']}]: ") or self.company_data['account_type']
        self.company_data['swift_code'] = input(f"SWIFT Code [{self.company_data['swift_code']}]: ") or self.company_data['swift_code']
    
    def edit_tax(self):
        """Edit tax information"""
        print("\\n--- Tax Information ---")
        self.company_data['vat_number'] = input(f"VAT Number [{self.company_data['vat_number']}]: ") or self.company_data['vat_number']
        self.company_data['tax_reference'] = input(f"Tax Reference [{self.company_data['tax_reference']}]: ") or self.company_data['tax_reference']
        tax_rate = input(f"Default Tax Rate [{self.company_data['default_tax_rate']}]: ")
        if tax_rate:
            try:
                self.company_data['default_tax_rate'] = float(tax_rate)
            except ValueError:
                print("Invalid tax rate, keeping current value")
    
    def edit_business(self):
        """Edit business information"""
        print("\\n--- Business Information ---")
        self.company_data['industry'] = input(f"Industry [{self.company_data['industry']}]: ") or self.company_data['industry']
        self.company_data['established_year'] = input(f"Established Year [{self.company_data['established_year']}]: ") or self.company_data['established_year']
        self.company_data['description'] = input(f"Description [{self.company_data['description']}]: ") or self.company_data['description']
    
    def display_data(self, data):
        """Display company data in a readable format"""
        print(f"Company: {data['name']}")
        print(f"Registration: {data['registration_number']}")
        print(f"Address: {data['street']}, {data['suburb']}, {data['province']} {data['postal_code']}")
        print(f"Contact: {data['email']} | {data['phone']} | WhatsApp: {data['whatsapp']}")
        print(f"Bank: {data['bank']} - {data['account_number']}")

def main():
    parser = argparse.ArgumentParser(description="Manage company details across multiple formats")
    parser.add_argument('--read', choices=['json', 'ini', 'csv', 'txt'], help='Read from specific format')
    parser.add_argument('--edit', action='store_true', help='Interactive editing mode')
    parser.add_argument('--update-all', action='store_true', help='Update all file formats')
    parser.add_argument('--validate', action='store_true', help='Validate all files exist')
    
    args = parser.parse_args()
    
    manager = CompanyDetailsManager()
    
    if args.read:
        if args.read == 'json':
            data = manager.read_json()
            if data:
                print(json.dumps(data, indent=2))
        elif args.read == 'ini':
            data = manager.read_ini()
            if data:
                manager.display_data(data)
    elif args.edit:
        manager.interactive_edit()
    elif args.update_all:
        manager.update_all_formats()
    elif args.validate:
        base_path = manager.base_path
        files = [
            'company_details.json',
            'company_details.ini',
            'company_details.csv',
            'company_details.yaml',
            'company_details.xml',
            'company_details.env',
            'COMPANY DETAILS'
        ]
        
        print("Validating files...")
        for file in files:
            file_path = base_path / file
            if file_path.exists():
                print(f"✓ {file}")
            else:
                print(f"✗ {file} - Missing")
    else:
        # Default: show current data and offer options
        print("Company Details Manager")
        print("=" * 30)
        manager.display_data(manager.company_data)
        print("\\nUse --help to see available options")
        print("Quick commands:")
        print("  --edit           : Interactive editing")
        print("  --update-all     : Update all file formats")
        print("  --validate       : Check if all files exist")

if __name__ == "__main__":
    main()
