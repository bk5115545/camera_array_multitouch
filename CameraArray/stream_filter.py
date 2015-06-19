
# Written By Alex Jaeger and Blaise Koch UALR EAC 2015

from threading import Thread, Event
import numpy as np
import cv2
import Queue

from threading import Thread, Event

class StreamFilter(Thread):
    def __init__(self, stream_id):
        Thread.__init__(self)

        self.id = stream_id

        self.inputQueue = Queue.Queue()
        self.outputQueue = Queue.Queue()

        self.operations = []

    def get_id(self):
        return self.id

    def add_frame(self, frame, device_id=-1):
        self.inputQueue.put((frame, device_id))

    def get_frame(self):
        if self.outputQueue.empty() is False:
            return self.outputQueue.get()

    def add_operation(self, operation_name, **kwargs):
        self.operations.extend([(operation_name, kwargs)])

    ##########
    # Operations
    ##########

    def bg_subtraction(self, frame):
		if isinstance(frame, (np.ndarray, np.generic)):
			return self.bg_subtractor.apply(frame)
		else:
			return frame

    def printHello(self, frame, Value=0):
        print "Hello " + str(Value)

    def printSomething(self, frame, Value=0, Blah=0):
        print "Something " + str(Value) + str(Blah)

    def printGoodBye(self, frame):
        print "Goodbye"

    ##########
    # Run Function
    ##########

    def run(self):
        while True:
        #    frame, device_id = self.inputQueue.get(True)
            frame = None

            for operation in self.operations:
                #print operation[1]
                if not operation[1]:
                    frame = operation[0](frame)
                else:
                    frame = operation[0](frame, **operation[1])

        #    self.outputQueue.put((frame, device_id))
