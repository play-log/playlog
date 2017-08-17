import PropTypes from 'prop-types';
import React from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDate, groupTracks} from '../../utils';

import AlbumIcon from '../../icons/album.svg';
import ArtistIcon from '../../icons/artist.svg';
import CalendarIcon from '../../icons/calendar.svg';
import PlayIcon from '../../icons/play.svg';
import TrackIcon from '../../icons/track.svg';

import Error from '../shared/error';
import Spinner from '../shared/spinner';

import Counters from './counters';
import DateChart from './date-chart';
import Navigation from './navigation';
import Nowplay from './nowplay';
import RecentTracks from './recent-tracks';
import User from './user';

import './index.css';

const Overview = ({
    biggestDay,
    counters,
    currentStreak,
    longestStreak,
    nowplay,
    recentTracks,
    recentlyAdded,
    user,
    years
}) => (
    <div className="overview">
        <div className="overview-sidebar">
            <div className="overview-sidebar-item">
                <User {...user} />
            </div>
            {
                nowplay &&
                    <div className="overview-sidebar-item">
                        <Nowplay {...nowplay} />
                    </div>
            }
            <div className="overview-sidebar-item">
                <Counters {...{
                    header: 'Current Streak',
                    data: [
                        {
                            icon: CalendarIcon,
                            label: 'days',
                            value: currentStreak.days
                        },
                        {
                            icon: PlayIcon,
                            label: 'plays',
                            value: currentStreak.plays
                        }
                    ],
                    footer: currentStreak.period
                }} />
            </div>
            <div className="overview-sidebar-item">
                <Counters {...{
                    header: 'Longest Streak',
                    data: [
                        {
                            icon: CalendarIcon,
                            label: 'days',
                            value: longestStreak.days
                        },
                        {
                            icon: PlayIcon,
                            label: 'plays',
                            value: longestStreak.plays
                        }
                    ],
                    footer: longestStreak.period
                }} />
            </div>
            <div className="overview-sidebar-item">
                <Counters {...{
                    header: 'Biggest Day',
                    data: [
                        {
                            icon: PlayIcon,
                            label: 'plays',
                            value: biggestDay.plays
                        }
                    ],
                    footer: biggestDay.day
                }} />
            </div>
            <div className="overview-sidebar-item">
                <Counters {...{
                    header: 'Recently Added',
                    data: [
                        {
                            icon: ArtistIcon,
                            label: 'artists',
                            value: recentlyAdded.artists
                        },
                        {
                            icon: AlbumIcon,
                            label: 'albums',
                            value: recentlyAdded.albums
                        },
                        {
                            icon: TrackIcon,
                            label: 'tracks',
                            value: recentlyAdded.tracks
                        }
                    ],
                    footer: recentlyAdded.period
                }} />
            </div>
        </div>
        <div className="overview-content">
            <div className="overview-content-header">Overview</div>
            <div className="overview-content-row">
                <div className="overview-content-row-col overview-content-row-col__one-fourth">
                    <Navigation counters={counters} />
                </div>
                <div className="overview-content-row-col overview-content-row-col__three-fourths">
                    <DateChart data={years} />
                </div>
            </div>
            <div className="overview-content-row">
                <RecentTracks data={recentTracks} />
            </div>
        </div>
    </div>
);

Overview.propTypes = {
    biggestDay: PropTypes.object.isRequired,
    counters: PropTypes.object.isRequired,
    currentStreak: PropTypes.object.isRequired,
    longestStreak: PropTypes.object.isRequired,
    nowplay: PropTypes.object,
    recentTracks: PropTypes.array.isRequired,
    recentlyAdded: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired,
    years: PropTypes.array.isRequired
};

class OverviewContainer extends React.Component {
    componentDidMount() {
        if (!this.props.data.loaded) {
            this.props.loadData();
        }
    }
    render() {
        let data = this.props.data,
            result = null;
        if (!data.loaded) {
            result = <Spinner fullscreen={true} />;
        } else {
            if (data.success) {
                result = <Overview {...data.payload} />;
            } else {
                result = <Error />;
            }
        }
        return result;
    }
}

OverviewContainer.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

const dataSelector = createSelector(
    state => state.overview,
    data => {
        if (data.loaded && data.success) {
            let {
                biggestDay,
                currentStreak,
                longestStreak,
                recentTracks,
                recentlyAdded,
                years
            } = data.payload;

            [currentStreak, longestStreak, recentlyAdded].forEach(item => {
                const startDate = formatDate(item.startDate);
                const endDate = formatDate(item.endDate);
                item.period = `${startDate} — ${endDate}`;
            });

            biggestDay.day = formatDate(biggestDay.day);

            data.payload.recentTracks = groupTracks(recentTracks);

            data.payload.years = years.map(item => ({
                label: item.year.toString(),
                value: item.plays
            }));
        }
        return data;
    }
);

export default connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.overviewRequest, dispatch)})
)(OverviewContainer);
