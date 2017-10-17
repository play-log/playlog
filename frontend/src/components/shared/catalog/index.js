import PropTypes from 'prop-types';
import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux'

import DateInput from '../date-input';
import Error from '../error';
import {Pagination, FIRST_PAGE, INITIAL_OFFSET, LIMIT} from '../pagination';
import SearchInput from '../search-input';
import Spinner from '../spinner';
import SwitchInput from '../switch-input';

import './index.css';

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
                    <div>
                        {data.payload.items.map(this.props.renderItem)}
                        <div className="catalog-list-total">
                            {total} Item{total === 1 ? '' : 's'} Found
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
    loadData: PropTypes.func.isRequired,
    renderItem: PropTypes.func.isRequired
};

export const createListContainer = (selector, loader) => connect(
    state => ({data: selector(state)}),
    dispatch => ({loadData: bindActionCreators(loader, dispatch)})
)(List);

export class Catalog extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.createState(this.props);
        this.setString = (key, val) => {
            let newState = {};
            newState[key] = val.length > 0 ? val : undefined;
            this.setState(newState);
        };
    }
    render() {
        return (
            <div className="catalog">
                <div className="catalog-filters">
                    {this.props.filters.map(item => this.renderFilter(item))}
                </div>
                <div className="catalog-container">
                    {
                        React.createElement(this.props.container, {
                            query: this.state,
                            renderItem: this.props.renderItem
                        })
                    }
                </div>
            </div>
        );
    }
    renderFilter(data, nested=false) {
        let component,
            props = {},
            rootClassName = nested
                ? 'catalog-filters-item-control-group-item'
                : 'catalog-filters-item',
            labelClassName = nested
                ? 'catalog-filters-item-control-group-item-label'
                : 'catalog-filters-item-label';

        switch (data.type) {
            case 'group':
                if (nested) {
                    console.error('max nesting level exceeded (limit 1)', nested);
                    return null;
                }
                component = 'div';
                props.className = 'catalog-filters-item-control-group';
                props.children = data.items.map(item => this.renderFilter(item, true));
                break;
            case 'date':
                component = DateInput;
                props.onChange = value => this.setString(data.name, value);
                break;
            case 'search':
                component = SearchInput;
                props.onChange = value => this.setString(data.name, value);
                break;
            case 'switch':
                component = SwitchInput
                props.options = data.options;
                props.initialValue = data.initialValue;
                props.onChange = value => {
                    let newState = {};
                    newState[data.name] = value;
                    this.setState(newState);
                };
                break;
            default:
                throw new Error(`Unexpected filter type: ${data.type}`);
        }

        return <div key={data.name} className={rootClassName}>
            <label className={labelClassName}>{data.label}</label>
            {React.createElement(component, props)}
        </div>
    }
    createState(props) {
        let state = {};
        props.filters.forEach(item => {
            switch (item.type) {
                case 'group':
                    item.items.forEach(item => {
                        if (item.type === 'switch') {
                            state[item.name] = item.initialValue;
                        }
                    });
                    break;
                case 'switch':
                    state[item.name] = item.initialValue;
                    break;
                default:
                    // pass
                    break;
            }
        });
        return state;
    }
}

const SearchFilterType = PropTypes.shape({
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired
});


const DateFilterType = PropTypes.shape({
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired
});

const SwitchFilterType = PropTypes.shape({
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    options: PropTypes.arrayOf(PropTypes.string).isRequired,
    initialValue: PropTypes.string.isRequired
});

const GroupFilterType = PropTypes.shape({
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    items: PropTypes.arrayOf(
        PropTypes.oneOfType([
            SearchFilterType,
            DateFilterType,
            SwitchFilterType
        ])
    ).isRequired
});

Catalog.propTypes = {
    container: PropTypes.func.isRequired,
    filters: PropTypes.arrayOf(
        PropTypes.oneOfType([
            GroupFilterType,
            SearchFilterType,
            DateFilterType,
            SwitchFilterType
        ])
    ).isRequired,
    renderItem: PropTypes.func.isRequired
};
