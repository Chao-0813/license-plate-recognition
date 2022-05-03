#載入requests套件
import requests
#需要載入os套件，可處理文件和目錄
import os
#創建目錄
os.makedirs('./img/',exist_ok=True)
url='http://192.168.217.102:8000/licence_plate.jpg'
r=requests.get(url)
with open('C:\MCUT_file\Independent Study\MySQL\static\Result.jpg','wb') as f:
#將圖片下載下來
    f.write(r.content)
print('Picture downloaded!')