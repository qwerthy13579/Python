#!/usr/bin/env python
import logging
logging.basicConfig(level = logging.INFO)

import time
import cv2
import sys
import numpy
import os
import pyrealsense as pyrs
size = 4
fn_haar = '/home/buddha/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
fn_dir = '/home/buddha/Desktop/opencv/att_faces'

print('Training...')

(images, lables, names, ids) = ([],[],{},0)
for(sudirs, dirs, files) in os.walk(fn_dir):
	for subdir in dirs:
		names[ids] = subdir
		subjectpath = os.path.join(fn_dir, subdir)
		for filename in os.listdir(subjectpath):
			path = subjectpath + '/' + filename
			lable = ids
			images.append(cv2.imread(path, 0))
			lables.append(int(lable))
		ids += 1
(im_width, im_height) = (130, 100)

(images, lables) = [numpy.array(lis) for lis in [images,lables]]
global modle
modle = cv2.face.createFisherFaceRecognizer()
modle.train(images, lables)

face_cascade = cv2.CascadeClassifier(fn_haar)

pyrs.start()
webcam = pyrs.Device()


while True:
	webcam.wait_for_frame()
	im = webcam.colour

    	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    	faces = face_cascade.detectMultiScale(gray,1.3, 5)
    	for(x,y,w,h) in faces:
		cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
		face = gray[y:y+h, x:x+w]
		face_resize = cv2.resize(face,(im_width, im_height))
		prediction = modle.predict(face_resize)
		cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)

		if prediction[1]<500:
			cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,0))
		else:
			cv2.putText(im,'Unknown Person',(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255))

	cv2.imshow('Opencv', im)
	key = cv2.waitKey(10)
	if key == 27:
		break
