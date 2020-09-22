import cv2
import numpy as np
def in_side(o,i):
    ox,oy,ow,oh =o
    ix,iy,iw,ih = i
    return (ox>ix) and (oy>ix) and (ox+ow<ix+iw) and (oy+oh<iy+ih)
def draw_person(image,person):
    x,y,w,h =person
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2,cv2.LINE_AA)




cap = cv2.VideoCapture('FPS walker.mp4')

while(True):
 _,img =cap.read()




 #get the feature
 hog =cv2.HOGDescriptor()
 #use  svm detector to seperate the image data
 hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
 found ,w =hog.detectMultiScale(img)

 founder =[]

 for ri,r in enumerate(found):
    for qi ,q in enumerate(found):
        if ri!= qi and in_side(r,q):
            break
        else:
            founder.append(r)
 for person in founder:
    draw_person(img ,person)
 #img =cv2.resize(img,(596,596))
 cv2.imshow('pedestrain',img)

 if cv2.waitKey(10)==27 or cap.isOpened()==False:
     break

cap.release()
cv2.destroyAllWindows()
