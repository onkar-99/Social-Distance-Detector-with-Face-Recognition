import os 
import cv2
import mtcnn
import pickle 
import numpy as np 
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model

######pathsandvairables#########
face_data = 'C:/Users/pedne/Desktop/onkar/Face-recognition-Using-Facenet-On-Tensorflow-2.X-master/Faces/Onkar'

face_detector = mtcnn.MTCNN()


def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std


i=0
for image_name in os.listdir(face_data):
    i+=1
    image_path = os.path.join(face_data,image_name)

    img_BGR = cv2.imread(image_path)
    img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)

    x = face_detector.detect_faces(img_RGB)
    x1, y1, width, height = x[0]['box']
    x1, y1 = abs(x1) , abs(y1)
    x2, y2 = x1+width , y1+height
    face = img_BGR[y1:y2 , x1:x2]
    cv2.imwrite('Face_recog/Faces/Onkar/img'+str(i)+'.png',face)
        
       

