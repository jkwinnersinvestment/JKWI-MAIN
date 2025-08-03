// Data storage and management
class DataManager {
    constructor() {
        this.data = {
            company: {
                name: "JK Winners Investment",
                tradingName: "JKWI",
                description: "JK Winners Investment (JKWI) is a comprehensive investment company structured to provide excellence across multiple sectors.",
                lastUpdated: new Date().toISOString()
            },
            directors: [
                {
                    id: 1,
                    name: "John Doe",
                    position: "President",
                    division: "Main Structure",
                    email: "john.doe@jkwi.com",
                    phone: "+1234567890",
                    createdAt: new Date().toISOString()
                }
            ],
            divisions: [
                { id: 1, name: "Mining Division", description: "Mineral extraction and resource development", head: "", reference: 2 },
                { id: 2, name: "Infrastructure Division", description: "Construction and development projects", head: "", reference: 2 },
                { id: 3, name: "Farming Division", description: "Agricultural and agribusiness ventures", head: "", reference: 2 },
                { id: 4, name: "Service Division", description: "Professional and consulting services", head: "", reference: 2 },
                { id: 5, name: "Finance Division", description: "Financial services and investment management", head: "", reference: 2 },
                { id: 6, name: "Legal Division", description: "Legal advisory and compliance services", head: "", reference: 2 },
                { id: 7, name: "Media Division", description: "Communications and media services", head: "", reference: 2 },
                { id: 8, name: "Social Division", description: "Community engagement and social impact", head: "", reference: 2 }
            ],
            partnerships: [
                { id: 1, name: "Chair Office", description: "Office of the Chair of the Board - Strategic leadership and governance oversight", reference: 3 },
                { id: 2, name: "Customer Interest", description: "Dedicated to serving our clients' needs and ensuring satisfaction", reference: 3 },
                { id: 3, name: "Investors", description: "Partnership opportunities for financial growth and development", reference: 3 },
                { id: 4, name: "Partners", description: "Strategic alliances for mutual growth and success", reference: 3 }
            ],
            members: [
                {
                    id: 1,
                    username: "winner001",
                    fullName: "Jane Smith",
                    email: "jane.smith@jkwi.com",
                    division: "Finance Division",
                    status: "Active",
                    registrationDate: new Date().toISOString()
                }
            ],
            activities: [],
            backups: []
        };
        
        this.loadData();
    }

    // Load data from localStorage
    loadData() {
        const savedData = localStorage.getItem('jkwi_data');
        if (savedData) {
            this.data = { ...this.data, ...JSON.parse(savedData) };
        }
        this.addActivity('System initialized');
        
        // Auto-load demo members if no existing data
        if (this.data.members.length === 1) { // Only has the default demo member
            this.loadDemoMembers();
        }
    }

    // Save data to localStorage
    saveData() {
        localStorage.setItem('jkwi_data', JSON.stringify(this.data));
        this.addActivity('Data saved to local storage');
    }

    // Add activity log
    addActivity(activity) {
        this.data.activities.unshift({
            id: Date.now(),
            description: activity,
            timestamp: new Date().toISOString()
        });
        
        // Keep only last 50 activities
        if (this.data.activities.length > 50) {
            this.data.activities = this.data.activities.slice(0, 50);
        }
    }

    // Company methods
    updateCompany(companyData) {
        this.data.company = { ...this.data.company, ...companyData, lastUpdated: new Date().toISOString() };
        this.addActivity(`Company information updated`);
        this.saveData();
    }

    getCompany() {
        return this.data.company;
    }

    // Directors methods
    addDirector(director) {
        const newDirector = {
            ...director,
            id: Date.now(),
            createdAt: new Date().toISOString()
        };
        this.data.directors.push(newDirector);
        this.addActivity(`New director added: ${director.name}`);
        this.saveData();
        return newDirector;
    }

    updateDirector(id, director) {
        const index = this.data.directors.findIndex(d => d.id == id);
        if (index !== -1) {
            this.data.directors[index] = { ...this.data.directors[index], ...director };
            this.addActivity(`Director updated: ${director.name}`);
            this.saveData();
            return this.data.directors[index];
        }
        return null;
    }

    deleteDirector(id) {
        const index = this.data.directors.findIndex(d => d.id == id);
        if (index !== -1) {
            const director = this.data.directors[index];
            this.data.directors.splice(index, 1);
            this.addActivity(`Director deleted: ${director.name}`);
            this.saveData();
            return true;
        }
        return false;
    }

    getDirectors() {
        return this.data.directors;
    }

