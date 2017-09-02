import PropTypes from 'prop-types';
import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux'
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDateTime} from '../../utils';

import DateInput from '../shared/date-input';
import Error from '../shared/error';
import {Pagination, FIRST_PAGE, INITIAL_OFFSET, LIMIT} from '../shared/pagination';
import SearchInput from '../shared/search-input';
import Spinner from '../shared/spinner';
import SwitchInput from '../shared/switch-input';

import './index.css';

const ORDER_FIELDS = ['artist_name', 'album_name', 'track_name', 'date'];
const DEFAULT_ORDER_FIELD = 'date';
const ORDER_DIRECTIONS = ['asc', 'desc'];
const DEFAULT_ORDER_DIRECTION = 'desc';


class List extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            page: FIRST_PAGE,
            offset: INITIAL_OFFSET
        };
        this.loadData = this.loadData.bind(this);
        this.handlePageChange = this.handlePageChange.bind(this);
    }
    componentDidMount() {
        this.loadData(this.props.query);
    }
    componentWillReceiveProps(nextProps) {
        if (nextProps.query !== this.props.query) {
            this.setState({page: FIRST_PAGE, offset: INITIAL_OFFSET}, () => {
                this.loadData(nextProps.query);
            })
        }
    }
    render() {
        let data = this.props.data,
            result = null;

        if (!data.loaded) {
            result = <Spinner />;
        } else {
            if (data.success) {
                const total = data.payload.total;

                result = (
                    <div className="plays-list">
                        <div className="plays-list-data">{
                            data.payload.items.map(({artist, album, track, date, rawDate}) =>
                                <div key={rawDate} className="plays-list-data-item">
                                    <span className="plays-list-data-item-name" title={
                                        `${artist.name} - ${album.name} - ${track.name}`
                                    }>
                                        <Link to={`/artists/${artist.id}`}>{artist.name}</Link>
                                        <span> &mdash; </span>
                                        <Link to={`/albums/${album.id}`}>{album.name}</Link>
                                        <span> &mdash; </span>
                                        <Link to={`/tracks/${track.id}`}>{track.name}</Link>
                                    </span>
                                    <span className="plays-list-data-item-date">{date}</span>
                                </div>
                            )
                        }</div>
                        <div className="plays-list-total">
                            {total} Item{total !== 1 ? 's' : ''} Found
                        </div>
                        <Pagination
                            currentPage={this.state.page}
                            onChange={this.handlePageChange}
                            totalItems={data.payload.total} />
                    </div>
                );
            } else {
                result = <Error />;
            }
        }
        return result;
    }
    handlePageChange(page, offset) {
        this.setState({page, offset}, () => this.loadData(this.props.query));
    }
    loadData(query) {
        this.props.loadData({
            offset: this.state.offset,
            limit: LIMIT,
            ...query
        });
    }
}

List.propTypes = {
    data: PropTypes.object.isRequired,
    query: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
};

const dataSelector = createSelector(
    state => state.plays,
    data => {
        if (data.loaded && data.success) {
            data.payload.items = data.payload.items.map(item => ({
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
                date: formatDateTime(item.date),
                rawDate: item.date
            }));
        }
        return data;
    }
);

const ListContainer = connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.playsRequest, dispatch)})
)(List);


class Plays extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            artist_name: undefined,
            album_name: undefined,
            track_name: undefined,
            date_lt: undefined,
            date_gt: undefined,
            order_field: DEFAULT_ORDER_FIELD,
            order_direction: DEFAULT_ORDER_DIRECTION
        };
        this.setString = (key, val) => {
            let newState = {};
            newState[key] = val.length > 0 ? val : undefined;
            this.setState(newState);
        };
        this.handleArtistNameChange = val => this.setString('artist_name', val);
        this.handleAlbumNameChange = val => this.setString('album_name', val);
        this.handleTrackNameChange = val => this.setString('track_name', val);
        this.handleDateLtChange = val => this.setString('date_lt', val);
        this.handleDateGtChange = val => this.setString('date_gt', val);
        this.handleOrderFieldChange = order_field => this.setState({order_field});
        this.handleOrderDirectionChange = order_direction => this.setState({order_direction});
    }
    render() {
        return (
            <div className="plays-content">
                <div className="plays-content-item">
                    <div className="plays-query">
                        <label className="plays-query-label">ARTIST</label>
                        <SearchInput onChange={this.handleArtistNameChange} />
                    </div>
                    <div className="plays-query">
                        <label className="plays-query-label">ALBUM</label>
                        <SearchInput onChange={this.handleAlbumNameChange} />
                    </div>
                    <div className="plays-query">
                        <label className="plays-query-label">TRACK</label>
                        <SearchInput onChange={this.handleTrackNameChange} />
                    </div>
                    <div className="plays-query">
                        <label className="plays-query-label">DATE</label>
                        <div className="plays-query-control-group">
                            <div className="plays-query-control-group-item">
                                <label className="plays-query-control-group-item-label">
                                    SINCE
                                </label>
                                <DateInput onChange={this.handleDateGtChange} />
                            </div>
                            <div className="plays-query-control-group-item">
                                <label className="plays-query-control-group-item-label">
                                    UNTIL
                                </label>
                                <DateInput onChange={this.handleDateLtChange} />
                            </div>
                        </div>
                    </div>
                    <div className="plays-query">
                        <label className="plays-query-label">ORDER</label>
                        <div className="plays-query-control-group">
                            <div className="plays-query-control-group-item">
                                <label className="plays-query-control-group-item-label">
                                    FIELD
                                </label>
                                <SwitchInput
                                    onChange={this.handleOrderFieldChange}
                                    options={ORDER_FIELDS}
                                    initialValue={DEFAULT_ORDER_FIELD} />
                            </div>
                            <div className="plays-query-control-group-item">
                                <label className="plays-query-control-group-item-label">
                                    DIRECTION
                                </label>
                                <SwitchInput
                                    onChange={this.handleOrderDirectionChange}
                                    options={ORDER_DIRECTIONS}
                                    initialValue={DEFAULT_ORDER_DIRECTION} />
                            </div>
                        </div>
                    </div>
                </div>
                <div className="plays-content-item">
                    <ListContainer query={this.state} />
                </div>
            </div>
        );
    }
}

export default Plays;
