import venusian

from aiohttp import web
from aiopg import sa

import playlog

from playlog import config, logging


logging.setup()


async def on_startup(app):
    app['db'] = await sa.create_engine(config.SA_URL)


async def on_cleanup(app):
    app['db'].close()
    await app['db'].wait_closed()


def run():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    scanner = venusian.Scanner(router=app.router)
    scanner.scan(playlog)
    web.run_app(app, host=config.HOST, port=config.PORT)
