// Main application logic
class JKWIApp {
    constructor() {
        this.currentSection = 'dashboard';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboard();
        this.populateDivisionSelects();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.dataset.section;
                this.showSection(section);
            });
        });

        // Forms
        document.getElementById('companyForm').addEventListener('submit', (e) => this.handleCompanyForm(e));
        document.getElementById('directorForm').addEventListener('submit', (e) => this.handleDirectorForm(e));
        document.getElementById('divisionForm').addEventListener('submit', (e) => this.handleDivisionForm(e));
        document.getElementById('memberForm').addEventListener('submit', (e) => this.handleMemberForm(e));

        // Modals
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => this.closeModal(e.target.closest('.modal')));
        });

        // Search
        document.getElementById('memberSearch').addEventListener('input', (e) => this.searchMembers(e.target.value));

        // Import file
        document.getElementById('importFile').addEventListener('change', (e) => this.handleImportFile(e));

        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target);
            }
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

        this.currentSection = sectionName;

        // Load section-specific data
        switch (sectionName) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'company':
                this.loadCompanyForm();
                break;
            case 'directors':
                this.loadDirectors();
                break;
            case 'divisions':
                this.loadDivisions();
                break;
            case 'partnerships':
                this.loadPartnerships();
                break;
            case 'members':
                this.loadMembers();
                break;
            case 'backup':
                this.loadBackups();
                break;
        }
    }

    loadDashboard() {
        const stats = dataManager.getStats();
        document.getElementById('totalMembers').textContent = stats.totalMembers;
        document.getElementById('totalDivisions').textContent = stats.totalDivisions;
        document.getElementById('totalDirectors').textContent = stats.totalDirectors;

        // Load recent activities
        const activities = dataManager.getActivities().slice(0, 10);
        const activityList = document.getElementById('activityList');
        activityList.innerHTML = activities.map(activity => `
            <li>
                ${activity.description} - 
                <span class="timestamp">${new Date(activity.timestamp).toLocaleString()}</span>
            </li>
        `).join('');
    }

    loadCompanyForm() {
        const company = dataManager.getCompany();
        document.getElementById('companyName').value = company.name;
        document.getElementById('tradingName').value = company.tradingName;
        document.getElementById('companyDescription').value = company.description;
    }

    handleCompanyForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const companyData = {
            name: formData.get('companyName') || document.getElementById('companyName').value,
            tradingName: formData.get('tradingName') || document.getElementById('tradingName').value,
            description: formData.get('companyDescription') || document.getElementById('companyDescription').value
        };
        
        dataManager.updateCompany(companyData);
        this.showNotification('Company information updated successfully!', 'success');
    }

    loadDirectors() {
        const directors = dataManager.getDirectors();
        const tbody = document.querySelector('#directorsTable tbody');
        tbody.innerHTML = directors.map(director => `
            <tr>
                <td>${director.name}</td>
                <td>${director.position}</td>
                <td>${director.division}</td>
                <td>${director.email}</td>
                <td>
                    <button class="btn-edit" onclick="app.editDirector(${director.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteDirector(${director.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    openDirectorModal(directorId = null) {
        const modal = document.getElementById('directorModal');
        const form = document.getElementById('directorForm');
        
        if (directorId) {
            const director = dataManager.getDirectors().find(d => d.id == directorId);
            if (director) {
                document.getElementById('directorId').value = director.id;
                document.getElementById('directorName').value = director.name;
                document.getElementById('directorPosition').value = director.position;
                document.getElementById('directorDivision').value = director.division;
                document.getElementById('directorEmail').value = director.email;
                document.getElementById('directorPhone').value = director.phone || '';
            }
        } else {
            form.reset();
            document.getElementById('directorId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editDirector(id) {
        this.openDirectorModal(id);
    }

    deleteDirector(id) {
        if (confirm('Are you sure you want to delete this director?')) {
            dataManager.deleteDirector(id);
            this.loadDirectors();
            this.showNotification('Director deleted successfully!', 'success');
        }
    }

    handleDirectorForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const directorData = {
            name: formData.get('directorName') || document.getElementById('directorName').value,
            position: formData.get('directorPosition') || document.getElementById('directorPosition').value,
            division: formData.get('directorDivision') || document.getElementById('directorDivision').value,
            email: formData.get('directorEmail') || document.getElementById('directorEmail').value,
            phone: formData.get('directorPhone') || document.getElementById('directorPhone').value
        };

        const directorId = document.getElementById('directorId').value;
        
        if (directorId) {
            dataManager.updateDirector(directorId, directorData);
            this.showNotification('Director updated successfully!', 'success');
        } else {
            dataManager.addDirector(directorData);
            this.showNotification('Director added successfully!', 'success');
        }

        this.closeModal(document.getElementById('directorModal'));
        this.loadDirectors();
    }

    loadDivisions() {
        const divisions = dataManager.getDivisions();
        const grid = document.getElementById('divisionsGrid');
        grid.innerHTML = divisions.map(division => `
            <div class="division-card">
                <div class="card-actions">
                    <button class="btn-edit" onclick="app.editDivision(${division.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteDivision(${division.id})">Delete</button>
                </div>
                <h3>${division.name}</h3>
                <p>${division.description}</p>
                ${division.head ? `<p><strong>Head:</strong> ${division.head}</p>` : ''}
            </div>
        `).join('');
    }

    openDivisionModal(divisionId = null) {
        const modal = document.getElementById('divisionModal');
        const form = document.getElementById('divisionForm');
        
        if (divisionId) {
            const division = dataManager.getDivisions().find(d => d.id == divisionId);
            if (division) {
                document.getElementById('divisionId').value = division.id;
                document.getElementById('divisionName').value = division.name;
                document.getElementById('divisionDescription').value = division.description;
                document.getElementById('divisionHead').value = division.head || '';
            }
        } else {
            form.reset();
            document.getElementById('divisionId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editDivision(id) {
        this.openDivisionModal(id);
    }

    deleteDivision(id) {
        if (confirm('Are you sure you want to delete this division?')) {
            dataManager.deleteDivision(id);
            this.loadDivisions();
            this.populateDivisionSelects();
            this.showNotification('Division deleted successfully!', 'success');
        }
    }

    handleDivisionForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const divisionData = {
            name: formData.get('divisionName') || document.getElementById('divisionName').value,
            description: formData.get('divisionDescription') || document.getElementById('divisionDescription').value,
            head: formData.get('divisionHead') || document.getElementById('divisionHead').value
        };

        const divisionId = document.getElementById('divisionId').value;
        
        if (divisionId) {
            dataManager.updateDivision(divisionId, divisionData);
            this.showNotification('Division updated successfully!', 'success');
        } else {
            dataManager.addDivision(divisionData);
            this.showNotification('Division added successfully!', 'success');
        }

        this.closeModal(document.getElementById('divisionModal'));
        this.loadDivisions();
        this.populateDivisionSelects();
    }

    loadPartnerships() {
        const partnerships = dataManager.getPartnerships();
        const grid = document.getElementById('partnershipsGrid');
        grid.innerHTML = partnerships.map(partnership => `
            <div class="partnership-card">
                <h3>${partnership.name}</h3>
                <p>${partnership.description}</p>
            </div>
        `).join('');
    }

    loadMembers() {
        const members = dataManager.getMembers();
        this.displayMembers(members);
    }

    displayMembers(members) {
        const tbody = document.querySelector('#membersTable tbody');
        tbody.innerHTML = members.map(member => `
            <tr>
                <td>${member.username}</td>
                <td>${member.fullName}</td>
                <td>${member.email}</td>
                <td>${member.division}</td>
                <td><span class="status-${member.status.toLowerCase()}">${member.status}</span></td>
                <td>${new Date(member.registrationDate).toLocaleDateString()}</td>
                <td>
                    <button class="btn-edit" onclick="app.editMember(${member.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteMember(${member.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    searchMembers(query) {
        if (query.trim() === '') {
            this.loadMembers();
        } else {
            const results = dataManager.searchMembers(query);
            this.displayMembers(results);
        }
    }

    openMemberModal(memberId = null) {
        const modal = document.getElementById('memberModal');
        const form = document.getElementById('memberForm');
        
        if (memberId) {
            const member = dataManager.getMembers().find(m => m.id == memberId);
            if (member) {
                document.getElementById('memberId').value = member.id;
                document.getElementById('memberUsername').value = member.username;
                document.getElementById('memberFullName').value = member.fullName;
                document.getElementById('memberEmail').value = member.email;
                document.getElementById('memberDivision').value = member.division;
                document.getElementById('memberStatus').value = member.status;
            }
        } else {
            form.reset();
            document.getElementById('memberId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editMember(id) {
        this.openMemberModal(id);
    }

    deleteMember(id) {
        if (confirm('Are you sure you want to delete this member?')) {
            dataManager.deleteMember(id);
            this.loadMembers();
            this.showNotification('Member deleted successfully!', 'success');
        }
    }

    handleMemberForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const memberData = {
            username: formData.get('memberUsername') || document.getElementById('memberUsername').value,
            fullName: formData.get('memberFullName') || document.getElementById('memberFullName').value,
            email: formData.get('memberEmail') || document.getElementById('memberEmail').value,
            division: formData.get('memberDivision') || document.getElementById('memberDivision').value,
            status: formData.get('memberStatus') || document.getElementById('memberStatus').value
        };

        const memberId = document.getElementById('memberId').value;
        
        if (memberId) {
            dataManager.updateMember(memberId, memberData);
            this.showNotification('Member updated successfully!', 'success');
        } else {
            dataManager.addMember(memberData);
            this.showNotification('Member added successfully!', 'success');
        }

        this.closeModal(document.getElementById('memberModal'));
        this.loadMembers();
    }

    populateDivisionSelects() {
        const divisions = dataManager.getDivisions();
        const selects = [
            document.getElementById('directorDivision'),
            document.getElementById('memberDivision')
        ];

        selects.forEach(select => {
            if (select) {
                const currentValue = select.value;
                select.innerHTML = '<option value="">Select Division</option>' +
                    divisions.map(division => 
                        `<option value="${division.name}">${division.name}</option>`
                    ).join('');
                select.value = currentValue;
            }
        });
    }

    loadBackups() {
        const backups = dataManager.getBackups();
        const backupList = document.getElementById('backupList');
        backupList.innerHTML = `
            <h3>Available Backups</h3>
            ${backups.length === 0 ? '<p>No backups available</p>' : 
                backups.map(backup => `
                    <div class="backup-item">
                        <div>
                            <strong>${backup.name}</strong><br>
                            <small>Created: ${new Date(backup.createdAt).toLocaleString()}</small>
                        </div>
                        <div>
                            <button class="btn-secondary" onclick="app.restoreBackup(${backup.id})">Restore</button>
                            <button class="btn-secondary" onclick="app.downloadBackup(${backup.id})">Download</button>
                        </div>
                    </div>
                `).join('')
            }
        `;
    }

    createBackup() {
        const backup = dataManager.createBackup();
        this.loadBackups();
        this.showNotification(`Backup created: ${backup.name}`, 'success');
    }

    restoreBackup(backupId) {
        if (confirm('Are you sure you want to restore this backup? This will overwrite current data.')) {
            if (dataManager.restoreBackup(backupId)) {
                this.showNotification('Backup restored successfully!', 'success');
                this.loadDashboard();
                location.reload(); // Refresh to show restored data
            } else {
                this.showNotification('Failed to restore backup', 'error');
            }
        }
    }

    downloadBackup(backupId) {
        const backup = dataManager.getBackups().find(b => b.id == backupId);
        if (backup) {
            const dataStr = JSON.stringify(backup.data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${backup.name}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }
    }

    exportData() {
        const data = dataManager.exportData();
        const dataBlob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Data_Export_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        this.showNotification('Data exported successfully!', 'success');
    }

    exportMembers() {
        const members = dataManager.getMembers();
        const csv = this.convertToCSV(members);
        const dataBlob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Members_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        URL.revokeObjectURL(url);
        this.showNotification('Members exported successfully!', 'success');
    }

    convertToCSV(data) {
        if (data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvRows = [headers.join(',')];
        
        for (const row of data) {
            const values = headers.map(header => {
                const escaped = ('' + row[header]).replace(/"/g, '\\"');
                return `"${escaped}"`;
            });
            csvRows.push(values.join(','));
        }
        
        return csvRows.join('\n');
    }

    handleImportFile(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    if (dataManager.importData(event.target.result)) {
                        this.showNotification('Data imported successfully!', 'success');
                        this.loadDashboard();
                        location.reload(); // Refresh to show imported data
                    } else {
                        this.showNotification('Failed to import data. Please check the file format.', 'error');
                    }
                } catch (error) {
                    this.showNotification('Invalid file format', 'error');
                }
            };
            reader.readAsText(file);
        }
    }

    generateWebsite() {
        const title = document.getElementById('websiteTitle').value;
        const includeDirectors = document.getElementById('includeDirectors').checked;
        const includeDivisions = document.getElementById('includeDivisions').checked;
        const includePartnerships = document.getElementById('includePartnerships').checked;
        const includeMembers = document.getElementById('includeMembers').checked;

        const company = dataManager.getCompany();
        const directors = dataManager.getDirectors();
        const divisions = dataManager.getDivisions();
        const partnerships = dataManager.getPartnerships();
        const members = dataManager.getMembers();

        // Generate HTML content based on original template
        let htmlContent = this.generateHTMLTemplate(
            title, company, 
            includeDirectors ? directors : [],
            includeDivisions ? divisions : [],
            includePartnerships ? partnerships : [],
            includeMembers ? members : []
        );

        // Create and download the file
        const dataBlob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Website_${new Date().toISOString().split('T')[0]}.html`;
        link.click();
        URL.revokeObjectURL(url);

        this.showNotification('Website generated and downloaded successfully!', 'success');
    }

    generateHTMLTemplate(title, company, directors, divisions, partnerships, members) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #2c3e50, #3498db); color: white; text-align: center; padding: 2rem 0; margin-bottom: 2rem; }
        .section { background: #f8f9fa; margin: 2rem 0; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .section h2 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 0.5rem; margin-bottom: 1rem; }
        .divisions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .division-card { background: white; padding: 1rem; border-radius: 5px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .governance-structure { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .governance-item { background: white; padding: 1rem; border-radius: 5px; border-left: 4px solid #3498db; }
        .work-with-us { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem; }
        .work-item { flex: 1; min-width: 200px; background: white; padding: 1rem; border-radius: 5px; text-align: center; }
        .members-info { background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 2rem; border-radius: 8px; text-align: center; }
        .reference-badge { background: #e74c3c; color: white; padding: 0.25rem 0.5rem; border-radius: 50%; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-right: 0.5rem; }
        footer { background: #2c3e50; color: white; text-align: center; padding: 2rem; margin-top: 3rem; }
        @media (max-width: 768px) { .divisions-grid { grid-template-columns: 1fr; } .governance-structure { grid-template-columns: 1fr; } .work-with-us { flex-direction: column; } }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>${company.name}</h1>
            <p>Trading as ${company.tradingName} - Your Gateway to Investment Excellence</p>
        </div>
    </header>
    <div class="container">
        <section class="section">
            <h2><span class="reference-badge">0</span>Company Main Structure</h2>
            <p>${company.description}</p>
        </section>
        ${directors.length > 0 ? `
        <section class="section">
            <h2><span class="reference-badge">1</span>Directors - Governing Body</h2>
            <p>Our governing structure ensures transparent leadership and strategic direction for the company.</p>
            <div class="governance-structure">
                ${directors.map(director => `
                <div class="governance-item">
                    <h3>${director.name}</h3>
                    <p><strong>Position:</strong> ${director.position}</p>
                    ${director.division ? `<p><strong>Division:</strong> ${director.division}</p>` : ''}
                    <p><strong>Email:</strong> ${director.email}</p>
                </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
        ${divisions.length > 0 ? `
        <section class="section">
            <h2><span class="reference-badge">2</span>Divisions</h2>
            <p>Our diverse portfolio of divisions ensures comprehensive coverage across multiple industries and sectors.</p>
            <div class="divisions-grid">
                ${divisions.map(division => `
                <div class="division-card">
                    <h3>${division.name}</h3>
                    <p>${division.description}</p>
                    ${division.head ? `<p><strong>Head:</strong> ${division.head}</p>` : ''}
                </div>
                `).join('')// filepath: c:\Users\jacob\Documents\JKWINNERSINVESTMENTNFO\information-management-system\js\app.js
// Main application logic
class JKWIApp {
    constructor() {
        this.currentSection = 'dashboard';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboard();
        this.populateDivisionSelects();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.dataset.section;
                this.showSection(section);
            });
        });

        // Forms
        document.getElementById('companyForm').addEventListener('submit', (e) => this.handleCompanyForm(e));
        document.getElementById('directorForm').addEventListener('submit', (e) => this.handleDirectorForm(e));
        document.getElementById('divisionForm').addEventListener('submit', (e) => this.handleDivisionForm(e));
        document.getElementById('memberForm').addEventListener('submit', (e) => this.handleMemberForm(e));

        // Modals
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => this.closeModal(e.target.closest('.modal')));
        });

        // Search
        document.getElementById('memberSearch').addEventListener('input', (e) => this.searchMembers(e.target.value));

        // Import file
        document.getElementById('importFile').addEventListener('change', (e) => this.handleImportFile(e));

        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target);
            }
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

        this.currentSection = sectionName;

        // Load section-specific data
        switch (sectionName) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'company':
                this.loadCompanyForm();
                break;
            case 'directors':
                this.loadDirectors();
                break;
            case 'divisions':
                this.loadDivisions();
                break;
            case 'partnerships':
                this.loadPartnerships();
                break;
            case 'members':
                this.loadMembers();
                break;
            case 'backup':
                this.loadBackups();
                break;
        }
    }

    loadDashboard() {
        const stats = dataManager.getStats();
        document.getElementById('totalMembers').textContent = stats.totalMembers;
        document.getElementById('totalDivisions').textContent = stats.totalDivisions;
        document.getElementById('totalDirectors').textContent = stats.totalDirectors;

        // Load recent activities
        const activities = dataManager.getActivities().slice(0, 10);
        const activityList = document.getElementById('activityList');
        activityList.innerHTML = activities.map(activity => `
            <li>
                ${activity.description} - 
                <span class="timestamp">${new Date(activity.timestamp).toLocaleString()}</span>
            </li>
        `).join('');
    }

    loadCompanyForm() {
        const company = dataManager.getCompany();
        document.getElementById('companyName').value = company.name;
        document.getElementById('tradingName').value = company.tradingName;
        document.getElementById('companyDescription').value = company.description;
    }

    handleCompanyForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const companyData = {
            name: formData.get('companyName') || document.getElementById('companyName').value,
            tradingName: formData.get('tradingName') || document.getElementById('tradingName').value,
            description: formData.get('companyDescription') || document.getElementById('companyDescription').value
        };
        
        dataManager.updateCompany(companyData);
        this.showNotification('Company information updated successfully!', 'success');
    }

    loadDirectors() {
        const directors = dataManager.getDirectors();
        const tbody = document.querySelector('#directorsTable tbody');
        tbody.innerHTML = directors.map(director => `
            <tr>
                <td>${director.name}</td>
                <td>${director.position}</td>
                <td>${director.division}</td>
                <td>${director.email}</td>
                <td>
                    <button class="btn-edit" onclick="app.editDirector(${director.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteDirector(${director.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    openDirectorModal(directorId = null) {
        const modal = document.getElementById('directorModal');
        const form = document.getElementById('directorForm');
        
        if (directorId) {
            const director = dataManager.getDirectors().find(d => d.id == directorId);
            if (director) {
                document.getElementById('directorId').value = director.id;
                document.getElementById('directorName').value = director.name;
                document.getElementById('directorPosition').value = director.position;
                document.getElementById('directorDivision').value = director.division;
                document.getElementById('directorEmail').value = director.email;
                document.getElementById('directorPhone').value = director.phone || '';
            }
        } else {
            form.reset();
            document.getElementById('directorId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editDirector(id) {
        this.openDirectorModal(id);
    }

    deleteDirector(id) {
        if (confirm('Are you sure you want to delete this director?')) {
            dataManager.deleteDirector(id);
            this.loadDirectors();
            this.showNotification('Director deleted successfully!', 'success');
        }
    }

    handleDirectorForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const directorData = {
            name: formData.get('directorName') || document.getElementById('directorName').value,
            position: formData.get('directorPosition') || document.getElementById('directorPosition').value,
            division: formData.get('directorDivision') || document.getElementById('directorDivision').value,
            email: formData.get('directorEmail') || document.getElementById('directorEmail').value,
            phone: formData.get('directorPhone') || document.getElementById('directorPhone').value
        };

        const directorId = document.getElementById('directorId').value;
        
        if (directorId) {
            dataManager.updateDirector(directorId, directorData);
            this.showNotification('Director updated successfully!', 'success');
        } else {
            dataManager.addDirector(directorData);
            this.showNotification('Director added successfully!', 'success');
        }

        this.closeModal(document.getElementById('directorModal'));
        this.loadDirectors();
    }

    loadDivisions() {
        const divisions = dataManager.getDivisions();
        const grid = document.getElementById('divisionsGrid');
        grid.innerHTML = divisions.map(division => `
            <div class="division-card">
                <div class="card-actions">
                    <button class="btn-edit" onclick="app.editDivision(${division.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteDivision(${division.id})">Delete</button>
                </div>
                <h3>${division.name}</h3>
                <p>${division.description}</p>
                ${division.head ? `<p><strong>Head:</strong> ${division.head}</p>` : ''}
            </div>
        `).join('');
    }

    openDivisionModal(divisionId = null) {
        const modal = document.getElementById('divisionModal');
        const form = document.getElementById('divisionForm');
        
        if (divisionId) {
            const division = dataManager.getDivisions().find(d => d.id == divisionId);
            if (division) {
                document.getElementById('divisionId').value = division.id;
                document.getElementById('divisionName').value = division.name;
                document.getElementById('divisionDescription').value = division.description;
                document.getElementById('divisionHead').value = division.head || '';
            }
        } else {
            form.reset();
            document.getElementById('divisionId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editDivision(id) {
        this.openDivisionModal(id);
    }

    deleteDivision(id) {
        if (confirm('Are you sure you want to delete this division?')) {
            dataManager.deleteDivision(id);
            this.loadDivisions();
            this.populateDivisionSelects();
            this.showNotification('Division deleted successfully!', 'success');
        }
    }

    handleDivisionForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const divisionData = {
            name: formData.get('divisionName') || document.getElementById('divisionName').value,
            description: formData.get('divisionDescription') || document.getElementById('divisionDescription').value,
            head: formData.get('divisionHead') || document.getElementById('divisionHead').value
        };

        const divisionId = document.getElementById('divisionId').value;
        
        if (divisionId) {
            dataManager.updateDivision(divisionId, divisionData);
            this.showNotification('Division updated successfully!', 'success');
        } else {
            dataManager.addDivision(divisionData);
            this.showNotification('Division added successfully!', 'success');
        }

        this.closeModal(document.getElementById('divisionModal'));
        this.loadDivisions();
        this.populateDivisionSelects();
    }

    loadPartnerships() {
        const partnerships = dataManager.getPartnerships();
        const grid = document.getElementById('partnershipsGrid');
        grid.innerHTML = partnerships.map(partnership => `
            <div class="partnership-card">
                <h3>${partnership.name}</h3>
                <p>${partnership.description}</p>
            </div>
        `).join('');
    }

    loadMembers() {
        const members = dataManager.getMembers();
        this.displayMembers(members);
    }

    displayMembers(members) {
        const tbody = document.querySelector('#membersTable tbody');
        tbody.innerHTML = members.map(member => `
            <tr>
                <td>${member.username}</td>
                <td>${member.fullName}</td>
                <td>${member.email}</td>
                <td>${member.division}</td>
                <td><span class="status-${member.status.toLowerCase()}">${member.status}</span></td>
                <td>${new Date(member.registrationDate).toLocaleDateString()}</td>
                <td>
                    <button class="btn-edit" onclick="app.editMember(${member.id})">Edit</button>
                    <button class="btn-delete" onclick="app.deleteMember(${member.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    searchMembers(query) {
        if (query.trim() === '') {
            this.loadMembers();
        } else {
            const results = dataManager.searchMembers(query);
            this.displayMembers(results);
        }
    }

    openMemberModal(memberId = null) {
        const modal = document.getElementById('memberModal');
        const form = document.getElementById('memberForm');
        
        if (memberId) {
            const member = dataManager.getMembers().find(m => m.id == memberId);
            if (member) {
                document.getElementById('memberId').value = member.id;
                document.getElementById('memberUsername').value = member.username;
                document.getElementById('memberFullName').value = member.fullName;
                document.getElementById('memberEmail').value = member.email;
                document.getElementById('memberDivision').value = member.division;
                document.getElementById('memberStatus').value = member.status;
            }
        } else {
            form.reset();
            document.getElementById('memberId').value = '';
        }
        
        modal.style.display = 'block';
    }

    editMember(id) {
        this.openMemberModal(id);
    }

    deleteMember(id) {
        if (confirm('Are you sure you want to delete this member?')) {
            dataManager.deleteMember(id);
            this.loadMembers();
            this.showNotification('Member deleted successfully!', 'success');
        }
    }

    handleMemberForm(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const memberData = {
            username: formData.get('memberUsername') || document.getElementById('memberUsername').value,
            fullName: formData.get('memberFullName') || document.getElementById('memberFullName').value,
            email: formData.get('memberEmail') || document.getElementById('memberEmail').value,
            division: formData.get('memberDivision') || document.getElementById('memberDivision').value,
            status: formData.get('memberStatus') || document.getElementById('memberStatus').value
        };

        const memberId = document.getElementById('memberId').value;
        
        if (memberId) {
            dataManager.updateMember(memberId, memberData);
            this.showNotification('Member updated successfully!', 'success');
        } else {
            dataManager.addMember(memberData);
            this.showNotification('Member added successfully!', 'success');
        }

        this.closeModal(document.getElementById('memberModal'));
        this.loadMembers();
    }

    populateDivisionSelects() {
        const divisions = dataManager.getDivisions();
        const selects = [
            document.getElementById('directorDivision'),
            document.getElementById('memberDivision')
        ];

        selects.forEach(select => {
            if (select) {
                const currentValue = select.value;
                select.innerHTML = '<option value="">Select Division</option>' +
                    divisions.map(division => 
                        `<option value="${division.name}">${division.name}</option>`
                    ).join('');
                select.value = currentValue;
            }
        });
    }

    loadBackups() {
        const backups = dataManager.getBackups();
        const backupList = document.getElementById('backupList');
        backupList.innerHTML = `
            <h3>Available Backups</h3>
            ${backups.length === 0 ? '<p>No backups available</p>' : 
                backups.map(backup => `
                    <div class="backup-item">
                        <div>
                            <strong>${backup.name}</strong><br>
                            <small>Created: ${new Date(backup.createdAt).toLocaleString()}</small>
                        </div>
                        <div>
                            <button class="btn-secondary" onclick="app.restoreBackup(${backup.id})">Restore</button>
                            <button class="btn-secondary" onclick="app.downloadBackup(${backup.id})">Download</button>
                        </div>
                    </div>
                `).join('')
            }
        `;
    }

    createBackup() {
        const backup = dataManager.createBackup();
        this.loadBackups();
        this.showNotification(`Backup created: ${backup.name}`, 'success');
    }

    restoreBackup(backupId) {
        if (confirm('Are you sure you want to restore this backup? This will overwrite current data.')) {
            if (dataManager.restoreBackup(backupId)) {
                this.showNotification('Backup restored successfully!', 'success');
                this.loadDashboard();
                location.reload(); // Refresh to show restored data
            } else {
                this.showNotification('Failed to restore backup', 'error');
            }
        }
    }

    downloadBackup(backupId) {
        const backup = dataManager.getBackups().find(b => b.id == backupId);
        if (backup) {
            const dataStr = JSON.stringify(backup.data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${backup.name}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }
    }

    exportData() {
        const data = dataManager.exportData();
        const dataBlob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Data_Export_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        this.showNotification('Data exported successfully!', 'success');
    }

    exportMembers() {
        const members = dataManager.getMembers();
        const csv = this.convertToCSV(members);
        const dataBlob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Members_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        URL.revokeObjectURL(url);
        this.showNotification('Members exported successfully!', 'success');
    }

    convertToCSV(data) {
        if (data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvRows = [headers.join(',')];
        
        for (const row of data) {
            const values = headers.map(header => {
                const escaped = ('' + row[header]).replace(/"/g, '\\"');
                return `"${escaped}"`;
            });
            csvRows.push(values.join(','));
        }
        
        return csvRows.join('\n');
    }

    handleImportFile(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                try {
                    if (dataManager.importData(event.target.result)) {
                        this.showNotification('Data imported successfully!', 'success');
                        this.loadDashboard();
                        location.reload(); // Refresh to show imported data
                    } else {
                        this.showNotification('Failed to import data. Please check the file format.', 'error');
                    }
                } catch (error) {
                    this.showNotification('Invalid file format', 'error');
                }
            };
            reader.readAsText(file);
        }
    }

    generateWebsite() {
        const title = document.getElementById('websiteTitle').value;
        const includeDirectors = document.getElementById('includeDirectors').checked;
        const includeDivisions = document.getElementById('includeDivisions').checked;
        const includePartnerships = document.getElementById('includePartnerships').checked;
        const includeMembers = document.getElementById('includeMembers').checked;

        const company = dataManager.getCompany();
        const directors = dataManager.getDirectors();
        const divisions = dataManager.getDivisions();
        const partnerships = dataManager.getPartnerships();
        const members = dataManager.getMembers();

        // Generate HTML content based on original template
        let htmlContent = this.generateHTMLTemplate(
            title, company, 
            includeDirectors ? directors : [],
            includeDivisions ? divisions : [],
            includePartnerships ? partnerships : [],
            includeMembers ? members : []
        );

        // Create and download the file
        const dataBlob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `JKWI_Website_${new Date().toISOString().split('T')[0]}.html`;
        link.click();
        URL.revokeObjectURL(url);

        this.showNotification('Website generated and downloaded successfully!', 'success');
    }

    generateHTMLTemplate(title, company, directors, divisions, partnerships, members) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: linear-gradient(135deg, #2c3e50, #3498db); color: white; text-align: center; padding: 2rem 0; margin-bottom: 2rem; }
        .section { background: #f8f9fa; margin: 2rem 0; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .section h2 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 0.5rem; margin-bottom: 1rem; }
        .divisions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .division-card { background: white; padding: 1rem; border-radius: 5px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .governance-structure { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .governance-item { background: white; padding: 1rem; border-radius: 5px; border-left: 4px solid #3498db; }
        .work-with-us { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem; }
        .work-item { flex: 1; min-width: 200px; background: white; padding: 1rem; border-radius: 5px; text-align: center; }
        .members-info { background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 2rem; border-radius: 8px; text-align: center; }
        .reference-badge { background: #e74c3c; color: white; padding: 0.25rem 0.5rem; border-radius: 50%; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-right: 0.5rem; }
        footer { background: #2c3e50; color: white; text-align: center; padding: 2rem; margin-top: 3rem; }
        @media (max-width: 768px) { .divisions-grid { grid-template-columns: 1fr; } .governance-structure { grid-template-columns: 1fr; } .work-with-us { flex-direction: column; } }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>${company.name}</h1>
            <p>Trading as ${company.tradingName} - Your Gateway to Investment Excellence</p>
        </div>
    </header>
    <div class="container">
        <section class="section">
            <h2><span class="reference-badge">0</span>Company Main Structure</h2>
            <p>${company.description}</p>
        </section>
        ${directors.length > 0 ? `
        <section class="section">
            <h2><span class="reference-badge">1</span>Directors - Governing Body</h2>
            <p>Our governing structure ensures transparent leadership and strategic direction for the company.</p>
            <div class="governance-structure">
                ${directors.map(director => `
                <div class="governance-item">
                    <h3>${director.name}</h3>
                    <p><strong>Position:</strong> ${director.position}</p>
                    ${director.division ? `<p><strong>Division:</strong> ${director.division}</p>` : ''}
                    <p><strong>Email:</strong> ${director.email}</p>
                </div>
                `).join('')}
            </div>
        </section>
        ` : ''}
        ${divisions.length > 0 ? `
        <section class="section">
            <h2><span class="reference-badge">2</span>Divisions</h2>
            <p>Our diverse portfolio of divisions ensures comprehensive coverage across multiple industries and sectors.</p>
            <div class="divisions-grid">
                ${divisions.map(division => `
                <div class="division-card">
                    <h3>${division.name}</h3>
                    <p>${division.description}</p>
                    ${division.head ? `<p><strong>Head:</strong> ${division.head}</p>` : ''}
                </div>
                `).join('')