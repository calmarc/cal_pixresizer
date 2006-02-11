#!/usr/bin/env python
# master branch
# Copyright (C) 2006 http://www.calmar.ws {{{
# http://www.calmar.ws/resize/COPYING
# }}}
# help functions         SUBROUTINES {{{
def dialog_2_destroy(widget, data): #{{{ (merge with overwritedestroy?) OK 
    global general
    general["what_error"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def update_preview_cb(file_chooser, preview): #{{{ OK
    try:
        filename = file_chooser.get_preview_filename()
        preview[1].set_markup("<b>" + os.path.split(filename)[1] + "</b>")
        if os.path.isfile(filename):
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 200, 125)
            preview[0].set_from_pixbuf(pixbuf)
            img = Image.open(filename)
            size = os.path.getsize(filename)
            if size/1024 == 0:
                bytes = str(size) + " bytes"
            else:
                bytes = str(size/1024) + " Kb"
            preview[2].set_markup(str(img.size[0]) + " x " + str(img.size[1]))
            preview[3].set_markup( bytes)
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(general["cwd"] +\
                    "bilder/folder.png", 96, 96)
            preview[0].set_from_pixbuf(pixbuf)

            preview[2].set_markup("<b>"+ str(len(os.listdir(filename))) +\
                    _("</b> items inside"))
            preview[3].set_markup("")
    except:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(general["cwd"] +\
                "bilder/file.png", 96, 96)
        preview[0].set_from_pixbuf(pixbuf)
        try:
            size = os.path.getsize(filename)
            size = str(size/1024) + " kb"
        except (TypeError, OSError):
            size = ""
        preview[2].set_markup( size )
        preview[3].set_markup(" ")
    file_chooser.set_preview_widget_active(True)
    return
#}}}
def overwrite_destroy(widget, data): #{{{ OK
    global general
    general["what_todo"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def get_spin_focus(widget, spinname): #{{{ OK
    global general
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
def trimlongline(loc_item, size=72): #{{{ OK
    if len(loc_item) >= size:
        loc_item = loc_item[0:size/4] + "..." + loc_item[-1*((size-size/4)-3):]
    return loc_item
#}}}
def entries_cb(editable, id_edit): #{{{ OK
    global imgprocess
    posi = editable.get_position()
    char = editable.get_chars(posi, posi+1)
    if char == " ":  # replace spaces with underlines
        editable.delete_text(posi,posi+1)
        editable.insert_text("_", posi)
    imgprocess[id_edit] = editable.get_text()
#}}}
def setcombo(combobox): #{{{ OK
    global imgprocess
    model = combobox.get_model()
    active = combobox.get_active()
    if active >= 0:
        imgprocess["ftype"]=model[active][0]
#}}}
#}}}
# little gui
def show_2_dialog(parent_widget, text, button_quit, button_ok): #{{{ (seems) OK
    global general
    mesbox = gtk.Dialog(_("attention:"), parent_widget, gtk.DIALOG_MODAL, ()) 
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)    
    label = gtk.Label()
    label.set_markup(text)
    mesbox.vbox.pack_start(label, True, True, 10)
    label.show()

    button = gtk.Button(button_quit)
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", dialog_2_destroy, (mesbox,"quit"))
    button.show()
    button = gtk.Button(button_ok)
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", dialog_2_destroy, (mesbox,"ok_pressed"))
    button.show()
    button.grab_focus()
    mesbox.show()
    mesbox.run()
#}}}
def show_overwrite_dialog(file): #{{{ (seems) OK
    global general
    mesbox = gtk.Dialog(_("attention:"), general["window"], gtk.DIALOG_MODAL, ()) 
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
    button.connect("clicked", overwrite_destroy, (mesbox,"ok_pressed"))
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
def label_nopic(): #{{{  OK
    general["todolabel"].set_markup("\n\n  <b>-- " + _("no pictures are selected") + " --</b> \n\n")
#}}}
def label_progress(count, tot, text, colorstring): #{{{ OK
    general["todolabel"].set_markup("\n\n<b>" + _("progress") + " (" + count + "/" + tot +\
            "): <span " + colorstring + ">" + text + "</span></b>\n\n")
