import PropTypes from 'prop-types';
import React from 'react';

import './index.css';

const NEIGHBOURS = 4;

export const FIRST_PAGE = 1;
export const INITIAL_OFFSET = 0;
export const LIMIT = 15;

export class Pagination extends React.Component {
    shouldComponentUpdate(nextProps) {
        return this.props.currentPage !== nextProps.currentPage;
    }
    render() {
        const pages = this.generatePages();

        return (
            <div className="shared-pagination">{
                Object.keys(pages).map(page => {
                    let props = {key: page, className: 'shared-pagination-item'},
                        label = page;
                    switch (pages[page]) {
                        case 'current':
                            props.className += ' shared-pagination-item__active';
                            break;
                        case 'less':
                        case 'more':
                            props.className += ' shared-pagination-item__noop';
                            label = '...';
                            break;
                        default:
                            props.onClick = () => {
                                let nextPage = parseInt(page, 10);
                                this.props.onChange(nextPage, this.calculateOffset(nextPage));
                            };
                            break;
                    }
                    return <span {...props}>{label}</span>;
                })
            }</div>
        );
    }
    calculateOffset(page) {
        return Math.abs(page * LIMIT - LIMIT);
    }
    generatePages() {
        let output = {},
            totalPages = Math.ceil(this.props.totalItems / LIMIT),
            offset,
            limit;

        if (totalPages < 2) {
            return output;
        }

        offset = this.props.currentPage - 1;
        limit = this.props.currentPage - NEIGHBOURS;
        limit = limit < 1 ? 1 : limit;
        for (let i = offset; i >= limit; i--) {
            output[i] = 'prev';
        }
        if (limit - 1 >= 2) {
            output[limit - 1] = 'less';
        }
        if (this.props.currentPage - NEIGHBOURS >= 1) {
            output[1] = 'first';
        }

        offset = this.props.currentPage + 1;
        limit = this.props.currentPage + NEIGHBOURS;
        limit = limit > totalPages ? totalPages : limit;
        for (let i = offset; i <= limit; i++) {
            output[i] = 'next';
        }
        if (totalPages - limit > 0) {
            output[limit + 1] = 'more';
        }
        if (this.props.currentPage + NEIGHBOURS <= totalPages) {
            output[totalPages] = 'last';
        }

        output[this.props.currentPage] = 'current';

        return output;
    }
}

Pagination.propTypes = {
    currentPage: PropTypes.number.isRequired,
    onChange: PropTypes.func.isRequired,
    totalItems: PropTypes.number.isRequired
};
