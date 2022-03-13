import cv2 
import time
import scipy as sp
import numpy as np
from threading import Thread

resolution = (1280,720)
# 720x480
url1 = "http://192.168.137.39:8080/video"
url2 = "http://192.168.137.229:8080/video"

#https://stackoverflow.com/questions/58293187/opencv-real-time-streaming-video-capture-is-slow-how-to-drop-frames-or-get-sync
class ThreadedCamera(object):
	def __init__(self, src, position = None, e1 = None, e2 = None):
		self.src = src
		self.capture = cv2.VideoCapture(src)
		self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

		self.FPS = 1/200 #Upper bound
		self.FPS_MS = int(self.FPS * 1000)

		# Start frame retrieval thread
		self.viewThread = Thread(target=self.update, args=())
		self.viewThread.daemon = True
		self.viewThread.start()

	def update(self):
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()
				self.newFrame = True
			time.sleep(self.FPS)

	def show_frame(self):
		cv2.imshow(self.src, self.frame)
		cv2.waitKey(self.FPS_MS)
		startPoint = (int(resolution[0]/2)-20, int(resolution[1]/2))
		endPoint = (int(resolution[0]/2)+20, int(resolution[1]/2))
		cv2.line(self.frame, startPoint, endPoint, (0,255,0), thickness=10) #crosshair horizontal
		startPoint = (int(resolution[0]/2), int(resolution[1]/2)-20)
		endPoint = (int(resolution[0]/2), int(resolution[1]/2)+20)
		cv2.line(self.frame, startPoint, endPoint, (0,255,0), thickness=10) #crosshair vertical	
		
if __name__ == '__main__':
	threaded_camera1 = ThreadedCamera(url1)
	threaded_camera2 = ThreadedCamera(url2)
	while True:
		try:
			threaded_camera1.show_frame()
			threaded_camera2.show_frame()
		except AttributeError:
			print("pass")
			pass
		