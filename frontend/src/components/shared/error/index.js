import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const Error = ({message}) => (
    <div className="shared-error">{message}</div>
);

Error.propTypes = {
    message: PropTypes.string
};

Error.defaultProps = {
    message: 'An error has occurred'
};

export default Error;
