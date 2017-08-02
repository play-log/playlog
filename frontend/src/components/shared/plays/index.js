import PropTypes from 'prop-types';
import React from 'react';

import Heart from '../heart';

import './index.css';

const Plays = ({data}) => {
    let result;
    if (data.length === 0) {
        result = <div className="shared-plays-empty">There are no items to display</div>;
    } else {
        result = data.map((group, idx) => (
            <div key={idx} className="shared-plays-group">
                <div className="shared-plays-group-title">{group.date}</div>
                <div className="shared-plays-group-list">{
                    group.items.map((item, idx) => (
                        <div key={idx} className="shared-plays-group-list-item">
                            <span className="shared-plays-group-list-item-heart">
                                <Heart enabled={item.isFavorite} />
                            </span>
                            <span className="shared-plays-group-list-item-data">
                                {item.data}
                            </span>
                            <span className="shared-plays-group-list-item-time">
                                {item.time}
                            </span>
                        </div>
                    ))
                }</div>
            </div>
        ));
    }
    return <div>{result}</div>;
};

Plays.propTypes = {
    data: PropTypes.arrayOf(PropTypes.shape({
        date: PropTypes.string.isRequired,
        items: PropTypes.arrayOf(PropTypes.shape({
            isFavorite: PropTypes.bool.isRequired,
            data: PropTypes.string.isRequired,
            time: PropTypes.string.isRequired
        }))
    })).isRequired
};

export default Plays;
