from PIL import Image,ImageTk
from tkinter import *
import tkinter as tk
import cv2
import numpy as np
import PIL
import tkinter.messagebox as tm
import csv
import pandas as pd
import os
from os import path
from tkinter_opencv import WebcamOnTkinter
from SocialDistancingDetector import Distance_Detector
import wmi
global root

def temp():
    if name_new.get():
        if os.path.exists('Employee_details.csv'):
            df=pd.read_csv('Employee_details.csv')
        else:
            df=pd.DataFrame(columns=['ID','Name','Email'])
        if name_new.get() not in df['Name'].values:
            df.loc[len(df)]=[id_new.get(),name_new.get(),email.get()]
            df.to_csv('Employee_details.csv',index = False)
        if not path.exists('Face_recog/Faces/'+name_new.get()):
            os.makedirs('Face_recog/Faces/'+name_new.get())
        Frame(root, bg='#b3c6ff',highlightbackground="black", highlightthickness=4,width=w-450, height=h, bd= 0).place(x=0,y=125)
        WebcamOnTkinter(name_new.get(),root)
    else:
        messagebox.showerror('Incomplete Data','Please enter all the details')

def new_emp():
    global id_new,name_new,email,root
    id_new = IntVar(root)
    name_new = StringVar(root)
    email = StringVar(root)
    Label(root, text="ID", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue',anchor=W).place(x=130, y=160)
    idd=Entry(root, textvariable=id_new).place(x=300, y=160)
    Label(root, text="Name", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue', anchor=W).place(x=130, y=220)
    name=Entry(root, textvariable=name_new).place(x=300, y=220)
    Label(root, text="Email", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue', anchor=W).place(x=130, y=280)
    pincode=Entry(root, textvariable=email).place(x=300, y=280)
    Button(root, text='Take Picture', width=20, font=("Open Sans", 13, 'bold'), bg='blue', fg='white',command=temp).place(x=500, y=460)

def view_camera():
    cameras=[]
    c = wmi.WMI()
    wql = "Select * From Win32_USBControllerDevice"
    for item in c.query(wql):
        q = item.Dependent.Caption
        if 'camera' in q.lower() or 'webcam' in q.lower():
            cameras.append(q)
    def get_index(btn,cameras):
        ind=cameras.index(btn.cget("text"))
        Distance_Detector(root,ind)
        
    for i,cam in enumerate(cameras):
        obj= Button(root, text=cam, width=19, font=("Open Sans", 10, 'bold'), bg='#b3d1ff', fg='black')
        obj.place(x=w-300, y=300 + (i+1)*70)
        obj.configure(command=lambda button=obj: get_index(button,cameras))
            
root = Tk()
root.title("Social Distancing Detector")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.state('zoomed')
Frame(root, bg='#b3c6ff',highlightbackground="black", highlightthickness=4,width=500, height=h, bd= 0).place(x=w-500,y=125)
Frame(root, bg='#b3c6ff',highlightbackground="black", highlightthickness=4,width=w-450, height=h, bd= 0).place(x=0,y=125)
Label(root, text="", bg='blue', width=w, height=8).place(x=0, y=0)
Label(root, text="Social Distancing Detector", height="2", font=("Calibri", 30,'bold'), fg='white',bg='blue').place(x=int(w/4)+130, y=10)
Button(root, text='View Available Cameras', width=19, font=("Open Sans", 15, 'bold'), bg='blue', fg='white',  command = view_camera).place(x=w-330, y=300)
Button(root, text='Add new Employee', width=19, font=("Open Sans", 15, 'bold'), bg='blue', fg='white',  command = new_emp).place(x=w-330, y=600)

root.mainloop()

