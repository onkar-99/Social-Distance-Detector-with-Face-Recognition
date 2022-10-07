import numpy as np
import cv2
import imutils
import os
import time
from tkinter import *
from PIL import Image, ImageTk
from Face_recog.detect import get_name
from Face_recog.send_email import send_email
import pandas as pd

class Distance_Detector:
    def __init__(self,root,ind):
        self.vs = cv2.VideoCapture(ind) # capture video frames, 0 is your default video camera
        self.root=root
        self.vs.set(3, 1280)
        self.vs.set(4, 720)
        self.panel = Label(self.root, bg='blue',width=800)  # initialize image panel
        self.panel.place(x=130, y=250)
        self.frameno=0
        self.Setup()
        self.starttime=time.time()
        self.video_loop()
        self.l1=0
        self.gn=get_name()
        
    def video_loop(self):
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            current_img = frame.copy()
            current_img = imutils.resize(current_img, width=800,height=900)
            video = current_img.shape
            self.frameno += 1
            self.ImageProcess(current_img)
            Frame = self.processedImg
            Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(Frame)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.root.after(10, self.video_loop)  # call the same function after 30 milliseconds

    def get_email(self,name):
        df=pd.read_csv('Employee_details.csv')
        if name in df['Name'].values:
            email=df[df['Name']==name]['Email'].values   
            return email
        else:
            messagebox.showerror('Failure','Face not in Database')
            return []
        
    def Check(self,a,  b):
        dist = ((a[0] - b[0]) ** 2 + 550 / ((a[1] + b[1]) / 2) * (a[1] - b[1]) ** 2) ** 0.5
        calibration = (a[1] + b[1]) / 2
        if 0 < dist < calibration:
            return True
        else:
            return False

    def Setup(self):
        global net, ln, LABELS
        weights = 'yolov3.weights'
        config = 'yolov3.cfg'
        labelsPath = 'coco.names'
        #os.path.sep.join([yolo, "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")
        net = cv2.dnn.readNetFromDarknet(config, weights)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


    def ImageProcess(self,image):
        global processedImg
        (H, W) = (None, None)
        frame = image.copy()
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        confidences = []
        outline = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                maxi_class = np.argmax(scores)
                confidence = scores[maxi_class]
                if LABELS[maxi_class] == "person":
                    if confidence > 0.5:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        outline.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
        box_line = cv2.dnn.NMSBoxes(outline, confidences, 0.5, 0.3)


        if len(box_line) > 0:
            flat_box = box_line.flatten()
            pairs = []
            center = []
            status = []
            for i in flat_box:
                (x, y) = (outline[i][0], outline[i][1])
                (w, h) = (outline[i][2], outline[i][3])
                center.append([int(x + w / 2), int(y + h / 2)])
                status.append(False)

            for i in range(len(center)):
                for j in range(len(center)):
                    close = self.Check(center[i], center[j])
                    
                    if close:
                        pairs.append([center[i], center[j]])
                        status[i] = True
                        status[j] = True
                    
            index = 0

            for i in flat_box:
                (x, y) = (outline[i][0], outline[i][1])
                (w, h) = (outline[i][2], outline[i][3])
                if status[index] == True:
                    names=self.gn.return_name(frame)
                    for name in names:
                        cv2.putText(frame, name[0], name[1], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        if time.time() - self.starttime >=5:
                            if name[0] !='unknown':
                                email=self.get_email(name[0])
                                if len(email) !=0:
                                    send_email(email)
                                self.starttime=time.time()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
                elif status[index] == False:
                    self.starttime=time.time()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                index += 1
            for h in pairs:
                cv2.line(frame, tuple(h[0]), tuple(h[1]), (0, 0, 255), 2)
        self.processedImg = frame.copy()