#}}}
def show_mesbox(parent, text): #{{{ OK
    mesbox = gtk.Dialog(_("Calmar's Picture Resizer"), parent, gtk.DIALOG_MODAL,\
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
# FileChooser callbacks
def open_filechooser(widget, event, data=None): #{{{
    global general

    dialog = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_select_multiple(True)

    vbox = gtk.VBox(False, 0)
    vbox.show()
    dialog.set_extra_widget(vbox)

    hbbox = gtk.HButtonBox()
    hbbox.set_layout(gtk.BUTTONBOX_DEFAULT_STYLE)
    vbox.pack_start(hbbox, False, False, 0)
    hbbox.show()

    label = gtk.Label()
    label.set_markup(_('<span color="#8a0000"><b>delete</b> selection</span>'))
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_delete, dialog)
    hbbox.add(button)

    label = gtk.Label()
    label.set_markup(_('<span color="#00008a">select <b>all</b> images</span>'))
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", lambda w, d: d.select_all(), dialog)
    hbbox.add(button)

    label = gtk.Label()
    label.set_markup(_('<span color="#402a20"><b>rotate left</b></span>'))
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_rotate, dialog, "-90")
    hbbox.add(button)

    label = gtk.Label()
    label.set_markup(_('<span color="#402a20"><b>rotate right</b></span>'))
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_rotate, dialog, "90")
    hbbox.add(button)

    label = gtk.Label()
    label.set_markup(_('<span color="#002a00"><b>view</b> (display)</span>'))
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_viewpics, dialog)
    hbbox.add(button)

    label = gtk.Label()
    label.set_markup("\n<b>Ctrl</b> + " + _("left mouse  click - for adding items") +\
            "\n<b>Shift</b> + " + _("left mouse click - for ranges"))
    label.show()
    vbox.pack_start(label, False, False, 0)


    filter = gtk.FileFilter()
    filter.set_name(_(" images              "))
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
    filter.set_name(_(" all files           "))
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
def dialog_delete(widget, dialog): # {{{  needs more work
    text = _("are you sure you want to <b>delete</b> selected items - forever?")
    show_2_dialog(dialog, text, _("cancel"), _("yes"))
    if general["what_error"] != "ok_pressed":
        return
    for item in dialog.get_filenames():
        if os.path.isdir(item):
            try: 
                os.rmdir(item) 
            except OSError,  (errno, strerror): 
                print  _('## sorry, could not remove directory:')
                print  "## " + item
                print "## " + str(errno) + ": " + strerror
                message = _('sorry, could not remove diretory:')
                message += item + "\n\n"
                message += str(errno) + ": " + strerror + "\n" 
                show_mesbox(dialog, message)
        else:
            try: 
                os.remove(item) 
            except OSError,  (errno, strerror): 
                print  _('## sorry, could not remove file:')
                print  "## " + item
                print "## " + str(errno) + ": " + strerror
                message = _('sorry, could not remove file:')
                message += item + "\n\n"
                message += str(errno) + ": " + strerror + "\n" 
                show_mesbox(dialog, message)

    dialog.set_current_folder(dialog.get_current_folder())
    general["what_error"] == ""
#}}}
def dialog_viewpics(widget, dialog): # {{{
    try:
        file = dialog.get_filenames()[0]
    except IndexError:
        return
    if os.path.isfile(file):
        if sys.platform in ["win32", "win16", "win64"]:
            if general["py2exe"]:
                exe = general["cwd"] + "imdisplay.exe"
            else:
                exe = "imdisplay.exe"
            tot = exe + ' "' + file + '"'
            exitstatus = os.popen(tot + " 2>&1").read()
            if exitstatus != "" :
                print _("## catched some error while trying to display picture")
                print "## " + exitstatus
        else:  # on linux open multiple selection
            tot = "display " + '"' +  '" "'.join(dialog.get_filenames()) + '"'
            exitstatus = os.popen(tot + " 2>&1").read()
            if exitstatus != "" :
                print _("## catched some error while trying to display picture")
                print "## " + exitstatus
    else:
        show_mesbox(dialog, _("that is no regular file, can not display it"))
