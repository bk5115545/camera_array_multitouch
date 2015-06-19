
import sys, time

import CameraArray
import cv2
########################################################################
########################################################################

device_ids = [0, 1]
devices = []
streams = []

if __name__ == "__main__":
		for ID in device_ids:
			device = CameraDevice(ID)
			s_filter = StreamFilter(ID)

			if device.acquire_camera():
				device.start()
				devices.extend([device])
			else:
				device.release_camera()
				del device
				continue

			s_filter.start()
			streams.extend([s_filter])


		try:
			while True:
				for dev in devices:
					frame = dev.get_frame()
					streams[dev.get_device_id()].add_frame(frame) #automatically shows stream

				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

		except KeyboardInterrupt:
			pass

		for device in devices:
			device.terminate()
			time.sleep(0.5) #wait for thread to shutdown

			device.release_camera()
			del device

		cv2.destroyAllWindows()
