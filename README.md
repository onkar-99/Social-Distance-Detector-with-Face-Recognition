# Social-Distance-Detector-with-Face-Recognition
In this repository, we would be determining if the people are following social distancing norms and then sending them email based on the output of Facial Recognition. This is a group project done in my Final Year of Computer Engineering


##Introduction
Social distancing is arguably the most effective non pharmaceutical way to prevent the spread of a disease. Our goal is to develop a software which can be used to detect distance between a group of people using a webcam or from video . As per the option selected, our system will find the distance between the people and generate a green bounding box if it is permissible, and a red bounding box if social distance is not followed and send the person notifications.

## Method:
First we detected people from the frames using Yolov3. Based on the coordinates we got for those people, we calculated the centroid for them. Later we found the distance between those centroids using Euclidean distance formula. If that distance is within the social distancing limits, we declared that the people are not following social distancing, and if the distance value is larger than social distancing threshold, we declared that the people are following social distancing. 
Incase, people were found to be breaking social distancing norms, then we use Face Recognition using Facenet, and compare the person from the people's database to get their contact information and send them a mail about social distancing norms not being followed. 
Additionally, we can connect multiple webcams at once and perform social distance detection simultaneously. 

The intended use of this project is for commercial reasons, where we have database with people/students/employees information like their images and their contact numbers.
There has been GUI given to add employee data into the database. 

## Implementation
You can download the Facenet weights required for Face Recognition from [here](https://drive.google.com/file/d/1BsBvasz-oniSqmbIgPmGLjMm5V4JGmjw/view?usp=sharing) and YOLOv3 weights file from [here](https://drive.google.com/file/d/1y8Qz1oAzqLdlG1lSs8LmXgSkr6PEHPgn/view?usp=sharing). 
Place the Facenet Face Recognition files in the Face_Recog folder and place the YOLOv3 weights file in the BASE folder

Place the images of the people in your database in the Faces folder in Face_recog. Make sure to make folders with their name and put images in those folders respectively. 
Then simply run index.py for checking output

## Deployement
The project was converted into an exe build using PyInstaller and converted into a Desktop Application for windows. The bundled exe can be downloaded from [here](https://drive.google.com/file/d/1KQWlaQMQLaBI4rgTD5VYyrcoGQCvRTPL/view?usp=sharing)
You can place it in the BASE folder for the program to run successfully.

## Output
The output below shows two camera feeds, where in both feeds people are following social distancing norms. 

<img src="/Social-Distancing-Detector-project/social_distance1.PNG" width="50%" height="50%">

In below example we got people not following social distancing norms, ie they are standing close to eachother, and hence are shown in red.

<img src="/Social-Distancing-Detector-project/social_distance2.PNG" width="50%" height="50%">

## Results
The YOLO model used performs is very efficient with Person Detection

<img src="/Social-Distancing-Detector-project/yoloResults.PNG" width="50%" height="50%">

The results of our model are shown below along with the precision and recall achieved by us.

<img src="/Social-Distancing-Detector-project/precisionRecall.PNG" width="50%" height="50%">