#}}}
def dialog_rotate(widget, dialog, direction): # {{{
    try:
        file = dialog.get_filenames()[0]
        if len(dialog.get_filenames()) > 1:
            show_mesbox(dialog, _("please select only <b>one</b> pic for rotating"))
            return
        if os.path.isdir(file):
            show_mesbox(dialog, _("don't know how to rotate a folder :P"))
            return
    except IndexError:
        return
# well or use mogrify. both don't provide useful error codes on MSwin at least
    fileext =  os.path.splitext(file)
    targetfile = file + ".rotate_tmp" + fileext[1]
    if general["py2exe"]:
        exe = general["cwd"] + "convert"
    else:
        exe = "convert"
    command = exe + ' -rotate "' + direction + '" ' + '"' + file + '" ' + '"' + targetfile + '"'
    exitstatus = os.popen(command + " 2>&1").read()
    if exitstatus == "": # seems ok
    ## secure overwriting
        if os.path.exists(targetfile) and os.path.getsize(targetfile) > 0 : # real test then here
            try:
                os.remove(file)
                try:
                    os.rename(targetfile, file)
                    print "## " + _("rotated") + "(" + direction + "): " + trimlongline(file, 62)
                except OSError, (errno, strerror):
                    print "## " + _("Error while tyring to replace the original file")
                    print "## " + _("you find your file now at:\n") + trimlongline(targetfile, 65)
                    text =  _("replacing your original file didn't succeed on:")
                    text += _(" \n\n " + file + "\n\n")
                    text += "<b>" + str(errno) + ": " + strerror + "</b>\n\n"
                    text += _("\nyou find your original file now at:\n") + targetfile
                    text += _("\n\n(may contact mac@calmar.ws )  ")
                    show_mesbox(dialog,text)

            except OSError, (errno, strerror):
               print "## " + _("ERROR while trying to replace your file with the rotated one")
               print "## " + _("you find the rotated file now at:")
               print "## " + trimlongline(targetfile, 65)
               text = _("replacing your original file didn't succeed on:")
               text += "\n\n " + file + "\n\n"
               text += "<b>" + str(errno) + ": " + strerror + "</b>\n\n"
               text += _("\nyou find your rotated file now at:\n") + targetfile
               text += _("\n\n(may contact mac@calmar.ws )  ")
               show_mesbox(dialog,text)
        else:
            print "## " + _("Error while tyring to rotate the file")
            text = _("rotating didn't succeed on:")
            text += "\n\n " + file + "\n\n"
            text += "<b>" + _("no further infos, sorry") + "</b>\n\n"
            text += _("(may contact mac@calmar.ws )  ")
            show_mesbox(dialog,text)
    else: # direct error probably
        plustext = ""
        if os.path.exists(targetfile) and os.path.getsize(targetfile) > 0 : # real test then here
            plustext = _("Nevertheless, there exists an produced (corrupt?) file at:\n" + targetfile)
        print "## " + _("Error while tyring to rotate the file")
        print "## " +  exitstatus
        if plustext != "":
            print "## " + plustext
        text = _("rotating didn't succeed on:")
        text += " \n\n " + file + "\n\n" 
        text += "<b>" + exitstatus + "</b>\n\n"
        if plustext != "":
            text += plustext
        text += _("\n\n(may contact mac@calmar.ws )  ")
        show_mesbox(dialog,text)
            
    dialog.emit("update-preview")
#}}}
# new
def toggle_percent(widget, data): #{{{
    if widget.get_property("visible"):
        data.show()
        widget.hide()
        general["percentbox"].set_sensitive(False)
        general["sizebox"].set_sensitive(True)
    else:
        data.hide()
        widget.show()
        general["percentbox"].set_sensitive(True)
        general["sizebox"].set_sensitive(False)
#}}}
def toggle_size(widget, data): #{{{
    if widget.get_property("visible"):
        data.show()
        widget.hide()
        general["percentbox"].set_sensitive(True)
        general["sizebox"].set_sensitive(False)
    else:
        data.hide()
        widget.show()
        general["percentbox"].set_sensitive(False)
        general["sizebox"].set_sensitive(True)
