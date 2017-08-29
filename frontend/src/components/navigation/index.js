import PropTypes from 'prop-types';
import React from 'react';
import {NavLink} from 'react-router-dom';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';

import {actions} from '../../redux';

import './index.css';

const Counter = ({value}) => <span className="navigation-counter">{value}</span>;

Counter.propTypes = {
    value: PropTypes.number.isRequired
};

const Link = ({children, to, counter}) => {
    if (counter) {
        children = <span>{children} <Counter value={counter} /></span>;
    }

    let props = {
        activeClassName: 'navigation-link__active',
        children: children,
        className: 'navigation-link',
        exact: true,
        to: to
    };

    return <NavLink {...props} />;
};

Link.propTypes = {
    children: PropTypes.node.isRequired,
    to: PropTypes.string.isRequired,
    counter: PropTypes.number
};

const Navigation = ({counters}) => (
    <div className="navigation">
        <Link to="/">Overview</Link>
        <Link to="/artists" counter={counters.artists}>Artists</Link>
        <Link to="/albums" counter={counters.albums}>Albums</Link>
        <Link to="/tracks" counter={counters.tracks}>Tracks</Link>
        <Link to="/plays" counter={counters.plays}>Plays</Link>
    </div>
);

Navigation.propTypes = {
    counters: PropTypes.object.isRequired
};

class NavigationContainer extends React.Component {
    componentDidMount() {
        if (!this.props.data.loaded) {
            this.props.loadData();
        }
    }
    render() {
        const data = this.props.data;
        const counters = data.loaded && data.success ? data.payload : {};
        return <Navigation counters={counters} />;
    }
}

export default connect(
    state => ({data: state.counters}),
    dispatch => ({loadData: bindActionCreators(actions.countersRequest, dispatch)})
)(NavigationContainer);
