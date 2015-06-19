
# Written By Blaise Koch and Alex Jaeger UALR EAC 2015
### Tests stream_filter.py method choosing

from CameraArray import StreamFilter

s_filter = StreamFilter(0)

s_filter.add_operation(s_filter.bg_subtraction_mog, algo="MOG2")

s_filter.start()