#}}}
def options_cb(widget): #{{{
    pass
#}}}
def create_commandline(): #{{{
    pass
#}}}
# major work
def start_resize(widget, event, data=None): #{{{ (probably) OK 
    global general
    global imgprocess

# messagebox when there are no files selexted
    if len(imgprocess["files_todo"]) == 0:
        show_mesbox(general["window"], _("Select some <b>pics</b> to work on"))
        return

    prefix = imgprocess["ent_prefix"]
    suffix = imgprocess["ent_suffix"]
    folder = imgprocess["ent_folder"]

    usesize = True
    if general["percentbox"].get_property("sensitive"):
        usesize = False
        

    if imgprocess["width"] == "0": # then, the spinner is selected
        width = str(imgprocess["spinWidth"].get_value_as_int())
    else:
        width = str(imgprocess["width"])
    if imgprocess["height"] == "0":
        height = str(imgprocess["spinHeight"].get_value_as_int())
    else:
        height = str(imgprocess["height"])
    if imgprocess["percent"] == "0":
        percent = str(imgprocess["spinPercent"].get_value_as_int())
    else:
        percent = str(imgprocess["percent"])
    if imgprocess["quality"] == "0":
        quality = str(imgprocess["spinQuality"].get_value_as_int())
    else:
        quality = str(imgprocess["quality"])
    ftype = imgprocess["ftype"]

    text = _("""  At least <u>one</u> must be set:  

              -> <b>Prefix</b>
              -> <b>Suffix</b>
              -> <b>subfolder to create pics in</b>
              -> <b>picture type</b>
     
 in order to prevent overwriting the original pictures""")
# messagebox when there is no suff, pre or folder
    if prefix == "" and suffix == "" and folder == "" and ftype == "":
            show_mesbox(general["window"], text)
            return

# to get the path of sample file
    splitfile = os.path.split(imgprocess["files_todo"][0])

# create folder when needed
    if folder != "" and not os.path.exists(splitfile[0] + "/" +folder):
        print "##" + _("create new folder: ") + folder + "  (" + \
                trimlongline(splitfile[0],38) + "/" + folder + ")"
        print
        try:
            os.mkdir(splitfile[0] + "/" + folder)
        except OSError, (errno, strerror):
            text = _("was not able to create your target folder") + "\n\n"
            text += _("please check that issue first") + "\n\n"
            text += str(errno) + ": " + strerror + "\n\n"
            show_mesbox(general["window"], text)
    else:
        print _("# sub-folder exists already")

# just some konsole messages
    if width == "99999":
       width_here = _("unlimited")
    else:
       width_here = width

    if height == "99999":
       height_here = _("unlimited")
    else:
       height_here = height

    if usesize:
        reso = width_here + " x " + height_here
    else:
        reso = percent + "%"

    print """\
## create new pictures: resizing:    %-s
                        quality:     %-s 
                        folder:      %-s 
                        prefix:      %-s 
                        suffix:      %-s
                        convert to:  %-s""" % \
                              (reso, quality, folder, prefix, suffix, ftype)

    print

# begin the loop
    total = len(imgprocess["files_todo"])
    counter=0
    dist = ""
    for sourcefile in imgprocess["files_todo"]:
        counter += 1
        sourcefile = string.replace(sourcefile, "\\","/")
        splitfile = os.path.split(sourcefile)
        resultpath = splitfile[0] + "/"  # targetdir of pics
        if folder != "":
            resultpath += folder + "/" 
        fname,ext=os.path.splitext(splitfile[1]); 
        if ftype == "":
            target_ext = ext
        else:
            target_ext = ftype
        targetfile = resultpath + prefix + fname + suffix + target_ext
# source and target file not set

# for py2exe only (looking for the convert.exe in the same dir...)
        if sys.platform in ["win32", "win16", "win64"]:
            if general["py2exe"]:
                exe = general["cwd"] + "convert.exe"
            else:
                exe = "convert.exe"
        else:
            exe = "convert" 
        if usesize:
            resize = width + "x" + height
        else:
            resize = percent + "%"

        command = exe + ' "' + sourcefile + '"' + " -resize " + resize +\
                    " -quality " + quality + ' "' + targetfile + '"'

