import pymysql

# Open database connection
db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)


# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS NUMPIC_DATA")

# Create table as per requirement
sql = """CREATE TABLE NUMPIC_DATA (
   ID INT unsigned auto_increment primary key,
   numplate VARCHAR(50),
   picture LONGBLOB,
   in_time VARCHAR(50),
   payment_status VARCHAR(50),
   payment INT,
   payment_time VARCHAR(50),
   out_time VARCHAR(50),
   extra_payment INT )"""

cursor.execute(sql)

print('Table created')
# disconnect from server
db.close()