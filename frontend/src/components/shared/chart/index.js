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
        this.handleClick = this.handleClick.bind(this);
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
                        <canvas ref="canvas" style={style} onClick={this.handleClick} />
                    </div>
            }
        </div>;
    }
    createChart() {
        let context = this.refs.canvas.getContext('2d'),
            params = {
                type: this.props.type,
                data: {
                    datasets: [this.state.dataset],
                    labels: this.state.labels
                },
                options: {
                    legend: {display: false},
                    hover: {}
                }
            };
        if (this.props.onClick) {
            params.options.onHover = (event, items) => {
                if (this.props.onClick) {
                    const canvas = this.refs.canvas;
                    canvas.style.cursor = items.length > 0 ? 'pointer' : 'default';
                }
            };
        }
        this.setState({chart: new ChartJS(context, params)});
    }
    isEmpty() {
        return this.state.dataset.data.length === 0;
    }
    handleClick(event) {
        if (this.props.onClick) {
            let chart = this.state.chart,
                elements = chart.getElementAtEvent(event);
            if (elements.length > 0) {
                let element = elements[0],
                    label = chart.data.labels[element._index],
                    value = chart.data.datasets[element._datasetIndex].data[element._index];
                this.props.onClick(label, value);
            }
        }
    }
}

Chart.propTypes = {
    data: PropTypes.arrayOf(PropTypes.shape({
        label: PropTypes.oneOfType([
            PropTypes.object,
            PropTypes.string
        ]).isRequired,
        value: PropTypes.number.isRequired
    })).isRequired,
    height: PropTypes.string,
    onClick: PropTypes.func,
    type: PropTypes.oneOf(['radar', 'bar', 'doughnut', 'pie', 'line']),
    width: PropTypes.string
};

Chart.defaultProps = {
    type: 'bar',
    width: '100%',
    height: ''
};

export default Chart;
