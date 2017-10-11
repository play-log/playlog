import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux';
import {createSelector} from 'reselect';

import {actions} from '../../../redux';

import Chart from '../../shared/chart';
import Error from '../../shared/error';
import Spinner from '../../shared/spinner';

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
        return <div className="overview-date-chart">
            {this.renderHeader()}
            <Chart data={this.state.data} height='190px' onClick={onClick} />
        </div>
    }
    renderHeader() {
        if (!this.props.period) {
            return null;
        }

        return <div className="overview-date-chart-header">
            <span className="overview-date-chart-header-breadcrumbs">
                {this.renderBreadcrumb(PERIOD_TYPE.YEAR)}
                {this.renderBreadcrumb(PERIOD_TYPE.MONTH)}
                {this.renderBreadcrumb(PERIOD_TYPE.DAY)}
            </span>
            <span className="overview-date-chart-header-reset" onClick={this.reset}>&#x2716;</span>
        </div>;
    }
    renderBreadcrumb(type) {
        let period = this.props.period,
            baseClassName = 'overview-date-chart-header-breadcrumbs-item',
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
    onChange: PropTypes.func.isRequired,
    period: PropTypes.object
};


class DateChartContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {period: null};
        this.handlePeriodChange = this.handlePeriodChange.bind(this);
    }
    componentDidMount() {
        this.props.loadData();
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
                    onChange={this.handlePeriodChange}
                    period={this.state.period} />;
            } else {
                result = <Error />;
            }
        }
        return result;
    }
    handlePeriodChange(period) {
        this.setState({period});
        this.props.loadData({period: period ? period.query : undefined});
    }
}

DateChartContainer.propTypes = {
    data: PropTypes.object.isRequired,
    loadData: PropTypes.func.isRequired
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
