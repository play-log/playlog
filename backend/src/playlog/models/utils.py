from sqlalchemy.sql import select


async def create(conn, table, params, *, scalar=True):
    method = getattr(conn, 'scalar' if scalar else 'execute')
    return await method(table.insert().values(**params))


async def find_one(conn, table, params):
    query = select([table])
    for key, value in params.items():
        query = query.where(getattr(table.c, key) == value)
    result = await conn.execute(query)
    return await result.fetchone()


async def update(conn, table, criteria, params):
    await conn.execute(table.update().values(**params).where(criteria))
