from bolinette import blnt
from bolinette.decorators import command


@command('init_db', 'Initialize the database')
@command.argument('flag', 'seeders', flag='s', summary='Run the seeders after database creation')
async def init_db(context: 'blnt.BolinetteContext', seeders: bool):
    context.logger.info('==== Initializing database ====')
    context.logger.info('**** Dropping all tables')
    await context.db.drop_all()
    context.logger.info('**** Creating all tables')
    await context.db.create_all()
    if seeders:
        context.logger.info('**** Running seeders')
        await context.db.run_seeders(log=True, tab=5)
    context.logger.info('==== Done ====')
