import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const ProgressBar = ({children, percent}) => {
    let value = children !== null
        ? <div className="shared-progress-bar-label-value">{children}</div>
        : null;
    return (
        <div className={`shared-progress-bar${value === null ? ' shared-progress-bar__small' : ''}`}>
            <div className="shared-progress-bar-label" style={{width: percent + '%'}}>{value}</div>
        </div>
    );
};

ProgressBar.propTypes = {
    children: PropTypes.node,
    percent: PropTypes.number.isRequired
};

ProgressBar.defaultProps = {
    children: null
};

export default ProgressBar;
