import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

class SwitchInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: this.props.initialValue};
        this.handleChange = this.handleChange.bind(this);
    }
    shouldComponentUpdate(nextProps, nextState) {
        return (
            nextProps.label !== this.props.label ||
            nextProps.options !== this.props.options ||
            nextState.value !== this.state.value
        );
    }
    render() {
        return (
            <div>
                <label className="shared-switch-input-label">{this.props.label}</label>
                {this.props.options.map(option => {
                    let className = 'shared-switch-input-option';
                    if (this.state.value === option) {
                        className += ' shared-switch-input-option__selected';
                    }

                    return <span {...{
                        children: option.replace('_', ' '),
                        className,
                        key: option,
                        onClick: () => this.handleChange(option)
                    }} />;
                })}
            </div>
        );
    }
    handleChange(value) {
        this.setState({value}, () => this.props.onChange(this.state.value));
    }
}

SwitchInput.propTypes = {
    initialValue: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    options: PropTypes.array.isRequired
};

export default SwitchInput;
