import cv2 
import sys          

if len(sys.argv) > 1: 
    arg = int(sys.argv[1]) 
else: 
    arg = 0 

mode = arg 
cap = cv2.VideoCapture(mode, cv2.CAP_DSHOW) 
while True: 
    ret, frame = cap.read()
    if not ret: 
        break 
    frame = cv2.flip(frame,1)
    cv2.imshow('live', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release() 
cv2.destroyAllWindows()
