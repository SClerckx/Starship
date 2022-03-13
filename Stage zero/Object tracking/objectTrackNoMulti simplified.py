import requests 
import cv2, time
import numpy as np
import _thread

#1280x720
#720x480
url1 = "http://192.168.0.206:8080" + "/shot.jpg"
url2 = "http://192.168.0.199:8080" + "/shot.jpg"

class Camera(object):
	def __init__(self, url):
		self.url = url
		self.started = False
		self.prevTime = 0
		self.update()
		
	def update(self):
		#https://www.youtube.com/watch?v=-mJXEzSD1Ic
		img_resp = requests.get(self.url)
		img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
		img = cv2.imdecode(img_arr, -1)

		cv2.imshow(self.url, img)
		
		curTime = time.time()
		fps = 1/(curTime - self.prevTime)
		self.prevTime = curTime
		print(fps)

		if cv2.waitKey(1) == 27:
			advance = False

cam1 = Camera(url1)
cam2 = Camera(url2)
advance = True

while advance:
	cam1.update()
	cam2.update()