
#include "camera_device.h"

CameraDevice::CameraDevice(int id) {
    device_id = id;

    screen_width = 0;
    screen_height = 0;
}

CameraDevice::CameraDevice(int id, int width, int height) {
    device_id = id;
    screen_width = width;
    screen_height = height;
}

int CameraDevice::GetDeviceId() {
    return device_id;
}

int CameraDevice::GetScreenWidth() {
    return screen_width;
}

int CameraDevice::GetScreenHeight() {
    return screen_height;
}
