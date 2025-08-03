/*
Enhanced web client for cloud-ready JKWI Information Management System
This replaces the existing JavaScript-only frontend with a more robust, cloud-integrated solution
*/

class CloudJKWIApp {
    constructor() {
        this.apiBaseUrl = this.getApiBaseUrl();
        this.authToken = localStorage.getItem('jkwi_auth_token');
        this.currentUser = JSON.parse(localStorage.getItem('jkwi_current_user') || '{}');
        this.isOnline = navigator.onLine;
        this.offlineQueue = JSON.parse(localStorage.getItem('jkwi_offline_queue') || '[]');
        
        this.init();
        this.setupNetworkListeners();
        this.setupAutoSync();
    }

    getApiBaseUrl() {
        // Auto-detect API base URL based on environment
        const isLocal = window.location.hostname === 'localhost';
        const baseUrl = isLocal 
            ? 'http://localhost:5000' 
            : window.location.origin;
        return `${baseUrl}/api`;
    }

    init() {
        if (!this.authToken) {
            this.showLoginForm();
        } else {
            this.validateToken().then(valid => {
                if (valid) {
                    this.setupMainApp();
                } else {
                    this.logout();
                }
            });
        }
        
        this.setupEventListeners();
        this.showNetworkStatus();
    }

    setupNetworkListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showNetworkStatus();
            this.processOfflineQueue();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showNetworkStatus();
        });
    }

    setupAutoSync() {
        // Sync data every 30 seconds when online
        setInterval(() => {
            if (this.isOnline && this.authToken) {
                this.syncData();
            }
        }, 30000);
    }

    async validateToken() {
        try {
            const response = await this.apiCall('/health', 'GET');
            return response.status === 'healthy';
        } catch (error) {
            return false;
        }
    }

    async apiCall(endpoint, method = 'GET', data = null, skipAuth = false) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (!skipAuth && this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        const config = {
            method,
            headers,
        };

        if (data && method !== 'GET') {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}${endpoint}`, config);
            
            if (response.status === 401) {
                this.logout();
                throw new Error('Authentication required');
            }

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'API request failed');
            }

            return result;
        } catch (error) {
            if (!this.isOnline) {
                // Queue the request for when we're back online
                this.queueOfflineRequest(endpoint, method, data);
                throw new Error('Currently offline. Request queued for later.');
            }
            throw error;
        }
    }

    queueOfflineRequest(endpoint, method, data) {
        this.offlineQueue.push({
            endpoint,
            method,
            data,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('jkwi_offline_queue', JSON.stringify(this.offlineQueue));
    }

    async processOfflineQueue() {
        if (this.offlineQueue.length === 0) return;

        const queueCopy = [...this.offlineQueue];
        this.offlineQueue = [];
        localStorage.setItem('jkwi_offline_queue', JSON.stringify(this.offlineQueue));

        for (const request of queueCopy) {
            try {
                await this.apiCall(request.endpoint, request.method, request.data);
                this.showNotification('Offline changes synchronized', 'success');
            } catch (error) {
                // Re-queue failed requests
                this.offlineQueue.push(request);
                console.error('Failed to sync offline request:', error);
            }
        }

        if (this.offlineQueue.length > 0) {
            localStorage.setItem('jkwi_offline_queue', JSON.stringify(this.offlineQueue));
        }
    }

    // Authentication Methods
    showLoginForm() {
        document.body.innerHTML = `
            <div class="login-container">
                <div class="login-form">
                    <img src="../DESIGN%20SYSTEM/JKWI%20LOGO/JKWI%20LOGO%20PNG/JK%20WINNERS%20INVESTMENT.png" alt="JKWI Logo" class="logo">
                    <h2>JKWI Information Management System</h2>
                    <p class="subtitle">Cloud-Based Member Portal</p>
                    
                    <form id="loginForm">
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input type="text" id="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" required>
                        </div>
                        <button type="submit" class="btn-primary">Login</button>
                    </form>
                    
                    <div class="register-link">
                        <p>New member? <a href="#" onclick="cloudApp.showRegisterForm()">Register here</a></p>
                    </div>
                    
                    <div class="network-status" id="networkStatus"></div>
                </div>
            </div>
        `;
        
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });
        
        this.showNetworkStatus();
    }

    showRegisterForm() {
        document.body.innerHTML = `
            <div class="login-container">
                <div class="login-form">
                    <img src="../DESIGN%20SYSTEM/JKWI%20LOGO/JKWI%20LOGO%20PNG/JK%20WINNERS%20INVESTMENT.png" alt="JKWI Logo" class="logo">
                    <h2>Register for JKWI Portal</h2>
                    
                    <form id="registerForm">
                        <div class="form-group">
                            <label for="regUsername">Username:</label>
                            <input type="text" id="regUsername" required>
                        </div>
                        <div class="form-group">
                            <label for="regEmail">Email:</label>
                            <input type="email" id="regEmail" required>
                        </div>
                        <div class="form-group">
                            <label for="regDivision">Division:</label>
                            <select id="regDivision" required>
                                <option value="">Select Division</option>
                                <option value="Mining Division">Mining Division</option>
                                <option value="Infrastructure Division">Infrastructure Division</option>
                                <option value="Farming Division">Farming Division</option>
                                <option value="Service Division">Service Division</option>
                                <option value="Finance Division">Finance Division</option>
                                <option value="Legal Division">Legal Division</option>
                                <option value="Media Division">Media Division</option>
                                <option value="Social Division">Social Division</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="regPassword">Password:</label>
                            <input type="password" id="regPassword" required>
                        </div>
                        <div class="form-group">
                            <label for="regConfirmPassword">Confirm Password:</label>
                            <input type="password" id="regConfirmPassword" required>
                        </div>
                        <button type="submit" class="btn-primary">Register</button>
                    </form>
                    
                    <div class="register-link">
                        <p>Already have an account? <a href="#" onclick="cloudApp.showLoginForm()">Login here</a></p>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });
    }

    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await this.apiCall('/login', 'POST', { username, password }, true);
            
            this.authToken = response.access_token;
            this.currentUser = response.user;
            
            localStorage.setItem('jkwi_auth_token', this.authToken);
            localStorage.setItem('jkwi_current_user', JSON.stringify(this.currentUser));
            
            this.setupMainApp();
            this.showNotification('Login successful!', 'success');
        } catch (error) {
            this.showNotification(error.message, 'error');
        }
    }

    async register() {
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const division = document.getElementById('regDivision').value;
        const password = document.getElementById('regPassword').value;
        const confirmPassword = document.getElementById('regConfirmPassword').value;

        if (password !== confirmPassword) {
            this.showNotification('Passwords do not match', 'error');
            return;
        }

        try {
            const response = await this.apiCall('/register', 'POST', {
                username, email, division, password
            }, true);
            
            this.authToken = response.access_token;
            this.currentUser = response.user;
            
            localStorage.setItem('jkwi_auth_token', this.authToken);
            localStorage.setItem('jkwi_current_user', JSON.stringify(this.currentUser));
            
            this.setupMainApp();
            this.showNotification('Registration successful!', 'success');
        } catch (error) {
            this.showNotification(error.message, 'error');
        }
    }

    logout() {
        this.authToken = null;
        this.currentUser = {};
        localStorage.removeItem('jkwi_auth_token');
        localStorage.removeItem('jkwi_current_user');
        this.showLoginForm();
    }

    // Main Application Setup
    setupMainApp() {
        document.body.innerHTML = `
            <div class="app-container">
                <header class="app-header">
                    <div class="header-left">
                        <img src="../DESIGN%20SYSTEM/JKWI%20LOGO/JKWI%20LOGO%20PNG/JK%20WINNERS%20INVESTMENT.png" alt="JKWI Logo" class="header-logo">
                        <h1>JKWI Management Portal</h1>
                    </div>
                    <div class="header-right">
                        <div class="user-info">
                            <span>Welcome, ${this.currentUser.username}</span>
                            <span class="user-division">${this.currentUser.division}</span>
                        </div>
                        <div class="network-status" id="networkStatus"></div>
                        <button onclick="cloudApp.logout()" class="btn-secondary">Logout</button>
                    </div>
                </header>

                <nav class="app-nav">
                    <button class="nav-link active" data-section="dashboard">Dashboard</button>
                    <button class="nav-link" data-section="company">Company</button>
                    <button class="nav-link" data-section="directors">Directors</button>
                    <button class="nav-link" data-section="divisions">Divisions</button>
                    <button class="nav-link" data-section="members">Members</button>
                    <button class="nav-link" data-section="partnerships">Partnerships</button>
                    <button class="nav-link" data-section="backup">Data Management</button>
                </nav>

                <main class="app-main">
                    <div id="dashboard" class="content-section active">
                        <h2>Dashboard</h2>
                        <div class="stats-grid" id="statsGrid">
                            <!-- Stats will be loaded here -->
                        </div>
                        <div class="sync-status">
                            <p>Last sync: <span id="lastSyncTime">Loading...</span></p>
                        </div>
                    </div>

                    <div id="company" class="content-section">
                        <h2>Company Information</h2>
                        <form id="companyForm">
                            <!-- Company form will be loaded here -->
                        </form>
                    </div>

                    <div id="directors" class="content-section">
                        <h2>Directors Management</h2>
                        <div class="action-buttons">
                            <button class="btn-primary" onclick="cloudApp.openDirectorModal()">Add Director</button>
                        </div>
                        <div class="table-container">
                            <table id="directorsTable">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Position</th>
                                        <th>Division</th>
                                        <th>Email</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- Directors will be loaded here -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div id="divisions" class="content-section">
                        <h2>Divisions Management</h2>
                        <div id="divisionsGrid">
                            <!-- Divisions will be loaded here -->
                        </div>
                    </div>

                    <div id="members" class="content-section">
                        <h2>Members Management</h2>
                        <div class="action-buttons">
                            <button class="btn-primary" onclick="cloudApp.openMemberModal()">Add Member</button>
                            <button class="btn-secondary" onclick="cloudApp.exportMembers()">Export</button>
                        </div>
                        <div class="search-container">
                            <input type="text" id="memberSearch" placeholder="Search members..." 
                                   onkeyup="cloudApp.searchMembers(this.value)">
                        </div>
                        <div class="table-container">
                            <table id="membersTable">
                                <thead>
                                    <tr>
                                        <th>Username</th>
                                        <th>Full Name</th>
                                        <th>Email</th>
                                        <th>Division</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- Members will be loaded here -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div id="partnerships" class="content-section">
                        <h2>Partnerships & Opportunities</h2>
                        <div id="partnershipsGrid">
                            <!-- Partnerships will be loaded here -->
                        </div>
                    </div>

                    <div id="backup" class="content-section">
                        <h2>Data Management</h2>
                        <div class="backup-actions">
                            <button class="btn-primary" onclick="cloudApp.exportAllData()">Export All Data</button>
                            <button class="btn-secondary" onclick="cloudApp.showBackupHistory()">Backup History</button>
                        </div>
                        <div id="backupHistory">
                            <!-- Backup history will be loaded here -->
                        </div>
                    </div>
                </main>

                <div id="notification" class="notification"></div>
                <div id="modalContainer"></div>
            </div>
        `;

        this.setupEventListeners();
        this.loadDashboard();
        this.showNetworkStatus();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const section = e.target.dataset.section;
                this.showSection(section);
            });
        });
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        document.getElementById(sectionName).classList.add('active');

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Load section data
        this.loadSectionData(sectionName);
    }

    async loadSectionData(section) {
        try {
            switch (section) {
                case 'dashboard':
                    await this.loadDashboard();
                    break;
                case 'company':
                    await this.loadCompany();
                    break;
                case 'directors':
                    await this.loadDirectors();
                    break;
                case 'divisions':
                    await this.loadDivisions();
                    break;
                case 'members':
                    await this.loadMembers();
                    break;
                case 'partnerships':
                    await this.loadPartnerships();
                    break;
            }
        } catch (error) {
            this.showNotification(`Failed to load ${section}: ${error.message}`, 'error');
        }
    }

    async loadDashboard() {
        try {
            const stats = await this.apiCall('/stats');
            document.getElementById('statsGrid').innerHTML = `
                <div class="stat-card">
                    <h3>Total Members</h3>
                    <span class="stat-number">${stats.totalMembers}</span>
                </div>
                <div class="stat-card">
                    <h3>Active Divisions</h3>
                    <span class="stat-number">${stats.totalDivisions}</span>
                </div>
                <div class="stat-card">
                    <h3>Directors</h3>
                    <span class="stat-number">${stats.totalDirectors}</span>
                </div>
                <div class="stat-card">
                    <h3>System Status</h3>
                    <span class="stat-number status-active">${stats.systemStatus}</span>
                </div>
            `;
            
            document.getElementById('lastSyncTime').textContent = new Date().toLocaleString();
        } catch (error) {
            console.error('Failed to load dashboard:', error);
        }
    }

    async loadMembers() {
        try {
            const members = await this.apiCall('/members');
            const tbody = document.querySelector('#membersTable tbody');
            tbody.innerHTML = members.map(member => `
                <tr>
                    <td>${member.username}</td>
                    <td>${member.fullName || 'N/A'}</td>
                    <td>${member.email}</td>
                    <td>${member.division}</td>
                    <td><span class="status-${member.status.toLowerCase()}">${member.status}</span></td>
                    <td>
                        <button class="btn-edit" onclick="cloudApp.editMember('${member.id}')">Edit</button>
                        <button class="btn-delete" onclick="cloudApp.deleteMember('${member.id}')">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Failed to load members:', error);
            this.showNotification('Failed to load members', 'error');
        }
    }

    async loadCompany() {
        try {
            const company = await this.apiCall('/company');
            document.getElementById('companyForm').innerHTML = `
                <div class="form-group">
                    <label for="companyName">Company Name:</label>
                    <input type="text" id="companyName" value="${company.name || ''}" required>
                </div>
                <div class="form-group">
                    <label for="tradingName">Trading Name:</label>
                    <input type="text" id="tradingName" value="${company.tradingName || ''}" required>
                </div>
                <div class="form-group">
                    <label for="companyDescription">Description:</label>
                    <textarea id="companyDescription" rows="4" required>${company.description || ''}</textarea>
                </div>
                <button type="submit" class="btn-primary">Update Company</button>
            `;
            
            document.getElementById('companyForm').addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateCompany();
            });
        } catch (error) {
            console.error('Failed to load company:', error);
            this.showNotification('Failed to load company information', 'error');
        }
    }

    async updateCompany() {
        try {
            const companyData = {
                name: document.getElementById('companyName').value,
                tradingName: document.getElementById('tradingName').value,
                description: document.getElementById('companyDescription').value
            };
            
            await this.apiCall('/company', 'PUT', companyData);
            this.showNotification('Company information updated successfully!', 'success');
        } catch (error) {
            this.showNotification('Failed to update company information', 'error');
        }
    }

    async loadDirectors() {
        try {
            const directors = await this.apiCall('/directors');
            const tbody = document.querySelector('#directorsTable tbody');
            tbody.innerHTML = directors.map(director => `
                <tr>
                    <td>${director.name}</td>
                    <td>${director.position}</td>
                    <td>${director.division}</td>
                    <td>${director.email}</td>
                    <td>
                        <button class="btn-edit" onclick="cloudApp.editDirector('${director.id}')">Edit</button>
                        <button class="btn-delete" onclick="cloudApp.deleteDirector('${director.id}')">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Failed to load directors:', error);
            this.showNotification('Failed to load directors', 'error');
        }
    }

    async loadDivisions() {
        try {
            const divisions = await this.apiCall('/divisions');
            const grid = document.getElementById('divisionsGrid');
            grid.innerHTML = divisions.map(division => `
                <div class="division-card">
                    <h3>${division.name}</h3>
                    <p>${division.description}</p>
                    <div class="division-actions">
                        <button class="btn-edit" onclick="cloudApp.editDivision('${division.id}')">Edit</button>
                        <button class="btn-delete" onclick="cloudApp.deleteDivision('${division.id}')">Delete</button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Failed to load divisions:', error);
            this.showNotification('Failed to load divisions', 'error');
        }
    }

    async loadPartnerships() {
        try {
            const partnerships = await this.apiCall('/partnerships') || [];
            const grid = document.getElementById('partnershipsGrid');
            grid.innerHTML = partnerships.map(partnership => `
                <div class="partnership-card">
                    <h3>${partnership.name}</h3>
                    <p>${partnership.description}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Failed to load partnerships:', error);
            this.showNotification('Failed to load partnerships', 'error');
        }
    }

    // Modal and CRUD operations
    openDirectorModal(directorId = null) {
        const modalHtml = `
            <div class="modal" id="directorModal">
                <div class="modal-content">
                    <span class="close" onclick="cloudApp.closeModal('directorModal')">&times;</span>
                    <h2>${directorId ? 'Edit Director' : 'Add Director'}</h2>
                    <form id="directorForm">
                        <input type="hidden" id="directorId" value="${directorId || ''}">
                        <div class="form-group">
                            <label for="directorName">Name:</label>
                            <input type="text" id="directorName" required>
                        </div>
                        <div class="form-group">
                            <label for="directorPosition">Position:</label>
                            <input type="text" id="directorPosition" required>
                        </div>
                        <div class="form-group">
                            <label for="directorDivision">Division:</label>
                            <select id="directorDivision" required>
                                <option value="">Select Division</option>
                                <option value="Mining Division">Mining Division</option>
                                <option value="Infrastructure Division">Infrastructure Division</option>
                                <option value="Farming Division">Farming Division</option>
                                <option value="Service Division">Service Division</option>
                                <option value="Finance Division">Finance Division</option>
                                <option value="Legal Division">Legal Division</option>
                                <option value="Media Division">Media Division</option>
                                <option value="Social Division">Social Division</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="directorEmail">Email:</label>
                            <input type="email" id="directorEmail" required>
                        </div>
                        <div class="form-group">
                            <label for="directorPhone">Phone:</label>
                            <input type="tel" id="directorPhone">
                        </div>
                        <button type="submit" class="btn-primary">Save Director</button>
                    </form>
                </div>
            </div>
        `;
        
        document.getElementById('modalContainer').innerHTML = modalHtml;
        document.getElementById('directorModal').style.display = 'block';
        
        document.getElementById('directorForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveDirector();
        });
        
        // Load existing data if editing
        if (directorId) {
            this.loadDirectorData(directorId);
        }
    }

    openMemberModal(memberId = null) {
        const modalHtml = `
            <div class="modal" id="memberModal">
                <div class="modal-content">
                    <span class="close" onclick="cloudApp.closeModal('memberModal')">&times;</span>
                    <h2>${memberId ? 'Edit Member' : 'Add Member'}</h2>
                    <form id="memberForm">
                        <input type="hidden" id="memberId" value="${memberId || ''}">
                        <div class="form-group">
                            <label for="memberUsername">Username:</label>
                            <input type="text" id="memberUsername" required>
                        </div>
                        <div class="form-group">
                            <label for="memberFullName">Full Name:</label>
                            <input type="text" id="memberFullName" required>
                        </div>
                        <div class="form-group">
                            <label for="memberEmail">Email:</label>
                            <input type="email" id="memberEmail" required>
                        </div>
                        <div class="form-group">
                            <label for="memberDivision">Division:</label>
                            <select id="memberDivision" required>
                                <option value="">Select Division</option>
                                <option value="Mining Division">Mining Division</option>
                                <option value="Infrastructure Division">Infrastructure Division</option>
                                <option value="Farming Division">Farming Division</option>
                                <option value="Service Division">Service Division</option>
                                <option value="Finance Division">Finance Division</option>
                                <option value="Legal Division">Legal Division</option>
                                <option value="Media Division">Media Division</option>
                                <option value="Social Division">Social Division</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="memberStatus">Status:</label>
                            <select id="memberStatus" required>
                                <option value="Active">Active</option>
                                <option value="Pending">Pending</option>
                                <option value="Inactive">Inactive</option>
                            </select>
                        </div>
                        <button type="submit" class="btn-primary">Save Member</button>
                    </form>
                </div>
            </div>
        `;
        
        document.getElementById('modalContainer').innerHTML = modalHtml;
        document.getElementById('memberModal').style.display = 'block';
        
        document.getElementById('memberForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveMember();
        });
        
        // Load existing data if editing
        if (memberId) {
            this.loadMemberData(memberId);
        }
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    async saveDirector() {
        try {
            const directorId = document.getElementById('directorId').value;
            const directorData = {
                name: document.getElementById('directorName').value,
                position: document.getElementById('directorPosition').value,
                division: document.getElementById('directorDivision').value,
                email: document.getElementById('directorEmail').value,
                phone: document.getElementById('directorPhone').value
            };

            if (directorId) {
                await this.apiCall(`/directors/${directorId}`, 'PUT', directorData);
                this.showNotification('Director updated successfully!', 'success');
            } else {
                await this.apiCall('/directors', 'POST', directorData);
                this.showNotification('Director added successfully!', 'success');
            }

            this.closeModal('directorModal');
            await this.loadDirectors();
        } catch (error) {
            this.showNotification('Failed to save director', 'error');
        }
    }

    async saveMember() {
        try {
            const memberId = document.getElementById('memberId').value;
            const memberData = {
                username: document.getElementById('memberUsername').value,
                fullName: document.getElementById('memberFullName').value,
                email: document.getElementById('memberEmail').value,
                division: document.getElementById('memberDivision').value,
                status: document.getElementById('memberStatus').value
            };

            if (memberId) {
                await this.apiCall(`/members/${memberId}`, 'PUT', memberData);
                this.showNotification('Member updated successfully!', 'success');
            } else {
                await this.apiCall('/members', 'POST', memberData);
                this.showNotification('Member added successfully!', 'success');
            }

            this.closeModal('memberModal');
            await this.loadMembers();
        } catch (error) {
            this.showNotification('Failed to save member', 'error');
        }
    }

    async editMember(id) {
        this.openMemberModal(id);
    }

    async editDirector(id) {
        this.openDirectorModal(id);
    }

    async deleteMember(id) {
        if (confirm('Are you sure you want to delete this member?')) {
            try {
                await this.apiCall(`/members/${id}`, 'DELETE');
                this.showNotification('Member deleted successfully!', 'success');
                await this.loadMembers();
            } catch (error) {
                this.showNotification('Failed to delete member', 'error');
            }
        }
    }

    async deleteDirector(id) {
        if (confirm('Are you sure you want to delete this director?')) {
            try {
                await this.apiCall(`/directors/${id}`, 'DELETE');
                this.showNotification('Director deleted successfully!', 'success');
                await this.loadDirectors();
            } catch (error) {
                this.showNotification('Failed to delete director', 'error');
            }
        }
    }

    async searchMembers(query) {
        try {
            const members = await this.apiCall('/members');
            const filteredMembers = members.filter(member =>
                member.username.toLowerCase().includes(query.toLowerCase()) ||
                member.fullName.toLowerCase().includes(query.toLowerCase()) ||
                member.email.toLowerCase().includes(query.toLowerCase())
            );
            
            const tbody = document.querySelector('#membersTable tbody');
            tbody.innerHTML = filteredMembers.map(member => `
                <tr>
                    <td>${member.username}</td>
                    <td>${member.fullName || 'N/A'}</td>
                    <td>${member.email}</td>
                    <td>${member.division}</td>
                    <td><span class="status-${member.status.toLowerCase()}">${member.status}</span></td>
                    <td>
                        <button class="btn-edit" onclick="cloudApp.editMember('${member.id}')">Edit</button>
                        <button class="btn-delete" onclick="cloudApp.deleteMember('${member.id}')">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Search failed:', error);
        }
    }

    async exportMembers() {
        try {
            const members = await this.apiCall('/members');
            const csv = this.convertToCSV(members);
            this.downloadFile(csv, `JKWI_Members_${new Date().toISOString().split('T')[0]}.csv`, 'text/csv');
            this.showNotification('Members exported successfully!', 'success');
        } catch (error) {
            this.showNotification('Failed to export members', 'error');
        }
    }

    async exportAllData() {
        try {
            const data = await this.apiCall('/export');
            const jsonData = JSON.stringify(data, null, 2);
            this.downloadFile(jsonData, `JKWI_Full_Export_${new Date().toISOString().split('T')[0]}.json`, 'application/json');
            this.showNotification('Data exported successfully!', 'success');
        } catch (error) {
            this.showNotification('Failed to export data', 'error');
        }
    }

    convertToCSV(data) {
        if (!data || data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvHeaders = headers.join(',');
        const csvRows = data.map(row => 
            headers.map(header => `"${row[header] || ''}"`).join(',')
        );
        
        return [csvHeaders, ...csvRows].join('\n');
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    }

    showBackupHistory() {
        // Placeholder for backup history functionality
        this.showNotification('Backup history feature coming soon!', 'info');
    }

    async syncData() {
        try {
            await this.loadSectionData('dashboard');
            document.getElementById('lastSyncTime').textContent = new Date().toLocaleString();
        } catch (error) {
            console.error('Sync failed:', error);
        }
    }

    showNetworkStatus() {
        const statusElement = document.getElementById('networkStatus');
        if (statusElement) {
            statusElement.innerHTML = this.isOnline 
                ? '<span class="status-online">🟢 Online</span>' 
                : '<span class="status-offline">🔴 Offline</span>';
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }

    // Additional utility methods would be implemented here
    // This is a simplified version showing the core cloud integration concepts
}

// Initialize the cloud app
const cloudApp = new CloudJKWIApp();
