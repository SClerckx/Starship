import requests 
import cv2, time
import numpy as np
import _thread

#1280x720
#720x480
url1 = "http://192.168.0.206:8080" + "/shot.jpg"
url2 = "http://192.168.0.199:8080" + "/shot.jpg"

def trackURL(url):
	started = False
	prevTime = 0

	while True:
		#https://www.youtube.com/watch?v=-mJXEzSD1Ic
		img_resp = requests.get(url)
		img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
		img = cv2.imdecode(img_arr, -1)

		if not started:
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			initBB = cv2.selectROI("Frame" + url, img, fromCenter=False,showCrosshair=True)
			# start OpenCV object tracker using the supplied bounding box
			# coordinates, then start the FPS throughput estimator as well

			tracker = cv2.legacy_TrackerMOSSE.create()

			# Initialize tracker with first frame and bounding box
			ok = tracker.init(img, initBB)

			started = True

		else:
			#https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/
			#https://www.youtube.com/watch?v=1FJWXOO1SRI

			# grab the new bounding box coordinates of the object
			(success, box) = tracker.update(img)
			# check to see if the tracking was a success
			
			#if success:
			#	(x, y, w, h) = [int(v) for v in box]
			#	cv2.rectangle(img, (x, y), (x + w, y + h),
			#		(0, 255, 0), 2)
			#cv2.imshow("AndroidCam" + url, img)
			
			curTime = time.time()
			fps = 1/(curTime - prevTime)
			prevTime = curTime
			print(fps)

			if cv2.waitKey(1) == 27:
				break

_thread.start_new_thread(trackURL, (url1, ))
_thread.start_new_thread(trackURL, (url2, ))

while 1:
	pass