import cv2
import numpy as np

roi = cv2.imread('res_test.jpg')
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
#cv2.waitKey(0)
# Open the webcam
cap = cv2.VideoCapture(0)

# kernel size depends on the image resolution
kernelOpen = np.ones((15,15))
kernelClose = np.ones((60,60))


while True:
	ret,frame = cap.read()

	#target = cv2.imread('skin163.jpg')
	frame = cv2.resize(frame,(360,240))
	cv2.imshow("frame",frame)
	hsvt = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	# calculating object histogram
	roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
	# normalize histogram and apply backprojection
	cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
	dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)
	# Now convolute with circular disc
	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	cv2.filter2D(dst,-1,disc,dst)
	# threshold and binary AND
	ret,thresh = cv2.threshold(dst,50,255,0)
	thresh = cv2.merge((thresh,thresh,thresh))

	maskOpen = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernelOpen)
	maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

	maskFinal = maskClose
	res = cv2.bitwise_and(frame,maskClose)
	resorig = cv2.bitwise_and(frame,thresh)

	# resorig is workiing best
	# Work to be done on resorig
	#res = np.vstack((frame,thresh,res))
	cv2.imshow("thresh",thresh)
	cv2.imshow("res",res)
	cv2.imshow("resorig",resorig)
	cv2.imshow("maskClose",maskClose)
	cv2.imshow("maskOpen",maskOpen)
	#cv2.imwrite('res.jpg',res)

	if cv2.waitKey(1)==ord('q'):
		break

# Release the webcam
cap.release()
cv2.destroyAllWindows()

