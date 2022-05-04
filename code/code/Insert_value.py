import pymysql
from datetime import datetime

now = datetime.now()
ct=now.strftime("%Y-%m-%d %H:%M:%S") 
print("current time:",ct)

# Open database connection
db = pymysql.connect(host='192.168.217.103',user='parking',password='!QAZ2wsx',database='TESTDB')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
#sql = """INSERT INTO NUMPLATE(numplate, in_time, payment_status, payment, payment_time, out_time, extra_payment)
   #VALUES ('EQC-5371', '2022-02-16 22:55:55', 'done', 200, '2022-02-16 23:59:55', '2022-02-16 23:59:59', 20)"""
sql ="INSERT INTO NUMPLATE_DATA(numplate, in_time, payment_status, payment, payment_time, out_time, extra_payment) \
   VALUES('%s', '%s', '%s', null, null, null, null)" % ('MXM-6351', ct, 'undone')

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
   print("Data inserted")
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()