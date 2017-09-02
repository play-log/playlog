import PropTypes from 'prop-types';
import React from 'react';
import {Link} from 'react-router-dom';

import './index.css';

const RecentTracks = ({data}) => {
    let result;

    if (data.length === 0) {
        result = <div className="overview-recent-tracks-empty">There are no items to display</div>;
    } else {
        result = data.map((group, idx) => (
            <div key={idx} className="overview-recent-tracks-group">
                <div className="overview-recent-tracks-group-title">{group.date}</div>
                <div className="overview-recent-tracks-group-list">{
                    group.items.map(({artist, album, track, time}, idx) => (
                        <div key={idx} className="overview-recent-tracks-group-list-item">
                            <span className="overview-recent-tracks-group-list-item-data">
                                <Link to={`/artists/${artist.id}`}>{artist.name}</Link>
                                <span> &mdash; </span>
                                <Link to={`/albums/${album.id}`}>{album.name}</Link>
                                <span> &mdash; </span>
                                <Link to={`/tracks/${track.id}`}>{track.name}</Link>
                            </span>
                            <span className="overview-recent-tracks-group-list-item-time">{time}</span>
                        </div>
                    ))
                }</div>
            </div>
        ));
    }

    return <div>{result}</div>;
};

RecentTracks.propTypes = {
    data: PropTypes.arrayOf(PropTypes.shape({
        date: PropTypes.string.isRequired,
        items: PropTypes.arrayOf(PropTypes.shape({
            artist: PropTypes.shape({
                id: PropTypes.number.isRequired,
                name: PropTypes.string.isRequired
            }).isRequired,
            album: PropTypes.shape({
                id: PropTypes.number.isRequired,
                name: PropTypes.string.isRequired
            }).isRequired,
            track: PropTypes.shape({
                id: PropTypes.number.isRequired,
                name: PropTypes.string.isRequired
            }).isRequired,
            time: PropTypes.string.isRequired
        }))
    })).isRequired
};

export default RecentTracks;
