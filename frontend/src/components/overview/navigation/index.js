import PropTypes from 'prop-types';
import React from 'react';
import {Link} from 'react-router-dom';

import AlbumIcon from '../../../icons/album.svg';
import ArtistIcon from '../../../icons/artist.svg';
import HeartIcon from '../../../icons/heart.svg';
import PlayIcon from '../../../icons/play.svg';
import TrackIcon from '../../../icons/track.svg';

import './index.css';

const DATA = [
    {key: 'artists', icon: ArtistIcon, link: '/artists'},
    {key: 'albums', icon: AlbumIcon, link: '/albums'},
    {key: 'tracks', icon: TrackIcon, link: '/tracks'},
    {key: 'plays', icon: PlayIcon, link: '/plays'},
    {key: 'favorites', icon: HeartIcon, link: '/favorites'},
];

const Item = ({icon, title, link, counter}) => (
    <div className="overview-navigation-item">
        <img className="overview-navigation-item-icon" src={icon} alt="" />
        <div className="overview-navigation-item-data">
            <Link to={link} className="overview-navigation-item-data-label">{title}</Link>
            <div className="overview-navigation-item-data-counter">{counter}</div>
        </div>
    </div>
);

Item.propTypes = {
    icon: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    link: PropTypes.string.isRequired,
    counter: PropTypes.number.isRequired
};

const Navigation = ({counters}) => (
    <div>{
        DATA.map(item =>
            <Item
                title={item.key}
                counter={counters[item.key]}
                {...item} />
        )
    }</div>
);

Navigation.propTypes = {
    counters: PropTypes.object.isRequired
};

export default Navigation;