    // Divisions methods
    addDivision(division) {
        const newDivision = {
            ...division,
            id: Date.now(),
            reference: 2
        };
        this.data.divisions.push(newDivision);
        this.addActivity(`New division added: ${division.name}`);
        this.saveData();
        return newDivision;
    }

    updateDivision(id, division) {
        const index = this.data.divisions.findIndex(d => d.id == id);
        if (index !== -1) {
            this.data.divisions[index] = { ...this.data.divisions[index], ...division };
            this.addActivity(`Division updated: ${division.name}`);
            this.saveData();
            return this.data.divisions[index];
        }
        return null;
    }

    deleteDivision(id) {
        const index = this.data.divisions.findIndex(d => d.id == id);
        if (index !== -1) {
            const division = this.data.divisions[index];
            this.data.divisions.splice(index, 1);
            this.addActivity(`Division deleted: ${division.name}`);
            this.saveData();
            return true;
        }
        return false;
    }

    getDivisions() {
        return this.data.divisions;
    }

    // Members methods
    addMember(member) {
        const newMember = {
            ...member,
            id: Date.now(),
            registrationDate: new Date().toISOString()
        };
        this.data.members.push(newMember);
        this.addActivity(`New member added: ${member.username}`);
        this.saveData();
        return newMember;
    }

    updateMember(id, member) {
        const index = this.data.members.findIndex(m => m.id == id);
        if (index !== -1) {
            this.data.members[index] = { ...this.data.members[index], ...member };
            this.addActivity(`Member updated: ${member.username}`);
            this.saveData();
            return this.data.members[index];
        }
        return null;
    }

    deleteMember(id) {
        const index = this.data.members.findIndex(m => m.id == id);
        if (index !== -1) {
            const member = this.data.members[index];
            this.data.members.splice(index, 1);
            this.addActivity(`Member deleted: ${member.username}`);
            this.saveData();
            return true;
        }
        return false;
    }

    getMembers() {
        return this.data.members;
    }

    searchMembers(query) {
        return this.data.members.filter(member => 
            member.username.toLowerCase().includes(query.toLowerCase()) ||
            member.fullName.toLowerCase().includes(query.toLowerCase()) ||
            member.email.toLowerCase().includes(query.toLowerCase())
        );
    }

    // Partnerships methods
    getPartnerships() {
        return this.data.partnerships;
    }

    // Activities methods
    getActivities() {
        return this.data.activities;
    }

    // Backup methods
    createBackup() {
        const backup = {
            id: Date.now(),
            name: `Backup_${new Date().toISOString().split('T')[0]}_${Date.now()}`,
            data: JSON.parse(JSON.stringify(this.data)),
            createdAt: new Date().toISOString()
        };
        this.data.backups.push(backup);
        this.addActivity(`Backup created: ${backup.name}`);
        this.saveData();
        return backup;
    }

    restoreBackup(backupId) {
        const backup = this.data.backups.find(b => b.id == backupId);
        if (backup) {
            this.data = { ...backup.data };
            this.addActivity(`System restored from backup: ${backup.name}`);
            this.saveData();
            return true;
        }
        return false;
    }

    getBackups() {
        return this.data.backups;
    }

    // Export/Import methods
    exportData() {
        return JSON.stringify(this.data, null, 2);
    }

    importData(jsonData) {
        try {
            const importedData = JSON.parse(jsonData);
            this.data = { ...this.data, ...importedData };
            this.addActivity('Data imported successfully');
            this.saveData();
            return true;
        } catch (error) {
            console.error('Import failed:', error);
            return false;
        }
    }

    // Statistics methods
    getStats() {
        return {
            totalMembers: this.data.members.length,
            totalDirectors: this.data.directors.length,
            totalDivisions: this.data.divisions.length,
            totalActivities: this.data.activities.length
        };
    }

    // Demo member methods
    loadDemoMembers() {
        // Demo members will be loaded from demo_members.js if available
        if (typeof demoMembers !== 'undefined' && Array.isArray(demoMembers)) {
            demoMembers.forEach(member => {
                const existing = this.data.members.find(m => m.username === member.username);
                if (!existing) {
                    this.data.members.push({
                        ...member,
                        id: this.data.members.length > 0 ? Math.max(...this.data.members.map(m => m.id)) + 1 : 1
                    });
                }
            });
            this.saveData();
            this.addActivity(`Loaded ${demoMembers.length} demo members`);
            return demoMembers.length;
        }
        return 0;
    }
}

// Initialize data manager
const dataManager = new DataManager();