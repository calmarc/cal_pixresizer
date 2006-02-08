#!/usr/bin/env python
# Copyright (C) 2006 http://www.calmar.ws {{{
# http://www.calmar.ws/resize/COPYING
# }}}
def get_spin_focus(widget, spinname): #{{{ OK
    general[spinname].set_active(True)
#}}}
def delete_event(widget, event, data=None): #{{{ OK
    gtk.main_quit()
    return False
#}}}
def quit_widget(widget, data): #{{{ OK
    data.hide()
    data.destroy()
#}}}
def quit_self(self, *args): #{{{ OK
    self.hide()
    self.destroy()
#}}}
def setvalue(widget, data): #{{{ OK
    global general
    imgprocess[data[0]] = data[1]
#}}}
def setcombo(combobox): #{{{ OK
    global imgprocess
    model = combobox.get_model()
    active = combobox.get_active()
    if active >= 0:
        imgprocess["ftype"]=model[active][0]
#}}}
def trimlongline(loc_item, size=72): #{{{ OK
    if len(loc_item) >= size:
        loc_item = loc_item[0:size/4] + "..." + loc_item[-1*((size-size/4)-3):]
    return loc_item
#}}}
def create_radios(vbox,values,text, id_radio, default): #{{{ OK
    for i in range(len(values)):
        if i == 0: # first should not get other radios as reference
            radio = None
        radio = gtk.RadioButton(radio, text[i])
        radio.connect("toggled", setvalue, (id_radio, values[i]))
        vbox.pack_start(radio, True, True, 0)
        if values[i] == default:
            radio.set_active(True)
    return radio # return last radio thing for spinner
#}}}
def update_preview_cb(file_chooser, preview): #{{{   don't close preview maybe
    try:
        filename = file_chooser.get_preview_filename()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 160, 160)
        preview[0].set_from_pixbuf(pixbuf)
        pil_img = Image.open(filename)
        size = os.path.getsize(filename)
        preview[1].set_markup("<b>" + os.path.split(filename)[1] + "</b>")
        preview[2].set_markup(str(pil_img.size[0]) + " x " + str(pil_img.size[1]))
        preview[3].set_markup( str(size/1024) + " kb")
        have_preview = True
    except:
        have_preview = False

    file_chooser.set_preview_widget_active(have_preview)
    return
#}}}
def open_filechooser(widget, event, data=None): #{{{
    global general

    dialog = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_select_multiple(True)

    vbox = gtk.VBox(True, 0)
    vbox.show()
    dialog.set_extra_widget(vbox)

    hbutton_box = gtk.HButtonBox()
    hbutton_box.set_layout(gtk.BUTTONBOX_DEFAULT_STYLE)
    vbox.pack_start(hbutton_box, True, True, 0)
    hbutton_box.show()

    button = gtk.Button(_("select all pics"))
# color
#    map = button.get_colormap()
#    colour = map.alloc_color("#440000")

#    style = button.get_style().copy()
#    style.bg[gtk.STATE_NORMAL] = colour
#    button.set_style(style)

    button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#cccccc"))

    button.show()
    button.connect("clicked", lambda w, d: d.select_all(), dialog)
    hbutton_box.add(button)

    label = gtk.Label()
    label.set_markup("<b>Ctrl</b> + " + _("left mouse  click - for adding items") +\
            "\n<b>Shift</b> + " + _("left mouse click - for ranges"))
    label.show()
    vbox.pack_start(label, False, False, 0)


    filter = gtk.FileFilter()
    filter.set_name(" Images ")
    filter.add_mime_type("image/jpeg")
    for i in [
        "avs", "bmp", "cgm", "dcx", "dib", "eps", "fax", "fig", "fits", "fpx", "gif",
        "hdf", "jbig", "jpg" "jpeg", "ico", "map", "matte", "miff", "mng", "mpeg", "mtv",
        "null", "pbm", "pcd", "pcl", "pcx", "pdf", "pgm", "pict", "plasma", "png",
        "pnm", "ppm", "ps", "ps2", "p7", "rad", "rgb", "rla", "rle", "sgi", "sun",
        "tga", "tiff", "tiff24", "tile", "uil", "uyvy", "vid", "viff", "xc", "xbm",
        "xpm", "xwd", "yuv" ]:
            filter.add_pattern("*." + i)

    dialog.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name(_(" all "))
    filter.add_pattern("*")
    dialog.add_filter(filter)

