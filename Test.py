
# Written By Alex Jaeger and Blaise Koch UALR EAC 2015
### Tests stream_filter.py method choosing

from stream_filter import StreamFilter

s_filter = StreamFilter(0)

s_filter.add_operation(s_filter.printGoodBye)

s_filter.add_operation(s_filter.printHello, Value=1)
s_filter.add_operation(s_filter.printHello, Value=2)

s_filter.start()
