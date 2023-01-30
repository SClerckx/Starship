import cv2 
import time
import scipy as sp
from scipy.spatial.transform import Rotation
import numpy as np
from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

resolution = (1280,720)
# 720x480
url1 = "http://192.168.0.200:8080//video"
#url1 = "http://10.0.117.254:8080//video"
#url2 = "http://10.0.119.72:8080//video"

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
		
		time.sleep(self.FPS*10) #Wait for high probability of first frame being ready for Box selection

		initBox = cv2.selectROI(src, self.frame, fromCenter=False,showCrosshair=True)
		self.tracker = cv2.TrackerCSRT.create()#cv2.legacy_TrackerMOSSE.create()
		self.tracker.init(self.frame, initBox)

		self.trackThread = Thread(target=self.track_frame, args=())
		self.trackThread.daemon = True
		self.trackThread.start()

		if position.any():
			self.position = position
		
		if e1.any():
			self.e1 = e1
			self.e2 = e2

		self.ray = e1
		self.angularResolution = 0.000605338*1.5 #rad/pix

	#def stopThreads(self):
		#self.viewThread.stop()
		#self.trackThread.stop()

	def update(self):
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()
				self.newFrame = True
			time.sleep(self.FPS)

	def show_frame(self):
		cv2.imshow(self.src, self.frame)
		cv2.waitKey(self.FPS_MS)
		if self.success:
			(x, y, w, h) = [int(v) for v in self.box]
			cv2.rectangle(self.frame, (x, y), (x + w, y + h),(0, 255, 0), 2)

	def track_frame(self):
		prevTime = time.time()
		while True:
			if self.newFrame:
				(self.success, self.box) = self.tracker.update(self.frame)
				self.newFrame = False
				self.getRay()
			time.sleep(self.FPS*2)
			currTime = time.time()
			print("trackDT: ",  currTime - prevTime)
			prevTime = currTime

	def getRay(self):
		(x, y, w, h) = [int(v) for v in self.box]
		center = (x + w/2, y + h/2)
		centerFromMiddle = (center[0]-resolution[0]/2, center[1]-resolution[1]/2)
		angle = (centerFromMiddle[0] * self.angularResolution, centerFromMiddle[1] * self.angularResolution)
		rotationVector1 = np.cross(self.e1, self.e2)
		rotationVector1 = rotationVector1 / np.linalg.norm(rotationVector1)
		rotation1 =  Rotation.from_rotvec(angle[0] * rotationVector1)
		intermediateRay = rotation1.apply(self.e1)
		rotationVector2 = np.cross(intermediateRay, rotationVector1)
		rotationVector2 = rotationVector2 / np.linalg.norm(rotationVector2)
		rotation2 = Rotation.from_rotvec(angle[1] * rotationVector2)
		self.ray = rotation2.apply(intermediateRay)
		#print(self.src + str(self.ray))

	def getLine(self,t):
		point = self.position + t*self.ray
		print(point)
		return point

def arrayTo2d(array):
	return np.array([[array[0]], [array[1]], [array[2]]])

def calculatePosition():
	cam1Ray = arrayTo2d(threaded_camera1.ray)
	cam2Ray = arrayTo2d(threaded_camera2.ray)
	cam1pos = arrayTo2d(threaded_camera1.position)
	cam2pos = arrayTo2d(threaded_camera2.position)

	A = np.hstack((cam1Ray, - cam2Ray))
	B = cam2pos - cam1pos

	x = np.linalg.lstsq(A,B)[0]

	solution = (threaded_camera1.getLine(x[0][0]) + threaded_camera2.getLine(x[1][0]))/2

	print(solution)
	return solution

plt.ion()
if __name__ == '__main__':
	threaded_camera1 = ThreadedCamera(url1, position=np.array([2.13, 0, 0]), e1 = np.array([-1, 0, 0]), e2 = np.array([0, 1, 0]))
	#threaded_camera2 = ThreadedCamera(url2, position=np.array([0, 1.36, 0]), e1 = np.array([0, -1, 0]), e2 = np.array([-1, 0, 0]))
	prevTime = time.time()
	plt.show()
	solutions = []
	while True:
		currentTime = time.time()
		if currentTime - prevTime > 0.1:
			#solutions.append(calculatePosition())
			prevTime = currentTime

		try:
			pass
			threaded_camera1.show_frame()
			#threaded_camera2.show_frame()
		except AttributeError:
			print("pass")
			pass
	


		