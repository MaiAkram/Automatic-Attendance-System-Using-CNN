import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import yagmail

# from PIL import ImageGrab

path = 'D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images): 

    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    with open('D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/Attendance/Attendance.csv','r+', encoding="Latin1") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
    #with open('D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/Attendance/Attendance.txt','r+') as f:
    #    myDataList = f.readlines()
    #    nameList = []
    #    for line in myDataList:
    #        entry = line.split(',')
    #        nameList.append(entry[0])
    #    if name not in nameList:
    #        now = datetime.now()
    #        dtString = now.strftime('%H:%M:%S')
    #        f.writelines(f'\n{name},{dtString}')

def automail(receiver):
    #date = datetime.date.today().strftime("%B %d, %Y")
    path = 'D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/Attendance'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    filename = newest
    sub = "Attendance Report for " #+ str(date)
    # mail information
    yag = yagmail.SMTP("maiakram2001@gmail.com", "plozsznzzupktlbo")

    # sent the mail
    yag.send(
        to=receiver,
        subject=sub, # email subject
        #contents=body,  # email body
        attachments= filename  # file attached
    )
    print("Email Sent!")
 
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(0)

def Recognition(): 
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
 
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                
 
        cv2.imshow('Webcam',img)
        if cv2.waitKey(1)==27:
            break

#Recognition()
#automail('maiakram2001@gmail.com')

