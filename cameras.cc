
// To compile:g++ cameras.cc camera_device.cc

#include "camera_device.h"
#include <iostream>

int main() {
    CameraDevice *cd = new CameraDevice(0);

    std::cout << cd->GetDeviceId();

    return 0;
}
