import PropTypes from 'prop-types';
import React from 'react';
import {BrowserRouter, NavLink, Route, Switch} from 'react-router-dom';

import NotFound from './components/not-found';
import Overview from './components/overview';

import './app.css';

const Link = ({children, to}) => {
    let props = {
        activeClassName: 'app-navigation-link__active',
        children: children,
        className: 'app-navigation-link',
        exact: true,
        to: to
    };

    return <NavLink {...props} />;
};

Link.propTypes = {
    children: PropTypes.node.isRequired,
    to: PropTypes.string.isRequired
};

const Counter = ({value}) => <span className="app-navigation-counter">{value}</span>;

Counter.propTypes = {
    value: PropTypes.string.isRequired
};

const Navigation = () => (
    <div className="app-navigation">
        <Link to="/">Overview</Link>
        <Link to="/artists">Artists <Counter value="311" /></Link>
        <Link to="/albums">Albums <Counter value="927" /></Link>
        <Link to="/tracks">Tracks <Counter value="6787" /></Link>
        <Link to="/plays">Plays <Counter value="53428" /></Link>
        <Link to="/favorites">Favorites <Counter value="200" /></Link>
    </div>
);

class App extends React.Component {
    render() {
        return (
            <div>
                <BrowserRouter>
                    <div>
                        <Route path="/:path" component={Navigation} />
                        <Switch>
                            <Route exact path="/" component={Overview} />
                            <Route component={NotFound}/>
                        </Switch>
                    </div>
                </BrowserRouter>
                <div className="app-footer">
                    Development and support &mdash; Ross Nomann, 2017
                </div>
            </div>
        );
    }
}

export default App;
