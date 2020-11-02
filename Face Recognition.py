import cv2
from datetime import datetime
import math,random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/trainer/trainer1.yml")
face_classifier = cv2.CascadeClassifier("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_classifier = cv2.CascadeClassifier("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_eye.xml")
def face_detector(img, size = .5):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h,x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img,roi
def eye_detector(img, size = .5):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    eyes = eye_classifier.detectMultiScale(gray,1.3,5)
    if eyes is():
        return img,[]
    for(x,y,w,h) in eyes:

        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h,x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img,roi
def generateotp():
    digits ='0123456789'
    otp =''
    for i in range(4):
        otp += digits[math.floor(random.random()*10)]
    return  otp
i=0
aadharcard1 = int(input("Enter The Aadhar Card"))
account = input("Enter The Account no")
mydb = mysql.connector.connect(
  host="localhost",
  user="Avinash",
  passwd="7440",
  database ="banklocker"
)
mycursor = mydb.cursor()
sql =("SELECT aadharcard,lockerid,emailid FROM customers WHERE account_no=%s")
mycursor.execute(sql,(account,))
myresult = mycursor.fetchone()
if myresult==None:
    print("Please Enter Your Valid Account Number")
else:
    i = str(myresult[1])
    now = datetime.now()
    datetime_format =now.strftime('%y-%m-%d %H:%M:%S')
    login = 'login'
    if (aadharcard1 != int(myresult[0])):
        print("Please Enter Your Valid Aadhar Card Number")

    else:
        email = 'akshay.murdiya@gmail.com'
        password = 'akshayjain'
        senderemail = str(myresult[2])
        mess = str(generateotp())
        message = mess
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = senderemail
        msg['Subject'] = 'otp'
        msg.attach(MIMEText(message, 'plain'))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email, password)
        text = msg.as_string()
        s.sendmail(email, senderemail, text)
        s.quit()
        correctotp = input("Enter The Otp")
        if (correctotp != mess):
            print("Please Enter The Valid Otp")
        else:
            cap = cv2.VideoCapture(0)
            while True:
                ret,frame =cap.read()
                image,face= face_detector(frame)
                images,eye = eye_detector(frame)
                try:
                    face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                    eye = cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
                    result1 = recognizer.predict(eye)
                    result = recognizer.predict(face)
                    if result[1] < 500 and result1[1]<500:
                        confidence = int(100 * (1 - (result[1]) / 300))
                        confidence1 = int(100 * (1 - (result1[1]) / 300))
                        display_string = str(confidence)+"% Confidence it is User "+str(confidence1)+"%"
                        cv2.putText(image,display_string,(100,120),cv2.FONT_HERSHEY_COMPLEX,1,(255,120,255),2)
                        cv2.imshow("Face and Eye Cropper",image)
                    if (confidence>75 and confidence1>70):
                        cv2.putText(image, "Access Grant", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255,0), 2)
                        cv2.imshow("Face and Eye Cropper",image)
                        if(i==0):
                            add_customer = "INSERT INTO transcations (locker_id,transcation_datetime,transcationinout) VALUES(%s,%s,%s)"
                            data_customer = (i, datetime_format, login)
                            mycursor.execute(add_customer, data_customer)
                            mydb.commit()
                        i=1
                    else:
                        cv2.putText(image, "Face and Eye is Not Match", (125, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                        cv2.putText(images, "Face and Eye is Not Match", (125,450 ), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow("Face and Eye Cropper", image)
                except:
                    cv2.putText(image, "Face and Eye Not Found", (125,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                    cv2.putText(images,"Face and Eye Not Found", (125, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                    cv2.imshow("Face and Eye Cropper", image)
                    pass
                if cv2.waitKey(1)==13:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
if i==1:
    now = datetime.now()
    datetime_format = now.strftime('%y-%m-%d %H:%M:%S')
    logout = 'logout'
    add_customer = "INSERT INTO transcations (locker_id,transcation_datetime,transcationinout) VALUES(%s,%s,%s)"
    data_customer = (i, datetime_format,logout)
    mycursor.execute(add_customer, data_customer)
    mydb.commit()
    email = 'akshay.murdiya@gmail.com'
    password = 'akshayjain'
    senderemail = str(myresult[2])
    message = 'Locker Access'
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = senderemail
    msg['Subject'] = 'Access Locker'
    msg.attach(MIMEText(message, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    text = msg.as_string()
    s.sendmail(email, senderemail, text)
    s.quit()
if(i==1):
    email = 'akshay.murdiya@gmail.com'
    password = 'akshayjain'
    senderemail = str(myresult[2])
    message = str(myresult[1])
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = senderemail
    msg['Subject'] = 'Information Access Locker Customer'
    msg.attach(MIMEText(message, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, password)
    text = msg.as_string()
    s.sendmail(email, senderemail, text)
    s.quit()