# preview widget
    dialog.set_use_preview_label(False)
    preview = gtk.VBox(False)
    preview.set_size_request(162,162)
    label = gtk.Label()
    label.set_alignment(0.5,1)
    label.show()
    preview.pack_start(label, False, False, 0)
    label2 = gtk.Label()
    label2.set_alignment(0.5,1)
    label2.show()
    preview.pack_start(label2, False, False, 0)
    label3 = gtk.Label()
    label3.set_alignment(0.5,1)
    label3.show()
    preview.pack_start(label3, False, False, 0)
    image = gtk.Image()
    image.show()
    preview.pack_start(image, False, False, 10)
    dialog.set_preview_widget(preview)
    dialog.set_preview_widget_active(False)

    dialog.connect("update-preview", update_preview_cb, (image, label, label2, label3))

# starting folder
    if general["pic_folder"] == "":
        if sys.platform in ["win32", "win16", "win64"]:
          homevar = os.getenv("HOMEDRIVE")
          homevar += "\\" + str(os.getenv("HOMEPATH"))
          if os.path.exists(homevar + "\My Documents"): homevar += "\My Documents"
          elif os.path.exists(homevar + "\Eigene Dateien"): 
             print "judihui"
             homevar += "\Eigene Dateien"
        else:
          homevar = os.getenv("HOME")
        if os.path.exists(homevar):
            dialog.set_current_folder(homevar)
    else:
        dialog.set_current_folder(general["pic_folder"])

#DELETE
#    dialog.set_current_folder("/home/calmar/pics/Auto_Salon_2005/ppp")
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        general["pic_folder"] = dialog.get_current_folder()
        print "nach:" + general["pic_folder"]
        imgprocess["files_todo"] =  dialog.get_filenames()
        labeltext=""
        if len(imgprocess["files_todo"]) == 1:
            labeltext += "\n\n" + trimlongline(imgprocess["files_todo"][0]) + "\n\n"
        elif len(imgprocess["files_todo"]) == 2:
            labeltext += "\n" + trimlongline(imgprocess["files_todo"][0]) + "\n" +\
                    trimlongline(imgprocess["files_todo"][1]) + "\n\n"
        elif len(imgprocess["files_todo"]) == 3:
            labeltext += "\n" + trimlongline(imgprocess["files_todo"][0]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][1]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][2]) + "\n"
        elif len(imgprocess["files_todo"]) == 4:
            labeltext +=  trimlongline(imgprocess["files_todo"][0]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][1]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][2]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][3]) + "\n"
        elif len(imgprocess["files_todo"]) == 5:
            labeltext +=  trimlongline(imgprocess["files_todo"][0]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][1]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][2]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][3]) + "\n"  +\
                    trimlongline(imgprocess["files_todo"][4]) 
        else:
            for i in range(0,3):
                labeltext += trimlongline(imgprocess["files_todo"][i]) +"\n"
            labeltext += ".....\n" 
            labeltext += trimlongline(imgprocess["files_todo"][-1])
        general["todolabel"].set_text(labeltext)
        counter=0
        print "## Die Bilder Auswahl:"
        print
        for file in imgprocess["files_todo"]:
            counter += 1
            string = "%3s: " + trimlongline(file,66)
            print string % (str(counter))
        print

    elif response == gtk.RESPONSE_CANCEL:
        dialog.destroy()
    dialog.destroy()
#}}}
def show_error_dialog(text): #{{{ (seems) OK
    global general
    mesbox = gtk.Dialog("Achtung:", general["window"], gtk.DIALOG_MODAL, ()) 
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)    
    label = gtk.Label()
    label.set_markup(text)
    mesbox.vbox.pack_start(label, True, True, 10)
    label.show()

    button = gtk.Button(_("quit processing"))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", error_destroy, (mesbox,"quit"))
    button.show()
    button = gtk.Button(_("skip and go on..."))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", error_destroy, (mesbox,"skip"))
    button.show()
    button.grab_focus()
    mesbox.show()
    mesbox.run()
