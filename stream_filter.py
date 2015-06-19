
import numpy as np
import cv2
import Queue

from threading import Thread, Event

class StreamFilter():
    def __init__(self, stream_id):
        self.id = stream_id

        self.inputQueue = Queue.Queue()
        self.outputQueue = Queue.Queue()

        self.operations = []
        self.operations_args = []

    def get_frame(self):
        if self.outputQueue.empty() is False:
            return self.outputQueue.get()

    def add_operation(self, operation_name):
        self.operations.extend([operation_name])

    def add_frame(self, frame):
        self.inputQueue.put(frame)

    def evaluate_operations(self):
        for operation in self.operations:
            operation()

    def bg_subtraction(self, frame):
		if isinstance(frame, (np.ndarray, np.generic)):
			return self.bg_subtractor.apply(frame)
		else:
			return frame

    def printHello(self):
        print "Hello"

    def printGoodBye(self):
        print "Goodbye"
