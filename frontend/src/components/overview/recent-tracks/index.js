import PropTypes from 'prop-types';
import React from 'react';

import Plays from '../../shared/plays';

import './index.css';

const RecentTracks = ({data}) => (
    <div>
        <div className="overview-recent-tracks-header">Recent Tracks</div>
        <Plays data={data} />
    </div>
);

RecentTracks.propTypes = {
    data: PropTypes.array.isRequired
};

export default RecentTracks;