# some printing again
        if dist == "":  # initialisize only once
            dist = len(splitfile[1]) + 1 # first sourcefile (no path) + 1

# print what you're going to do... preparation here
        command_print = "convert: " + "%-" + str(dist) + "s --> " +\
                trimlongline(targetfile,58 - dist )

        text = trimlongline(targetfile,65 - dist )
        label_progress(str(counter), str(total), text,"") 
        print command_print % (splitfile[1][-1*(dist-1):]) # initial file lenght (dist-1)

# wait and update
        while gtk.events_pending():
            gtk.main_iteration(False)

# source und target the same?   refuse then, may continue     
        if sourcefile == targetfile:
            text = _("<b>source</b> and <b>target</b> are the same!") + "\n\n" +\
_("(...cowardly refuses to overwrite)")
            print "#### " + _("source and target are the same!") + " ####"
            show_2_dialog(general["window"], text, _("quit processing"), _("skip and go on..."))
            if general["what_error"] != "ok_pressed":
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
        if os.path.exists(targetfile):
            if general["what_todo"] != "all_overwrite":
                show_overwrite_dialog(targetfile)
            if general["what_todo"] == "ok_pressed":
                general["what_todo"] = ""
                print _("# skipped: ") + trimlongline(targetfile,58)
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

# the actual work/progress
        exitstatus = os.popen(command + " 2>&1").read()
        if exitstatus != "":  # an error or similar, assuming otherwise all is ok
            if os.path.exists(targetfile) and os.path.getsize(targetfile) == 0 :
                try:
                    os.remove(targetfile)
                except OSError,  (errno, strerror): 
                    print _("## there is a currupt (filesize == 0 Bytes) generated file")
                    print "## " + targetfile
                    print _("## trying to delete it, didn't succeed")
                    print "## " + str(errno) + ": " + strerror
                    print _("## please check that issue yourself as well")

            print "## " + _("ERROR while working on that picture")
            print exitstatus
            print
            text = _("imagemagick terminated with an <b>error</b> while working on:")
            text += " \n\n " + sourcefile + "\n\n"
            text += "<b>" + exitstatus + "</b>\n\n"
            text += _("(may contact mac@calmar.ws)  ")
            show_2_dialog(general["window"], text, _("quit processing"), _("skip and go on..."))
            if general["what_error"] != "ok_pressed":
                imgprocess["files_todo"]=[]
                label_progress(str(counter),str(total), _("canceled!"),"color='#550000'") 
                while gtk.events_pending():
                    gtk.main_iteration(False)
                time.sleep(2.4)
                label_nopic()
                print
                print _("# converting has stopped ")
                print
                return
# exitstatus == "" , I optimistically assume, file gots created properly

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
#  table  for whole thing there
#########################################################################

    table = gtk.Table(rows=6, columns=2, homogeneous=False)
    mainbox.pack_start(table, False, False, 0)

##################
#  over hbox for sizes

    general["sizebox"] = gtk.HBox(True, 0)
    table.attach(general["sizebox"], 0, 2, 0, 1, gtk.EXPAND)
    general["sizebox"].set_sensitive(True)

#### width

    vbox = gtk.VBox(False, 0)
    general["sizebox"].pack_start(vbox, False, False, 5)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("max. width") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "1600x", "1280x", "1024x", "800x", "640x",\
            "480x", _("specific:") ]
    values = [ "99999", "1600", "1280", "1024", "800", "640", "480", "0"]
    default = "99999"
    general["radio_width"] = create_radios(vbox, values, text, "width", default)
    imgprocess["width"] = 99999

    imgprocess["spinWidth"].set_wrap(False)
    vbox.pack_start(imgprocess["spinWidth"], False, False, 0)


