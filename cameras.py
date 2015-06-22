# Written By Blaise Koch and Alex Jaeger UALR EAC 2015

from CameraArray import *

import cv2
import sys, time

########################################################################
########################################################################

device_ids = [0]
devices = []

stream_ids = [0]
streams = []

if __name__ == "__main__":
	
	for ID in stream_ids:
		stream = StreamFilter(ID)
		
		stream.add_operation(stream.bg_subtraction, algo="MOG")
		#stream.add_operation(stream.blob_detection)

		streams.extend([stream])
		streams[ID].start()

	for ID in device_ids:
		device = CameraDevice(ID)

		if device.acquire_camera():
			device.start()
			devices.extend([device])
		
		else:
			device.release_camera()
			del device
			continue

	try:
		while True:
			for dev in devices:
				frame = dev.get_frame()
				
				streams[dev.get_device_id()].add_frame(frame, dev.get_device_id())
				frame = streams[dev.get_device_id()].get_frame()
				frame = streams[dev.get_device_id()].blob_detection(frame)
				
				try:
					cv2.imshow("Device: " + str(dev.get_device_id()), frame)
				except Exception:
					time.sleep(0.1)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	except KeyboardInterrupt:
		pass

	for device in devices:
		device.terminate()
		time.sleep(0.5) #wait for thread to shutdown

		device.release_camera()
		del device

	bg_sub_stream.terminate()
	time.sleep(0.5)
	del bg_sub_stream

	cv2.destroyAllWindows()
