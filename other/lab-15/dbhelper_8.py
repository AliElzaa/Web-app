import pymysql
import datetime

class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='mytwits_user',
            passwd='mytwits_password',
            db='mytwits')

    def get_all_twits(self):
        query = "select u.username, t.twit_id, t.twit, t.created_at from twits t, users u where t.user_id=u.user_id order by t.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples

    def get_twit(self,twit_id):
        query = "select twit from twits where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, twit_id)
            return cursor.fetchone()  
            # more detals about cursor.fetchone at
            # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html

    def add_twit(self,twit,user_id):
        query = "insert into twits (twit,user_id) values \
        (%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(query, (twit,user_id))
            return self.db.commit()

    def update_twit(self,twit,twit_id):
        query = "update twits set twit=%s where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,(twit,twit_id))
            return self.db.commit()

    def delete_twit(self,twit_id):
        query = "delete from twits where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, twit_id)
            return self.db.commit()

    def check_password(self,username,password):
        query = "select user_id from users where username = %s and password=%s;"
        with self.db.cursor() as cursor:
            user_id = None
            cursor.execute(query,(username,password))
            return cursor.fetchone()
