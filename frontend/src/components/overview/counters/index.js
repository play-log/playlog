import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const Counters = ({header, data, footer}) => (
    <div>
        <div className="overview-counters-header">{header}</div>
        {
            data.map((item, idx) => (
                <div key={idx} className="overview-counters-item">
                    <img className="overview-counters-item-icon" src={item.icon} alt="" />
                    <div className="overview-counters-item-data">
                        <div className="overview-counters-item-data-label">{item.label}</div>
                        <div className="overview-counters-item-data-value">{item.value}</div>
                    </div>
                </div>
            ))
        }
        <div className="overview-counters-footer">{footer}</div>
    </div>
);

Counters.propTypes = {
    header: PropTypes.node.isRequired,
    data: PropTypes.arrayOf(PropTypes.shape({
        icon: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        value: PropTypes.number.isRequired
    })),
    footer: PropTypes.node.isRequired
};

export default Counters;
