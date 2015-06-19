
#ifndef camera_device_h
#define camera_device_h

class CameraDevice {

    int device_id;
    int screen_width;
    int screen_height;

public:
    CameraDevice(int);
    CameraDevice(int, int, int);

    int GetDeviceId();
    int GetScreenWidth();
    int GetScreenHeight();

    void AcquireCamera();
    void ReleaseCamera();
};

#endif // camera_device_h
