import React from 'react';

const Membership: React.FC = () => {
    return (
        <div className="membership-container">
            <h2>Membership Information</h2>
            <p>Welcome to the JK Winners Investment Membership page. Here you will find all the necessary information regarding the membership process.</p>
            
            <h3>Membership Benefits</h3>
            <ul>
                <li>Access to exclusive investment opportunities</li>
                <li>Networking with industry professionals</li>
                <li>Regular updates on market trends and insights</li>
                <li>Participation in member-only events and webinars</li>
            </ul>

            <h3>How to Become a Member</h3>
            <ol>
                <li>Fill out the membership application form.</li>
                <li>Submit the required documentation for verification.</li>
                <li>Await confirmation of your membership status.</li>
                <li>Receive your membership ID and welcome package.</li>
            </ol>

            <p>If you have any questions regarding the membership process, please contact our support team.</p>
        </div>
    );
};

export default Membership;