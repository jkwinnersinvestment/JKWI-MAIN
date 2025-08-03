import React from 'react';
import { Link } from 'react-router-dom';
import './components.css';

const Navigation: React.FC = () => {
    return (
        <nav className="navigation">
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/directors">Directors</Link></li>
                <li><Link to="/divisions">Divisions</Link></li>
                <li><Link to="/membership">Membership</Link></li>
            </ul>
        </nav>
    );
};

export default Navigation;