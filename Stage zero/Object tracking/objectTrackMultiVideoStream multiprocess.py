from math import fabs
import cv2 
import time
import scipy as sp
from scipy.spatial.transform import Rotation
import numpy as np
import multiprocessing as mp

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

resolution = (1280,720)
# 720x480
url1 = "http://10.0.117.254:8080//video"
url2 = "http://10.0.119.72:8080//video"

#https://stackoverflow.com/questions/58293187/opencv-real-time-streaming-video-capture-is-slow-how-to-drop-frames-or-get-sync

def cameraProcess(src):
	capture = cv2.VideoCapture(src)
	capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

	FPS = 1/200 #Upper bound
	FPS_MS = int(FPS * 1000)

	newFrame = False
	while not newFrame:
		if capture.isOpened():
			(status, frame) = capture.read()
			newFrame = True

	initBox = cv2.selectROI(src, frame, fromCenter=False,showCrosshair=True)
	tracker = cv2.TrackerCSRT.create()#cv2.legacy_TrackerMOSSE.create()
	tracker.init(frame, initBox)

	prevTime = time.time()

	newFrame = False
	while True:
		if (time.time() - prevTime > FPS):
			if capture.isOpened() and not newFrame:
				(status, frame) = capture.read()
				newFrame = True

		success = False
		if newFrame:
			(success, box) = tracker.update(frame)
			newFrame = False

			print("detection: ", time.time() - prevTime)
			prevTime = time.time()
		
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
		cv2.imshow(src, frame)
		cv2.waitKey(FPS_MS)

			#time.sleep(FPS*2)
			


if __name__ == '__main__':
	manager = mp.Manager()
	read = manager.list() 

	p1 = mp.Process(target=cameraProcess, args=(url1,), daemon=True)
	p1.start()

	p2 = mp.Process(target=cameraProcess, args=(url2,), daemon=True)
	p2.start()

	while True:
		if len(read) > 0:
			print(read[-1])
	p.join()
	


		