from playlog.decorators import autowired, route
from playlog.actions import play


@route.get('/plays')
@autowired
async def find_many(request, db):
    return await play.find_many(db, dict(request.query))
