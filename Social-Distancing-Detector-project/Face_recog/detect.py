import cv2 
import numpy as np
import mtcnn
from Face_recog.architecture import *
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
from sklearn.preprocessing import Normalizer
import ctypes
import os
import pandas as pd
from datetime import datetime
import keyboard

class get_name:
    def __init__(self):
        self.face_encoder = InceptionResNetV2()
        path_m = "Face_recog/facenet_keras_weights.h5"
        self.face_encoder.load_weights(path_m)
        encodings_path = 'Face_recog/encodings/encodings.pkl'
        self.face_detector = mtcnn.MTCNN()
        with open(encodings_path, 'rb') as f:
            self.encoding_dict = pickle.load(f)

    def record_face(self,name):
        if os.path.isfile('record_face.csv'):
            df=pd.read_csv('record_face.csv')
        else:
            df=pd.DataFrame(columns=['Name','Day','Time'])
            
        if name in df['Name'].values:
            return
        else:
            day=datetime.now().strftime('%Y-%m-%d')
            time=datetime.now().strftime('%H:%M')
    
            df.loc[len(df)]=[name,day,time]
            df.to_csv('record_face.csv',index=False)
            ctypes.windll.user32.MessageBoxW(0, 'Recorded for {}'.format(name), 'SUCCCESS!!!', 0)
            return
                    
    def normalize(self,img):
        mean, std = img.mean(), img.std()
        return (img - mean) / std
    
    def get_face(self,img, box):
        x1, y1, width, height = box
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = img[y1:y2, x1:x2]
        return face, (x1, y1), (x2, y2)
    
    def get_encode(self, face, size):
        face = self.normalize(face)
        face = cv2.resize(face, size)
        encode = self.face_encoder.predict(np.expand_dims(face, axis=0))[0]
        return encode
        
    def return_name(self,img):
        confidence_t=0.99
        recognition_t=0.5
        required_size = (160,160)
        l2_normalizer = Normalizer('l2')
    
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_detector.detect_faces(img_rgb)
        name = 'unknown'
        names=[]
        for res in results:
            if res['confidence'] < confidence_t:
                continue
            face, pt_1, pt_2 = self.get_face(img_rgb, res['box'])
            encode = self.get_encode(face, required_size)
            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            name = 'unknown'
    
            distance = float("inf")
            for db_name, db_encode in self.encoding_dict.items():
                dist = cosine(db_encode, encode)
                if dist < recognition_t and dist < distance:
                    name = db_name
                    distance = dist
                    names.append([name,pt_1])
                    
        return names
    
            
        
    
