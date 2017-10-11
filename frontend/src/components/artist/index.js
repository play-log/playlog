import PropTypes from 'prop-types';
import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDateTime} from '../../utils';

import DateChart from '../shared/date-chart';
import Error from '../shared/error';
import ProgressBar from '../shared/progress-bar';
import Spinner from '../shared/spinner';

import PlayIcon from '../../icons/play.svg';
import SunriseIcon from '../../icons/sunrise.svg';
import SunsetIcon from '../../icons/sunset.svg';

import './index.css';

const Album = ({data: {id, name, plays, firstPlay, lastPlay, playsPercent}}) => (
    <div className="artist-albums-item">
        <div className="artist-albums-item-data">
            <div className="artist-albums-item-data-name">
                <Link to={`/albums/${id}`}>{name}</Link>
            </div>
            <div className="artist-albums-item-data-period">
                {firstPlay} &mdash; {lastPlay}
            </div>
        </div>
        <div className="artist-albums-item-bar">
            <ProgressBar percent={playsPercent}>
                {plays}
            </ProgressBar>
        </div>
    </div>
);

class Artist extends React.Component {
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
                    id,
                    name,
                    firstPlay,
                    lastPlay,
                    plays,
                    albums
                } = data.payload;

                result = (
                    <div className="artist">
                        <div className="artist-header">{name}</div>
                        <div className="artist-panel">
                            <div className="artist-panel-data">
                                <div className="artist-panel-data-item">
                                    <img className="artist-panel-data-item" src={SunriseIcon} alt="" />
                                    <div className="artist-panel-data-item-data">
                                        <div className="artist-panel-data-item-data-label">First Play</div>
                                        <div className="artist-panel-data-item-data-value">{firstPlay}</div>
                                    </div>
                                </div>
                                <div className="artist-panel-data-item">
                                    <img className="artist-panel-data-item-icon" src={SunsetIcon} alt="" />
                                    <div className="artist-panel-data-item-data">
                                        <div className="artist-panel-data-item-data-label">Last Play</div>
                                        <div className="artist-panel-data-item-data-value">{lastPlay}</div>
                                    </div>
                                </div>
                                <div className="artist-panel-data-item">
                                    <img className="artist-panel-data-item-icon" src={PlayIcon} alt="" />
                                    <div  className="artist-panel-data-item-data">
                                        <div className="artist-panel-data-item-data-label">Total Plays</div>
                                        <div className="artist-panel-data-item-data-value">{plays}</div>
                                    </div>
                                </div>
                            </div>
                            <div className="artist-panel-chart">
                                <DateChart filter={{kind: 'artist', value: id}} height="130px" type="line" />
                            </div>
                        </div>
                        <div className="artist-albums">
                            {albums.map(item => <Album key={item.id} data={item} />)}
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

Artist.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

const dataSelector = createSelector(
    state => state.artist,
    data => {
        if (data.loaded && data.success) {
            let {firstPlay, lastPlay, albums} = data.payload;

            data.payload.firstPlay = formatDateTime(firstPlay);
            data.payload.lastPlay = formatDateTime(lastPlay);

            const maxPlays = Math.max(...albums.map(item => item.plays));

            data.payload.albums = albums.map(({id, name, firstPlay, lastPlay, plays}) => ({
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
    dispatch => ({loadData: bindActionCreators(actions.artistRequest, dispatch)})
)(Artist);
