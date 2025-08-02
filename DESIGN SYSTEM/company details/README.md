# Company Details Management System

This directory contains your company details in multiple formats for maximum compatibility with different systems and applications.

## 📁 Available Formats

### 1. **JSON Format** (`company_details.json`)
- **Best for:** APIs, web applications, JavaScript
- **Structure:** Hierarchical with nested objects
- **Readable by:** Most programming languages, REST APIs

### 2. **Environment Variables** (`company_details.env`)
- **Best for:** Environment configuration, Docker, deployment
- **Structure:** KEY=VALUE pairs
- **Readable by:** Shell scripts, Docker, CI/CD systems

### 3. **Plain Text** (`COMPANY DETAILS`)
- **Best for:** Human reading, documentation
- **Structure:** Descriptive text with clear sections
- **Readable by:** Humans, text parsers, your invoice system

### 4. **CSV Format** (`company_details.csv`)
- **Best for:** Spreadsheets, databases, bulk import
- **Structure:** Comma-separated values with headers
- **Readable by:** Excel, Google Sheets, databases

### 5. **YAML Format** (`company_details.yaml`)
- **Best for:** Configuration files, automation tools
- **Structure:** Human-readable structured data
- **Readable by:** Ansible, Kubernetes, configuration systems

### 6. **INI Format** (`company_details.ini`)
- **Best for:** Windows applications, configuration files
- **Structure:** Sections with key=value pairs
- **Readable by:** Windows apps, configuration parsers

### 7. **XML Format** (`company_details.xml`)
- **Best for:** Enterprise systems, SOAP APIs, legacy systems
- **Structure:** Tagged markup language
- **Readable by:** Enterprise software, XML parsers

## 🛠️ Management Tools

### **Python Script** (`company_manager.py`)
Advanced command-line tool for managing company details:

```bash
# View current details
python company_manager.py

# Interactive editing
python company_manager.py --edit

# Update all file formats
python company_manager.py --update-all

# Validate all files exist
python company_manager.py --validate

# Read specific format
python company_manager.py --read json
```

### **Windows Batch File** (`manage_company.bat`)
Simple menu-driven interface for Windows users:
- Double-click to run
- Choose from menu options
- No command-line knowledge required

## 📋 Current Company Information

**Company:** JK WINNERS INVESTMENT(PTY)Ltd  
**Registration:** 2013/047375/07  
**Type:** Private Company  

**Address:**  
22 Sloane Street  
Bryanston, GAUTENG 1619  
South Africa  

**Contact:**  
📧 Email: info@jkwinnersinvestment.co.za  
📞 Phone: 010 085 3553  
📱 WhatsApp: 0839887569  

**Banking:**  
🏦 Bank: FNB  
🏢 Branch Code: 250655  
💳 Account: 63151527133  
👤 Account Name: JK Winners Investment (Pty)Ltd  

**Business:**  
🏭 Industry: Investment  
📅 Established: 2013  
📝 Description: Investment Company  

## 🔄 How to Update Details

### Method 1: Interactive Editing
```bash
python company_manager.py --edit
```
Follow the prompts to update any section.

### Method 2: Direct File Editing
1. Edit any of the format files directly
2. Run update script to sync all formats:
   ```bash
   python company_manager.py --update-all
   ```

### Method 3: Windows Interface
1. Double-click `manage_company.bat`
2. Choose "Edit company details"
3. Follow the prompts

## 🔗 Integration Examples

### For Invoice System
```python
# Read from JSON format
import json
with open('company_details.json', 'r') as f:
    company = json.load(f)['company']
    
company_name = company['name']
company_address = company['address']['full_address']
```

### For Environment Variables
```bash
# Load environment variables
source company_details.env
echo $COMPANY_NAME
echo $EMAIL
```

### For Spreadsheet Import
1. Open Excel/Google Sheets
2. Import `company_details.csv`
3. All data will be in columns

### For Configuration Files
```python
# Read from INI format
import configparser
config = configparser.ConfigParser()
config.read('company_details.ini')

company_name = config['company']['name']
email = config['contact']['email']
```

## 🔒 Data Validation

Run validation to ensure all files are present and consistent:
```bash
python company_manager.py --validate
```

## 📝 Notes

- **VAT Number** and **Tax Reference** fields are currently empty - update when available
- **Website** field is empty - add when you have a website
- **SWIFT Code** field is empty - add if needed for international transfers
- All formats are automatically synchronized when using the management tools
- Files are saved with UTF-8 encoding for international character support

## 🚀 Quick Start

1. **View details:** Double-click `manage_company.bat`
2. **Edit details:** Choose option 2 from the menu
3. **Update invoice system:** Your automated invoice system will automatically read from these files
4. **Backup:** Keep copies of these files in a safe location

## 🔧 Troubleshooting

**Problem:** Python script doesn't run  
**Solution:** Ensure Python 3.6+ is installed and in PATH

**Problem:** Batch file doesn't work  
**Solution:** Right-click and "Run as administrator"

**Problem:** Files missing after editing  
**Solution:** Run `python company_manager.py --update-all` to regenerate

**Problem:** Encoding issues  
**Solution:** All files use UTF-8 encoding - ensure your editor supports it

---

*Last updated: July 30, 2025*  
*Company: JK WINNERS INVESTMENT(PTY)Ltd*
