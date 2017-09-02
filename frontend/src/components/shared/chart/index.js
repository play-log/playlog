import ChartJS from 'chart.js';
import PropTypes from 'prop-types';
import React from 'react';

import './defaults';

class Chart extends React.Component {
    constructor(props) {
        super(props);
        let data = [],
            labels = [];
        props.data.forEach(item => {
            data.push(item.value);
            labels.push(item.label);
        });
        this.state = {
            chart: null,
            labels: labels,
            dataset: {data: data}
        };
    }
    componentDidMount() {
        if (!this.isEmpty()) {
            this.createChart();
        }
    }
    componentWillUnmount() {
        if (this.state.chart) {
            this.state.chart.destroy();
        }
    }
    render() {
        let {height, width} = this.props,
            style = {height, width};

        return <div>
            {
                this.isEmpty()
                    ? <div>There are no data to display</div>
                    : <div>
                        <canvas ref="canvas" style={style} />
                    </div>
            }
        </div>;
    }
    createChart() {
        let context = this.refs.canvas.getContext('2d');
        this.setState({
            chart: new ChartJS(context, {
                type: this.props.type,
                data: {
                    datasets: [this.state.dataset],
                    labels: this.state.labels
                },
                options: {
                    legend: {
                        display: false
                    }
                }
            })
        });
    }
    isEmpty() {
        return this.state.dataset.data.length === 0;
    }
}

Chart.propTypes = {
    data: PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.string.isRequired,
        value: PropTypes.number.isRequired
    })).isRequired,
    type: PropTypes.oneOf(['radar', 'bar', 'doughnut', 'pie', 'line']),
    width: PropTypes.string,
    height: PropTypes.string
};

Chart.defaultProps = {
    type: 'bar',
    width: '100%',
    height: ''
};

export default Chart;
