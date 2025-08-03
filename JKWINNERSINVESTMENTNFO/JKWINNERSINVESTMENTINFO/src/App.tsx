import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Directors from './pages/Directors';
import Divisions from './pages/Divisions';
import Membership from './pages/Membership';
import './styles/globals.css';

const App = () => {
    return (
        <Router>
            <Header />
            <Navigation />
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/directors" component={Directors} />
                <Route path="/divisions" component={Divisions} />
                <Route path="/membership" component={Membership} />
            </Switch>
        </Router>
    );
};

export default App;