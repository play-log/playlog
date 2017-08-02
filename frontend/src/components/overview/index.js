import PropTypes from 'prop-types';
import React from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';

import {actions} from '../../redux';

import AlbumIcon from '../../icons/album.svg';
import ArtistIcon from '../../icons/artist.svg';
import CalendarIcon from '../../icons/calendar.svg';
import PlayIcon from '../../icons/play.svg';
import TrackIcon from '../../icons/track.svg';

import Counters from './counters';
import DateChart from './date-chart';
import Navigation from './navigation';
import Nowplay from './nowplay';
import RecentTracks from './recent-tracks';
import User from './user';

import './index.css';

const Overview = ({
    data: {
        biggestDay,
        counters,
        currentStreak,
        longestStreak,
        nowplay,
        recentTracks,
        recentlyAdded,
        user,
        years
    }
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
                    footer: `${currentStreak.startDate} — ${currentStreak.endDate}`
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
                    footer: `${longestStreak.startDate} — ${longestStreak.endDate}`
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
                    footer: biggestDay.date
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
                    footer: `${recentlyAdded.startDate} — ${recentlyAdded.endDate}`
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
    data: PropTypes.object.isRequired // TODO: shape
};


class OverviewContainer extends React.Component {
    componentDidMount() {
        this.props.loadData();
    }
    render() {
        let data = this.props.data,
            result = null;
        if (!data.loaded) {
            // TODO: styles
            result = <div>LOADING...</div>;
        } else {
            if (data.success) {
                result = <Overview data={data.payload} />;
            } else {
                // TODO: styles
                console.log('FAILED', data.payload);
                result = <div>FAILED</div>;
            }
        }
        return result;
    }
}

OverviewContainer.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

export default connect(
    state => ({data: state.overview}),
    dispatch => ({loadData: bindActionCreators(actions.overviewRequest, dispatch)})
)(OverviewContainer);
