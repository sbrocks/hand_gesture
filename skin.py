import cv2
import numpy as np 

cap = cv2.VideoCapture(0)

i=0
while True:
	ret,frame = cap.read()
	cv2.imshow("frame",frame)
	cv2.imwrite("skin"+str(i)+".jpg",frame)
	i=i+1
	if cv2.waitKey(1)==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()