## height

    vbox = gtk.VBox(False, 0)
    general["sizebox"].pack_start(vbox, False, False, 5)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("max. height") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "x1200", "x1024",  "x768", "x600", "x480",\
             "x320", _("specific:") ]
    values = [ "99999", "1200", "1024", "768", "600", "480", "320", "0"]
    default = "768"
    general["radio_height"] = create_radios(vbox, values, text, "height", default)
    imgprocess["height"] = 768

    imgprocess["spinHeight"].set_wrap(False)
    vbox.pack_start(imgprocess["spinHeight"], False, False, 0)

################## overbox finish

##################
#  over hbox for percent

    general["percentbox"] = gtk.HBox(False, 0)
    table.attach(general["percentbox"], 2, 3, 0, 1, gtk.EXPAND)
    general["percentbox"].set_sensitive(False)

#### percent

    vbox = gtk.VBox(False, 0)
    general["percentbox"].pack_start(vbox, False, False, 5)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("size in %") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ "100%", "90%", "80%", "70%", "60%", "50%", "40%", _("specific:") ]
    values = [ "100", "90", "80", "70", "60", "50", "40", "0"]
    default = "60"
    general["radio_percent"] = create_radios(vbox, values, text, "percent", default)
    imgprocess["percent"] = 60

    imgprocess["spinPercent"].set_wrap(False)
    vbox.pack_start(imgprocess["spinPercent"], False, False, 0)

################## overbox finish
#  to toggle sensitivity of the above boxes
    
    but1 = gtk.Button()
    but1.set_size_request(-1, 8)
    align1 = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align1.set_padding(6, 6, 0, 5)
    align1.add(but1)
#    but1.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#34a1ff"))
    but2 = gtk.Button()
    but2.set_size_request(-1, 8)
#    but2.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#34a1ff"))
    align2 = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align2.set_padding(6, 6, 0, 5)
    align2.add(but2)

    but1.connect("clicked", toggle_percent, but2)
    table.attach(align1, 0, 2, 1, 2, gtk.FILL)

    but2.connect("clicked", toggle_size, but1)
    table.attach(align2, 2, 3, 1, 2, gtk.FILL)

## separator
    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 5)
    separator = gtk.VSeparator()
    align.add(separator)
    table.attach(align,3,4,0,2)

## quality

    vbox = gtk.VBox(False, 0)
    table.attach(vbox, 4, 5, 0, 1)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>' + _("quality") + '</b></span>')
    vbox.pack_start(label, False, False, 0)

    text = [ "100%", "97%", "94%", "90%", "85%", "80%", "60%", _("specific")]
    values = [ "100", "97", "94", "90", "85", "80", "60", "0"]
    default = "94"
    general["radio_quality"] = create_radios(vbox, values, text, "quality", default)
    imgprocess["quality"] = 94

    imgprocess["spinQuality"].set_wrap(False)
    vbox.pack_start(imgprocess["spinQuality"], False, False, 0)

## separator
    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 5)
    separator = gtk.VSeparator()
    align.add(separator)
    table.attach(align,5,6,0,2)

#### prefix/suffix/folder entries

    vbox = gtk.VBox(False, 0)
    table.attach(vbox, 6, 7, 0, 1)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>&lt;' + _("PREFIX") + '&gt;</b></span>file.jpg')
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(15)
    entry.set_alignment(0.49)
    entry.connect('changed',entries_cb, "ent_prefix")
    vbox.pack_start(entry, False, False, 0)

    label = gtk.Label()
    label.set_markup('\nfile<span foreground="#000060"><b>&lt;' + _("SUFFIX") + '&gt;</b></span>.jpg')
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(15)
    entry.set_alignment(0.49)
    entry.connect('changed',entries_cb, "ent_suffix")
    vbox.pack_start(entry, False, False, 0)

    label = gtk.Label()
    label.set_markup('\n<span foreground="#000060"><b>' + _("sub-folder") + "</b></span>, " +\
            _("for\nthe <u>new</u> pics"))
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(15)
    entry.set_alignment(0.49)
    entry.connect('changed',entries_cb, "ent_folder")
    vbox.pack_start(entry, False, False, 0)

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
#  advanced options

#    box = gtk.HBox(False, 0)
#    mainbox.pack_start(box, False, False, 0)

