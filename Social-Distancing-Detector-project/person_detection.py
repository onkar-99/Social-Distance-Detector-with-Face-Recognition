import numpy as np
import cv2
import imutils
import os
import time
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import random 

class Distance_Detector:
    def __init__(self):
        self.vs = cv2.VideoCapture('rtsp://admin:Password@94.206.63.150:554/unicast/c3/s0/live') # capture video frames, 0 is your default video camera
        self.frameno=0
        self.Setup()
        self.starttime=time.time()
        self.person_count=0
        self.vehicle_count=0
        self.video_loop()
        
        
    def video_loop(self):
        while True:
            ok, frame = self.vs.read()  # read frame from video stream
            if ok:  # frame captured without any errors
                current_img = frame.copy()
                current_img = imutils.resize(current_img, width=800,height=900)
                video = current_img.shape
                self.frameno += 1
                self.ImageProcess(current_img)
                Frame = self.processedImg
                cv2.imshow('result',Frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            else:
                break
        cv2.destroyAllWindows()
        self.vs.release()
       

        
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
        #ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


    def ImageProcess(self,image):
        global processedImg
        pcount=0
        vcount=0
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
            for ind,i in enumerate(flat_box):
                pcount+=1
                (x, y) = (outline[i][0], outline[i][1])
                (w, h) = (outline[i][2], outline[i][3])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)
        self.processedImg = frame.copy()
        if pcount > self.person_count:
            self.person_count=pcount
            print(self.person_count)

Distance_Detector()