import cv2
import keyboard
from deepface import DeepFace
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if success:
        resp = DeepFace.find(img_path=img,db_path= "static/images", model_name = 'Facenet',enforce_detection=True,distance_metric='cosine')
        print(resp)
        if not resp.empty:
            name=resp[resp['Facenet_cosine']==min(resp['Facenet_cosine'])]['identity'].values[0]
            #name=name.split('.')[0].split('/')[1]
        else:
            name='unknown'
        cv2.putText(img, name,(100,100), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 2)     
        cv2.waitKey(1)
        cv2.imshow('image',img)
    if keyboard.is_pressed('esc'):
        break
cv2.destroyAllWindows()
cap.release()
