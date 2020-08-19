import asyncpg

async def init_database(app):
    app['log'].info("Init db pool")
    app["db_pool"] = await asyncpg.create_pool(dsn=app["postgresql_dsn"],
                            loop=app["loop"],
                            min_size=10, max_size=app["pool_threads"])
    await create_db_model(app)

async def create_db_model(app):
    app['log'].info("Create database model")
    async with app['db_pool'].acquire() as conn:
        pass
        #await conn.execute(open("schema.sql", "r").read().replace("\n", ""))