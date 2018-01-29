# encoding=utf-8
from install_data import *
import json
from persist_data import database
from controller import install_bulk_data

log = logging.getLogger('controller')


def get_user_info(user_id):
    try:
        db = database()
        result = db.query_user_info(user_id)
        return json.dumps(result)
    except Exception as e:
        log.error('get_user_info error %s' % e)


def init_data():
    try:
        install_bulk_data()
    except Exception as e:
        log.error('init bulk data error %s' % e)
