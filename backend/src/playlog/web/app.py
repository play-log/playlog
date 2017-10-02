import venusian

from aiohttp import web
from aiopg import sa
from aioredis import create_redis

import playlog.web

from playlog import config, logging
from playlog.session import Session
from playlog.web.framework.middlewares import error_middleware, response_middleware
from playlog.web.submissions.middlewares import submissions_middleware


logging.setup()


async def on_startup(app):
    app['db'] = await sa.create_engine(config.SA_URL)
    app['redis'] = await create_redis(config.REDIS_URL)
    app['session'] = Session(app['redis'])


async def on_cleanup(app):
    app['db'].close()
    await app['db'].wait_closed()

    app['redis'].close()
    await app['redis'].wait_closed()


def run():
    app = web.Application(middlewares=[
        submissions_middleware,
        response_middleware,
        error_middleware
    ])
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    scanner = venusian.Scanner(router=app.router)
    scanner.scan(playlog.web)
    if config.DEBUG:
        import aioreloader
        aioreloader.start()
    web.run_app(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
