# encoding=utf-8
import sqlite3
import logging

from settings import DB_PATH

log = logging.getLogger('persistent')


class database():
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
        except Exception as e:
            log.error('error connect to db %s' % e)

    def close_co(self):
        self.conn.close()

    def init_user_info(self):
        try:
            co = self.conn
            cu = co.cursor()
            create_user_table_sql = "create table user(id varchar(15) primary key not null, is_admin varchar(10), email varchar(38))"
            cu.execute(create_user_table_sql)
            co.commit()
            co.close()
        except Exception as e:
            log.error('create user table error %s' % e)

    def query_user_info(self, user_id):
        try:
            co = self.conn
            cu = co.cursor()
            query_sql = "select * from user where id = %s" % user_id
            cu.execute(query_sql)
            data = cu.fetchone()
            result = dict(
                id=data[0],
                is_admin=data[1],
                email=data[2]
            )
            co.close()
            return result
        except Exception as e:
            log.error('query user info error %s' % e)

    def update_from_userrole(self, id, is_admin):
        try:
            co = self.conn
            cu = co.cursor()
            add_user_sql = "update user set is_admin = '%s' where id = '%s'" %(is_admin, id)
            cu.execute(add_user_sql)
            co.commit()
        except Exception as e:
            log.error('add user error %s' % e)

    def insert_from_userrole(self, id, is_admin):
        try:
            co = self.conn
            cu = co.cursor()
            add_user_sql = "insert into user(id, is_admin) values('%s', '%s')" %(id, is_admin)
            cu.execute(add_user_sql)
            co.commit()
        except Exception as e:
            log.error('add user error %s' % e)

    def update_from_user(self, id, email):
        try:
            co = self.conn
            cu = co.cursor()
            add_email_sql = "update user set email = '%s' where id = '%s'" % (email, id)
            cu.execute(add_email_sql)
            co.commit()
        except Exception as e:
            log.error('add email error %s' % e)

    def insert_from_user(self, id, email):
        try:
            co = self.conn
            cu = co.cursor()
            add_email_sql = "insert into user(id, email) values('%s','%s')" % (id, email)
            cu.execute(add_email_sql)
            co.commit()
        except Exception as e:
            log.error('add email error %s' % e)

    def query_all_user_info(self):
        try:
            co = self.conn
            cu = co.cursor()
            query_all_sql = "select * from user"
            cu.execute(query_all_sql)
            result = cu.fetchall()
            return result
        except Exception as e:
            log.error('query all user info wrong % s' % e)