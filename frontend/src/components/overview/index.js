import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {DATE_FORMAT, formatDate} from '../../utils';

import AlbumIcon from '../../icons/album.svg';
import ArtistIcon from '../../icons/artist.svg';
import CalendarIcon from '../../icons/calendar.svg';
import PlayIcon from '../../icons/play.svg';
import TrackIcon from '../../icons/track.svg';

import DateChart from '../shared/date-chart';
import Error from '../shared/error';
import Spinner from '../shared/spinner';

import Counters from './counters';
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
    user
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
            {
                currentStreak && <div className="overview-sidebar-item">
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
            }
            {
                longestStreak && <div className="overview-sidebar-item">
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
            }
            {
                biggestDay && <div className="overview-sidebar-item">
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
            }
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
                    <div style={{padding: '5px 0'}}>
                        <DateChart height="190px" />
                    </div>
                </div>
            </div>
            <div className="overview-content-header">Recent Tracks</div>
            <div className="overview-content-row">
                <RecentTracks data={recentTracks} />
            </div>
        </div>
    </div>
);

Overview.propTypes = {
    biggestDay: PropTypes.object,
    counters: PropTypes.object.isRequired,
    currentStreak: PropTypes.object,
    longestStreak: PropTypes.object,
    nowplay: PropTypes.object,
    recentTracks: PropTypes.array.isRequired,
    recentlyAdded: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired
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

function groupTracks(items) {
    const result = {};

    items.forEach(item => {
        const date = moment.utc(item.date).local();
        const key = date.clone().startOf('day').unix();
        if (!result.hasOwnProperty(key)) {
            result[key] = {date: date.format(DATE_FORMAT), items: []};
        }
        result[key].items.push({
            artist: {
                id: item.artistId,
                name: item.artist
            },
            album: {
                id: item.albumId,
                name: item.album
            },
            track: {
                id: item.trackId,
                name: item.track
            },
            time: date.format('HH:mm')
        });
    });

    return Object.keys(result).sort().reverse().map(key => result[key]);
}

const dataSelector = createSelector(
    state => state.overview,
    data => {
        if (data.loaded && data.success) {
            let {
                biggestDay,
                currentStreak,
                longestStreak,
                recentTracks,
                recentlyAdded
            } = data.payload;

            [currentStreak, longestStreak, recentlyAdded].forEach(item => {
                if (item) {
                    const startDate = formatDate(item.startDate);
                    const endDate = formatDate(item.endDate);
                    item.period = `${startDate} — ${endDate}`;
                }
            });

            if (biggestDay) {
                biggestDay.day = formatDate(biggestDay.day);
            }

            data.payload.recentTracks = groupTracks(recentTracks);
        }
        return data;
    }
);

export default connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.overviewRequest, dispatch)})
)(OverviewContainer);
