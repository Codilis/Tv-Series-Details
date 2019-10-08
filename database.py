import mysql.connector
from mysql.connector import errorcode

class Connection:
    def __init__(self, user, password):
        self.config = {
          'user': user,
          'password': password,
          'host': '127.0.0.1',
          'raise_on_warnings': False,
        }

    def connect(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.c = self.cnx.cursor()
        try:
            self.c.execute("CREATE DATABASE movies")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                pass
        self.c.execute("USE movies")

    def create_table(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS series_details(Id INT AUTO_INCREMENT PRIMARY KEY,Email VARCHAR(255), series VARCHAR(255))')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(err.msg)

    def insert_value(self,email, series):    
        data = {'email':email, 'series':series}
        sql = ("INSERT INTO series_details(Email,series) VALUES (%(email)s, %(series)s)")
        x = 0
        try:
            self.c.execute(sql, data)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('name already exist')
        self.cnx.commit()

    def select_value(self,value):
        sql = ("SELECT series FROM series_details where email = %(name)s")
        data = {'name':value}
        sel = self.c.execute(sql, data)
        data = self.c.fetchall()
        return data

    def select_all(self):
        sql = ("SELECT Email,series FROM series_details")
        sel = self.c.execute(sql)
        data = self.c.fetchall()
        return data

    def close_connection(self):
        self.c.close()
        self.cnx.close()
