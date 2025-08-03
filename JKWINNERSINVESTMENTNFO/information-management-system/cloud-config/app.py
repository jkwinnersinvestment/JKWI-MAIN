# Cloud-Ready Flask Application for JKWI Information Management System
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Initialize Firebase (alternative cloud database option)
try:
    if os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH'):
        cred = credentials.Certificate(os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH'))
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully")
    else:
        db = None
        print("⚠️ Firebase not configured, using local storage fallback")
except Exception as e:
    print(f"⚠️ Firebase initialization failed: {e}")
    db = None

class CloudDataManager:
    """Enhanced data manager with cloud database support"""
    
    def __init__(self):
        self.use_cloud = db is not None
        self.local_data = self._get_default_data()
        
    def _get_default_data(self):
        """Default data structure for local fallback"""
        return {
            'company': {
                'name': 'JK Winners Investment',
                'tradingName': 'JKWI',
                'description': 'JK Winners Investment (JKWI) is a comprehensive investment company structured to provide excellence across multiple sectors.',
                'lastUpdated': datetime.now().isoformat()
            },
            'directors': [],
            'divisions': [
                {'id': 1, 'name': 'Mining Division', 'description': 'Mineral extraction and resource development', 'head': ''},
                {'id': 2, 'name': 'Infrastructure Division', 'description': 'Construction and development projects', 'head': ''},
                {'id': 3, 'name': 'Farming Division', 'description': 'Agricultural and agribusiness ventures', 'head': ''},
                {'id': 4, 'name': 'Service Division', 'description': 'Professional and consulting services', 'head': ''},
                {'id': 5, 'name': 'Finance Division', 'description': 'Financial services and investment management', 'head': ''},
                {'id': 6, 'name': 'Legal Division', 'description': 'Legal advisory and compliance services', 'head': ''},
                {'id': 7, 'name': 'Media Division', 'description': 'Communications and media services', 'head': ''},
                {'id': 8, 'name': 'Social Division', 'description': 'Community engagement and social impact', 'head': ''}
            ],
            'members': [],
            'activities': [],
            'partnerships': [
                {'id': 1, 'name': 'Chair Office', 'description': 'Office of the Chair of the Board - Strategic leadership and governance oversight'},
                {'id': 2, 'name': 'Customer Interest', 'description': 'Dedicated to serving our clients\' needs and ensuring satisfaction'},
                {'id': 3, 'name': 'Investors', 'description': 'Partnership opportunities for financial growth and development'},
                {'id': 4, 'name': 'Partners', 'description': 'Strategic alliances for mutual growth and success'}
            ]
        }
    
    async def get_collection(self, collection_name):
        """Get data from cloud or local storage"""
        if self.use_cloud:
            try:
                docs = db.collection(collection_name).stream()
                return [{'id': doc.id, **doc.to_dict()} for doc in docs]
            except Exception as e:
                print(f"Cloud fetch error for {collection_name}: {e}")
                return self.local_data.get(collection_name, [])
        else:
            return self.local_data.get(collection_name, [])
    
    async def save_to_collection(self, collection_name, doc_id, data):
        """Save data to cloud or local storage"""
        if self.use_cloud:
            try:
                doc_ref = db.collection(collection_name).document(doc_id)
                doc_ref.set(data)
                return True
            except Exception as e:
                print(f"Cloud save error for {collection_name}: {e}")
                return False
        else:
            if collection_name not in self.local_data:
                self.local_data[collection_name] = []
            
            # Update existing or add new
            existing_index = next((i for i, item in enumerate(self.local_data[collection_name]) 
                                 if item.get('id') == doc_id), None)
            
            data['id'] = doc_id
            if existing_index is not None:
                self.local_data[collection_name][existing_index] = data
            else:
                self.local_data[collection_name].append(data)
            return True
    
    async def delete_from_collection(self, collection_name, doc_id):
        """Delete data from cloud or local storage"""
        if self.use_cloud:
            try:
                db.collection(collection_name).document(doc_id).delete()
                return True
            except Exception as e:
                print(f"Cloud delete error for {collection_name}: {e}")
                return False
        else:
            if collection_name in self.local_data:
                self.local_data[collection_name] = [
                    item for item in self.local_data[collection_name] 
                    if item.get('id') != doc_id
                ]
            return True

# Initialize cloud data manager
cloud_data = CloudDataManager()

# User Management
users_db = {}  # In production, this should be in the cloud database

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    division = data.get('division', '')
    
    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Create user
    user_data = {
        'username': username,
        'password_hash': password_hash,
        'email': email,
        'division': division,
        'created_at': datetime.now().isoformat(),
        'is_active': True
    }
    
    users_db[username] = user_data
    
    # Create access token
    access_token = create_access_token(identity=username)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'username': username,
            'email': email,
            'division': division
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username not in users_db:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user = users_db[username]
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.get('is_active', True):
        return jsonify({'error': 'Account is deactivated'}), 401
    
    access_token = create_access_token(identity=username)
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'username': username,
            'email': user['email'],
            'division': user['division']
        }
    }), 200

# Company Management
@app.route('/api/company', methods=['GET'])
@jwt_required()
async def get_company():
    """Get company information"""
    company_data = await cloud_data.get_collection('company')
    if company_data:
        return jsonify(company_data[0] if isinstance(company_data, list) else company_data)
    return jsonify(cloud_data.local_data['company'])

