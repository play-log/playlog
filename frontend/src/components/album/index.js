import PropTypes from 'prop-types';
import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDateTime} from '../../utils';

import Chart from '../shared/chart';
import Error from '../shared/error';
import ProgressBar from '../shared/progress-bar';
import Spinner from '../shared/spinner';

import PlayIcon from '../../icons/play.svg';
import SunriseIcon from '../../icons/sunrise.svg';
import SunsetIcon from '../../icons/sunset.svg';

import './index.css';

const Track = ({data: {id, name, plays, playsPercent, firstPlay, lastPlay}}) => (
    <div className="album-tracks-item">
        <div className="album-tracks-item-data">
            <div className="album-tracks-item-data-name">
                <Link to={`/tracks/${id}`}>{name}</Link>
            </div>
            <div className="album-tracks-item-data-period">
                {firstPlay} &mdash; {lastPlay}
            </div>
        </div>
        <div className="album-tracks-item-bar">
            <ProgressBar percent={playsPercent}>
                {plays}
            </ProgressBar>
        </div>
    </div>
);

class Album extends React.Component {
    componentDidMount() {
        this.props.loadData(this.props.match.params.id);
    }
    render() {
        let data = this.props.data,
            result = null;
        if (!data.loaded) {
            result = <Spinner />;
        } else {
            if (data.success) {
                let {
                    artistId,
                    artistName,
                    name,
                    firstPlay,
                    lastPlay,
                    plays,
                    years,
                    tracks
                } = data.payload;
                result = (
                    <div className="album">
                        <div className="album-header">
                            <Link to={`/artists/${artistId}`}>{artistName}</Link>
                            <span> &mdash; </span>
                            <span>{name}</span>
                        </div>
                        <div className="album-panel">
                            <div className="album-panel-data">
                                <div className="album-panel-data-item">
                                    <img className="album-panel-data-item-icon" src={SunriseIcon} alt="" />
                                    <div className="album-panel-data-item-data">
                                        <div className="album-panel-data-item-data-label">First Play</div>
                                        <div className="album-panel-data-item-data-value">{firstPlay}</div>
                                    </div>
                                </div>
                                <div className="album-panel-data-item">
                                    <img className="album-panel-data-item-icon" src={SunsetIcon} alt="" />
                                    <div className="album-panel-data-item-data">
                                        <div className="album-panel-data-item-data-label">Last Play</div>
                                        <div className="album-panel-data-item-data-value">{lastPlay}</div>
                                    </div>
                                </div>
                                <div className="album-panel-data-item">
                                    <img className="album-panel-data-item-icon" src={PlayIcon} alt="" />
                                    <div  className="album-panel-data-item-data">
                                        <div className="album-panel-data-item-data-label">Total Plays</div>
                                        <div className="album-panel-data-item-data-value">{plays}</div>
                                    </div>
                                </div>
                            </div>
                            <div className="album-panel-chart">
                                <Chart type="line" data={years} height='130px' />
                            </div>
                        </div>
                        <div className="album-tracks">
                            {tracks.map(item => <Track key={item.id} data={item} />)}
                        </div>
                    </div>
                );
            } else {
                result = <Error />;
            }
        }
        return result;
    }
}

Album.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

const dataSelector = createSelector(
    state => state.album,
    data => {
        if (data.loaded && data.success) {
            let {firstPlay, lastPlay, years, tracks} = data.payload;

            data.payload.firstPlay = formatDateTime(firstPlay);
            data.payload.lastPlay = formatDateTime(lastPlay);

            data.payload.years = years.map(({year, plays}) => ({label: year.toString(), value: plays}));

            const maxPlays = Math.max(...tracks.map(item => item.plays));

            data.payload.tracks = tracks.map(({id, name, firstPlay, lastPlay, plays}) => ({
                id: id,
                name: name,
                firstPlay: formatDateTime(firstPlay),
                lastPlay: formatDateTime(lastPlay),
                plays: plays,
                playsPercent: Math.round(plays * 100 / maxPlays)
            }));
        }
        return data;
    }
);

export default connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.albumRequest, dispatch)})
)(Album);
