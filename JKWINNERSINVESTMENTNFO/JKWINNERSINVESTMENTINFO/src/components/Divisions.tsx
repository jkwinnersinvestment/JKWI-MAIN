import React from 'react';
import { useEffect, useState } from 'react';
import divisionsData from '../data/divisions.json';

const Divisions: React.FC = () => {
    const [divisions, setDivisions] = useState([]);

    useEffect(() => {
        setDivisions(divisionsData);
    }, []);

    return (
        <div className="divisions-container">
            <h2>Our Divisions</h2>
            <div className="divisions-list">
                {divisions.map((division, index) => (
                    <div key={index} className="division-card">
                        <h3>{division.name}</h3>
                        <p>{division.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Divisions;