#}}}
def error_destroy(widget, data): #{{{ (merge with overwritedestroy?) OK 
    global general
    general["what_error"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def show_overwrite_dialog(file): #{{{ (seems) OK
    global general
    mesbox = gtk.Dialog(_("Attention:"), general["window"], gtk.DIALOG_MODAL, ()) 
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)    
    label = gtk.Label()
    label.set_markup(_("Target picture <b>already exists</b>:") + "\n\n" + trimlongline(file,68))
    mesbox.vbox.pack_start(label, True, True, 10)
    label.show()

    button = gtk.Button(_("quit processing"))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", overwrite_destroy, (mesbox,"cancel"))
    button.show()

    button = gtk.Button(_("skip"))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", overwrite_destroy, (mesbox,"skip"))
    button.grab_focus()
    button.show()

    button = gtk.Button(_("overwrite"))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", overwrite_destroy, (mesbox,"overwrite"))
    button.show()
    button = gtk.Button(_("ALL overwrite"))
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", overwrite_destroy, (mesbox,"all_overwrite"))
    button.show()
    mesbox.show()
    mesbox.run()
#}}}
def overwrite_destroy(widget, data): #{{{ OK
    global general
    general["what_todo"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def show_mesbox(text): #{{{ OK
    mesbox = gtk.Dialog(_("Calmar's Picture Resizer"), general["window"], gtk.DIALOG_MODAL,\
            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)) 
    mesbox.connect("destroy", quit_self)
    mesbox.connect("delete_event", quit_self)    
    label = gtk.Label()
    label.set_markup(text)
    label.show()
    mesbox.vbox.pack_start(label, True, True, 15)
    mesbox.show()
    response = mesbox.run()
    mesbox.destroy()
#}}}
def label_nopic(): #{{{  OK
    general["todolabel"].set_markup("\n\n  <b>-- " + _("no pictures are selected") + " --</b> \n\n")
#}}}
def label_progress(count, tot, text, colorstring): #{{{ OK
    general["todolabel"].set_markup("\n\n<b>" + _("progress") + " (" + count + "/" + tot +\
            "): <span " + colorstring + ">" + text + "</span></b>\n\n")
#}}}
def start_resize(widget, event, data=None): #{{{ (probably) OK 
    global general
    global imgprocess

# messagebox when there are no files selexted
    if len(imgprocess["files_todo"]) == 0:
        show_mesbox(_("Select some <b>pics</b> to work on"))
        return

# get data for processing, well maybe messagebox for stripping?
    prefix = imgprocess["entry1"].get_text().strip()
    suffix = imgprocess["entry2"].get_text().strip()
    folder = imgprocess["entry3"].get_text().strip()

    if imgprocess["width"] == "0": # then, the spinner is selected
        imgprocess["width"] = str(imgprocess["spinWidth"].get_value_as_int())
    if imgprocess["height"] == "0":
        imgprocess["height"] = str(imgprocess["spinHeight"].get_value_as_int())
    if imgprocess["quality"] == "0":
        imgprocess["quality"] = str(imgprocess["spinQuality"].get_value_as_int())


# messagebox when there is no suff, pre or folder
    if prefix == "" and suffix == "" and folder == "" and imgprocess["ftype"] == "":
        text = _("""  At least <u>one</u> must be set:  

             -> <b>Prefix</b>
             -> <b>Suffix</b>
             -> <b>subfolder to create in</b>
             -> <b>picture type</b>
 
 in order to prevent overwriting the original pictures""")
        show_mesbox(text)
        return

# to get the path of sample file
    splitfile = os.path.split(imgprocess["files_todo"][0])

# create folder when needed
    if folder != "" and not os.path.exists(splitfile[0] + "/" +folder):
        print "##" + _("create new folder: ") + folder + "  (" + \
                trimlongline(splitfile[0],38) + "/" + folder + ")"
        print
        os.mkdir(splitfile[0] + "/" + folder)
    else:
        print _("# sub-folder exists already")

    if str(imgprocess["width"]) == "99999":
       width_here = _("unlimited")
    else:
       width_here = imgprocess["width"]

    if str(imgprocess["height"]) == "99999":
       height_here = _("unlimited")
    else:
       height_here = imgprocess["height"]

    print """\
## Erstelle die Bilder: max. Breite: %-s
                        max. Hoehe:  %-s 
                        Qualitaet:   %-s 
                        Ordner:      %-s 
                        Prefix:      %-s 
                        Suffix:      %-s
                        Convert to:  %-s""" % \
                              (width_here, height_here, imgprocess["quality"],\
                              folder, prefix, suffix, imgprocess["ftype"])

    print
    total = len(imgprocess["files_todo"])
    counter=0
    dist = ""
    for sourcefile in imgprocess["files_todo"]:
        counter += 1

        splitfile = os.path.split(sourcefile)
        resultpath = splitfile[0] + "/"  # targetdir of pics
        if folder != "":
            resultpath += folder + "/" 

        fname,ext=os.path.splitext(splitfile[1]); 
        if imgprocess["ftype"] == "":
            target_ext = ext
        else:
            target_ext = imgprocess["ftype"]

        resultfile = resultpath + prefix + fname + suffix + target_ext
