import moment from 'moment';
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
import Spinner from '../shared/spinner';

import PlayIcon from '../../icons/play.svg';
import SunriseIcon from '../../icons/sunrise.svg';
import SunsetIcon from '../../icons/sunset.svg';

import './index.css';

class Track extends React.Component {
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
                    albumId,
                    albumName,
                    name,
                    firstPlay,
                    lastPlay,
                    totalPlays,
                    plays,
                    years
                } = data.payload;
                result = (
                    <div className="track">
                        <div className="track-header">
                            <Link to={`/artists/${artistId}`}>{artistName}</Link>
                            <span> &mdash; </span>
                            <Link to={`/albums/${albumId}`}>{albumName}</Link>
                            <span> &mdash; </span>
                            <span>{name}</span>
                        </div>
                        <div className="track-panel">
                            <div className="track-panel-data">
                                <div className="track-panel-data-item">
                                    <img className="track-panel-data-item-icon" src={SunriseIcon} alt="" />
                                    <div className="track-panel-data-item-data">
                                        <div className="track-panel-data-item-data-label">First Play</div>
                                        <div className="track-panel-data-item-data-value">{firstPlay}</div>
                                    </div>
                                </div>
                                <div className="track-panel-data-item">
                                    <img className="track-panel-data-item-icon" src={SunsetIcon} alt="" />
                                    <div className="track-panel-data-item-data">
                                        <div className="track-panel-data-item-data-label">Last Play</div>
                                        <div className="track-panel-data-item-data-value">{lastPlay}</div>
                                    </div>
                                </div>
                                <div className="track-panel-data-item">
                                    <img className="track-panel-data-item-icon" src={PlayIcon} alt="" />
                                    <div className="track-panel-data-item-data">
                                        <div className="track-panel-data-item-data-label">Total Plays</div>
                                        <div className="track-panel-data-item-data-value">{totalPlays}</div>
                                    </div>
                                </div>
                            </div>
                            <div className="track-panel-chart">
                                <Chart type="line" data={years} height='130px' />
                            </div>
                        </div>
                        <div className="track-plays">
                            {Object.entries(plays).map(([year, items]) => (
                                <div key={year} className="track-plays-group">
                                    <div className="track-plays-group-header">{year}</div>
                                    <div className="track-plays-group-items">
                                        {items.map(item => (
                                            <div className="track-plays-group-items-item" key={item.unix}>
                                                <div className="track-plays-group-items-item-month">
                                                    {item.month}
                                                </div>
                                                <div className="track-plays-group-items-item-monthday">
                                                    {item.monthday}
                                                </div>
                                                <div className="track-plays-group-items-item-time">
                                                    {item.weekday}, {item.time}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            } else {
                result = <Error />
            }
        }
        return result;
    }
}

Track.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

const dataSelector = createSelector(
    state => state.track,
    data => {
        if (data.loaded && data.success) {
            let {firstPlay, lastPlay, years, plays} = data.payload;

            data.payload.firstPlay = formatDateTime(firstPlay);
            data.payload.lastPlay = formatDateTime(lastPlay);

            data.payload.years = years.map(({year, plays}) => ({label: year.toString(), value: plays}));

            let groupedPlays = {}
            plays.forEach(item => {
                const date = moment.utc(item.date).local();
                const year = date.year();
                if (!groupedPlays.hasOwnProperty(year)) {
                    groupedPlays[year] = []
                }
                groupedPlays[year].push({
                    unix: date.unix(),
                    month: date.format('MMM'),
                    monthday: date.format('DD'),
                    weekday: date.format('ddd'),
                    time: date.format('HH:mm')
                });
            });
            data.payload.plays = groupedPlays;
        }
        return data;
    }
);

export default connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.trackRequest, dispatch)})
)(Track);
