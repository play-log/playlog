import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const Spinner = ({fullscreen}) => (
    <div className={`shared-spinner${fullscreen ? ' shared-spinner__fullscreen' : ''}`}>
        <div className="shared-spinner-dot"></div>
        <div className="shared-spinner-dot"></div>
        <div className="shared-spinner-dot"></div>
    </div>
);

Spinner.propTypes = {
    fullscreen: PropTypes.bool
};

Spinner.defaultProps = {
    fullscreen: false
};

export default Spinner;