# for py2exe only (looking for the convert.exe in the same dir...)
        if sys.platform == "win32":
            command = general["cwd"] + "convert.exe " + '"' + sourcefile + '"' + " -resize " + str(imgprocess["width"]) + "x" + str(imgprocess["height"])\
                + " -quality " + str(imgprocess["quality"]) + ' "' + resultfile + '"'
        else:
            command = "convert " + '"' + sourcefile + '"' + " -resize " + str(imgprocess["width"]) + "x" + str(imgprocess["height"])\
                + " -quality " + str(imgprocess["quality"]) + ' "' + resultfile + '"'

# wait and update
        while gtk.events_pending():
            gtk.main_iteration(False)

        if dist == "":
            dist = len(splitfile[1]) + 1 # sourcefile (no path) + 1

# print what you're going to do... preparation here
        command_print = "convert: " + "%-" + str(dist) + "s --> " + trimlongline(resultfile,58 - dist )

#        text =  trimlongline(folder,30) + "/" + prefix + fname + suffix + ext
        text =  trimlongline(folder,30) + "/" + prefix + fname + suffix + ext
        text = trimlongline(resultfile,58 - dist )
        label_progress(str(counter), str(total), text,"") 
        print command_print % (splitfile[1][-1*(dist-1):]) # maximum initial file lenght (dist-1)

# source und target the same?   refuse then      
        if sourcefile == resultfile:
            text = _("<b>source</b> and <b>target</b> are the same!") + "\n\n" +\
_("(...cowardly refuses to overwrite)")
            print "#### " + _("source and target are the same!") + " ####"
            show_error_dialog(text)
            if general["what_error"] != "skip":
                imgprocess["files_todo"]=[]
                label_progress(str(counter),str(total),_("stopped!"),"color='#550000'") 

                while gtk.events_pending():
                    gtk.main_iteration(False)
                time.sleep(2.0)
                label_nopic()
                print
                print _("# converting has stopped ")
                print
                return
            else:
                continue

# check if file exists and may show 'overwrite dialog'
        if os.path.exists(resultfile):
            if general["what_todo"] != "all_overwrite":
                show_overwrite_dialog(resultfile)
        if general["what_todo"] == "skip":
            general["what_todo"] = ""
            print _("# skipped: ") + trimlongline(resultfile,58)
            continue
        elif general["what_todo"] == "cancel":
            general["what_todo"] = ""
            imgprocess["files_todo"]=[]
            label_progress(str(counter),str(total),_("stopped!"),"color='#550000'") 
            while gtk.events_pending():
                gtk.main_iteration(False)
            time.sleep(2.0)
            label_nopic()
            print
            print _("# converting has stopped ")
            print

            return
        elif general["what_todo"] == "overwrite":
            general["what_todo"] = ""

# the actual work
        if sys.platform in ["win32", "win16", "win64"]:
             exitstatus = [0, _("no further details unter MS Win, sorry")]
             exitstatus[0] = os.system(command)
        else:
             exitstatus = commands.getstatusoutput(command)
        if exitstatus[0] != 0:
