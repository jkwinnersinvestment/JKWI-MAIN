# JKWI Demo Data for GitHub

This directory contains realistic demo data for the JKWI (JK Winners Investment) cloud system, featuring South African members, directors, and company information.

## 📋 Demo Data Contents

### Members (10 demo members)
- **Sipho Mthembu** - Mining Division Executive
- **Lindiwe Dlamini** - Finance Division Premium Member  
- **Mandla Zulu** - Infrastructure Division Engineer
- **Naledi Mokoena** - Legal Division Attorney
- **Tshepo Maluleke** - Farming Division Specialist
- **Precious Nkomo** - Media Division Manager
- **Kagiso Ndlovu** - Service Division Operations
- **Lerato Molefe** - Social Division Community Developer
- **Mpho Mashaba** - Mining Division Engineer
- **Dumisani Mabaso** - Finance Division Executive

### Directors (4 senior directors)
- **Justice Motsepe** - Mining Division Director
- **Faith Ramaphosa** - Finance Division Director
- **Hope Sisulu** - Infrastructure Division Director
- **Grace Malema** - Legal Division Director

### Company Information
- **Name**: JK Winners Investment
- **Registration**: 2019/123456/07
- **Founded**: 2019
- **Headquarters**: Sandton, Johannesburg

### Divisions (8 active divisions)
1. **Finance Division** - R5M budget
2. **Mining Division** - R15M budget  
3. **Infrastructure Division** - R12M budget
4. **Farming Division** - R8M budget
5. **Legal Division** - R3M budget
6. **Media Division** - R2.5M budget
7. **Service Division** - R4M budget
8. **Social Division** - R3.5M budget

### Partnerships (2 strategic partnerships)
- **Anglo American** - Mining operations alliance
- **Standard Bank** - Financial services partnership

## 🚀 How to Use This Demo Data

### Option 1: Automatic Loading (Recommended)

1. **Start your JKWI cloud system:**
   ```bash
   cd cloud-config
   python app.py
   ```

2. **Load demo data automatically:**
   ```bash
   # In a new terminal
   python load_demo_data.py
   ```

3. **Access the system:**
   - Open browser to `http://localhost:5000`
   - Login with any of the demo users or admin:
     - **Admin**: `jkwi_admin` / `Admin123!`
     - **Member**: `sipho.mthembu123` / `password123`

### Option 2: Manual Import

1. **Start the system and login as admin**
2. **Use the import feature in the web interface**
3. **Upload the `jkwi_demo_data.json` file**

### Option 3: API Integration

```python
import requests
import json

# Load demo data
with open('jkwi_demo_data.json', 'r') as f:
    demo_data = json.load(f)

# Post to your API endpoints
base_url = "http://localhost:5000"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

# Load members
for member in demo_data['members']:
    response = requests.post(f"{base_url}/api/members", 
                           json=member, headers=headers)
    print(f"Loaded: {member['fullName']}")
```

## 🎯 Demo Scenarios

### Test User Journeys

1. **Executive Access**: Login as Dumisani Mabaso (Finance Executive)
2. **Division Management**: View Mining Division with Justice Motsepe
3. **Member Services**: Check Service Division operations
4. **Legal Compliance**: Review legal division with Grace Malema

### Data Relationships

- Each member belongs to a specific division
- Directors lead their respective divisions
- Members have realistic South African contact details
- Company partnerships reflect real industry connections

## 📊 Data Statistics

- **Total Members**: 10 (across 8 divisions)
- **Total Directors**: 4 (senior leadership)
- **Total Divisions**: 8 (operational units)
- **Total Budget**: R53M (combined division budgets)
- **Geographic Coverage**: Johannesburg, Cape Town, Durban, Pretoria, Bloemfontein

## 🌍 South African Context

This demo data reflects authentic South African business environment:

- **Names**: Traditional and modern South African names
- **Locations**: Major South African cities and provinces
- **Industries**: Mining, finance, infrastructure (key SA sectors)
- **Contact Details**: Realistic SA phone numbers and addresses
- **Business Structure**: Reflects SA corporate governance

## 🔒 Security Notes

- All demo data is fictional and for testing only
- Phone numbers and emails are not real
- Financial figures are for demonstration purposes
- Use only in development/testing environments

## 📝 Customization

To modify the demo data:

1. **Edit `jkwi_demo_data.json`** directly
2. **Run `create_demo_data.py`** to generate new data
3. **Use `load_demo_data.py`** to import changes

### Adding New Members

```json
{
  "id": "mem011",
  "username": "new.member123",
  "fullName": "New Member Name",
  "email": "new.member@jkwi.co.za",
  "division": "Mining Division",
  "status": "Active",
  "membershipNumber": "JKWI-2024-0011"
}
```

## 🤝 Contributing

To contribute additional demo data:

1. Follow South African naming conventions
2. Use realistic business information
3. Maintain data relationships (division assignments)
4. Test with the load script before committing

## 📞 Support

For questions about the demo data:

- Check the main JKWI documentation
- Review the API endpoints
- Test with the provided scripts
- Ensure your cloud system is running

---

**🎉 Happy Testing with JKWI Demo Data!**

This demo data provides a solid foundation for testing all aspects of your JKWI cloud system with realistic South African business information.
