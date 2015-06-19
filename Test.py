

### Tests stream_filter.py method choosing


from stream_filter import StreamFilter


s_filter = StreamFilter(0)

s_filter.add_operation(s_filter.printHello)
s_filter.add_operation(s_filter.printGoodBye)


s_filter.evaluate_operations()
