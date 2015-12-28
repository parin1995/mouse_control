import numpy as np
import cv2
from Xlib import X, display



print 'Calibration:'
m=[False,False,False,False,False]
cap = cv2.VideoCapture(-1)
p=False
roi = np.zeros([23*5,23,3])
count=0
while(cap.isOpened()):#center
	ret, frame=cap.read()
	row,col,ch=frame.shape
	
	cv2.rectangle(frame,(305,225),(330,250),(0,255,0),1)#center
	cv2.imshow('frame',frame)
	
	if m[0]:	
		
		roi[0*23:0*23+23,0:23]=frame[227:250, 307:330]
		break
	ch = 0xFF & cv2.waitKey(1) 
	if ch == 27:
        	break
        if ch == ord('1'):
        	m[0]=True	

while(cap.isOpened()):#left
	ret, frame=cap.read()
	cv2.rectangle(frame,(15,225),(40,250),(0,255,0),1)#top
	
	cv2.imshow('frame',frame)
	if m[1]:
		roi[1*23:1*23+23,0:23]=frame[227:250, 17:40]
		break

	ch = 0xFF & cv2.waitKey(1) 
	if ch == 27:
        	break	
	if ch == ord('2'):
        	m[1]=True
while(cap.isOpened()):#right
	ret, frame=cap.read()
	row,col,ch=frame.shape
	cv2.rectangle(frame,(605,225),(630,250),(0,255,0),1)#bottom
	cv2.imshow('frame',frame)
	if m[2]:
		roi[2*23:2*23+23,0:23]=frame[227:250, 607:630]
		break
	ch = 0xFF & cv2.waitKey(1) 
	if ch == 27:
        	break
	if ch == ord('3'):
        	m[2]=True
while(cap.isOpened()):#top
	ret, frame=cap.read()
	row,col,ch=frame.shape
	cv2.rectangle(frame,(305,15),(330,40),(0,255,0),1)#left
	cv2.imshow('frame',frame)
	if m[3]:
		roi[3*23:3*23+23,0:23]=frame[17:40, 307:330]
		break
	ch = 0xFF & cv2.waitKey(1) 
	if ch == 27:
        	break
	if ch == ord('4'):
        	m[3]=True
while(cap.isOpened()):#bottom
	ret, frame=cap.read()
	cv2.rectangle(frame,(305,440),(330,465),(0,255,0),1)#right
	cv2.imshow('frame',frame)
	if m[4]:
		roi[4*23:4*23+23,0:23]=frame[442:465, 307:330]
		break
		
	
		
	ch = 0xFF & cv2.waitKey(1) 
	if ch == 27:
        	break
	if ch == ord('5'):
        	m[4]=True
        	p=True

if p:
	
	cv2.imwrite('roi.jpg',roi);
	roi=cv2.imread('roi.jpg')
	cv2.destroyWindow('frame')
	cv2.imshow('roi',roi)
	hsv_roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
	roihist = cv2.calcHist([hsv_roi],[0, 1], None, [180, 256], [0, 180, 0, 256] )

	while(True):
		ret, frame=cap.read()
		cv2.imshow('frame',frame)
		hsv_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
		dst = cv2.calcBackProject([hsv_frame],[0,1],roihist,[0,180,0,256],1)
		
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
		cv2.filter2D(dst,-1,disc,dst)
		ret,thresh = cv2.threshold(dst,50,255,cv2.THRESH_BINARY)
		thresh = cv2.merge((thresh,thresh,thresh))
	
		
		res = cv2.bitwise_and(frame,thresh)

		cv2.GaussianBlur(dst, (3,3), 0, dst)

		kernel = np.ones((5,5),np.uint8)
	
		imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
		
		thresh = cv2.erode(thresh,kernel,iterations = 2)
		thresh = cv2.dilate(thresh,kernel,iterations = 2)

		thresh = cv2.dilate(thresh,kernel,iterations = 2)
		thresh = cv2.erode(thresh,kernel,iterations = 2)
		edges = cv2.Canny(thresh,100,200)
		cv2.imshow('thresh',thresh)
		cv2.imshow('edges',edges)

		contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		cont=frame.copy()
		

		larea=0
		lindex = 0
		area=0
		l=len(contours)
		
		if l>0:
			for i in range(0,l):
				cnt=contours[i]
				area=cv2.contourArea(cnt)
				if area > larea:
					larea=area
					lindex=i
				
			
			cnt=contours[lindex]		
			cv2.drawContours(cont, [cnt], 0, (0,255,0), 3)	
			cv2.imshow('contours',cont)
			center=frame.copy()
		
			M = cv2.moments(cnt)
			if int(M['m00']) is not 0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				cv2.circle(center, (cx, cy), 4, (0, 255, 0), -1)
				
		
		
			if count is 0:
				cx1=cx
				cy1=cy
		
			
			cx1=cx
			cy1=cy
			cv2.imshow('center',center)
			d = display.Display()
			s = d.screen()
			root = s.root
			root.warp_pointer(2*cx,2*cy)
			d.sync()
			count=1
		ch = 0xFF & cv2.waitKey(1) 
		if ch == 27:
        		break
		
cap.release()
cv2.destroyAllWindows()
