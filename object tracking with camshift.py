import cv2
import numpy as np
fourcc =cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('shouji.avi',fourcc,20.0,(720,528))
def click_event(event,x,y ,flag, param):
    if event ==cv2.EVENT_LBUTTONDOWN:


        strtet=str(x)+' ,'+str(y)
        font=cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame,strtet,(x,y),font,1,(255,255,0),3)
        cv2.imshow('image',frame)


cap=cv2.VideoCapture('phone.mp4')
ret ,frame = cap.read()
x,y,w,h= 550,500,150,200

track_window = (x,y,w,h)
roi = frame[y:y+h,x:x+w]

cv2.imshow('target',roi)

hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
mask =cv2.inRange(hsv_roi,np.array((0,60,32)),np.array((180,255,255)))
roi_hist =cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
#set up termination criteria
term_crit = (cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)
while(cap.isOpened()):

 ret, frame =cap.read()

 hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 dst =cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
 #apply meanshift to get new position
 ret, track_window = cv2.CamShift(dst,track_window,term_crit)

 x,y,w,h =track_window
 cv2.putText(frame,'my hand',(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(123,255,3),2)
 pts = cv2.boxPoints(ret)
 pts =np.int0(pts)
 frame = cv2.polylines(frame,[pts],True,(0,0,255),3)


#draw picture
 #x,y,w,h =track_window
 #cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),3)

 cv2.imshow('image',frame)
 cv2.setMouseCallback('image', click_event)
 cv2.imshow('dst',dst)
 out.write(frame)
 if cv2.waitKey(60) ==27:
     break
cap.release()
cv2.destroyAllWindows()