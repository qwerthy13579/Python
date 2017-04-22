#!/usr/bin/env python
import logging
logging.basicConfig(level = logging.INFO)
import cv2
import time
import sys
import os
import numpy
import pyrealsense as pyrs


fn_haar = '/home/buddha/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
fn_dir = '/home/buddha/Desktop/opencv/att_faces'
fn_name= sys.argv[1]
path = os.path.join(fn_dir, fn_name)
size = 4

if not os.path.isdir(path):
	try:	
		os.mkdir(path)
		print("New Person Created")
	except OSError as e:
		if e.errno == 17:
			os.chmod(path, 0777);


	


(im_width, im_height)=(130,100)
face_cascade = cv2.CascadeClassifier(fn_haar)

pyrs.start()
webcam = pyrs.Device()



count = 0
while count < 30:
	
	webcam.wait_for_frame()
	im = webcam.colour
	im = cv2.flip(im,1,0)
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	mini = cv2.resize(gray,(gray.shape[1]/size, gray.shape[0]/size))
	faces = face_cascade.detectMultiScale(mini)
	faces = sorted(faces, key=lambda x: x[3])
	'''for(x,y,w,h) in faces:
		cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
		face = gray[y:y+h, x:x+w]
		face_resize = cv2.resize(face,(im_width, im_height))
		cv2.imwrite('%s/%s.png' % (path,count),face_resize)
	count += 1'''
	if faces:
		face_i = faces[0]
		(x,y,w,h) = [v * size for v in face_i]
		face = gray[y:y+h,x:x+w]
		face_resize = cv2.resize(face, (im_width, im_height))
		pin = sorted([int(n[:n.find('.')])for n in os.listdir(path)
			if n[0]!='.']+[0])[-1]+1
		cv2.imwrite('%s/%s.png' % (path,pin), face_resize)
		cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)
		
	count += 1

	
	cv2.imshow('Opencv', im)
	key = cv2.waitKey(5)
	if key == 27:
		break
print("Updated!")
