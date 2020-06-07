import sqlite3 as sql
import datetime
import dateutil.parser
import random
import string

def randomString(stringLength):
    letters = string.ascii_letters
    print(len(letters))
    return ''.join(random.choice(letters) for i in range(stringLength))

conn = sql.connect('urls.db')
cursor = conn.cursor()
now= datetime.datetime.now()
x=list(cursor.execute("SELECT expiry FROM urls"))
expiry_list=[]
for i in range(0,len(x)):
    date = dateutil.parser.parse(x[i][0])
    expiry_list.append(date)

for i in expiry_list:
    if i <now :
        print("expired")
        print("deleting from database")
        
        cursor.execute("DELETE FROM urls WHERE expiry='2020-06-05 15:17:00';")
        print('deleted')
    else:
        print(i)
