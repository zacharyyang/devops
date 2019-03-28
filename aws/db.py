# -*- coding: utf-8 -*-
# * Author        : Zachary  mail : zachary_yzh@126.com
# * Create time   : 2019-03-27 23:39
# * Description   :

import pymysql
from conf import *


class MySQL:
    def __init__(self):
        self.host = DB_CMDB_HOST
        self.port = DB_CMDB_PORT
        self.user = DB_CMDB_USER
        self.password = DB_CMDB_PASSWORD
        self.database = DB_CMDB_DATABASE

    def getConnect(self):
        if not self.database:
            raise (NameError, "Can't get database name.")
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "connect database err.")
        else:
            return cur

    def execQuery(self, sql):
        cur = self.getConnect()
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.close()
        return result

    def execNonQuery(self, sql):
        cur = self.getConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    db = MySQL()
    a = db.execQuery("select * from test;")
    x = "insert into test value(3,'yangzhiheng');"
    db.execNonQuery(x)
    print(a)