from playlog.decorators import route
from playlog.actions import play


@route.get('/plays')
async def find_many(request):
    async with request.app['db'].acquire() as conn:
        return await play.find_many(conn, dict(request.query))
