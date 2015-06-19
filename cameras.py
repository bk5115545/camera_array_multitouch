import cv2
import sys, time
from camera_device import CameraDevice

########################################################################
########################################################################

device_ids = [0, 1]
devices = []
	
if __name__ == "__main__":
        for ID in device_ids:
                device = CameraDevice(ID)
                if device.acquire_camera():
                        device.start()
                        devices.extend([device])
                else:
                        device.release_camera()
                        del device

        try:
                while True:
                        for dev in devices:
                                frame = dev.get_frame()
                                if frame is not None and frame is not False:
                                        cv2.imshow('Device: ' + str(dev.get_device_id()), frame)
                                else:
                                        print("wtf")
                
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
