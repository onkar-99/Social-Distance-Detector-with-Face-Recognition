# Social-Distance-Detector-with-Face-Recognition
In this repository, we would be determining if the people are following social distancing norms and then sending them email based on the output of Facial Recognition


##Introduction
Social distancing is arguably the most effective non pharmaceutical way to prevent the spread of a disease. Our goal is to develop a software which can be used to detect distance between a group of people using a webcam or from video . As per the option selected, our system will find the distance between the people and generate a green bounding box if it is permissible, and a red bounding box if social distance is not followed and send the person notifications.

## Method:
First we detected people from the frames using Yolov3. Based on the coordinates we got for those people, we calculated the centroid for them. Later we found the distance between those centroids using Euclidean distance formula. If that distance is within the social distancing limits, we declared that the people are not following social distancing, and if the distance value is larger than social distancing threshold, we declared that the people are following social distancing. 
Incase, people were found to be breaking social distancing norms, then we use Face Recognition using Facenet, and compare the person from the people's database to get their contact information and send them a mail about social distancing norms not being followed. 
Additionally, we can connect multiple webcams at once and perform social distance detection simultaneously. 

The intended use of this project is for commercial reasons, where we have database with people/students/employees information like their images and their contact numbers.
There has been GUI given to add employee data into the database. 

##Deployement
The project was converted into an exe build using PyInstaller and converted into a Desktop Application for windows. 

##Output
The output below shows two camera feeds, where in both feeds people are following social distancing norms. 
![img][]
