# Written By Blaise Koch and Alex Jaeger UALR EAC 2015

from CameraArray import *

import cv2
import sys, time

########################################################################
########################################################################

device_ids = [0]

devices = {}
streams = {}

if __name__ == "__main__":

	for ID in device_ids:
		device = CameraDevice(ID)

		if device.acquire_camera():
			devices[ID] = device
			streams[ID] = StreamFilter(ID)
			
			streams[ID].add_operation(streams[ID].bg_subtraction, algo="MOG")
			streams[ID].add_operation(streams[ID].namefdsa)
			
			streams[ID].start()

		else:
			device.release_camera()
			del device
			continue

	try:
		while True:
			for dev_id in devices.keys():
				dev = devices[dev_id]
				stream = streams[dev_id]

				frame = dev.get_frame()

				stream.add_frame(frame, dev_id)
				frame = stream.get_frame()

				try:
					cv2.imshow("Device: " + str(dev_id), frame)
				except Exception:
					time.sleep(0.1)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	except KeyboardInterrupt:
		pass

	for dev_id in devices.keys():
		device = devices[dev_id]
		device.terminate()
		time.sleep(0.5) #wait for thread to shutdown

		device.release_camera()
		del device

	for stream_id in streams.keys():
		stream = streams[stream_id]

		stream.terminate()
		time.sleep(0.5) #wait for internal stuff to shutdown
		
		del stream

	cv2.destroyAllWindows()
