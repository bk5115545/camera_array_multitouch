

### Tests stream_filter.py method choosing


import CameraArray


s_filter = StreamFilter(0)

s_filter.add_operation(s_filter.printHello)
s_filter.add_operation(s_filter.printGoodBye)


s_filter.evaluate_operations()
