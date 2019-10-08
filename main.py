from get_info import grabber
from send_email import Email
from database import Connection
import configparser

###user credential details block
config = configparser.ConfigParser()
config.read('config.cfg')
MysqlHost = config.get('MOVIES', 'MYSQL_HOST')
username = config.get('MOVIES', 'MYSQL_USER')
password = config.get('MOVIES', 'MYSQL_PASSWORD')

##-----------------------------------------------------------------------------
##-----------------------------------------------------------------------------
conn = Connection(username, password)
conn.connect()
conn.create_table()

print("Enter Number of Users you want to Register", end=" ")
n=int(input())
for i in range(n):
  x=input("Email address:")
  tv=input("TV series:")
  insert = True
  for ser in conn.select_value(x):
    if ser[0] == tv:
      insert = False
  if insert:
    conn.insert_value(x.lower(), tv.lower())
  else:
    print("Database already has your information")

email = Email()
grab = grabber()
for x in conn.select_all():
  recv, series = x[0], x[1]
  email.send(recv, grab.information(series))
    
conn.close_connection()


