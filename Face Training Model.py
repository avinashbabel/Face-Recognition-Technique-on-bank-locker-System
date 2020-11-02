import cv2
import numpy as np
from os import listdir
from os.path import isfile,join
import os
from datetime import datetime
import mysql.connector
data_path = "C:/faces2/"
mypath = os.listdir(data_path)
for i in mypath:
    sub_directory = data_path+i
    onlyfiles = [f for f in listdir(sub_directory) if isfile(join(sub_directory,f))]
#onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
Traning_Data, Labels = [],[]
for i in mypath:
    sub_directory1 = data_path + i
    for id, files in enumerate(onlyfiles):
        image_path = sub_directory1 + "/" + onlyfiles[id]
        images = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
        Traning_Data.append(np.asarray(images,dtype=np.uint8))
        Labels.append(id)
Labels = np.asarray(Labels, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Traning_Data),np.asarray(Labels))
model.write("C:/Users/'Dell/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/trainer/trainer1.yml")
print("Model Training Complete!!!")