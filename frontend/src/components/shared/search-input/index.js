import debounce from 'lodash.debounce';
import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

class SearchInput extends React.Component {
    constructor(props) {
        super(props);
        this.onChange = debounce(this.props.onChange, this.props.delay);
        this.handleChange = this.handleChange.bind(this);
    }
    shouldComponentUpdate() {
        return false;
    }
    render() {
        return (
            <div>
                <label className="shared-search-input-label">{this.props.label}:</label>
                <input
                    className="shared-search-input-field"
                    type="text"
                    onChange={this.handleChange} />
            </div>
        );
    }
    handleChange(event) {
        this.onChange(event.target.value);
    }
}

SearchInput.propTypes = {
    delay: PropTypes.number,
    label: PropTypes.string,
    onChange: PropTypes.func.isRequired
}

SearchInput.defaultProps = {
    delay: 500,
    label: 'Search'
};

export default SearchInput;
