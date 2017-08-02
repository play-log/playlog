import PropTypes from 'prop-types';
import React from 'react';

import Chart from '../../shared/chart';

import './index.css';

const DateChart = ({data}) => (
    <div className="overview-date-chart">
        <Chart data={data} height='220px' />
    </div>
);

DateChart.propTypes = {
    data: PropTypes.array.isRequired
};

export default DateChart;
