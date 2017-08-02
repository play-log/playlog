import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const Bar = () => (
    <div className="overview-nowplay-bar">
        <div className="overview-nowplay-bar-item"></div>
        <div className="overview-nowplay-bar-item"></div>
        <div className="overview-nowplay-bar-item"></div>
        <div className="overview-nowplay-bar-item"></div>
        <div className="overview-nowplay-bar-item"></div>
    </div>
);

const Nowplay = ({artist, album, title}) => (
    <div>
        <div className="overview-nowplay-header">Current Track</div>
        <div className="overview-nowplay-body">
            <div className="overview-nowplay-body-icon">
                <Bar />
            </div>
            <div className="overview-nowplay-body-track">
                {title}
            </div>
        </div>
        <div className="overview-nowplay-footer">From &laquo;{album}&raquo; of &laquo;{artist}&raquo;</div>
    </div>
);

Nowplay.propTypes = {
    artist: PropTypes.string.isRequired,
    album: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired
};

export default Nowplay;
