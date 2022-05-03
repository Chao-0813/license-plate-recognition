import pymysql
from datetime import datetime

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
    
def insertBLOB_toMySQL(numplate,picture):

   print("Inserting BLOB into NUMPIC_DATA table")
   try:
      db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB') #test.py與MySQL連線
   
      mycursor = db.cursor()
   
      #sql2= "UPDATE NUMPIC_DATA SET picture=LOAD_FILE('C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg') where numplate=%s" %(ocr_result)
      sql2= "INSERT INTO NUMPIC_DATA(numplate,picture) VALUES(%s,%s)"
   
      empPicture = convertToBinaryData(picture)
   
      # Convert data into tuple format
      insert_blob_tuple = (numplate,empPicture)
      mycursor.execute(sql2, insert_blob_tuple)
      db.commit()
      print("Image inserted successfully as a LONGBLOB into NUMPIC_DATA table")

   except pymysql.connect.Error as error:
      print(f"Failed inserting BLOB data into NUMPIC_DATA table:\n {error}")

def write_file(data,filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB_fromMySQL(picture):
    print("Reading BLOB data from NUMPIC_DATA table \n")

    try:
        db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB') #test.py與MySQL連線

        mycursor = db.cursor()

        mycursor.execute("SELECT picture from NUMPIC_DATA")
        all_data = mycursor.fetchall()
        for row in all_data:
            image = row[0]
            write_file(image, picture)
        print("Storing picture and bio-data on 'C:\MCUT_file\Independent Study\MySQL\Picture\Stored_pic\' \n")
        print("Success!")

    except pymysql.connect.Error as error:
        print(f"Failed read BLOB data from NUMPIC_DATA table:\n {error}")



# Prepare SQL query to INSERT a record into the database.

now = datetime.now()
ct=now.strftime("%Y-%m-%d_%H%M%S")
print("current time:",ct)

# Open database connection
db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB')

# prepare a cursor object using cursor() method
mycursor = db.cursor()

try:

   ocr_result='EQC-5371'

   # Execute the SQL command

   #mycursor.execute("INSERT INTO NUMPIC_DATA(numplate) VALUES('%s')" % (ocr_result))

   #insertBLOB_toMySQL(ocr_result,"C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg")
   insertBLOB_toMySQL(ocr_result,"C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg")
   filename=f'{ct}.jpg'
   readBLOB_fromMySQL(f"C:\MCUT_file\Independent Study\MySQL\Picture\Stored_pic\{filename}")
   
   mycursor.execute("UPDATE NUMPIC_DATA SET in_time='%s', payment_status='%s', payment=null, payment_time=null, out_time=null, \
      extra_payment=null where numplate='%s'" % (ct, 'undone', ocr_result))
   
   # Commit your changes in the database
   db.commit()
   print("All Data inserted")
except:
   # Rollback in case there is any error
   db.rollback()


# disconnect from server
db.close()