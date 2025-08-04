const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.static('public'));

// Data directory
const DATA_DIR = path.join(__dirname, '..', 'MEMBERS');
const APPLICATIONS_DIR = path.join(__dirname, '..', 'APPLICATIONS');

// Ensure directories exist
async function ensureDirectories() {
    try {
        await fs.mkdir(DATA_DIR, { recursive: true });
        await fs.mkdir(APPLICATIONS_DIR, { recursive: true });
        console.log('✅ Data directories initialized');
    } catch (error) {
        console.error('❌ Failed to create directories:', error);
    }
}

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        message: 'JKWI Information Management System is running',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        endpoints: {
            health: '/api/health',
            register: '/api/register',
            members: '/api/members',
            applications: '/api/applications'
        }
    });
});

// Register new user endpoint
app.post('/api/register', async (req, res) => {
    try {
        const { username, email, full_name, role = 'member' } = req.body;
        
        if (!username || !email || !full_name) {
            return res.status(400).json({
                success: false,
                error: 'Missing required fields: username, email, full_name'
            });
        }

        // Generate user ID
        const userId = crypto.randomBytes(16).toString('hex');
        const token = crypto.randomBytes(32).toString('hex');
        
        const user = {
            id: userId,
            username,
            email,
            full_name,
            role,
            status: 'pending_verification',
            created_at: new Date().toISOString(),
            token
        };

        // Save user to file
        const userFile = path.join(DATA_DIR, `user_${userId}.json`);
        await fs.writeFile(userFile, JSON.stringify(user, null, 2));

        console.log(`✅ User registered: ${username} (${userId})`);
        
        res.json({
            success: true,
            message: 'User registered successfully',
            user: {
                id: userId,
                username,
                email,
                full_name,
                role,
                status: 'pending_verification'
            },
            token
        });
    } catch (error) {
        console.error('❌ Registration error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error during registration'
        });
    }
});

// Submit member application
app.post('/api/members', async (req, res) => {
    try {
        const memberData = req.body;
        
        if (!memberData.personal_info || !memberData.personal_info.email) {
            return res.status(400).json({
                success: false,
                error: 'Invalid member data - missing personal information'
            });
        }

        // Generate application ID if not provided
        if (!memberData.application_id) {
            memberData.application_id = `JKWI-${Date.now()}-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
        }

        // Add processing metadata
        memberData.processed_at = new Date().toISOString();
        memberData.status = 'submitted';
        memberData.processing_status = 'pending_review';
        memberData.member_id = crypto.randomBytes(8).toString('hex').toUpperCase();

        // Save application
        const applicationFile = path.join(APPLICATIONS_DIR, `application_${memberData.application_id}.json`);
        await fs.writeFile(applicationFile, JSON.stringify(memberData, null, 2));

        // Also save to members directory for approved applications
        const memberFile = path.join(DATA_DIR, `member_${memberData.member_id}.json`);
        const memberRecord = {
            ...memberData,
            member_status: 'pending_approval',
            approval_required: true
        };
        await fs.writeFile(memberFile, JSON.stringify(memberRecord, null, 2));

        console.log(`✅ Application submitted: ${memberData.application_id} for ${memberData.personal_info.first_name} ${memberData.personal_info.last_name}`);

        res.json({
            success: true,
            message: 'Application submitted successfully',
            application_id: memberData.application_id,
            member_id: memberData.member_id,
            status: 'submitted',
            next_steps: [
                'Application review by JKWI team',
                'Email verification',
                'Background check (if applicable)',
                'Final approval and welcome package'
            ]
        });
    } catch (error) {
        console.error('❌ Application submission error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error during application submission'
        });
    }
});

// Get all applications
app.get('/api/applications', async (req, res) => {
    try {
        const files = await fs.readdir(APPLICATIONS_DIR);
        const applications = [];

        for (const file of files) {
            if (file.endsWith('.json')) {
                const filePath = path.join(APPLICATIONS_DIR, file);
                const data = await fs.readFile(filePath, 'utf8');
                applications.push(JSON.parse(data));
            }
        }

        res.json({
            success: true,
            count: applications.length,
            applications: applications.sort((a, b) => new Date(b.processed_at) - new Date(a.processed_at))
        });
    } catch (error) {
        console.error('❌ Error fetching applications:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

// Get all members
app.get('/api/members', async (req, res) => {
    try {
        const files = await fs.readdir(DATA_DIR);
        const members = [];

        for (const file of files) {
            if (file.startsWith('member_') && file.endsWith('.json')) {
                const filePath = path.join(DATA_DIR, file);
                const data = await fs.readFile(filePath, 'utf8');
                const member = JSON.parse(data);
                // Remove sensitive information
                delete member.financial_info;
                members.push(member);
            }
        }

        res.json({
            success: true,
            count: members.length,
            members: members.sort((a, b) => new Date(b.processed_at) - new Date(a.processed_at))
        });
    } catch (error) {
        console.error('❌ Error fetching members:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

// Start server
async function startServer() {
    await ensureDirectories();
    
    app.listen(PORT, () => {
        console.log(`🚀 JKWI Information Management System started on port ${PORT}`);
        console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
        console.log(`📋 API endpoints available at: http://localhost:${PORT}/api/`);
    });
}

// Error handling
process.on('uncaughtException', (error) => {
    console.error('❌ Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});

startServer();