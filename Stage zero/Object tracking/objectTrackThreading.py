import cv2
import time
from threading import Thread

# 1280x720
# 720x480
# "rtsp://192.168.0.206:8080/h264_ulaw.sdp"
url1 = "http://192.168.0.199:8080/shot.jpg"
#url2 = "http://192.168.0.199:8080"


class ThreadedCamera(object):
	def __init__(self, src):
		self.src = src
		self.capture = cv2.VideoCapture(src)
		self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

		# FPS = 1/X
		# X = desired FPS
		self.FPS = 1/60
		self.FPS_MS = int(self.FPS * 1000)

		# Start frame retrieval thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()

	def update(self):
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()
			time.sleep(self.FPS)

	def show_frame(self):
		cv2.imshow(self.src, self.frame)
		cv2.waitKey(self.FPS_MS)


threaded_camera = ThreadedCamera(url1)
while True:
	try:
		threaded_camera.show_frame()
	except AttributeError:
		pass