# there was an error, print and ask what to do
            text = _("Imagemagick terminated with an <b>error</b> while working on:") + " \n\n " +\
                    sourcefile + " \n\n<b>" +  str(exitstatus[0]) + ": " + exitstatus[1] +\
                    "</b>\n\n" + _("(may contact mac@calmar.ws )  ")
            print "#### " + _("ERROR while working on that picture") + "####"
            print str(exitstatus[0]) + ": " + exitstatus[1]
            print
            show_error_dialog(text)
            if general["what_error"] != "skip":
                imgprocess["files_todo"]=[]
                label_progress(str(counter),str(total), _("canceled!"),"color='#550000'") 
                while gtk.events_pending():
                    gtk.main_iteration(False)
                time.sleep(2.4)
                label_nopic()
                print _("# converting has stopped ")
                return

    print
    print _("# the pics got generated")
    print 

    label_progress(str(total),str(total), _("finish!"),"color='#000070'") 

    while gtk.events_pending():
        gtk.main_iteration(False)
    time.sleep(2.0)

    general["what_todo"] = ""
    imgprocess["files_todo"]=[]
    folder=""
    label_nopic()
#}}}
def main(): #{{{ OK

    global imgprocess

    print "==============================="
    print "Calmar's Picture Resize Utility"
    print "==============================="
    print

    general["window"].set_title("Calmar's Picture Resizer - http://www.calmar.ws")
    general["window"].set_default_size(500,300)
    general["window"].connect("delete_event", delete_event)
    general["window"].set_border_width(10)

    mainbox = gtk.VBox(False, 0)
    general["window"].add(mainbox)

#########################################################################
# buttons  in top hbox

    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/calmar.png")
    box.pack_start(image, False, False , 0)

    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/exit.png")
    but_quit = gtk.Button()
    hbox=gtk.HBox()
    hbox.pack_end(image, False, False, 0)
    but_quit.add(hbox)
    label = gtk.Label(_("exit"))
    hbox.pack_end(label, False, False, 0)

    but_quit.connect("clicked", delete_event, None)
    box.pack_end(but_quit, False, False, 0)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)

#########################################################################
#  vbox for radios below

    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

#### width

    vbox = gtk.VBox(False, 0)
    box.pack_start(vbox, False, False, 20)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("max. width") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "1600 x ...", "1280 x ...", "1024 x ...", "800 x ...", "640 x ...",\
            "480 x ...", "120 x ...", "specific:" ]
    values = [ "99999", "1600", "1280", "1024", "800", "640", "480", "120" ,"0"]
    default = "99999"
    general["radio_width"] = create_radios(vbox, values, text, "width", default)
    imgprocess["width"] = 99999

    imgprocess["spinWidth"].set_wrap(False)
    vbox.pack_start(imgprocess["spinWidth"], False, False, 0)


## height

    vbox = gtk.VBox(False, 0)
    box.pack_start(vbox, False, False, 20)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("max. height") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "... x 1200", "... x 1024",  "... x 768", "... x 600", "... x 480",\
             "... x 320", "... x 80", _("specific:") ]
    values = [ "99999", "1200", "1024", "768", "600", "480", "320", "80", "0"]
    default = "768"
    general["radio_height"] = create_radios(vbox, values, text, "height", default)
    imgprocess["height"] = 768

    imgprocess["spinHeight"].set_wrap(False)
    vbox.pack_start(imgprocess["spinHeight"], False, False, 0)

## quality

    vbox = gtk.VBox(False, 0)
    box.pack_start(vbox, False, False, 20)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("quality") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ "100%", "97%", "94%", "90%", "85%", "80%", "70%", "50%", _("specific")]
    values = [ "100", "97", "94", "90", "85", "80", "70", "50", "0"]
    default = "94"
    general["radio_quality"] = create_radios(vbox, values, text, "quality", default)
    imgprocess["quality"] = 94

    imgprocess["spinQuality"].set_wrap(False)
    vbox.pack_start(imgprocess["spinQuality"], False, False, 0)

