import aiohttp
import aiohttp.web
import configparser
import aiohttp_jinja2
import jinja2
import uvloop
import asyncio
from aiohttp import web
import logging
import traceback
import colorlog
import model, views
from middleware import setup_middlewares
import os
from pythonjsonlogger import jsonlogger
from utils import *


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def init(logger):
    app = web.Application()
    app['log'] = logger
    app['loop'] = asyncio.get_event_loop()
    app['db_pool'] = None
    config_file = "/config/app.conf"
    config = configparser.RawConfigParser()
    config.read(config_file)
    app['postgresql_dsn'] = config["POSTGRESQL"]["dsn"]
    app['pool_threads'] = int(config["POSTGRESQL"]["pool_threads"])
    app['host'] =  config["APP"]["host"]
    app['port'] = int(config["APP"]["port"])
    app['log'].info("Start app")
    app['background_tasks'] = []
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'),filters={"filter_example":filter_example})  # setup jinja2 environment
    return app



def start(app):
    try:
        setup_routes(app)
        #setup_middlewares(app)
        asyncio.ensure_future(model.init_database(app))
        app.on_startup.append(start_background_tasks)
        app.on_cleanup.append(cleanup_background_tasks)
        web.run_app(app, host=app['host'], port=app['port'])
    except Exception:
        app['log'].error("Start error")
        app['log'].error(traceback.format_exc())

async def start_background_tasks(app):
        await asyncio.sleep(1)
        app['log'].info("start_background_tasks")
        app['background_tasks'].append(app['loop'].create_task(views.task(app)))

async def cleanup_background_tasks(app):
        app['log'].info("cleanup_background_tasks")
        await terminate_coroutine(app)



def setup_routes(app):
    app.router.add_get('/', views.about)



async def terminate_coroutine(app):
    app['log'].error('Stop request received')
    for task in app['background_tasks']:
        task.cancel()
    app['log'].info("App stopped")
    app['loop'].stop()



if __name__ == '__main__':
    #config

    #logger
    log_level = logging.INFO
    logger = colorlog.getLogger('log')
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)s %(levelname)s: %(message)s (%(module)s:%(lineno)d)')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    jsonlog = logging.FileHandler('logging.log')
    jsonlog.setLevel(logging.WARNING)
    formatter = jsonlogger.JsonFormatter('%(created)s %(asctime)s %(levelname)s %(message)s %(module)s %(lineno)d)')
    jsonlog.setFormatter(formatter)
    logger.addHandler(jsonlog)


    #run app
    app=init(logger)
    start(app)


    #config
    log_level = logging.DEBUG
    logger = colorlog.getLogger('log')
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)s %(levelname)s: %(message)s (%(module)s:%(lineno)d)')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    jsonlog = logging.FileHandler('logging.log')
    jsonlog.setLevel(logging.WARNING)
    formatter = jsonlogger.JsonFormatter('%(created)s %(asctime)s %(levelname)s %(message)s %(module)s %(lineno)d)')
    jsonlog.setFormatter(formatter)
    logger.addHandler(jsonlog)


    #run app
    app = init(logger)
    start(app)