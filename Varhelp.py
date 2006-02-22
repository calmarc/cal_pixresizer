def trimlongline(item, size=70):
    if len(item) >= size:
        item = item[0:size/4] + "..." + item[-1*((size-size/4)-3):]
    return item

def loc_enc(text, encod): 
    obj = unicode(text, 'utf-8')
    return obj.encode( encod)

def utf8_enc(text, encod):
    obj = unicode(text, encod)
    return obj.encode('utf-8')

def quit_self(widget, *args):
    widget.hide()
    widget.destroy()
