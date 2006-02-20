class vh:
    def __init__(self):
        pass

    def trimlongline(self, item, size=72): #{{{
        if len(item) >= size:
            item = item[0:size/4] + "..." + item[-1*((size-size/4)-3):]
        return item
#}}}
