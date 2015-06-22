
# Written By Alex Jaeger and Blaise Koch UALR EAC 2015

import numpy as np
import cv2
import Queue
import collections

from threading import Thread, Event, Lock
import time

class StreamFilter(Thread):
    def __init__(self, stream_id, shutdown_event = Event()):
        Thread.__init__(self)

        self.id = stream_id
        self.shutdown_event = shutdown_event

        self.input_queue  = Queue.Queue(maxsize = 100)
        self.output_queue = collections.deque(maxlen = 100) #keep most recent X frames
        
        self.input_lock = Lock()  #might as well do this anyway
        self.output_lock = Lock() #deque doesn't do it's own locking

        self.operations = []
        self.operations_lock = Lock()
        
        self.bg_subtractors = {
                                "MOG":cv2.BackgroundSubtractorMOG(),    \
                                "MOG2": cv2.BackgroundSubtractorMOG2(), \
##                              "GMG": cv2.BackgroundSubtractorGMG()    \
                              }


    def run(self):
        while not self.shutdown_event.is_set():
            frame = None
            device_id = -1
            try:
                with self.input_lock:
                    try:
                        frame, device_id = self.input_queue.get_nowait()
                    except Queue.Empty:
			time.sleep(0.01)
            except Queue.Empty:  #Queue.get has an implicit timeout that we should catch and try again on 
                continue

            operations_tmp = []
            with self.operations_lock:
                operations_tmp = self.operations
                
            for operation in operations_tmp:
                if not operation[1]:
                    frame = operation[0](frame)
                else:
                    frame = operation[0](frame, **operation[1])

            with self.output_lock:
		print("outputting: " + str(frame))
                self.outputQueue.put((frame, device_id))

    def get_id(self):
        return self.id

    def add_frame(self, frame, device_id=-1):
        with self.input_lock:
            if self.input_queue.full():
		return False
            self.input_queue.put((frame, device_id))
	return True

    def get_frame(self, latest = False, wait = False):
        img, device_id = None, None
        if wait:
            if latest:
                while img is None:
                    try:
                        with self.output_lock:
                            img, device_id = self.output_queue.popleft()
                        break
                    except IndexError:
                        time.sleep(0.01)
            else:
                while img is None:
                    try:
                        with self.output_lock:
                            img, device_id = self.output_queue.pop()
                        break
                    except IndexError:
                        time.sleep(0.01)
        else:
            try:
                if latest:
                    with self.output_lock:
                        img, device_id = self.output_queue.popleft()
                else:
                    with self.output_lock:
                        img, device_id = self.output_queue.pop()
            except IndexError:
                pass
        return img

    def clear_input_buffer(self):
        with self.output_lock:
            self.output_queue.clear()

    def add_operation(self, operation_name, **kwargs):
        with self.operations_lock:
            self.operations.extend([(operation_name, kwargs)])

    def terminate(self):
        self.shutdown_event.set()
        with self.input_lock:
            self.input_queue.empty()

    def bg_subtraction(self, frame, algo="MOG"):
        if isinstance(frame, (np.ndarray, np.generic)):
            try:
                return self.bg_subtractors[algo.uppercase()].apply(frame)
            except:
                return Exception("No such background subtraction algorithm.\nValid algorithms are " + ", ".join(bg_subtractors.keys()))
        else:
            return frame
