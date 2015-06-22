
# Written By Alex Jaeger and Blaise Koch UALR EAC 2015

import sys, cv2
from threading import Thread, Event, Lock
import numpy as np

class CameraDevice(Thread):
	def __init__(self, device_id, width=None, height=None, stop_event=None):
		Thread.__init__(self)
		self.device_id = device_id
		self.width = width
		self.height = height
		self.stop_event = Event() if stop_event is None else stop_event

		self.acquired = False
		self.frame_lock = Lock()
		self.frame = None
		self.capture_lock = Lock()
		self.capture = None

	def acquire_camera(self):
		if self.acquired:
			return self.acquired
		else:
			with self.capture_lock:
				self.capture = cv2.VideoCapture(self.device_id)
			self.acquired = True

		if not self.capture.isOpened():
			try:
				with self.capture_lock:
					self.capture.open()
				self.acquired = True
			except Exception:
				return self.acquired

		if self.height is not None:
			try:
				with self.capture_lock:
					self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.height)
			except Exception as e:
				sys.stderr.write("Error setting capture height to " + str(self.height) + " on camera device " + str(self.device_id) + "\r\n")
				sys.stderr.write(str(e) + "\r\n")

		if self.width is not None:
			try:
				with self.capture_lock:
					self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.width)
			except Exception as e:
				sys.stderr.write("Error setting capture width to " + str(self.width) + " on camera device " + str(self.device_id) + "\r\n")
				sys.stderr.write(str(e) + "\r\n")

		self.acquired = True
		self.start()
		return self.acquired

	def release_camera(self):
		try:
			with self.capture_lock:
				self.capture.release()
				self.capture = None
			self.acquired = False
		except Exception:
			return False
		return True

	def terminate(self):
		self.stop_event.set()

	def get_frame(self):
		with self.frame_lock:
			if self.frame is not None:
				return self.frame
			else:
				return self.acquired

	def get_device_id(self):
		return self.device_id

	def run(self):
		while not self.stop_event.is_set():
			ret, frame = None, None
			with self.capture_lock:
				ret, frame = self.capture.read()

			if ret:
				with self.frame_lock:
					self.frame = frame
			else:
				sys.stderr.write("Problem reading frame for device " + str(self.device_id) + "\r\n")

	def get_height(self):
		with self.capture_lock:
			if self.capture:
				return self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) if self.height is None else self.height
			else:
				return -1

	def get_width(self):
		with self.capture_lock:
			if self.capture:
				return self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH) if self.width is None else self.width
			else:
				return -1
