import cv2 as cv
import numpy as np
from ml_engine import Ml_engine
from datetime import datetime
#capture the video through camera
cap=cv.VideoCapture(0)
now=datetime.now()

#set and call the model from another file 
model_path="kasih path"
ml=Ml_engine(model=model_path)


while True:
    failed,frame=cap.read()
    if not failed:
        print("failed to read the frame")
        break

    Boxes=ml.predict(frame)

    #olah boxes
    if Boxes is not None:
        for box in Boxes:
            x,y,w,h,confidence=box
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv.putText(frame,f"{confidence:.2f}",(x,y-10),cv.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

        #save image
        file_name="nama file"+str(now)+".jpg"
        cv.imwrite(file_name,frame)


    cv.imshow("frame", frame)

    