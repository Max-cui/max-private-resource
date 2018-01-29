# encoding=utf-8
import time
from flask import Flask
from flask import request
from flask import make_response
from settings import setup_logging
from controller import *
from persist_data import database
from schedule_job import schedule_job

log = logging.getLogger(__name__)


def init_db():
    try:
        db = database()
        db.init_user_info()
    except Exception as e:
        log.error('ini_db error %s' % e)


def setup_routes(app):
    @app.errorhandler(500)
    def internal_server_error(e):
        return 'this is a misson to do internal error', 500

    @app.errorhandler(404)
    @app.route('/api/user')
    def get_user():
        try:
            if len(request.args.get('ouid', '')) == 8 and isinstance(len(request.args.get('ouid', '')), int):
                user_id = request.args.get('ouid', '')
                return get_user_info(user_id)
            elif len(request.args.get('buid', '')) == 8 and isinstance(len(request.args.get('buid', '')), int):
                user_id = request.args.get('buid', '')
                return get_user_info(user_id)
            else:
                rs = make_response('not found', 404)
                return rs
        except Exception as e:
            log.exception('get user info failed %s' % e)


def create_app(name=None):
    setup_logging()
    app = Flask(name or __name__)
    setup_routes(app)
    app.debug = False
    init_db()
    init_data()
    schedule_job()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('192.168.0.107', 7789)
