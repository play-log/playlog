import logging

from aiohttp.web import Response

from playlog.decorators import autowired, route


logger = logging.getLogger(__name__)

KEYMAP = [
    ('artist', 'a'),
    ('album', 'b'),
    ('title', 't'),
    ('length', 'l')
]


@route.post('/submissions/nowplay')
@autowired
async def nowplay(request, nowplay):
    post = await request.post()
    data = {a: post.get(b, '').strip() for a, b in KEYMAP}
    try:
        data['length'] = int(data['length'])
    except ValueError:
        logger.warn('Invalid length of current track: %s', data)
    else:
        if all(data.values()):
            logger.info('Setting current track: %s', data)
            await nowplay.set(**data)
        else:
            logger.warn('Unable to set current track: %s', data)
    return Response(text='OK')
