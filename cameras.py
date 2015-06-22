# Written By Blaise Koch and Alex Jaeger UALR EAC 2015

from CameraArray import *

import cv2
import sys, time

########################################################################
########################################################################

device_ids = [0, 1]
devices = []

streams = []

if __name__ == "__main__":

	bg_sub_stream = StreamFilter(0)
	streams.extend([bg_sub_stream])

	bg_sub_stream.add_operation(bg_sub_stream.bg_subtraction, algo="MOG")

	bg_sub_stream.start()

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

				bg_sub_stream.add_frame(frame, dev.get_device_id())
				fg_mask = bg_sub_stream.get_frame()

				try:
					cv2.imshow("Device: " + str(dev.get_device_id()), fg_mask)
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