@app.route('/api/company', methods=['PUT'])
@jwt_required()
async def update_company():
    """Update company information"""
    data = request.get_json()
    data['lastUpdated'] = datetime.now().isoformat()
    
    success = await cloud_data.save_to_collection('company', 'main', data)
    if success:
        return jsonify({'message': 'Company updated successfully', 'data': data})
    return jsonify({'error': 'Failed to update company'}), 500

# Directors Management
@app.route('/api/directors', methods=['GET'])
@jwt_required()
async def get_directors():
    """Get all directors"""
    directors = await cloud_data.get_collection('directors')
    return jsonify(directors)

@app.route('/api/directors', methods=['POST'])
@jwt_required()
async def add_director():
    """Add new director"""
    data = request.get_json()
    director_id = str(int(datetime.now().timestamp() * 1000))
    
    director_data = {
        **data,
        'id': director_id,
        'createdAt': datetime.now().isoformat()
    }
    
    success = await cloud_data.save_to_collection('directors', director_id, director_data)
    if success:
        return jsonify({'message': 'Director added successfully', 'data': director_data}), 201
    return jsonify({'error': 'Failed to add director'}), 500

@app.route('/api/directors/<director_id>', methods=['PUT'])
@jwt_required()
async def update_director(director_id):
    """Update director"""
    data = request.get_json()
    data['updatedAt'] = datetime.now().isoformat()
    
    success = await cloud_data.save_to_collection('directors', director_id, data)
    if success:
        return jsonify({'message': 'Director updated successfully', 'data': data})
    return jsonify({'error': 'Failed to update director'}), 500

@app.route('/api/directors/<director_id>', methods=['DELETE'])
@jwt_required()
async def delete_director(director_id):
    """Delete director"""
    success = await cloud_data.delete_from_collection('directors', director_id)
    if success:
        return jsonify({'message': 'Director deleted successfully'})
    return jsonify({'error': 'Failed to delete director'}), 500

# Divisions Management
@app.route('/api/divisions', methods=['GET'])
@jwt_required()
async def get_divisions():
    """Get all divisions"""
    divisions = await cloud_data.get_collection('divisions')
    return jsonify(divisions)

@app.route('/api/divisions', methods=['POST'])
@jwt_required()
async def add_division():
    """Add new division"""
    data = request.get_json()
    division_id = str(int(datetime.now().timestamp() * 1000))
    
    division_data = {
        **data,
        'id': division_id,
        'createdAt': datetime.now().isoformat()
    }
    
    success = await cloud_data.save_to_collection('divisions', division_id, division_data)
    if success:
        return jsonify({'message': 'Division added successfully', 'data': division_data}), 201
    return jsonify({'error': 'Failed to add division'}), 500

# Members Management
@app.route('/api/members', methods=['GET'])
@jwt_required()
async def get_members():
    """Get all members"""
    members = await cloud_data.get_collection('members')
    return jsonify(members)

@app.route('/api/members', methods=['POST'])
@jwt_required()
async def add_member():
    """Add new member"""
    data = request.get_json()
    member_id = str(int(datetime.now().timestamp() * 1000))
    
    member_data = {
        **data,
        'id': member_id,
        'registrationDate': datetime.now().isoformat()
    }
    
    success = await cloud_data.save_to_collection('members', member_id, member_data)
    if success:
        return jsonify({'message': 'Member added successfully', 'data': member_data}), 201
    return jsonify({'error': 'Failed to add member'}), 500

@app.route('/api/members/<member_id>', methods=['PUT'])
@jwt_required()
async def update_member(member_id):
    """Update member"""
    data = request.get_json()
    data['updatedAt'] = datetime.now().isoformat()
    
    success = await cloud_data.save_to_collection('members', member_id, data)
    if success:
        return jsonify({'message': 'Member updated successfully', 'data': data})
    return jsonify({'error': 'Failed to update member'}), 500

@app.route('/api/members/<member_id>', methods=['DELETE'])
@jwt_required()
async def delete_member(member_id):
    """Delete member"""
    success = await cloud_data.delete_from_collection('members', member_id)
    if success:
        return jsonify({'message': 'Member deleted successfully'})
    return jsonify({'error': 'Failed to delete member'}), 500

# Statistics and Dashboard
@app.route('/api/stats', methods=['GET'])
@jwt_required()
async def get_stats():
    """Get system statistics"""
    directors = await cloud_data.get_collection('directors')
    divisions = await cloud_data.get_collection('divisions')
    members = await cloud_data.get_collection('members')
    
    stats = {
        'totalDirectors': len(directors),
        'totalDivisions': len(divisions),
        'totalMembers': len(members),
        'systemStatus': 'Active'
    }
    
    return jsonify(stats)

# Data Export/Import
@app.route('/api/export', methods=['GET'])
@jwt_required()
async def export_data():
    """Export all data"""
    export_data = {}
    collections = ['company', 'directors', 'divisions', 'members', 'partnerships']
    
    for collection in collections:
        export_data[collection] = await cloud_data.get_collection(collection)
    
    export_data['exported_at'] = datetime.now().isoformat()
    export_data['exported_by'] = get_jwt_identity()
    
    return jsonify(export_data)

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cloud_db': 'connected' if cloud_data.use_cloud else 'local_fallback'
    })

# Serve the web application
@app.route('/')
def index():
    """Serve the main web application"""
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
