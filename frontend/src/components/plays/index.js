import React from 'react';
import {Link} from 'react-router-dom';
import {createSelector} from 'reselect';

import {actions} from '../../redux';
import {formatDateTime} from '../../utils';

import {Catalog, createListContainer} from '../shared/catalog';

import './index.css';

const dataSelector = createSelector(
    state => state.plays,
    data => {
        if (data.loaded && data.success) {
            data.payload.items = data.payload.items.map(item => ({
                artist: {
                    id: item.artistId,
                    name: item.artist
                },
                album: {
                    id: item.albumId,
                    name: item.album
                },
                track: {
                    id: item.trackId,
                    name: item.track
                },
                date: formatDateTime(item.date),
                rawDate: item.date
            }));
        }
        return data;
    }
);

const ListContainer = createListContainer(dataSelector, actions.playsRequest);

const FILTERS = [
    {type: 'search', name: 'artist', label: 'ARTIST'},
    {type: 'search', name: 'album', label: 'ALBUM'},
    {type: 'search', name: 'track', label: 'TRACK'},
    {
        type: 'group',
        name: 'date_group',
        label: 'DATE',
        items: [
            {type: 'date', name: 'date_gt', label: 'SINCE'},
            {type: 'date', name: 'date_lt', label: 'UNTIL'}
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
                options: ['artist', 'album', 'track', 'date'],
                initialValue: 'date'
            },
            {
                type: 'switch',
                name: 'order_direction',
                label: 'DIRECTION',
                options: ['asc', 'desc'],
                initialValue: 'desc'
            }
        ]
    }
];

const renderItem = ({artist, album, track, date, rawDate}) => (
    <div key={rawDate} className="plays-item">
        <span className="plays-item-name" title={
            `${artist.name} - ${album.name} - ${track.name}`
        }>
            <Link to={`/artists/${artist.id}`}>{artist.name}</Link>
            <span> &mdash; </span>
            <Link to={`/albums/${album.id}`}>{album.name}</Link>
            <span> &mdash; </span>
            <Link to={`/tracks/${track.id}`}>{track.name}</Link>
        </span>
        <span className="plays-item-date">{date}</span>
    </div>
);

const Plays = () => (
    <Catalog
        container={ListContainer}
        filters={FILTERS}
        renderItem={renderItem} />
);

export default Plays;
