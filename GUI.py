import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from threading import Thread
from tkinter import * 
from tkinter.ttk import *
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time

from AutomatedAttendanceSystem import Recognition, automail
#from Train import Training

window = tk.Tk()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

app=FullScreenApp(window)

class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/BG0.jpg")
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

e = Example(window)
e.pack(fill=BOTH, expand=YES)
C = tk.Canvas(window, height=600, width=600)

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

window.title("Smart Attendance System Using Facial Recognition")

message3 = tk.Label(window, text="Smart Attendance System" ,fg="white",bg="#8a2e7f" ,width=55 ,height=1,font=('Helvetica', 30, ' bold '))
message3.place(relx = 0.5, rely = 0.1, anchor = CENTER)

frame4 = tk.Frame(window, bg="#8a2e7f")
frame4.place(relx=0.5, rely=0.17, relwidth=0.2, relheight=0.05,anchor=CENTER)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year, fg="white",bg="#262523" ,width=55 ,height=1,font=('Helvetica', 20, ' bold '))
datef.pack(fill='both',expand=1)


frame1 = tk.Frame(window, bg="#ffffff")
frame1.place(relx=0.057, rely=0.21, relwidth=0.35, relheight=0.78)


head1 = tk.Label(frame1, text="Attendance Recording", fg="white",bg="#8a2e7f" ,font=('Helvetica', 17, ' bold ') )
head1.place(x=0,y=0)

frame2 = tk.Frame(window, bg="#ffffff")
frame2.place(relx=0.59, rely=0.21, relwidth=0.35, relheight=0.38)


head2 = tk.Label(frame2, text="Automail", fg="white",bg="#8a2e7f" ,font=('Helvetica', 17, ' bold ') )
head2.grid(row=0,column=0)

frame3 = tk.Frame(window, bg="#ffffff")
frame3.place(relx=0.59, rely=0.63, relwidth=0.35, relheight=0.36)


head3 = tk.Label(frame2, text="Enrollments", fg="white",bg="#8a2e7f" ,font=('Helvetica', 17, ' bold ') )
head3.grid(row=0,column=0)

##################################################LEFT SIDE########################################################################

lbl = tk.Label(frame2, text="Receiver Email",width=20  ,height=1  ,fg="white"  ,bg="#8a2e7f" ,font=('Helvetica', 13, ' bold ') )
lbl.place(relx=0.3, rely=0.1)

txt = tk.Entry(frame2,width=23 ,fg="black",font=('Helvetica', 13 ))
txt.place(relx=0.3, rely=0.2)

def get_data():
  rMail=txt.get()
  return automail(rMail)

snd = tk.Button(frame2, text="Send",command=get_data ,fg="white"  ,bg="#8a2e7f"  ,width=35  ,height=1, activebackground = "white" ,font=('Helvetica', 13, ' bold '))
snd.place(x=100, y=230) # LINKING MODULES!

##########################################################Progress Bar###################################################################

def progress_Measure(): 
  import time 
  time.sleep(2)
  progress['value'] = 20
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 40
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 50
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 60
  window.update_idletasks() 
  time.sleep(5) 

  progress['value'] = 100



def bar(): 
  Thread(target = Training).start()
  Thread(target = progress_Measure()).start()

trainImg = tk.Button(frame3, text="Train",fg="white", command=bar ,bg="#507d2a" ,width=34 ,height=1, activebackground = "white",font=('Helvetica',15,' bold '))
trainImg.place(x=37, y=400)

progress = Progressbar(frame2,length=200,orient = HORIZONTAL, mode='determinate')
progress.place(x=150,y=450)

##################RIGHT SIDE################################################################################################

lbl3 = tk.Label(frame1, text="Class",width=20,fg="white",bg="#8a2e7f"  ,height=1 ,font=('Helvetica', 13, ' bold '))
lbl3.place(x=140, y=50)

cls = tk.Entry(frame1, width=23 ,fg="black",font=('Helvetica', 13 ))
cls.place(x=140, y=110)

###########################################################################################################################

def Recognizer():
  Recognition()

trackImg = tk.Button(frame1, text="Take Attendance",fg="white"  ,bg="#507d2a" ,command=Recognizer, width=35  ,height=1, activebackground = "white" ,font=('Helvetica', 15, ' bold '))
trackImg.place(x=35,y=150)

###############################QUIT###########################################################################################

tv= Treeview(frame1,columns =('name','attendance'),selectmode='browse',show=["headings"])
tv.column('name',width=225,anchor=tk.CENTER)
#tv.column('id',width=155,anchor=tk.CENTER)
tv.column('attendance',width=225,anchor=tk.CENTER)
tv.grid(row=2,column=0,padx=(20,0),pady=(250,0),columnspan=4)

tv.heading('name',text ='Name_ID')
#tv.heading('id',text ='ID')
tv.heading('attendance',text ='Attendance')

scroll=Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(250,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

def clear_tree():
  x=tv.get_children()
  if x != '()': # checks if there is something in the first row
    for child in x:
      tv.delete(child)
  
def Show_attendance():
  import csv
  with open('D:/UNI/Year 3/Semester 1/Artificial Intelligence for Engineering/Project/Attendance_System/Attendance/Attendance.csv','r+', encoding="Latin1") as f:
        myDataList = f.readlines()
        reader = csv.DictReader(myDataList, delimiter=',')
        for column in reader:
            nm = column['Name_ID']
            #id = column['ID']
            if column['Attendance'] != None:
                ent = "Present"
            else:
                ent = "Absent"
            tv.insert("", 0, values=(nm, ent))
      
Show_button = tk.Button(frame1, text="Show Attendance",fg="white" ,command=Show_attendance ,bg="green", width=15 ,height=1,activebackground = "white" ,font=('Helvetica', 12, ' bold '))
Show_button.place(x=35, y=200)

Clr_button = tk.Button(frame1, text="Clear",fg="white" ,command=clear_tree ,bg="red", width=17 ,height=1,activebackground = "white" ,font=('Helvetica', 12, ' bold '))
Clr_button.place(x=285, y=200)

#####################################################################################################################

def destroy():
  window.destroy()

quitWindow = tk.Button(frame1,text="Quit",fg="white",bg="red",width=35,height=1,command=destroy,activebackground = "white",font=('Helvetica', 15, ' bold '))
quitWindow.place(x=30, y=490)

############################################### END ###################################################################################################

#window.configure(menu=menubar)
window.mainloop()
