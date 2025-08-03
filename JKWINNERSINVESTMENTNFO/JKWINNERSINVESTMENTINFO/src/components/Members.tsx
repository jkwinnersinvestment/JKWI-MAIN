import React from 'react';

const Members: React.FC = () => {
    return (
        <section className="members-section">
            <h2>Members - Winners Community</h2>
            <p>Welcome to the Winners Community! Every member of JK Winners Investment is a valued "Winner" in our community.</p>
            <div className="membership-info">
                <h3>Membership Registration Process</h3>
                <ol>
                    <li>Complete our vigorous registration system through NAKO.</li>
                    <li>Undergo thorough verification and background checks.</li>
                    <li>Receive approval and member status confirmation.</li>
                    <li>Create your unique username and secure password.</li>
                    <li>Welcome to the Winners family!</li>
                </ol>
            </div>
            <p style={{ fontStyle: 'italic' }}>"All members are referred to as Winners - because success is our shared destination."</p>
        </section>
    );
};

export default Members;