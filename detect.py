import cv2 
import numpy as np 
import imutils 
import winsound 
import threading 
import time 
import sys


# 1 pc 0 for webcam 
if len(sys.argv) > 1: 
    arg = int(sys.argv[1])
else: 
    arg = 0 

mode = arg

cap = cv2.VideoCapture(mode, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

# get first frame 
# compare difference with the next frame 
# if difference is high enough = motion = alarm 
_, start_frame = cap.read() 
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY) 
start_frame  = cv2.GaussianBlur(start_frame, (21,21),0)

alarm = False 
alarm_mode = False 
alarm_cnt = 0 

def beep(): 
    global alarm 
    for _ in range(5): 
        if not alarm_mode: 
            break 
        winsound.Beep(2500,1000)
    alarm = False 

while True:
    _, frame = cap.read() 
    frame = imutils.resize(frame, width=500)
    if alarm_mode: 
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5),0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25,255,cv2.THRESH_BINARY)[1]
        start_frame = frame_bw 

        if threshold.sum() > 300: # smaller the number the sensitive the detection 300  
            alarm_cnt +=1 
        else: 
            if alarm_cnt > 0: 
                alarm_cnt-=1 

        cv2.imshow('Cam', threshold)
    else: 
        cv2.imshow('cam', frame)
    
    if alarm_cnt > 20: 
        if not alarm: 
            alarm = True 
            threading.Thread(target=beep).start() 
    
    key = cv2.waitKey(30)
    if key == ord('t'): 
        time.sleep(5)
        alarm_mode = not alarm_mode
        alarm_cnt = 0 
    
    if key == ord('q'): 
        alarm_mode = False 
        break 

cap.release()
cv2.destroyAllWindows()


