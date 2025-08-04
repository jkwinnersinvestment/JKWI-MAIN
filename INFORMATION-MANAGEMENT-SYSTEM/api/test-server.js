const http = require('http');
const fs = require('fs').promises;

async function testAPI() {
    console.log('🧪 Testing JKWI API endpoints...');
    
    // Test data
    const testMember = {
        personal_info: {
            first_name: "John",
            last_name: "Test",
            email: "john.test@example.com",
            phone_primary: "+1234567890",
            date_of_birth: "1990-01-01",
            gender: "Male",
            nationality: "South African",
            id_number: "1234567890123",
            address: {
                street: "123 Test Street",
                city: "Test City",
                province_state: "Test Province",
                postal_code: "12345",
                country: "South Africa"
            }
        },
        jkwi_info: {
            username: "johntest",
            division: "Service Division",
            experience: "Testing applications",
            status: "pending_approval"
        },
        financial_info: {
            bank_name: "Test Bank",
            account_number: "1234567890",
            account_type: "Savings",
            swift_code: "TESTBANK"
        },
        emergency_contact: {
            name: "Jane Test",
            relationship: "Spouse",
            phone: "+1234567891",
            email: "jane.test@example.com"
        },
        preferences: {
            newsletter: true,
            terms_accepted: true,
            privacy_accepted: true,
            data_accuracy_confirmed: true
        }
    };

    const baseURL = 'http://localhost:3000';
    
    try {
        // Test health endpoint
        console.log('1. Testing health endpoint...');
        const healthResponse = await fetch(`${baseURL}/api/health`);
        const healthData = await healthResponse.json();
        console.log('✅ Health check:', healthData.status);

        // Test registration
        console.log('2. Testing user registration...');
        const registerResponse = await fetch(`${baseURL}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: testMember.jkwi_info.username,
                email: testMember.personal_info.email,
                full_name: `${testMember.personal_info.first_name} ${testMember.personal_info.last_name}`,
                role: 'member'
            })
        });
        const registerData = await registerResponse.json();
        console.log('✅ Registration:', registerData.success ? 'Success' : 'Failed');

        // Test member application submission
        console.log('3. Testing member application submission...');
        const memberResponse = await fetch(`${baseURL}/api/members`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${registerData.token || 'test-token'}`
            },
            body: JSON.stringify(testMember)
        });
        const memberData = await memberResponse.json();
        console.log('✅ Member application:', memberData.success ? 'Success' : 'Failed');
        
        if (memberData.success) {
            console.log(`📋 Application ID: ${memberData.application_id}`);
            console.log(`👤 Member ID: ${memberData.member_id}`);
        }

        // Test fetching applications
        console.log('4. Testing applications retrieval...');
        const appsResponse = await fetch(`${baseURL}/api/applications`);
        const appsData = await appsResponse.json();
        console.log(`✅ Applications count: ${appsData.count || 0}`);

        console.log('\n🎉 All tests completed successfully!');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        console.log('\n💡 Make sure the server is running: npm start');
    }
}

// Run tests
testAPI();