#    label = gtk.Label()
#    label.set_markup( _("<b>option:</b>"))
#    box.pack_start(label, False, False, 0)
#    combo = gtk.combo_box_new_text()
#    combo.set_wrap_width(1)
#    list = ["", "-resize", "-strip", "-unsharp", "-vignette" ,"-tint", "-trim", "-unsharp",\
#            "-threshold", "-radial-blur", "-posterize" ]
#    list.sort()
#    for ext in list:
#        combo.append_text(ext)
#    combo.set_active(0)
#    box.pack_start(combo, False, False, 0)
#    combo.connect('changed', options_cb)

#    button = gtk.CheckButton("Width/Hight as max")
#    button.connect("toggled", options_cb, "max")
#    box.pack_start(button, False, False, 0)

#    separator = gtk.HSeparator()
#    mainbox.pack_start(separator, False, False, 5)

#########################################################################
## todo label
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
    image.set_from_file(general["cwd"] + "bilder/go.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("start converting  "))
    hbox.pack_end(label, False, False, 0)
    but_start = gtk.Button()
    but_start.add(hbox)
    but_start.connect("clicked", start_resize, None)
    box.pack_end(but_start, False, False, 0)


    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/open.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("select pictures...  "))
    hbox.pack_end(label, False, False, 0)
    files = gtk.Button()
    files.add(hbox)
    files.connect("clicked", open_filechooser, None)
    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 15)
    align.add(files)
    box.pack_end(align, False, False, 0)

    files.grab_focus()


#########################################################################
# show

    font_desc = pango.FontDescription("Courier")
    if font_desc:
        general["todolabel"].modify_font(font_desc)


    general["window"].show_all()
    but1.hide()
    gtk.main()
    return 0      
#}}}
# imports, head (at the bottom haha)
#imports... vars...  {{{ OK
import os, sys,  time, glob, string
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
            "py2exe"       : False,
            "sizebox"      : True,
            "percentbox"   : False,
            "radio_width"  : radio_bogus,
            "radio_height" : radio_bogus,
            "radio_percent" : radio_bogus,
            "radio_quality" : radio_bogus,
            "window" : gtk.Window(gtk.WINDOW_TOPLEVEL)}

if sys.path[0][-12:] == "\library.zip":  #for py2exe
    general["py2exe"] = True
    general["cwd"] = sys.path[0][0:-12] + "/"
else:
    general["cwd"] = sys.path[0] + "/"
gettext.bindtextdomain('cal_pixresizer', general["cwd"] + "locale")

# imgprocess (global)- data (source) for image processing
imgprocess = { "ent_prefix"  : "",
               "ent_suffix"  : "",
               "ent_folder"  : "",
               "ftype"       : "",
               "files_todo"  : [],
               "width"       : "",
               "height"      : "",
               "percent"     : "",
               "quality"     : ""}
adj = gtk.Adjustment(1024, 10, 2000, 1, 100, 0)
adj.connect("value_changed", get_spin_focus, "radio_width" )
imgprocess["spinWidth"] = gtk.SpinButton(adj, 1.0, 0)
imgprocess["spinWidth"].set_numeric(True)  #spinnervalue needed later
adj = gtk.Adjustment(768, 10, 2000, 1, 100, 0)
adj.connect("value_changed", get_spin_focus, "radio_height" )
imgprocess["spinHeight"] = gtk.SpinButton(adj, 1.0, 0)
imgprocess["spinHeight"].set_numeric(True)
adj = gtk.Adjustment(60, 10, 400, 1, 30, 0)
adj.connect("value_changed", get_spin_focus, "radio_percent" )
imgprocess["spinPercent"] = gtk.SpinButton(adj, 1.0, 0)
imgprocess["spinPercent"].set_numeric(True)
adj = gtk.Adjustment(90, 10, 100, 1, 10, 0)
adj.connect("value_changed", get_spin_focus, "radio_quality" )
imgprocess["spinQuality"] = gtk.SpinButton(adj,0.1, 0)
imgprocess["spinQuality"].set_numeric(True)

if __name__ == "__main__":
    main()
#}}}