#### prefix/suffix/folder

    vbox = gtk.VBox(False, 0)
    box.pack_start(vbox, False, False, 20)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>&lt;' + _("PREFIX") + '&gt;</b></span>file.jpg')
    vbox.pack_start(label, False, False, 0)
    imgprocess["entry1"].set_alignment(0.5)
    vbox.pack_start(imgprocess["entry1"], False, False, 0)

    label = gtk.Label()
    label.set_markup('\nfile<span foreground="#000060"><b>&lt;' + _("SUFFIX") + '&gt;</b></span>.jpg')

    vbox.pack_start(label, False, False, 0)
    imgprocess["entry2"].set_alignment(0.5)
    vbox.pack_start(imgprocess["entry2"], False, False, 0)

    label = gtk.Label()
    label.set_markup('\n<span foreground="#000060"><b>' + _("sub-folder") + "</b></span>, " +\
            _("for\nthe <u>new</u> pics"))
    vbox.pack_start(label, False, False, 0)
    imgprocess["entry3"].set_alignment(0.5)
    vbox.pack_start(imgprocess["entry3"], False, False, 0)

    label = gtk.Label()
    label.set_markup("\n" + _("<b>convert</b> to:"))
    vbox.pack_start(label, False, False, 0)
    combo = gtk.combo_box_new_text()
    combo.set_wrap_width(3)
    list = ["", ".jpg", ".png", ".tif", ".pdf" ,".bmp", ".gif", ".ico",\
            ".pbm", ".xpm", ".pcd" ]
    for ext in list:
        combo.append_text(ext)
    combo.set_active(0)
    vbox.pack_start(combo, False, False, 0)
    combo.connect('changed', setcombo)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)

#########################################################################
# label 

    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

    label_nopic()
    box.pack_start(general["todolabel"], False, False , 0)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)

#########################################################################
# buttons  in last box

    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/open.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("select pictures...  "))
    hbox.pack_end(label, False, False, 0)
    but_files = gtk.Button()
    but_files.add(hbox)
    but_files.connect("clicked", open_filechooser, None)
    box.pack_start(but_files, False, False, 0)

    but_files.grab_focus()

    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/go.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("start converting  "))
    hbox.pack_end(label, False, False, 0)
    but_start = gtk.Button()
    but_start.add(hbox)
    but_start.connect("clicked", start_resize, None)
    box.pack_end(but_start, False, False, 0)

#########################################################################
# show

    font_desc = pango.FontDescription("Courier")
    if font_desc:
        general["todolabel"].modify_font(font_desc)


    general["window"].show_all()

    gtk.main()
    return 0      
#}}}
#imports... vars...  {{{ OK
import os, sys,  time, glob, commands
import gtk, pygtk, pango
# PIL needs some help, when py2exe-d
import Image, PngImagePlugin, JpegImagePlugin

# for pyexe only: comment out
#pygtk.require('2.0')

import gettext
gettext.textdomain('cal_pixresizer')
_ = gettext.gettext

#if gtk.pygtk_version < (2,4,0):
#   print "PyGtk 2.4.0"
#   raise SystemExit

# general (global) - used on many function
radio_bogus = gtk.RadioButton() #radio_ must be radio, gtk calls it before assigned
general = { "todolabel"    : gtk.Label(), 
            "what_todo"    : "",
            "what_errror"  : "",
            "pic_folder"   : "",
            "radio_width"  : radio_bogus,
            "radio_height" : radio_bogus,
            "radio_quality" : radio_bogus,
            "window" : gtk.Window(gtk.WINDOW_TOPLEVEL)}

if sys.path[0][-12:] == "\library.zip":  #for py2exe
    general["cwd"] = sys.path[0][0:-12] + "/"
else:
    general["cwd"] = sys.path[0] + "/"
gettext.bindtextdomain('cal_pixresizer', general["cwd"] + "locale")

# imgprocess (global)- data (source) for image processing
imgprocess = { "entry1" : gtk.Entry(15),
               "entry2" : gtk.Entry(15),
               "entry3" : gtk.Entry(25),
               "ftype" : "",
               "files_todo" : [],
               "width" : 0,
               "height" : 0 ,
               "quality" : 0}
adj = gtk.Adjustment(1024, 30, 2000, 1, 100, 0)
adj.connect("value_changed", get_spin_focus, "radio_width" )
imgprocess["spinWidth"] = gtk.SpinButton(adj, 1.0, 0)
imgprocess["spinWidth"].set_numeric(True)  #spinnervalue needed later
adj = gtk.Adjustment(768, 30, 2000, 1, 100, 0)
adj.connect("value_changed", get_spin_focus, "radio_height" )
imgprocess["spinHeight"] = gtk.SpinButton(adj, 1.0, 0)
imgprocess["spinHeight"].set_numeric(True)
adj = gtk.Adjustment(90, 10, 100, 1, 10, 0)
adj.connect("value_changed", get_spin_focus, "radio_quality" )
imgprocess["spinQuality"] = gtk.SpinButton(adj,0.1, 0)
imgprocess["spinQuality"].set_numeric(True)

if __name__ == "__main__":
    main()
#}}}
