import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const DATE_FORMAT = 'DD.MM.YYYY';
const DATETIME_REGEX = /^[\d]{2}\.[\d]{2}\.[\d]{4}$/;

class DateInput extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.state = {
            dateString: '',
            dateObject: null
        };
    }
    shouldComponentUpdate(nextProps, nextState) {
        return (
            nextProps.label !== this.props.label ||
            nextState.dateString !== this.state.dateString ||
            nextState.dateObject !== this.state.dateObject
        )
    }
    render() {
        let {dateString, dateObject} = this.state,
            {label} = this.props,
            hasError = dateString.length > 0 && dateObject === null;

        return (
            <div>
                <label className="shared-date-input-label">{label}:</label>
                <input
                    className={`shared-date-input-field${!hasError ? '' : ' shared-date-input-field__error'}`}
                    type="text"
                    placeholder={DATE_FORMAT}
                    onChange={this.handleChange}
                    value={dateString} />
            </div>
        );
    }
    handleChange(event) {
        let dateString = event.target.value,
            dateObject = null;
        if (dateString.length > 0 && DATETIME_REGEX.test(dateString)) {
            dateObject = moment(dateString, DATE_FORMAT);
            if (!dateObject.isValid()) {
                dateObject = null;
            } else {
                dateObject = dateObject.utc();
            }
        }
        this.setState({dateString, dateObject}, () => {
            if (this.state.dateObject) {
                this.props.onChange(this.state.dateObject.format('YYYY-MM-DD'));
            } else if (this.state.dateString.length === 0) {
                this.props.onChange('');
            }
        });
    }
}

DateInput.propTypes = {
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired
}

export default DateInput;
