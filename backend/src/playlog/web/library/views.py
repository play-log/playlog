from datetime import datetime, timedelta

from playlog.actions import album, artist, play, track
from playlog.config import USER_EMAIL, USER_NAME
from playlog.lib import gravatar
from playlog.web.framework.decorators import autowired, route


@route.get('/counters')
@autowired
async def counters(request, db):
    return {
        'artists': await artist.count_total(db),
        'albums': await album.count_total(db),
        'tracks': await track.count_total(db),
        'plays': await play.count_total(db)
    }


@route.get('/overview')
@autowired
async def overview(request, db):
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)

    return {
        'current_streak': await play.get_current_streak(db),
        'longest_streak': await play.get_longest_streak(db),
        'biggest_day': await play.get_biggest_day(db),
        'recently_added': {
            'artists': await artist.count_new(db, month_ago),
            'albums': await album.count_new(db, month_ago),
            'tracks': await track.count_new(db, month_ago),
            'start_date': month_ago,
            'end_date': now
        },
        'user': {
            'avatar_src': gravatar.get_url(USER_EMAIL, size=64),
            'name': USER_NAME,
            'listening_since': await play.get_listening_since(db)
        },
        'nowplay': await request.app['nowplay'].get(),
        'counters': {
            'artists': await artist.count_total(db),
            'albums': await album.count_total(db),
            'tracks': await track.count_total(db),
            'plays': await play.count_total(db)
        },
        'years': await play.count_per_year(db),
        'recent_tracks': await play.get_recent(db)
    }


@route.get('/artists')
@autowired
async def find_artists(request, db):
    return await artist.find_many(db, dict(request.query))


@route.get('/artists/{id:\d+}')
@autowired
async def find_artist(request, db):
    artist_id = request.match_info['id']
    data = dict(await artist.find_one(db, id=artist_id))
    data['albums'] = await album.find_for_artist(db, artist_id)
    data['years'] = await play.count_per_year_for_artist(db, artist_id)
    return data


@route.get('/albums')
@autowired
async def find_albums(request, db):
    return await album.find_many(db, dict(request.query))


@route.get('/albums/{id:\d+}')
@autowired
async def find_album(request, db):
    album_id = request.match_info['id']
    data = dict(await album.find_one(db, id=album_id))
    data['tracks'] = await track.find_for_album(db, album_id)
    data['years'] = await play.count_per_year_for_album(db, album_id)
    return data


@route.get('/tracks')
@autowired
async def find_tracks(request, db):
    return await track.find_many(db, dict(request.query))


@route.get('/tracks/{id:\d+}')
@autowired
async def find_track(request, db):
    track_id = request.match_info['id']
    data = dict(await track.find_one(db, id=track_id))
    data['total_plays'] = data.pop('plays')
    data['plays'] = await play.find_for_track(db, track_id)
    data['years'] = await play.count_per_year_for_track(db, track_id)
    return data


@route.get('/plays')
@autowired
async def find_plays(request, db):
    return await play.find_many(db, dict(request.query))
