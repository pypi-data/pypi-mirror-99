# -*- coding: utf-8 -
from .gt_flask import GtFlask
from .constant import VERSION
import logging.config
import os
import importlib

def create_log_path(log_path):
    """
    文件日志不会自动生成目录，只能先自行创建，否则日志报错
    """
    if not os.path.exists(log_path):
        os.makedirs(log_path)

def create_app(config):
    create_log_path(config.LOGGER_CONFIG['path'])
    logging.config.dictConfig(config.LOGGER_CONFIG)
    global app
    app = GtFlask(__name__)
    app.logger.info('---基础框架正在初始化中, 框架版本:V{}---'.format(VERSION))
    app.init_app()
    app.config.from_object(config)

    if app.config.get('SQLALCHEMY_DATABASE_URI'):
        init_sqlalchemy(app)

    if app.config.get('MONGO_URI'):
        init_mongodb(app)

    if app.config.get('CELERY_BROKER_URL') and app.config.get('RESULT_BACKEND'):
        init_celery(app)

    if app.config.get('PROCESSOR'):
        from .processor import Processor
        app.logger.info('初始化任务处理器...')
        processor = Processor()
        processor.start()
        app.processor = processor

    if config.MODULES:
        app.modules = load_modules(config.MODULES)
    
    return app

def release_app():
    app.logger.info('---基础框架正在停止...')
    unload_modules()

    if app.processor:
        app.logger.info('停止任务处理器')
        app.processor.stop()
        
    app.logger.info('基础框架退出.')

def load_modules(modules_config):
    app.logger.info('开始加载模块...')
    modules = []

    for module in modules_config:
        name = module['name']
        app.logger.info('加载模块：{}'.format(name))

        try:
            inst = importlib.import_module(name, module['package'])
            init_app = getattr(inst, 'init_app')
            init_app(app)
            modules.append(inst)
        except:
            app.logger.error('Load Module [{}] Error.'.format(name), exc_info = True)

    return modules

def unload_modules():
    if not app.modules:
        return

    app.logger.info('开始卸载模块...')

    for module in app.modules:
        try:
            app.logger.info('卸载模块：{}'.format(module.__name__))
            uninit_app = getattr(module, 'uninit_app')
            uninit_app(app)
        except:
            app.logger.warning('Unload Module [{}] Error.'.format(module.__name__))

def init_sqlalchemy(app):
    app.logger.info('初始化数据库...')
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    app.db = db

def init_mongodb(app):
    app.logger.info('初始化MongoDB...')
    from flask_pymongo import PyMongo
    from webcore.mongo_encoder import MongoEncoder
    mongo_db = PyMongo(app)
    app.mongo_db = mongo_db
    app.register_encoder(MongoEncoder())

def init_celery(app):
    app.logger.info('初始化Celery...')
    from celery import Celery

    celery = Celery(
        app.import_name,
        backend = app.config['RESULT_BACKEND'],
        broker = app.config['CELERY_BROKER_URL']
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

