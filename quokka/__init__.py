#!/usr/bin/env python
# -*- coding: utf-8 -*-
VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "pre-Alpha"
__description__ = "Hack of Quokka (398be6f9a2bbccb4cf96e17f422b1c2fad6a57f9) \
                   for personal use"
__author__ = "Daniel H. Morgan <dhm@streamgardens.com>"
__email__ = "dhm@streamgardens.com"
__license__ = "MIT License"
__copyright__ = "Copyright 2015, Open Knowledge Tools"


try:
    from .core.admin import create_admin
    from .core.app import QuokkaApp
    # from .core.middleware import HTTPMethodOverrideMiddleware
    admin = create_admin()
except:
    pass


def create_app_base(config=None, test=False, admin_instance=None, **settings):
    app = QuokkaApp('quokka')
    app.config.load_quokka_config(config=config, test=test, **settings)
    if test or app.config.get('TESTING'):
        app.testing = True
    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    app = create_app_base(
        config=config, test=test, admin_instance=admin_instance, **settings
    )
    from .ext import configure_extensions
    configure_extensions(app, admin_instance or admin)
    # app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    return app


def create_api(config=None, **settings):
    return None


def create_celery_app(app=None):
    from celery import Celery
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    taskbase = celery.Task

    class ContextTask(taskbase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return taskbase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
