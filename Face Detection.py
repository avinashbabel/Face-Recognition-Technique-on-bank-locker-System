import cv2
import os
import mysql.connector
import datetime
face_classifier = cv2.CascadeClassifier("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_classifier = cv2.CascadeClassifier("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_eye.xml")
def face_extractor(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None
    for(x,y,w,h) in faces:
        cropped_face =img[y:y+h, x:x+w]
    return  cropped_face

mydb = mysql.connector.connect(
    host="localhost",
    user="Avinash",
    passwd="7440",
    database ="banklocker"

)
name1 = input("Enter The Name Customer")
nameofnominess1 = input("Enter The Nmae of Nominess")
address1 = input("Enter The Address")
MOBILE12 = input("Enter The Mobile No.")
NOMINESSMOBILE21 = input("Enter The Nominees Mobile No.")
account_no1 = input("Enter The Account No.")
emailid1 = input("Enter The emailid")
aadharcard1 = (input("Enter The Aadhar Card No."))
yob = int(input("Enter The Year of Birth"))
mob = int(input("Enter The Month of Birth"))
dob = int(input("Enter The Date of Birth"))
dateofbirth1 = datetime.date(yob,mob,dob)
gender1 = input("Enter The Gender")
mycursor = mydb.cursor()

add_customer ="INSERT INTO customers (name, nameofnominess, address,account_no, MOBILE1, NOMINESSMOBILE2,gender ,dateofbirth,emailid,aadharcard) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
data_customer=(name1,nameofnominess1,address1,account_no1,MOBILE12,NOMINESSMOBILE21,gender1,dateofbirth1,emailid1,aadharcard1)
mycursor.execute(add_customer,data_customer)
mydb.commit()

face_id = input("Enter User Id")
x = "C:/faces2/picture"+str(face_id)
os.makedirs(x)
count = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count=count+1
        face =cv2.resize(face_extractor(frame),(200,200))
        face =cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        file_name_path = x+"/"+"user"+'.'+str(count)+'.jpg'
        cv2.imwrite(file_name_path,face)
        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)

    else:
        print("Face is not Found")
        pass
    if(cv2.waitKey(1)==13 or count==100):
        break
cap.release()
cv2.destroyAllWindows()
def eye_extractor(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    eyes = eye_classifier.detectMultiScale(gray,1.1,3)
    if eyes is():
        return None
    for(x,y,w,h) in eyes:
        cropped_eye =img[y:y+h, x:x+w]
    return  cropped_eye
cap = cv2.VideoCapture(0)
j =face_id
count =100
while True:
    ret,frame = cap.read()
    if eye_extractor(frame) is not None:
        count = count + 1
        eye = cv2.resize(eye_extractor(frame), (200, 200))
        eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
        file_name_path = x+"/"+"user."+ str(count) + '.jpg'
        cv2.imwrite(file_name_path, eye)
        cv2.putText(eye, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Eye Cropper",eye)
    else:
        print("Eye is not Found")
        pass
    if (cv2.waitKey(1) == 13 or count == 200):
        break

cap.release()
cv2.destroyAllWindows()
print("collecting sample complete!!!")







