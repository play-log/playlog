import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const Heart = ({enabled}) => {
    let className = `shared-heart shared-heart__${enabled ? 'on' : 'off'}`;
    return <span className={className}></span>;
};

Heart.propTypes = {
    enabled: PropTypes.bool.isRequired
};

export default Heart;
