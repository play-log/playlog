import PropTypes from 'prop-types';
import React from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {bindActionCreators} from 'redux'
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDate} from '../../utils';

import DateInput from '../shared/date-input';
import Error from '../shared/error';
import {Pagination, FIRST_PAGE, INITIAL_OFFSET, LIMIT} from '../shared/pagination';
import ProgressBar from '../shared/progress-bar';
import SearchInput from '../shared/search-input';
import Spinner from '../shared/spinner';
import SwitchInput from '../shared/switch-input';

import './index.css';

const ORDER_FIELDS = ['artist_name', 'album_name', 'plays', 'first_play', 'last_play'];
const DEFAULT_ORDER_FIELD = 'artist_name';
const ORDER_DIRECTIONS = ['asc', 'desc'];
const DEFAULT_ORDER_DIRECTION = 'asc';


const Item = ({id, artist, name, plays, firstPlay, lastPlay, playsPercent}) => (
    <div className="albums-list-item">
        <div className="albums-list-item-data">
            <div className="albums-list-item-data-name">
                <Link to={`/artists/${artist.id}`}>{artist.name}</Link>
                <span> &mdash; </span>
                <Link to={`/albums/${id}`}>{name}</Link>
            </div>
            <div className="albums-list-item-data-period">{firstPlay} &mdash; {lastPlay}</div>
        </div>
        <div className="albums-list-item-bar">
            <ProgressBar percent={playsPercent}>
                {plays}
            </ProgressBar>
        </div>
    </div>
);

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
                    <div className="albums-list">
                        {
                            data.payload.items.map(item =>
                                <Item key={item.id} {...item} />
                            )
                        }
                        <div className="albums-list-total">
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
    state => state.albums,
    data => {
        if (data.loaded && data.success) {
            const maxPlays = Math.max(...data.payload.items.map(item => item.plays));

            data.payload.items = data.payload.items.map(item => ({
                id: item.id,
                artist: {
                    id: item.artistId,
                    name: item.artist
                },
                name: item.name,
                plays: item.plays,
                firstPlay: formatDate(item.firstPlay),
                lastPlay: formatDate(item.lastPlay),
                playsPercent: Math.round(item.plays * 100 / maxPlays)
            }));
        }
        return data;
    }
);

const ListContainer = connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.albumsRequest, dispatch)})
)(List);

class Albums extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            artist_name: undefined,
            album_name: undefined,
            first_play_lt: undefined,
            first_play_gt: undefined,
            last_play_lt: undefined,
            last_play_gt: undefined,
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
        this.handleFirstPlayLtChange = val => this.setString('first_play_lt', val);
        this.handleFirstPlayGtChange = val => this.setString('first_play_gt', val);
        this.handleLastPlayLtChange = val => this.setString('last_play_lt', val);
        this.handleLastPlayGtChange = val => this.setString('last_play_gt', val);
        this.handleOrderFieldChange = order_field => this.setState({order_field});
        this.handleOrderDirectionChange = order_direction => this.setState({order_direction});
    }
    render() {
        return (
            <div className="albums-content">
                <div className="albums-content-item">
                    <div className="albums-query">
                        <label className="albums-query-label">ARTIST</label>
                        <SearchInput onChange={this.handleArtistNameChange} />
                    </div>
                    <div className="albums-query">
                        <label className="albums-query-label">TITLE</label>
                        <SearchInput onChange={this.handleAlbumNameChange} />
                    </div>
                    <div className="albums-query">
                        <label className="albums-query-label">FIRST PLAY</label>
                        <div className="albums-query-control-group">
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
                                    SINCE
                                </label>
                                <DateInput onChange={this.handleFirstPlayGtChange} />
                            </div>
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
                                    UNTIL
                                </label>
                                <DateInput onChange={this.handleFirstPlayLtChange} />
                            </div>
                        </div>
                    </div>
                    <div className="albums-query">
                        <label className="albums-query-label">LAST PLAY</label>
                        <div className="albums-query-control-group">
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
                                    SINCE
                                </label>
                                <DateInput onChange={this.handleLastPlayGtChange} />
                            </div>
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
                                    UNTIL
                                </label>
                                <DateInput onChange={this.handleLastPlayLtChange} />
                            </div>
                        </div>
                    </div>
                    <div className="albums-query">
                        <label className="albums-query-label">ORDER</label>
                        <div className="albums-query-control-group">
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
                                    FIELD
                                </label>
                                <SwitchInput
                                    onChange={this.handleOrderFieldChange}
                                    options={ORDER_FIELDS}
                                    initialValue={DEFAULT_ORDER_FIELD} />
                            </div>
                            <div className="albums-query-control-group-item">
                                <label className="albums-query-control-group-item-label">
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
                <div className="albums-content-item">
                    <ListContainer query={this.state} />
                </div>
            </div>
        );
    }
}

export default Albums;
