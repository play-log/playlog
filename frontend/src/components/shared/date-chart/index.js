import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';
import {createSelector} from 'reselect';

import {actions} from '../../../redux';

import Chart from '../chart';
import Error from '../error';
import Spinner from '../spinner';

import './index.css';

const PERIOD_TYPE = {
    YEAR: 0,
    MONTH: 1,
    DAY: 2,
    HOUR: 3
};

class Period {
    constructor(type, date) {
        let queryFormat,
            displayFormat;

        switch (type) {
            case PERIOD_TYPE.YEAR:
                queryFormat = 'YYYY';
                displayFormat = 'YYYY';
                break;
            case PERIOD_TYPE.MONTH:
                queryFormat = 'YYYY-MM';
                displayFormat = 'MMM';
                break;
            case PERIOD_TYPE.DAY:
                queryFormat = 'YYYY-MM-DD';
                displayFormat = 'DD';
                break;
            case PERIOD_TYPE.HOUR:
            default:
                queryFormat = 'YYYY-MM-DD-HH';
                displayFormat = 'HH:00';
                break;
        }

        this.type = type;
        this.date = date;

        this.query = date.format(queryFormat);
        this.display = date.clone().local().format(displayFormat);
    }
    toString() {
        return this.display;
    }
}

class DateChart extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.createState(props);
        this.handleClick = period => this.props.onChange(period);
        this.reset = () => this.props.onChange(null);
    }
    componentWillReceiveProps(nextProps) {
        this.setState(this.createState(nextProps));
    }
    render() {
        let onClick;
        if (!this.props.period || this.props.period.type !== PERIOD_TYPE.DAY) {
            onClick = this.handleClick;
        }
        return <div className="shared-date-chart">
            {this.renderHeader()}
            <Chart
                data={this.state.data}
                height={this.props.height}
                onClick={onClick}
                type={this.props.type} />
        </div>
    }
    renderHeader() {
        if (!this.props.period) {
            return null;
        }

        return <div className="shared-date-chart-header">
            <span className="shared-date-chart-header-breadcrumbs">
                {this.renderBreadcrumb(PERIOD_TYPE.YEAR)}
                {this.renderBreadcrumb(PERIOD_TYPE.MONTH)}
                {this.renderBreadcrumb(PERIOD_TYPE.DAY)}
            </span>
            <span className="shared-date-chart-header-reset" onClick={this.reset}>&#x2716;</span>
        </div>;
    }
    renderBreadcrumb(type) {
        let period = this.props.period,
            baseClassName = 'shared-date-chart-header-breadcrumbs-item',
            className = baseClassName,
            dateFormat,
            hasDelimiter,
            isClickable,
            onClick;

        switch (type) {
            case PERIOD_TYPE.YEAR:
                dateFormat = 'YYYY';
                hasDelimiter = false;
                isClickable = period.type !== PERIOD_TYPE.YEAR;
                break;
            case PERIOD_TYPE.MONTH:
                if (period.type === PERIOD_TYPE.YEAR) {
                    return null;
                }
                dateFormat = 'MMMM';
                hasDelimiter = true;
                isClickable = period.type === PERIOD_TYPE.DAY;
                break;
            case PERIOD_TYPE.DAY:
                if (period.type !== PERIOD_TYPE.DAY) {
                    return null;
                }
                dateFormat = 'DD';
                hasDelimiter = true;
                isClickable = false;
                break;
            default:
                return null;
        }

        if (isClickable) {
            onClick = () => this.props.onChange(new Period(type, period.date));
            className += ` ${className}__link`;
        }

        return [
            hasDelimiter && <span key="breadcrumb-delimiter" className={baseClassName}> / </span>,
            <span key="breadcrumb" className={className} onClick={onClick}>
                {period.date.format(dateFormat)}
            </span>
        ];
    }
    createState(props) {
        let periodType;

        if (props.period) {
            switch (props.period.type) {
                case PERIOD_TYPE.YEAR:
                    periodType = PERIOD_TYPE.MONTH;
                    break;
                case PERIOD_TYPE.MONTH:
                    periodType = PERIOD_TYPE.DAY;
                    break;
                case PERIOD_TYPE.DAY:
                default:
                    periodType = PERIOD_TYPE.HOUR;
                    break;
            }
        } else {
            periodType = PERIOD_TYPE.YEAR;
        }

        return {
            data: props.data.map(({date, value}) => ({
                label: new Period(periodType, date),
                value: value
            }))
        };
    }
}

DateChart.propTypes = {
    data: PropTypes.array.isRequired,
    height: PropTypes.string,
    onChange: PropTypes.func.isRequired,
    period: PropTypes.object,
    type: PropTypes.string
};


class DateChartContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {period: null};
        this.loadData = period => this.props.loadData({
            period: period ? period.query : undefined,
            filter_kind: this.props.filter ? this.props.filter.kind : undefined,
            filter_value: this.props.filter ? this.props.filter.value : undefined
        });
        this.handlePeriodChange = period => {
            this.setState({period});
            this.loadData(period);
        };
    }
    componentDidMount() {
        this.loadData();
    }
    render() {
        let data = this.props.data,
            result = null;
        if (!data.loaded) {
            result = <Spinner />;
        } else {
            if (data.success) {
                result = <DateChart
                    data={data.payload}
                    height={this.props.height}
                    onChange={this.handlePeriodChange}
                    period={this.state.period}
                    type={this.props.type} />;
            } else {
                result = <Error />;
            }
        }
        return result;
    }
}

DateChartContainer.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired,
    filter: PropTypes.shape({
        kind: PropTypes.oneOf(['artist', 'album', 'track']).isRequired,
        value: PropTypes.number.isRequired
    }),
    height: PropTypes.string,
    type: PropTypes.string
};

const dataSelector = createSelector(
    state => state.playsCount,
    data => {
        if (data.loaded && data.success) {
            data.payload = data.payload.map(item => ({
                date: moment.utc(item.label),
                value: item.value
            }));
        }
        return data;
    }
);

export default connect(
    state => ({data: dataSelector(state)}),
    dispatch => ({loadData: bindActionCreators(actions.playsCountRequest, dispatch)})
)(DateChartContainer);
