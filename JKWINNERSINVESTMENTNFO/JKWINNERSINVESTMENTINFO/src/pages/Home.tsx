import React from 'react';
import Header from '../components/Header';
import Navigation from '../components/Navigation';
import CompanyStructure from '../components/CompanyStructure';
import Divisions from '../components/Divisions';
import Governance from '../components/Governance';
import Members from '../components/Members';

const Home: React.FC = () => {
    return (
        <div>
            <Header />
            <Navigation />
            <CompanyStructure />
            <Divisions />
            <Governance />
            <Members />
        </div>
    );
};

export default Home;