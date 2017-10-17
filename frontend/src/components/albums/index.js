import React from 'react';
import {Link} from 'react-router-dom';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDate} from '../../utils';

import {Catalog, createListContainer} from '../shared/catalog';
import ProgressBar from '../shared/progress-bar';

import './index.css';

const dataSelector = createSelector(
    state => state.albums,
    data => {
        if (data.loaded && data.success) {
            const maxPlays = Math.max(...data.payload.items.map(item => item.plays));

            data.payload.items = data.payload.items.map(item => ({
                id: item.id,
                artist: {
                    id: item.artistId,
                    name: item.artist
                },
                name: item.name,
                plays: item.plays,
                firstPlay: formatDate(item.firstPlay),
                lastPlay: formatDate(item.lastPlay),
                playsPercent: Math.round(item.plays * 100 / maxPlays)
            }));
        }
        return data;
    }
);

const ListContainer = createListContainer(dataSelector, actions.albumsRequest);

const FILTERS = [
    {type: 'search', name: 'artist', label: 'ARTIST'},
    {type: 'search', name: 'name', label: 'TITLE'},
    {
        type: 'group',
        name: 'first_play_group',
        label: 'FIRST PLAY',
        items: [
            {type: 'date', name: 'first_play_gt', label: 'SINCE'},
            {type: 'date', name: 'first_play_lt', label: 'UNTIL'}
        ]
    },
    {
        type: 'group',
        name: 'last_play_group',
        label: 'LAST PLAY',
        items: [
            {type: 'date', name: 'last_play_gt', label: 'SINCE'},
            {type: 'date', name: 'last_play_lt', label: 'UNTIL'}
        ]
    },
    {
        type: 'group',
        name: 'order_group',
        label: 'ORDER',
        items: [
            {
                type: 'switch',
                name: 'order_field',
                label: 'FIELD',
                options: ['artist', 'name', 'plays', 'first_play', 'last_play'],
                initialValue: 'artist'
            },
            {
                type: 'switch',
                name: 'order_direction',
                label: 'DIRECTION',
                options: ['asc', 'desc'],
                initialValue: 'asc'
            }
        ]
    }
];

const renderItem = ({id, artist, name, plays, firstPlay, lastPlay, playsPercent}) => (
    <div key={id} className="albums-item">
        <div className="albums-item-data">
            <div className="albums-item-data-name">
                <Link to={`/artists/${artist.id}`}>{artist.name}</Link>
                <span> &mdash; </span>
                <Link to={`/albums/${id}`}>{name}</Link>
            </div>
            <div className="albums-item-data-period">{firstPlay} &mdash; {lastPlay}</div>
        </div>
        <div className="albums-item-bar">
            <ProgressBar percent={playsPercent}>
                {plays}
            </ProgressBar>
        </div>
    </div>
);

const Albums = () => (
    <Catalog
        container={ListContainer}
        filters={FILTERS}
        renderItem={renderItem} />
);

export default Albums;
