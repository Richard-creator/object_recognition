import cv2
import numpy as np

cap=cv2.VideoCapture('cap.mp4')
ret ,frame = cap.read()
x,y,w,h= 200,300,150,200

track_window = (x,y,w,h)
roi = frame[y:y+h,x:x+w]

cv2.imshow('target',roi)

hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
mask =cv2.inRange(hsv_roi,np.array((0,60,32)),np.array((180,255,255)))
roi_hist =cv2.calcHist([hsv_roi],[0],mask,[90],[0,90])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
#set up termination criteria
term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)
while(cap.isOpened()):

 ret, frame =cap.read()

 hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 dst =cv2.calcBackProject([hsv],[0],roi_hist,[0,90],1)
 #apply meanshift to get new position
 ret, track_window = cv2.meanShift(dst,track_window,term_crit)

#draw picture
 x,y,w,h =track_window
 cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),3)

 cv2.imshow('image',frame)
 cv2.imshow('dst',dst)
 if cv2.waitKey(30) ==27:
     break
cap.release()
cv2.destroyAllWindows()