import PropTypes from 'prop-types';
import React from 'react';

import DefaultAvatar from '../../../icons/default-avatar.png';

import './index.css';

const User = ({avatarSrc, name, listeningSince}) => (
    <div className="overview-user">
        <img className="overview-user-avatar" src={avatarSrc || DefaultAvatar} alt="" />
        <div className="overview-user-info">
            <div className="overview-user-info-name">{name}</div>
            {
                listeningSince && <div className="overview-user-info-date">
                    Listening since {listeningSince}
                </div>
            }
        </div>
    </div>
);

User.propTypes = {
    avatarSrc: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    listeningSince: PropTypes.number
};

export default User;
