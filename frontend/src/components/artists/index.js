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

const ORDER_FIELDS = ['name', 'plays', 'first_play', 'last_play'];
const DEFAULT_ORDER_FIELD = 'name';
const ORDER_DIRECTIONS = ['asc', 'desc'];
const DEFAULT_ORDER_DIRECTION = 'asc';


const Item = ({id, name, plays, firstPlay, lastPlay, playsPercent}) => (
    <div className="artists-list-item">
        <div className="artists-list-item-data">
            <div className="artists-list-item-data-name">
                <Link to={`/artists/${id}`}>{name}</Link>
            </div>
            <div className="artists-list-item-data-period">{firstPlay} &mdash; {lastPlay}</div>
        </div>
        <div className="artists-list-item-bar">
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
                    <div className="artists-list">
                        {
                            data.payload.items.map(item =>
                                <Item key={item.name} {...item} />
                            )
                        }
                        <div className="artists-list-total">
                            {total} item{total !== 1 ? 's' : ''} found
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
    state => state.artists,
    data => {
        if (data.loaded && data.success) {
            const maxPlays = Math.max(...data.payload.items.map(item => item.plays));

            data.payload.items = data.payload.items.map(item => ({
                id: item.id,
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
    dispatch => ({loadData: bindActionCreators(actions.artistsRequest, dispatch)})
)(List);

class Artists extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: undefined,
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
        this.handleNameChange = val => this.setString('name', val);
        this.handleFirstPlayLtChange = val => this.setString('first_play_lt', val);
        this.handleFirstPlayGtChange = val => this.setString('first_play_gt', val);
        this.handleLastPlayLtChange = val => this.setString('last_play_lt', val);
        this.handleLastPlayGtChange = val => this.setString('last_play_gt', val);
        this.handleOrderFieldChange = order_field => this.setState({order_field});
        this.handleOrderDirectionChange = order_direction => this.setState({order_direction});
    }
    render() {
        return (
            <div className="artists-content">
                <div className="artists-content-item">
                    <div className="artists-query">
                        <SearchInput label="name" onChange={this.handleNameChange} />
                    </div>
                    <div className="artists-query">
                        <DateInput label="first play start" onChange={this.handleFirstPlayGtChange} />
                    </div>
                    <div className="artists-query">
                        <DateInput label="first play end" onChange={this.handleFirstPlayLtChange} />
                    </div>
                    <div className="artists-query">
                        <DateInput label="last play start" onChange={this.handleLastPlayGtChange} />
                    </div>
                    <div className="artists-query">
                        <DateInput label="last play end" onChange={this.handleLastPlayLtChange} />
                    </div>
                    <div className="artists-query">
                        <SwitchInput
                            label="Order"
                            onChange={this.handleOrderFieldChange}
                            options={ORDER_FIELDS}
                            initialValue={DEFAULT_ORDER_FIELD} />
                    </div>
                    <div className="artists-query">
                        <SwitchInput
                            label="Direction"
                            onChange={this.handleOrderDirectionChange}
                            options={ORDER_DIRECTIONS}
                            initialValue={DEFAULT_ORDER_DIRECTION} />
                    </div>
                </div>
                <div className="artists-content-item">
                    <ListContainer query={this.state} />
                </div>
            </div>
        );
    }
}

export default Artists;
