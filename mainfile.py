import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time
import pymysql.cursors
from PIL import Image
from pyzbar.pyzbar import decode
print(cv2.__version__)
image = cv2.imread('cartest18.jpg')

image = imutils.resize(image, width=500)
# * . : )
cv2.imshow("Original Image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray = cv2.bilateralFilter(gray, 11, 17, 17)


edged = cv2.Canny(gray, 170, 200)
cv2.imshow("bilateral filter",gray)

(new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] 
NumberPlateCnt = None 


count = 0
for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break


mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
new_image = cv2.bitwise_and(image,image,mask=mask)
cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
cv2.imshow("Final_image",new_image)


config = ('-l eng --oem 1 --psm 3')


text = pytesseract.image_to_string(new_image, config=config)


raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
        'v_number': [text]}

df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
df.to_csv('data.csv')


text=text.replace(" ","")
text=text.replace("-","")
text=text.replace(".","")
text=text.replace("*","")
text=text.replace(":","")
text=text.replace(")","")
text=text.replace("}","")
print('Number plate detected : ',text)


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='mysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record

        sql = "SELECT count(*)  FROM empvehiclerecord WHERE vehicleno= %s"
        mum= cursor.execute(sql, (text,))
        result = cursor.fetchone()
        #print('result',result)
        for i in result:
            b=result[i]
        if b==0 :
            #print("Valid Employee open the gate")
            sql1 = "SELECT count(*)  FROM empvehiclerecord WHERE alternatevehicle= %s"
            mum1 = cursor.execute(sql1, (text,))
            result1 = cursor.fetchone()
            #print('result', result1)
            for i in result1:
                b1 = result[i]
            if b1>0:
                print("valid emp open the gate")

            else:
                print("scan your id")
                cap = cv2.VideoCapture(0)

                while (True):

                    ret, frame = cap.read()




                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        # eturn_value, image = camera.read()
                        cv2.imwrite('opencv' + str(1) + '.png', frame)
                        break


                cap.release()
                cv2.destroyAllWindows()
                data = decode(Image.open('opencv1.png'))
                print(data)
                a = ''.join(map(str, data))
                empid = a[15:16]

                print('scanned emp id is',empid)
                sql = "SELECT count(*)  FROM empvehiclerecord WHERE empid= %s"
                mum = cursor.execute(sql, (empid,))
                result = cursor.fetchone()
                #print('result', result)
                for i in result:
                    b3= result[i]
                print(b3)
                if b3>0:
                    print("valid employee open the gate \n alternate vehicle registered")
                    sql2 = "UPDATE empvehiclerecord SET alternatevehicle = %s WHERE empid = %s"
                    cursor.execute(sql2,(text,empid))
                else:
                    print("Invaild Id.. Entry Restricted")

        elif b>0:
            print("vaild emp open the gate")
        else:
            print("Vehicle Not Registered")
finally:
    connection.close()
cv2.waitKey(0)
