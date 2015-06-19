# Written By Blaise Koch and Alex Jaeger UALR EAC 2015


from CameraArray import *

import cv2
import sys, time

########################################################################
########################################################################

device_ids = [2, 1]
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
            continue

    try:
        while True:
            for dev in devices:
                frame = dev.get_frame()
                cv2.imshow("Device: " + str(dev.get_device_id()), frame)

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
