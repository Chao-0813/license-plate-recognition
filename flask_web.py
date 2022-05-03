from glob import glob
from re import A
from time import time
from flask import Flask #匯入Flask模組
app = Flask(__name__) #建立Flask物件
from flask import request #Flask以request模組取得參數值
from flask import render_template #Flask使用render_template讀取網頁檔

import pymysql #匯入pymysal模組

from datetime import datetime #匯入datetime模組


#insert_pic======================================================================================================================

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB_toMySQL(picture):
    print("Inserting BLOB into PICTURE_DATA table")
    try:
        db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB') #test.py與MySQL連線

        mycursor = db.cursor()
        sql_insert_blob_query = """ INSERT INTO PICTURE_DATA
                          (picture) VALUES (%s)"""

        empPicture = convertToBinaryData(picture)

        # Convert data into tuple format
        insert_blob_tuple = (empPicture)
        result = mycursor.execute(sql_insert_blob_query, insert_blob_tuple)
        db.commit()
        print("Image inserted successfully as a LONGBLOB into PICTURE_DATA table", result)

    except pymysql.connect.Error as error:
        print(f"Failed inserting BLOB data into PICTURE_DATA table:\n {error}")

def write_file(data,filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBLOB_fromMySQL(picture):
    print("Reading BLOB data from PICTURE_DATA table \n")

    try:
        db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB') #test.py與MySQL連線

        mycursor = db.cursor()

        mycursor.execute("SELECT picture from PICTURE_DATA")
        all_data = mycursor.fetchall()
        for row in all_data:
            image = row[0]
            write_file(image, picture)
        print("Storing employee image and bio-data on disk \n")
        print("Success!")

    except pymysql.connect.Error as error:
        print(f"Failed read BLOB data from PICTURE_DATA table:\n {error}")

#flask=======================================================================================================================

try: 
    db = pymysql.connect(host='localhost',user='root',password='HRCray621',database='TESTDB') #test.py與MySQL連線
    print("MySQL DB connected")
except:
    print ("Error: unable to fetch data") #否則連線失敗

mycursor =db.cursor() #呼叫游標執行的函式

@app.route('/get',methods=['GET']) #建立Flask網址路由,用GET方法傳送資料
def getpost():
    now=datetime.now() #變數now儲存現在時間
    ct=now.strftime("%Y-%m-%d_%H%M%S")#此ct為pg1現在時間:
    try:
        mycursor.execute("SELECT * FROM NUMPIC_DATA")
    except:
        print ("Error: unable to fetch data") #否則連線失敗
    
    return render_template('Insert_numplate_pg1.html',**locals())#render_template('網頁檔案名稱',**locals()) , 
                                                                 #**locals()指傳送所有參數及區域變數 ,
                                                                 #return回傳值,執行完函式後傳回主程式的資料 

@app.route('/post',methods=['POST'])#建立Flask網址路由,用POST方法傳送資料
def submit():
    try:
        mycursor.execute("SELECT numplate FROM NUMPIC_DATA")# Fetch all the rows in a list of lists.
        all_data = mycursor.fetchall()

        numplate_LIST=[]
        for row in all_data:
            numplate_LIST.append(row[0])

        print(f'numplate_LIST:{numplate_LIST}')
    except:
        print("Error: unable to fetch data") #否則連線失敗
    
    global username
    username=request.values['input_value'] #values取得POST參數值

    if username in numplate_LIST:
        print(f'{username} 在numplate_LIST中存在')

        now=datetime.now() #變數now儲存現在時間
        ct=now.strftime("%Y-%m-%d_%H%M%S")

        mycursor.execute("UPDATE NUMPIC_DATA SET payment_time='%s' where numplate='%s'" % (ct, username))#UPDATE更新原有資料
        db.commit()

        mycursor.execute("SELECT in_time FROM NUMPIC_DATA where numplate='%s'" %(username))
        results = mycursor.fetchall()
        for row in results:
            global in_time
            in_time = row[0]
        print(in_time)

        mycursor.execute("SELECT payment_time FROM NUMPIC_DATA where numplate='%s'" %(username))
        results = mycursor.fetchall()
        for row in results:
            global payment_time
            payment_time = row[0]
        print(payment_time)

        time_1 = datetime.strptime(in_time,"%Y-%m-%d_%H%M%S")
        time_2 = datetime.strptime(payment_time,"%Y-%m-%d_%H%M%S")

        global time_interval
        time_interval = time_2 - time_1
        print(time_interval)
        print(f"Total hour:{int(str(time_interval)[0])}")

        return render_template('InOut_timestamp.html')
        #return render_template('InOut_timestamp.html', data=dt)
    else:
        print(f'{username}不存在在numplate_LIST中')
        return '查無此車牌!'


@app.route('/post2',methods=['POST'])#建立Flask網址路由,用POST方法傳送資料
def submit2():
    a=2
    if str(time_interval)[1:2]==":":
        a=1
    if int(str(time_interval)[0:a]) < 1:
        fee="20"
    elif 1 <= int(str(time_interval)[0:a]) < 2:
        fee="40"
    elif 2 <= int(str(time_interval)[0:a]) < 3:
        fee="60"
    elif 3 <= int(str(time_interval)[0:a]) < 4:
        fee="80"
    else:
        fee="100"

    try:
        mycursor.execute("SELECT ID,numplate,in_time,payment_status,payment,payment_time,out_time,extra_payment\
            FROM NUMPIC_DATA where numplate='%s'" % (username))
        dt = mycursor.fetchall() #取得data的所有資料
        return render_template('InOut_timestamp1.html', data=dt,**locals())

    except:
        return '查無此車牌照片!'

@app.route('/post3',methods=['POST'])#建立Flask網址路由,用POST方法傳送資料
def submit3():
    a=2
    if str(time_interval)[1:2]==":":
        a=1
    if int(str(time_interval)[0:a]) < 1:
        fee="20"
    elif 1 <= int(str(time_interval)[0:a]) < 2:
        fee="40"
    elif 2 <= int(str(time_interval)[0:a]) < 3:
        fee="60"
    elif 3 <= int(str(time_interval)[0:a]) < 4:
        fee="80"
    else:
        fee="100"

    now=datetime.now() #變數now儲存現在時間
    ct=now.strftime("%Y-%m-%d_%H%M%S")
    try:
    # Fetch all the rows in a list of lists.

        mycursor.execute("SELECT ID,numplate,in_time,payment_status,payment,payment_time,out_time,extra_payment \
            FROM NUMPIC_DATA where numplate='%s'" % (username))
        dt = mycursor.fetchall() #取得data的所有資料

        paid=request.values['paid_fee'] #values取得POST參數值
        
        if paid == fee:
            mycursor.execute("UPDATE NUMPIC_DATA SET payment_status='done',payment=%s where numplate='%s'" %(fee,username))
            db.commit()
            return render_template('InOut_timestamp2.html', data=dt)
        else:
            return '未投入正確金額!'

    except:
        return '查無此車牌!'




if __name__ == '__main__': #執行Flask程式
  app.run() #http://127.0.0.1:5000/get

        #insertBLOB_toMySQL("C:\MCUT_file\Independent Study\MySQL\Picture\Result.jpg")從資料夾存進MySQL
        #ctime=f'{ct}'
        #insert_numplate=f"_{username}.jpg"
        #filename=f"{ctime+insert_numplate}"
        #readBLOB_fromMySQL(f"C:\MCUT_file\Independent Study\MySQL\Picture\Stored_pic\{filename}")從MySQL讀取並存入資料夾
