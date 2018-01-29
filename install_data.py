# encoding=utf-8
import logging
import time
import os
from persist_data import database
from settings import RESOURCE_PATH

log = logging.getLogger('InstallData')


''' 
parse two table which are user_cass_[DATA] and userrole_caas_[DATE]
and write those critical key to db
'''


def get_data_path():
    return RESOURCE_PATH + time.strftime('%Y%m%d', time.localtime(time.time()))

def get_daily_name(fix_name):
    list = [fix_name, time.strftime('%Y%m%d', time.localtime(time.time()))]
    table_name = ''.join(list)
    return table_name


def install_bulk_data():
    if is_exist():
        userrole_dict = setup_userrole_dict()
        user_dict = setup_user_dict()
        try:
            db = database()
            user = db.query_all_user_info()
            u_id = []
            for i in user:
                u_id.append(i[0])
            for j in userrole_dict:
                if j in u_id:
                    db.update_from_userrole(j, userrole_dict[j])
                else:
                    db.insert_from_userrole(j, userrole_dict[j])
            db.close_co()
        except Exception as e:
            log.error('install userrole error %s' % e)
        try:
            db = database()
            user = db.query_all_user_info()
            u_id = []
            for i in user:
                u_id.append(i[0])
            for j in user_dict:
                if j in u_id:
                    db.update_from_user(j, user_dict[j])
                else:
                    db.insert_from_user(j, user_dict[j])
            db.close_co()
        except Exception as e:
            log.error('install user error %s ' % e)
    else:
        log.error('data table is not exist anymore')


def is_exist():
    list = ['user_caas_', time.strftime('%Y%m%d', time.localtime(time.time()))]
    user_table = ''.join(list)
    list = ['userrole_caas_', time.strftime('%Y%m%d', time.localtime(time.time()))]
    userrole_table = ''.join(list)
    try:
        if os.path.exists(get_data_path()):
            try:
                if os.path.exists(get_data_path() + '/' + user_table) and os.path.exists(get_data_path() + '/' + userrole_table):
                    return True
            except:
                log.error('data table is all removed or partly removed')
    except Exception as e:
        log.error('resource path missing %s' % e)


def setup_userrole_dict(t_name = 'userrole_caas_'):
    daily_userrole = get_daily_name(t_name)
    path = get_path(daily_userrole)
    userrole_dict = dict()
    try:
        with open(path, 'rb') as file:
            for line in file:
                userrole_dict[line.strip()[:8]] = (lambda x=line.strip()[10:11]: 'true' if x == '1' else 'false')()
            return userrole_dict
    except Exception as e:
        log.error('process userrole_cass table error %s' % e)


def setup_user_dict(t_name='user_caas_'):
    daily_userrole = get_daily_name(t_name)
    path = get_path(daily_userrole)
    user_dict = dict()
    try:
        with open(path, 'rb') as file:
            for line in file:
                if line.strip() != "":
                    if line.split('!^!^')[1].split('!^')[0] != '':
                        user_dict[line.strip()[:8]] = line.split('!^!^')[1].split('!^')[0]
                else:
                    pass
            return user_dict
    except Exception as e:
        log.error(u'can not setup user_dict %s' % e)


def get_path(t_name):
    return get_data_path() + '/' + t_name

# class Cache():
#     def __init__(self):
#         self.ca = FileCache('app', app_cache_dir=CACHE_PATH)
#
#     def put(self,key,value):
#         self.ca[key] = value
#
#     def get(self,key):
#         isadmin = self.ca[key][0]
#         email = self.ca[key][1]
#         return isadmin, email
#
#     def close(self):
#         self.ca.close()


if __name__ == '__main__':
    key = '01'
    value = ['isadmin', 'test@test.com']
    c = Cache()
    c.put(key, value)
