#!/usr/bin/env python
# Copyright (C) 2006 http://www.calmar.ws #{{{
# http://www.calmar.ws/resize/COPYING
### little FUNCTIONS 
#              gui related
#}}}
# little gui
def quit_widget(widget, data): #{{{
    data.hide()
    data.destroy()
#}}}
def quit_self(widget, *args): #{{{
    widget.hide()
    widget.destroy()
#}}}
def delete_event(widget, event, data=None): #{{{
    userdata_save()
    gtk.main_quit()
    return False
#}}}
def toggle_percent(widget, data): #{{{
    data.show()
    widget.hide()
    general["percentbox"].set_sensitive(False)
    general["sizebox"].set_sensitive(True)
#}}}
def toggle_size(widget, data): #{{{
    data.show()
    widget.hide()
    general["percentbox"].set_sensitive(True)
    general["sizebox"].set_sensitive(False)
#}}}
def get_spin_focus(widget, spinname): #{{{
    global general
    general[spinname].set_active(True)
#}}}
def setvalue(widget, data): #Radio buttons... #{{{
    global general
    imgprocess[data[0]] = data[1]
#}}}
def entries_cb(editable, id_edit): #{{{
    global imgprocess
    posi = editable.get_position()
    char = editable.get_chars(posi, posi+1)
    if char == " ":  # replace spaces with underlines
        editable.delete_text(posi,posi+1)
        editable.insert_text("_", posi)
    imgprocess[id_edit] = editable.get_text()
#}}}
def setcombo(combobox): #{{{
    global imgprocess
    model = combobox.get_model()
    active = combobox.get_active()
    if active >= 0:
        imgprocess["ftype"]=model[active][0]
#              main label
#}}}
def label_nopic(): #{{{
    general["todolabel"].set_markup("\n\n  <b>-- %s --</b> \n\n" % _("no pictures are selected"))
#}}}
def label_progress(count, tot, text, colorstring): #{{{
    general["todolabel"].set_markup("\n\n<b>%s (%s/%s): <span %s>%s</span></b>\n\n" %(
            _("progress"), count, tot, colorstring, text))
#}}}
def files_print_label(files_todo): #{{{
    labeltext=""
    if len(files_todo) == 1:
        labeltext = "\n\n%s\n\n" % trimlongline(files_todo[0])
    elif len(imgprocess["files_todo"]) == 2:
        labeltext = "\n%s\n%s\n\n" % (trimlongline(files_todo[0]), trimlongline(files_todo[1]))
    elif len(files_todo) == 3:
        labeltext = "\n%s\n%s\n%s\n" % (trimlongline(files_todo[0]), trimlongline(files_todo[1]),
                trimlongline(files_todo[2]))
    elif len(files_todo) == 4:
        labeltext = "%s/\n%s\n%s\n%s\n" % (trimlongline(files_todo[0]),
                trimlongline(files_todo[1]), trimlongline(files_todo[2]),
                trimlongline(files_todo[3]))
    elif len(files_todo) == 5:
        labeltext = "%s\n%s\n%s\n%s\n%s" % (trimlongline(files_todo[0]),
                trimlongline(files_todo[1]), trimlongline(files_todo[2]),
                trimlongline(files_todo[3]), trimlongline(files_todo[4]))
    else:
        for i in range(0,3):
            labeltext += "%s\n" % ( trimlongline(files_todo[i]))
        labeltext += ".....\n"
        labeltext += trimlongline(files_todo[-1])

# encoding hack. grr
    if general["mswin"]:
        general["todolabel"].set_text(labeltext)
    else:
        general["todolabel"].set_text(utf8_enc(labeltext))
#              create radios
#}}}
def create_radios(vbox,values,text, id_radio, default): #{{{
    for i in range(len(values)):
        if i == 0: # first should not get other radios as reference
            radio = None
        radio = gtk.RadioButton(radio, text[i])
        radio.connect("toggled", setvalue, (id_radio, values[i]))
        vbox.pack_start(radio, True, True, 0)
        if values[i] == default:
            radio.set_active(True)
    return radio # return last radio thing for spinner
#              various
#}}}
# little various
def trimlongline(item, size=72): #{{{
    if len(item) >= size:
        item = item[0:size/4] + "..." + item[-1*((size-size/4)-3):]
    return item
#}}}
def stopprogress(widget, data): #{{{ bla bla
    global imgprocess
#   callback for setting var while someone presses stop during progress
    imgprocess["stop_progress"]=True
#              userdata
#}}}
def userdata_load(): #{{{
    global general
    global imgprocess

    filename = general["cwd"] + "data_cal_pixresizer.cpd"
    d = shelve.open(filename)
    try:
        for key in ["size_or_not", "viewer", "pic_folder", "bin_folder"]:
            general[key] = d[key]
        for key in ["ftype", "files_todo", "width", "height", "percent", "quality",\
                "ent_prefix", "ent_suffix", "ent_folder"]:
            imgprocess[key] = d[key]
    except KeyError:
        print "## " + _("no valid userdata found")
    d.close()
#}}}
def userdata_save(): #{{{
    global general
    global imgprocess

    d = shelve.open(general["cwd"] + "data_cal_pixresizer.cpd")
    for key in ["viewer", "pic_folder", "bin_folder"]:
        d[key] = general[key]
    for key in ["ftype", "files_todo", "width", "height", "percent", "quality",\
            "ent_prefix", "ent_suffix", "ent_folder"]:
        d[key] = imgprocess[key]
    d["size_or_not"] = general["sizebox"].get_property("sensitive")
    d.close()
#              encoding stuff
#}}}
def loc_enc(text): #{{{
    obj = unicode(text, 'utf-8')
    return obj.encode( general["encoding"])
#}}}
def utf8_enc(text): #{{{
    obj = unicode(text, general["encoding"])
    return obj.encode('utf-8')
### various mesboxes
#}}}
# messageboxes
def show_2_dialog(parent_widget, text, button_quit, button_ok): #{{{
    global general
    general["dialot2_q"] == ""
    mesbox = gtk.Dialog(_("attention:"), parent_widget, gtk.DIALOG_MODAL, ())
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)
    mesbox.set_size_request(700,-1)

    vbox = gtk.VBox()
    vbox.show()
    label = gtk.Label()
    label.set_line_wrap(True)
    label.set_markup(text)
    label.show()
    vbox.pack_start(label, True, True, 15)
    align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
    align.set_padding(5, 5, 20, 20)
    align.show()
    align.add(vbox)
    mesbox.vbox.pack_start(align, True, True, 15)

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
def show_overwrite_dialog(filename): # merge with the above maybe? #{{{
    global general
    mesbox = gtk.Dialog(_("attention:"), general["window"], gtk.DIALOG_MODAL, ())
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)
    mesbox.set_size_request(700,-1)
    vbox = gtk.VBox()
    vbox.show()
    label = gtk.Label()
    label.set_line_wrap(True)
# encoding hack. grr
    if not general["mswin"]:
        filename = utf8_enc(filename)

    label.set_markup("%s\n\n%s" % (_("Target picture <b>already exists</b>:"), trimlongline(filename ,68)))
    label.show()
    vbox.pack_start(label, True, True, 10)
    align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
    align.set_padding(5, 5, 20, 20)
    align.show()
    align.add(vbox)
    mesbox.vbox.pack_start(align, True, True, 15)

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
def show_mesbox(parent, text): #{{{
    mesbox = gtk.Dialog(_("Calmar's Picture Resizer"), parent, gtk.DIALOG_MODAL,\
            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    mesbox.connect("destroy", quit_self)
    mesbox.connect("delete_event", quit_self)
    mesbox.set_size_request(700,-1)

    vbox = gtk.VBox()
    vbox.show()
    label = gtk.Label()
    label.set_line_wrap(True)
# encoding hack. grr
#    if general["mswin"]:
#        text = utf8_enc(text)
    text = utf8_enc(text)
    label.set_markup(text)
    label.show()
    vbox.pack_start(label, True, True, 15)
    align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
    align.set_padding(5, 5, 20, 20)
    align.show()
    align.add(vbox)
    mesbox.vbox.pack_start(align, True, True, 15)

    mesbox.show()
    mesbox.run()
    mesbox.destroy()
#             related
#}}}
def overwrite_destroy(widget, data): #{{{
    global general
    general["overwrite_q"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def dialog_2_destroy(widget, data): # (merge with overwritedestroy?) #{{{
    global general
    general["dialot2_q"] = str(data[1])
    data[0].hide()
    data[0].destroy()
### FileChooser things
#}}}
# converting loop
def create_subfolder(folder, filen): #{{{
    if folder != "" and not os.path.exists(filen + "/" + folder):
        print "## %s: %s (%s/%s)" % (_("create new folder: "), folder,
                     trimlongline(filen, 38), folder)
        try:
            os.mkdir(filen + "/" + folder)
        except OSError, (errno, errstr):
            print
            print "## %s" % _("was not able to create target directory: converting will stop")
            print "## %s: %s" % (str(errno), errstr)
            print

            text = "<big><b>%s</b></big>\n\n%s/<b>%s</b>\n\n%s\n\n%s: %s" % (
                    _("was not able to create your target folder"),
                    trimlongline(filen ,48), folder,
                    _("please check that issue first"),
                    str(errno), errstr)
            show_mesbox(general["window"], text)
            return False
    else:
        print "## %s" % _("sub-folder exists already")
    return True
#}}}
def print_settings(width, height, usesize, quality,  folder, prefix, suffix, ftype): #{{{
    if width == "9999":
       width_here = _("unlimited")
    else:
       width_here = width

    if height == "9999":
       height_here = _("unlimited")
    else:
       height_here = height

    if usesize:
        if width == "9999" and height == "9999":
            reso = "%s x %s (--> keep lenght 100%%)" % (width_here, height_here)
        else:
            reso = "%s x %s" % (width_here, height_here)
    else:
        reso = percent + "%"

    print """\
## create new pictures: resizing   : %-s
                        quality    : %-s
                        folder     : %-s
                        prefix     : %-s
                        suffix     : %-s
                        convert to : %-s""" % \
                              (reso, quality, folder, prefix, suffix, ftype)

    print
#}}}
def get_imgprocess(): #{{{
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
    return (prefix, suffix, folder, usesize, width, height, percent, quality, ftype)
#}}}
def no_files_there_selected(): #{{{
    if not imgprocess["files_todo"]:
        show_mesbox(general["window"], "<big><b>%s</b></big>" % (
                _("Select some <b>pics</b> to work on")))
        return True
#}}}
def print_stop_message(counter, total): #{{{
    general["stop_button"].hide()
    label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
    print
    print "## %s" % _("stop button pressed: converting has stopped")
    print
    show_mesbox(general["window"], "<big><b>%s</b></big>" % _("progress stopped"))
    files_print_label(imgprocess["files_todo"])
#}}}
def go_on_source_is_equal_target(counter, total): #{{{
    print "## " + _("source and target are the same!")
    text = "%s\n\n%s" % (_("<b>source</b> and <b>target</b> are the same!"),
            _("(...cowardly refuses to overwrite)"))
    show_2_dialog(general["window"], text, _("quit processing"), _("skip and go on..."))
    if general["dialot2_q"] != "ok_pressed":
        general["stop_button"].hide()
        label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
        while gtk.events_pending():
            gtk.main_iteration(False)
        time.sleep(2.0)
        print
        print "## %s" % _("converting has stopped")
        print
        files_print_label(imgprocess["files_todo"])
        return False
    else:
        return True
#}}}
def start_resize(widget, event, data=None): #{{{
    global general
    global imgprocess

    if no_files_there_selected():
        return
# get imgprocess data
    prefix, suffix, folder, usesize, width, height, percent, quality, ftype = get_imgprocess()

# messagebox when there is no suff, pre or folder
    if prefix == "" and suffix == "" and folder == "" and ftype == "":
            text = _("""  At least <u>one</u> must be set:

              -> <b>Prefix</b>
              -> <b>Suffix</b>
              -> <b>subfolder to create pics in</b>
              -> <b>picture type</b>

 in order to prevent overwriting the original pictures""")
            show_mesbox(general["window"], text)
            return

# to get the path of sample (first) file
    splitfile = os.path.split(imgprocess["files_todo"][0])

# create folder when needed
    if not create_subfolder(folder, splitfile[0]):
        return
# just some konsole messages
    print_settings(width, height, usesize, quality, folder, prefix, suffix, ftype)

# loop preparations
    total = len(imgprocess["files_todo"])
    counter = 0
    dist = ""
    imgprocess["stop_progress"] = False
    general["stop_button"].show()
    general["stop_button"].grab_focus()
    general["overwrite_q"] != ""
#######################################################################
# begin the loop
#######################################################################
    for sourcefile in imgprocess["files_todo"]:
        while gtk.events_pending():
            gtk.main_iteration(False)
# check if stop got pressed
        if imgprocess["stop_progress"]:
            print_stop_message(counter, total)
            return
        counter += 1
# split filenames into pieces and create targetfile name
        sourcefile = string.replace(sourcefile, "\\","/") # for later source == target?
        splitfile = os.path.split(sourcefile)
        resultpath = splitfile[0] + "/"
        if folder != "":    # targetdir of pics
            resultpath += folder + "/"
        fname,ext=os.path.splitext(splitfile[1]);  # file itself
        if ftype == "":
            target_ext = ext
        else:
            target_ext = ftype
        targetfile = resultpath + prefix + fname + suffix + target_ext

# some printing issue
        if dist == "":  # initialisize only once
            dist = len(splitfile[1]) + 1 # first sourcefile (no path) + 1

# print what you're going to do... preparation here
        command_print = "convert: " + "%-" + str(dist) + "s --> " +\
                trimlongline(targetfile,58 - dist )

        text = trimlongline(targetfile,65 - dist )
        label_progress(str(counter), str(total), text,"")
        print command_print % (splitfile[1][-1*(dist-1):]) # initial file lenght (dist-1)

# source und target the same?  continue or stop?
        if sourcefile == targetfile:
            if go_on_source_is_equal_target(counter, total):
                continue
            else:
                return
# check if file exists and may show 'overwrite dialog'
        if os.path.exists(targetfile):
            if general["overwrite_q"] != "all_overwrite":
                show_overwrite_dialog(targetfile)
                while gtk.events_pending():
                    gtk.main_iteration(False)
                if general["overwrite_q"] == "ok_pressed":
                    general["overwrite_q"] != ""
                    print _("# skipped: ") + trimlongline(targetfile,58)
                    continue
                elif general["overwrite_q"] == "cancel":
                    general["overwrite_q"] != ""
                    general["stop_button"].hide()
                    label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
                    while gtk.events_pending():
                        gtk.main_iteration(False)
                    time.sleep(2.0)
                    print
                    print _("# converting has stopped ")
                    print
                    files_print_label(imgprocess["files_todo"])
                    return
                elif general["overwrite_q"] == "overwrite":
                    general["overwrite_q"] != ""

        pre = ""
        if general["py2exe"]:
            pre = general["cwd"]
        exe = pre + "convert"

        if usesize:
            if width == "9999" and height == "9999":
                resize = "100%"
            else:
                resize = width + "x" + height
        else:
            resize = percent + "%"

# the actual work/progress
        tot = [exe, sourcefile,"-resize", resize, "-quality", quality, targetfile]
        try:
            pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,\
                    stderr=subprocess.PIPE, shell=False)
            err_output = pipe.stderr.read()
        except OSError, (errno, errstr):
            print "## %s" % _("error while trying to convert the picture")
            print "## %s: %s" % (str(errno), errstr)
            text = "%s\n\n%s\n\n%s: %s\n\n%s" % (
                    _("catched an <b>error</b> while working on:"),
                    sourcefile, str(errno), errstr,
                    _("(may contact mac@calmar.ws)"))
            show_2_dialog(general["window"], text, _("quit processing"), _("skip and go on..."))
            if general["dialot2_q"] != "ok_pressed":
                general["stop_button"].hide()
                label_progress(str(counter),str(total), _("canceled!"),"color='#550000'")
                while gtk.events_pending():
                    gtk.main_iteration(False)
                time.sleep(2.4)
                print
                print "## %s" % _("converting has stopped")
                print
                files_print_label(imgprocess["files_todo"])
                return
            else:
                continue

        if err_output != "" : # an error, since not empty or so
            print "## %s" % _("ERROR while working on that picture")
            print "## %s" % err_output
            print
            if os.path.exists(targetfile) and os.path.getsize(targetfile) == 0 : # del bogus
                try:
                    os.remove(targetfile)
                except OSError,  (errno, errstr):
                    print "## %s" % _(" there is a currupt (filesize == 0 bytes) generated file")
                    print "## %s" % targetfile
                    print "## %s" % _("trying to delete, didn't succeed")
                    print "## %s: %s" % (str(errno), errstr)
                    print "## %s" % _("please check that issue yourself as well")

            text = "%s\n\n%s\n<b>%s</b>\n\n%s" % (
                    _("imagemagick terminated with an <b>error</b> while working on:"),
                    sourcefile, err_output, _("(may contact mac@calmar.ws)"))
            show_2_dialog(general["window"], text, _("quit processing"), _("skip and go on..."))
            if general["dialot2_q"] != "ok_pressed":
                general["stop_button"].hide()
                label_progress(str(counter),str(total), _("canceled!"),"color='#550000'")
                while gtk.events_pending():
                    gtk.main_iteration(False)
                time.sleep(2.4)
                #label_nopic()
                # imgprocess["files_todo"]=[]
                print
                print _("# converting has stopped ")
                print
                files_print_label(imgprocess["files_todo"])
                return

    print
    print "## %s" % _("progress finished")
    print

    general["stop_button"].hide()
    label_progress(str(total),str(total), _("finish!"),"color='#000070'")

    while gtk.events_pending():
        gtk.main_iteration(False)
    time.sleep(2.0)

    files_print_label(imgprocess["files_todo"])
### major GUI
#}}}
# filechooser things
def open_filechooser(widget, acgroup): #{{{
    global general

    dialog = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                   general["window"],
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_select_multiple(True)
    dialog.set_size_request(700,500)

    dialog.add_accel_group(acgroup)

# main vbox overall there
    vbox = gtk.VBox()
    vbox.show()

# set main widget
    dialog.set_extra_widget(vbox)

# first hbox packed in align packed in main vbox
    hbox = gtk.HBox()
    hbox.show()

    align = gtk.Alignment(xalign=0.5, yalign=0.0, xscale=0.0, yscale=0.0)
    align.set_padding(0, 0, 0, 0)
    align.add(hbox)
    align.show()

    vbox.pack_start(align, False, False, 0)

# then table
    table = gtk.Table(rows=6, columns=8, homogeneous=False)
    table.show()
    hbox.pack_start(table, False, False, 0)

    label = gtk.Label()
    label.set_markup('<span color="#8a0000" size="larger">' +
            _("<b><u>d</u></b>elete selection") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.add_accelerator('clicked', acgroup, ord('d'), 0, gtk.ACCEL_VISIBLE )
    button.connect("clicked", dialog_delete, dialog)
    table.attach(button, 1, 2, 0, 1, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#00008a" size="larger">' +
            _("select <b><u>a</u></b>ll images") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.add_accelerator('clicked', acgroup, ord('a'), 0, gtk.ACCEL_VISIBLE )
    button.connect("clicked", lambda w, d: d.select_all(), dialog)
    table.attach(button, 2, 3, 0, 1, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#002a00" size="larger">' +
            _("pre<b><u>v</u></b>iew pictures") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_viewpics, dialog)
    button.add_accelerator('clicked', acgroup, ord('v'), 0, gtk.ACCEL_VISIBLE )
    table.attach(button, 3, 4, 0, 1, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#402a20" size="larger">' +
            _("rotate l<b><u>e</u></b>ft") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_rotate, dialog, "-90")
    button.add_accelerator('clicked', acgroup, ord('e'), 0, gtk.ACCEL_VISIBLE )
    table.attach(button, 1, 2, 1, 2, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#402a20" size="larger">' +
            _("rotate <b><u>r</u></b>ight") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_rotate, dialog, "+90")
    button.add_accelerator('clicked', acgroup, ord('r'), 0, gtk.ACCEL_VISIBLE )
    table.attach(button, 2, 3, 1, 2, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#405a30" size="larger">' + _("choose viewer") + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.connect("clicked", dialog_setupviewer, dialog)
    table.attach(button, 3, 4, 1, 2, gtk.FILL)

    label = gtk.Label()
    label.set_markup('<span color="#610e4d" size="larger">' +
            _('edit e<b><u>x</u></b>if comment') + '</span>')
    label.show()
    button = gtk.Button()
    button.add(label)
    button.show()
    button.add_accelerator('clicked', acgroup, ord('x'), 0, gtk.ACCEL_VISIBLE )
    button.connect("clicked", dialog_exif_cb, dialog)
    table.attach(button, 2, 3, 2, 3, gtk.FILL)

    align = gtk.Alignment(0.5, 0.0, 0.0, 0.0)
    align.set_padding(10, 10, 10, 10)
    align.show()
    exiflabel = gtk.Label()
    exiflabel.show()
    exiflabel.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#000050'))
    align.add(exiflabel)

    table.attach(align, 0, 6, 3, 4, gtk.FILL)

#    label = gtk.Label()
#    label.set_markup("\n<b>Ctrl</b> + " + _("left mouse  click - for adding items") +\
#            "\n<b>Shift</b> + " + _("left mouse click - for ranges"))
#    label.show()

#    table.attach(label, 0, 6, 4, 5, gtk.FILL)

# file filter
    filefilter = gtk.FileFilter()
    filefilter.set_name(_(" images              "))
    filefilter.add_mime_type("image/jpeg")
    ext_list = [
        ".avs", ".bmp", ".cgm", ".cmyk", ".dcx", ".dib", ".eps", ".fax", ".fig",
        ".fits", ".fpx", ".gif", ".gif87", ".hdf", ".ico", ".jbig", ".jpg", ".jpeg", ".map",
        ".matte", ".miff", ".mng", ".mpeg", ".mtv", ".null", ".pbm", ".pcd",
        ".pcl", ".pcx", ".pdf", ".pgm", ".pict", ".plasma", ".png", ".pnm", ".ppm",
        ".ps", ".ps2", ".p7", ".rad", ".rgb", ".rla", ".rle", ".sgi", ".sun", ".text",
        ".tga", ".tiff", ".tiff24", ".tile", ".uil", ".uyvy", ".vicar", ".vid", ".viff",
        ".xbm", ".xc", ".xpm" ]
    for i in ext_list:
            filefilter.add_pattern("*" + i)

    dialog.add_filter(filefilter)
    filefilter = gtk.FileFilter()
    filefilter.set_name(_(" all files           "))
    filefilter.add_pattern("*")
    dialog.add_filter(filefilter)

# preview widget
    dialog.set_use_preview_label(False)
    preview = gtk.VBox(False)
    preview.set_size_request(220,220)
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
    dialog.set_preview_widget_active(True)

# could also 'remove the tupble thing there'
    dialog.connect("update-preview", update_preview_cb, (image, label, label2, label3), exiflabel)

# starting folder
    if general["pic_folder"] == "":
        if general["mswin"]:
          homevar = os.getenv("HOMEDRIVE")
          homevar += "\\" + str(os.getenv("HOMEPATH"))
          if os.path.exists(homevar + "\My Documents"):
              homevar += "\My Documents"
          elif os.path.exists(homevar + "\Eigene Dateien"):
             homevar += "\Eigene Dateien"
        else:
          homevar = os.getenv("HOME")
        if os.path.exists(homevar):
            dialog.set_current_folder(homevar)
    else:
        dialog.set_current_folder(general["pic_folder"])
# dialog run
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        general["pic_folder"] = dialog.get_current_folder()
        imgprocess["files_todo"] = dialog.get_filenames()
        files_print_label(imgprocess["files_todo"])
        counter=0
        print "## Die Bilder Auswahl:"
        print
        for filename in imgprocess["files_todo"]:
            counter += 1
            string = "%3s: " + trimlongline(filename,65)
            print string % (str(counter))
        print

    elif response == gtk.RESPONSE_CANCEL:
        dialog.destroy()
    dialog.destroy()
#}}}
def update_preview_cb(file_chooser, preview, exiflabel ): #{{{
    filename = str(file_chooser.get_preview_filename())  # str needed once on M$
    comment = get_jhead_exif(filename)
    if comment != "":
        exiflabel.set_text(trimlongline(comment,55))
    else:
        exiflabel.set_text("")
    path, filen = os.path.split(filename)
    if file != "":
# encoding hack. grr
        if general["mswin"]:
            preview[1].set_markup("<b>" + filen + "</b>")
        else:
            preview[1].set_markup("<b>" + utf8_enc(filen) + "</b>")
    else:
        preview[1].set_markup("<b>(got no name)</b>")
    if os.path.exists(filename): # once was necessary on M$, or so...
        if os.path.isfile(filename):
            try:
                try:
                    size = os.path.getsize(filename)
                    if (size/1024) == 0:
                        bytes = str(size) + " bytes"
                    else:
                        bytes = str(size/1024) + " Kb"
                except (OSError):
                    bytes = "(got no size)"  # well, should never reach here anyway
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 230, 200)
                preview[0].set_from_pixbuf(pixbuf)
                img = Image.open(filename)
                preview[2].set_markup(str(img.size[0]) + " x " + str(img.size[1]))
                preview[3].set_markup(bytes)
            except (gobject.GError, TypeError, IOError): # file but not viewable
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(general["cwd"] +
                            "bilder/file.png", 96, 96)
                    preview[0].set_from_pixbuf(pixbuf)
                    preview[2].set_markup(bytes)
                    preview[3].set_markup("")
                except (gobject.GError, TypeError, IOError): # file but not viewable
                    pass
        else: # is dir (or so, hm)
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(general["cwd"] +
                        "bilder/folder.png", 96, 96)
                preview[0].set_from_pixbuf(pixbuf)
                preview[2].set_markup("<b>"+ str(len(os.listdir(filename))) +
                        _("</b> items inside"))
                preview[3].set_markup("")
            except (gobject.GError, TypeError, IOError): # file but not viewable
                pass
    return
#             rotate
#}}}
def dialog_delete(widget, dialog): # needs more work #{{{
    text = "<big>%s</big>" % _("are you sure you want to <b>delete</b> selected items - forever?")
    show_2_dialog(dialog, text, _("cancel"), _("yes"))
    if general["dialot2_q"] != "ok_pressed":
        return
    for item in dialog.get_filenames():
        if os.path.isdir(item):
            try:
                os.rmdir(item)
                print "## %s: %s" % ( _("folder removed:"), trimlongline(item,40))
                dialog.set_current_folder(dialog.get_current_folder())
            except OSError,  (errno, errstr):
                print "## %s" %  _("error while trying to delete")
                print "## %s: %s" % (str(errno), errstr)
                dialog_delete_error(dialog, item,
                        _('sorry, could not remove directory:'), errno, errstr)
        else:
            try:
                os.remove(item)
                print "## %s: %s" % (_("file removed:"), trimlongline(item,40))
                dialog.set_current_folder(dialog.get_current_folder())
            except OSError,  (errno, errstr):
                print "## %s" %  _("error while trying to delete")
                print "## %s: %s" % (str(errno), errstr)
                dialog_delete_error(dialog, item,
                        _('sorry, could not remove file:'), errno, errstr)
#}}}
def dialog_delete_error(dialog, item, text, errno, errstr): #{{{
    print "## %s" % text
    print "## %s" % item
    print "## %s: %s" % (str(errno), errstr)
    message = "<big><b>%s</b></big>\n\n%s\n\n%s: %s" % (_("sorry, could not remove file:"),
                                            item, str(errno), errstr)
    show_mesbox(dialog, message)
#             exif comments
#}}}
def get_jhead_exif(file): #{{{
    if not os.path.isfile(file):
        return ""
    fname,ext=os.path.splitext(file);  # file itself
    if ext != ".jpg" and ext != ".jpeg" and ext != ".tif" \
            and ext != ".tiff" and ext != ".tiff24" \
            and ext != ".JPG" and ext != ".JPEG" and ext != ".TIF" \
            and ext != ".TIFF" and ext != ".TIFF24":
        return ""
    pre = ""
    if general["py2exe"]:
        pre = general["cwd"]
    tot = [pre + "jhead"]
    tot.append(str(file))
    try:
        pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=False)
        std_output = pipe.stdout.read()
        err_output = pipe.stderr.read()
    except OSError, (errno, errstr):
        print "## jhead: %s: %s" % (str(errno), errstr)
        return ""
    if err_output != "":
        print "## jhead (ERROR): %s" % err_output
        return ""
    std_output = std_output.split("\n")
    comment = ""
    for item in std_output:
        if item[0:7] == "Comment":
            if comment != "":
                comment += "\n"
            comment += item.split(":")[1][1:]
    return utf8_enc(comment)
#}}}
def show_exif_dialog(parent_widget, text, button_quit, button_ok, file): #{{{
    global general
    general["dialot2_q"] == ""
    mesbox = gtk.Dialog(_("Exif Dialog:"), parent_widget, gtk.DIALOG_MODAL, ())
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)

    align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
    align.set_padding(5, 5, 20, 20)
    align.show()
    vbox = gtk.VBox()
    vbox.show()
    align.add(vbox)
    mesbox.vbox.pack_start(align, True, True, 15)

    label = gtk.Label()
    label.set_markup(text)
    label.show()
    vbox.pack_start(label, True, True, 15)

    textview = gtk.TextView()
    textbuffer = textview.get_buffer()
    comment = get_jhead_exif(file).strip()
    textbuffer.set_text(comment)
    textview.show()
    textview.set_size_request(400, 10)
    textview.set_editable(True)
    textview.set_wrap_mode(gtk.WRAP_NONE)
    textview.set_justification(gtk.JUSTIFY_LEFT)
    textview.set_left_margin(0)
    textview.set_accepts_tab(False)

    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    sw.add(textview)
    sw.show()
    vbox.pack_start(sw, False, False, 0)

    button1 = gtk.Button(button_quit)
    mesbox.action_area.pack_start(button1, True, True, 0)
    button1.connect("clicked", dialog_2_destroy, (mesbox,"quit"))
    button1.show()

    button = gtk.Button(button_ok)
    mesbox.action_area.pack_start(button, True, True, 0)
    button.connect("clicked", dialog_2_destroy, (mesbox,"ok_pressed"))
    button.show()

    mesbox.show()
    textview.grab_focus()

    mesbox.action_area.set_focus_chain((button, button1))

    mesbox.run()
    return textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(), True)
#}}}
def dialog_exif_cb(widget, dialog): #{{{
    files =  dialog.get_filenames()
    if not files:
        return
    filen = files[0]

    if os.path.isdir(filen):
        print "## " + _("can not yet set Exif comments to a directory :P")
        show_mesbox(dialog, "<big><b>%s</b></big>" % (
                 _("can not yet set Exif comments to a directory :P")))
        return
    fname,ext=os.path.splitext(filen);  # file itself
    if ext != ".jpg" and ext != ".jpeg" and ext != ".tif" \
            and ext != ".tiff" and ext != ".tiff24" \
            and ext != ".JPG" and ext != ".JPEG" and ext != ".TIF" \
            and ext != ".TIFF" and ext != ".TIFF24":
        print "## jhead: %s" %  _("does not seem to be a jpg or tiff picture?")
        show_mesbox(dialog, "<big><b>%s</b></big>" %
                    _("does not seem to be a .jpg or .tiff picture?"))
        return

    labeltext = "<big><b>%s</b></big>\n%s" % (_("Exif Comment Editing:"),
                                              _("(see output details on the console)"))
    newcomment = show_exif_dialog(dialog, labeltext, _("cancel"), _("OK, save that"), filen)

    if general["dialot2_q"] == "ok_pressed":
        pre = ""
        if general["py2exe"]:
            pre = general["cwd"]
        tot = [pre + "jhead"]
        tot.append("-cl")

        newcomment = newcomment.strip()
# reverse encoding here, hm, only win2000?
        newcomment = loc_enc(newcomment)

        if str(newcomment) == "":
            tot.append(' ')  # cheating! may change later
        else:
            tot.append(str(newcomment))
        tot.append(filen)
        try:
            pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,\
                    stderr=subprocess.PIPE, shell=False)
            std_output = pipe.stdout.read()
            err_output = pipe.stderr.read()
        except OSError, (errno, errstr):
            print "## jhead (ERROR): %s: %s" % (str(errno), errstr)
            show_mesbox(dialog, "<big><b>%s</b></big>\n\n%s: %s" % (
                _("error while trying to set Exif comment:"), str(errno), errstr))
            return ""
        if err_output != "": # does not reach here unfortunately
            print "## jhead (ERROR): %s" % err_output
            return ""

        print "## jhead: %s" % trimlongline(std_output.replace("\n",""),62)

#        check of correct output, modified... ?
        dialog.emit("update-preview")
        return
    else:
        return
#             rotate
#}}}
def dialog_rotate(widget, dialog, direction): #{{{
    try:
        filen = dialog.get_filenames()[0]  # can be 'None' ?
        if len(dialog.get_filenames()) > 1:
            show_mesbox(dialog, "<big>%s</big>" % _("please select only <b>one</b> pic for rotating"))
            return
        if os.path.isdir(filen):
            show_mesbox(dialog, "<big>%s</big>" % _("don't know how to rotate a folder :P"))
            return
    except IndexError:
        return

    fileext = os.path.splitext(filen)
    targetfile = filen + "_rot" + fileext[1]
    pre = ""
    if general["py2exe"]:
        pre = general["cwd"]
    tot = [pre + "convert","-rotate", direction, filen, targetfile]
    try:
        pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,\
                stderr=subprocess.PIPE, shell=False)
        std_output = pipe.stdout.read()
        err_output = pipe.stderr.read()
    except OSError, (errno, errstr):
        print "## " + _("error while trying to rotate the picture")
        print "## " + str(errno) + ": " + errstr
        return

    if err_output != "" :
        plustext = ""
        if os.path.exists(targetfile) and os.path.getsize(targetfile) > 0 : # real test then here
            plustext = _("Nevertheless, there exists an produced (corrupt?) file at:\n") + targetfile
        print "## %s" % _("error while trying to rotate the picture")
        print "## %s" %  std_output
        if plustext != "":
            print "## %s" % plustext
        text = "<big><b>%s</b></big>:\n\n%s\n\n<b>%s</b>\n\n" % (
                         _("rotating didn't succeed on"), filen, err_output)
        if plustext != "":
            text += plustext
        text += "\n\n%s" % _("(may contact mac@calmar.ws)")
        show_mesbox(dialog,text)
        return

    ## everything seems to be ok
    ## (hopefully) secure overwriting
    if os.path.exists(targetfile) and os.path.getsize(targetfile) > 0 : # real test then here
        try:
            if ( fileext[1] == ".jpg" or fileext[1] == ".jpeg" ) and \
                    (os.path.getsize(filen) - 51200) > os.path.getsize(targetfile):
                print "## %s" % _("Your rotated jpg is smaller than your original file")
                print "## %s" % _("I won't overwrite the file. Find your rotated file, now,")
                print "## %s" % _("with an _rot suffix added")

                text = "<b>%s</b>\n\n%s\n\n%s%s%s" % (
                        _("target file is smaller than your original file"),
                        _("I won't replace your original file."),
                        _("You find your rotated file now with an '_rot' suffix. "),
                        _("imagemagick's jpeg rotate is not lossless, so don't use it on "),
                        _("your original pictures."))

                show_mesbox(dialog,text)
                dialog.set_current_folder(dialog.get_current_folder())
            else:
                os.remove(filen) # could also first move for more security
                try:
                    os.rename(targetfile, filen)
                    print "## %s (%s): %s" % ( _("rotated"), direction, trimlongline(filen, 62))
                except OSError, (errno, errstr):
                    print "## %s" % _("Error while tyring to replace the original file")
                    print "## %s: %s" % (str(errno), errstr)
                    print "## %s:\n## %s" % (_("you find your file now at"),
                            trimlongline(targetfile, 65))
                    text = "<big><b>%s</b></big>\n\n%s\n<b>%s: %s</b>\n\n%s:\n\n%s\n%s" % (
                                _("replacing your original file didn't succeed on:"),
                                filen, str(errno), errstr, _("you find your file now at:"),
                                targetfile, _("(may contact mac@calmar.ws)"))
                    show_mesbox(dialog,text)

        except OSError, (errno, errstr):
           print "## %s" % _("ERROR while trying to replace your file with the rotated one")
           print "## %s: %s" % (str(errno), errstr)
           print "## %s" % _("you find the rotated file now at:")
           print "## %s" % trimlongline(targetfile, 65)
           text = "<big><b>%s</b></big>\n\n%s\n<b>%s: %s</b>\n\n%s:\n\n%s\n%s" % (
                       _("replacing your original file didn't succeed on:"),
                       filen, str(errno), errstr, _("you find your file now at:"),
                       targetfile, _("(may contact mac@calmar.ws)"))
           show_mesbox(dialog,text)
    else:
        print "## %s" % _("Error while tyring to rotate the file")
        print "## %s" % std_output
        text = "<big><b>%s</b></big>\n\n%s\n\n%s\n\n%s" % (
                _("rotating didn't succeed on:"), filen, std_output,
                _("(may contact mac@calmar.ws)"))
        show_mesbox(dialog,text)

    dialog.emit("update-preview")
#             view pics
#}}}
def dialog_viewpics(widget, dialog): #{{{
    if general["viewer"] == "":
        if general["mswin"]:
            print "## %s" % _("select first your viewer (whatever you have) and then try again")
            dialog_setupviewer(None, dialog) #### hmmm
            return
        else:
            general["viewer"] == "display" # for not windows platorms
    try:   # Probably when a folder is selected. Should change later
        filen = dialog.get_filenames()[0]
    except IndexError:
        return
    files = dialog.get_filenames()
    file_show = []
    for filen in files:
        if os.path.isfile(filen):
            file_show.append(filen)
    if not file_show:
        show_mesbox(dialog, "<big><b>%s</b></big>" % _("can not display anything, sorry"))
        return

    tot = [general["viewer"]]
    if general["mswin"]:
        tot.append(files[0])  # for windows viewer only one file?
    else:
        tot += file_show
    try:
        pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,\
                stderr=subprocess.PIPE, shell=False)
        err_output = pipe.stderr.read()
    except OSError, (errno, errstr):
        print _("## error while trying to display the picture(s)")
        print "## %s: %s" % (str(errno), errstr)
        text = "<big><b>%s</b></big>\n\n%s: %s" % (
                _("Error while trying to display the pictures(s)"), str(errno), errstr)
        show_mesbox(dialog, text)
        return

    if err_output != "" :
        print _("## error while trying to display the picture(s)")
        print "## (ERROR): %s" % err_output
        text = "<big><b>%s</b></big>\n\n%s" % (
                _("Error while trying to display the pictures(s)"), err_output )
        show_mesbox(dialog, text )
#}}}
def dialog_setupviewer(widget, dialog_main): #{{{
    dialog = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                   dialog_main,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                   gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.set_select_multiple(False)

    align = gtk.Alignment(xalign=0.5, yalign=0.0, xscale=0.0, yscale=0.0)
    align.set_padding(0, 0, 0, 0)
    align.show()

    dialog.set_extra_widget(align)

    label = gtk.Label()

    text = "\n%s\n\n" % _("<b>Select</b> your <b>previewer</b> for your images - e.g:")
    if general["mswin"]:
        text += "            C:\\Programs\\irfanview\\<b>i_view32.exe</b>" + "\n"
        text += "            C:\\Programs\\GIMP-2.0\\bin\\<b>gimp-2.2.exe</b>" + "\n"
        text += "            <b>.....</b>" + "\n"
    else:
        text += "                   /usr/bin/<b>display</b>" + "\n"
        text += "                   /usr/bin/<b>qiv</b>" + "\n"
        text += "                   ....." + "\n"

    label.set_markup(text)
    label.show()

    align.add(label)

# file filter

    filefilter = gtk.FileFilter()
    filefilter.set_name(_(" all files          "))
    filefilter.add_pattern("*")
    dialog.add_filter(filefilter)

    filefilter = gtk.FileFilter()
    filefilter.set_name(_(" MS-Win executables "))
    filefilter.add_pattern("*.exe")
    dialog.add_filter(filefilter)

# preview widget
    dialog.set_use_preview_label(False)

# starting folder
    if general["bin_folder"] != "":
        dialog.set_current_folder(general["bin_folder"])

    response = dialog.run()

    if response == gtk.RESPONSE_OK:
        general["bin_folder"] = dialog.get_current_folder()
        try:   # Probably when folder is selected, should do in a different way, so
            general["viewer"]  = dialog.get_filenames()[0]
        except IndexError:
            print "## %s" % _("no binary selected? May try again")
            return
    dialog.destroy()
### converting
#}}}
# main and gui
def gui_todo_box(mainbox): #{{{
    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

    if imgprocess["files_todo"] != []:
        files_print_label(imgprocess["files_todo"])
        counter=0
        print "## Die Bilder Auswahl:"
        print
        for filen in imgprocess["files_todo"]:
            counter += 1
            string = "%3s: " + trimlongline(filen,66)
            print string % (str(counter))
        print
    else:
        label_nopic()

    box.pack_start(general["todolabel"], False, False , 0)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)
#}}}
def gui_top_box(mainbox): #{{{
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

#}}}
def gui_last_box(mainbox, acgroup): #{{{
    box = gtk.HBox(False, 0)
    mainbox.pack_start(box, False, False, 0)

    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/go.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("start converting  "))
    hbox.pack_end(label, False, False, 0)
    button = gtk.Button()
    button.add(hbox)
    button.connect("clicked", start_resize, None)
    box.pack_end(button, False, False, 0)

    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/open.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("select pictures...  "))
    hbox.pack_end(label, False, False, 0)
    button = gtk.Button()
    button.add(hbox)
    button.connect("clicked", open_filechooser, acgroup)

    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 15)
    align.add(button)
    box.pack_end(align, False, False, 0)

    button.grab_focus()

    hbox=gtk.HBox()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/stop.png")
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label(_("STOP "))
    hbox.pack_end(label, False, False, 0)
    general["stop_button"].add(hbox)
    general["stop_button"].connect("clicked", stopprogress, None)
    box.pack_end(general["stop_button"], False, False, 0)
#}}}
def gui_setting_box(mainbox): #{{{
    table = gtk.Table(rows=6, columns=2, homogeneous=False)
    mainbox.pack_start(table, False, False, 0)

# over hbox for sizes

    general["sizebox"] = gtk.HBox(True, 0)
    table.attach(general["sizebox"], 0, 2, 0, 1, gtk.EXPAND)
    general["sizebox"].set_sensitive(general["size_or_not"])

# width

    vbox = gtk.VBox(False, 0)
    general["sizebox"].pack_start(vbox, False, False, 5)

    label = gtk.Label()
    label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("width"))
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "1600x", "1280x", "1024x", "800x", "640x",\
            "480x", _("specific:") ]
    values = [ "9999", "1600", "1280", "1024", "800", "640", "480", "0"]
    default = imgprocess["width"]
    general["radio_width"] = create_radios(vbox, values, text, "width", default)

    imgprocess["spinWidth"].set_wrap(False)
    vbox.pack_start(imgprocess["spinWidth"], False, False, 0)


# height

    vbox = gtk.VBox(False, 0)
    general["sizebox"].pack_start(vbox, False, False, 5)

    label = gtk.Label()
    label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("height"))
    vbox.pack_start(label, False, False, 0)

    text = [ _("no limit"), "x1200", "x1024",  "x768", "x600", "x480",\
             "x320", _("specific:") ]
    values = [ "9999", "1200", "1024", "768", "600", "480", "320", "0"]
    default = imgprocess["height"]
    general["radio_height"] = create_radios(vbox, values, text, "height", default)

    imgprocess["spinHeight"].set_wrap(False)
    vbox.pack_start(imgprocess["spinHeight"], False, False, 0)

# overbox finish

# over hbox for percent

    general["percentbox"] = gtk.HBox(False, 0)
    table.attach(general["percentbox"], 2, 3, 0, 1, gtk.EXPAND)
    general["percentbox"].set_sensitive(not general["size_or_not"])


# percent

    vbox = gtk.VBox(False, 0)
    general["percentbox"].pack_start(vbox, False, False, 5)

    label = gtk.Label()
    label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("size in %"))
    vbox.pack_start(label, False, False, 0)

    text = [ "100%", "90%", "80%", "70%", "60%", "50%", "40%", _("specific:") ]
    values = [ "100", "90", "80", "70", "60", "50", "40", "0"]
    default = imgprocess["percent"]
    general["radio_percent"] = create_radios(vbox, values, text, "percent", default)

    imgprocess["spinPercent"].set_wrap(False)
    vbox.pack_start(imgprocess["spinPercent"], False, False, 0)

# overbox finish
#  to toggle sensitivity of the above boxes

    but1 = gtk.Button()
    but1.set_size_request(-1, 8)
    align1 = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align1.set_padding(6, 6, 0, 5)
    align1.add(but1)
    but2 = gtk.Button()
    but2.set_size_request(-1, 8)
    align2 = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align2.set_padding(6, 6, 0, 5)
    align2.add(but2)

    but1.connect("clicked", toggle_percent, but2)
    table.attach(align1, 0, 2, 1, 2, gtk.FILL)

    but2.connect("clicked", toggle_size, but1)
    table.attach(align2, 2, 3, 1, 2, gtk.FILL)

## Vseparator
    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 5)
    separator = gtk.VSeparator()
    align.add(separator)
    table.attach(align,3,4,0,2)

## quality

    vbox = gtk.VBox(False, 0)
    table.attach(vbox, 4, 5, 0, 1)

    label = gtk.Label()
    label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("quality"))
    vbox.pack_start(label, False, False, 0)

    text = [ "100%", "97%", "94%", "90%", "85%", "80%", "60%", _("specific")]
    values = [ "100", "97", "94", "90", "85", "80", "60", "0"]
    default = imgprocess["quality"]
    general["radio_quality"] = create_radios(vbox, values, text, "quality", default)

    imgprocess["spinQuality"].set_wrap(False)
    vbox.pack_start(imgprocess["spinQuality"], False, False, 0)

## separator
    align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
    align.set_padding(0, 0, 5, 5)
    separator = gtk.VSeparator()
    align.add(separator)
    table.attach(align,5,6,0,2)

# prefix/suffix/folder entries

    vbox = gtk.VBox(False, 0)
    table.attach(vbox, 6, 7, 0, 1)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>&lt;%s&gt;</b></span>file.jpg' % _("PREFIX"))
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(60)
    entry.set_alignment(0.49)
    entry.set_text(imgprocess["ent_prefix"])
    entry.connect('changed',entries_cb, "ent_prefix")
    vbox.pack_start(entry, False, False, 0)

    label = gtk.Label()
    label.set_markup('\nfile<span foreground="#000060"><b>&lt;%s&gt;</b></span>.jpg' % _("SUFFIX"))
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(60)
    entry.set_alignment(0.49)
    entry.set_text(imgprocess["ent_suffix"])
    entry.connect('changed',entries_cb, "ent_suffix")
    vbox.pack_start(entry, False, False, 0)

    label = gtk.Label()
    label.set_markup('\n<span foreground="#000060"><b>%s</b></span>, %s' % (_("sub-folder"),
                                        _("for\nthe <u>new</u> pics")))
    vbox.pack_start(label, False, False, 0)
    entry = gtk.Entry(60)
    entry.set_alignment(0.49)
    entry.set_text(imgprocess["ent_folder"])
    entry.connect('changed',entries_cb, "ent_folder")
    vbox.pack_start(entry, False, False, 0)

    label = gtk.Label()
    label.set_markup("%s\n" % _("<b>convert</b> to:"))
    vbox.pack_start(label, False, False, 0)
    combo = gtk.combo_box_new_text()
    combo.set_wrap_width(6)
# the empty one must be there: it's the default, and also set so when no userdata!
    ext_list = ["",
        ".avs", ".bmp", ".cgm", ".cmyk", ".dcx", ".dib", ".eps", ".fax", ".fig",
        ".fits", ".fpx", ".gif", ".gif87", ".hdf", ".ico", ".jbig", ".jpg", ".jpeg", ".map",
        ".matte", ".miff", ".mng", ".mpeg", ".mtv", ".null", ".pbm", ".pcd",
        ".pcl", ".pcx", ".pdf", ".pgm", ".pict", ".plasma", ".png", ".pnm", ".ppm",
        ".ps", ".ps2", ".p7", ".rad", ".rgb", ".rla", ".rle", ".sgi", ".sun", ".text",
        ".tga", ".tiff", ".tiff24", ".tile", ".uil", ".uyvy", ".vicar", ".vid", ".viff",
        ".xbm", ".xc", ".xpm"]
    for ext in ext_list:
        combo.append_text(ext)
    combo.set_active(ext_list.index(imgprocess["ftype"]))
    vbox.pack_start(combo, False, False, 0)
    combo.connect('changed', setcombo)

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)
    return but1, but2
#}}}
def main(): #{{{

    global imgprocess

    general["window"].set_title("Calmar's Picture Resizer - http://www.calmar.ws")
    general["window"].set_default_size(500,300)
    general["window"].connect("delete_event", delete_event)
    general["window"].set_border_width(10)

    acgroup = gtk.AccelGroup()
    general["window"].add_accel_group(acgroup)

    mainbox = gtk.VBox(False, 0)
    general["window"].add(mainbox)

    gui_top_box(mainbox)
    but1, but2 = gui_setting_box(mainbox)
    gui_todo_box(mainbox)
    gui_last_box(mainbox, acgroup)

# show
    font_desc = pango.FontDescription("Courier")
    if font_desc:
        general["todolabel"].modify_font(font_desc)

    general["window"].show_all()

# if showing depends on size_or_not boolean / needs to be at the end or so
    if general["size_or_not"]:
        but1.hide()
        but2.show()
        general["percentbox"].set_sensitive(False)
        general["sizebox"].set_sensitive(True)
    else:
        but2.hide()
        but1.show()
        general["percentbox"].set_sensitive(True)
        general["sizebox"].set_sensitive(False)

    general["stop_button"].hide()

    gtk.main()
    return 0
#}}}
### imports, head (at the bottom :) #{{{
#imports... vars...
import os, sys,  time, string, shelve, subprocess
import gtk, pygtk, pango, gobject
import gettext, locale

# for pyexe 
# PIL needs some help, when py2exe'd
import dbhash
import Image, PngImagePlugin, JpegImagePlugin

gettext.textdomain('cal_pixresizer')
_ = gettext.gettext

locale.setlocale(locale.LC_ALL, "")

# py2exe does not like it
#if gtk.pygtk_version < (2,4,0):
#   print "PyGtk 2.4.0"
#   raise SystemExit
# general (global) - used on many function
radio_bogus = gtk.RadioButton() #radio_ must be radio, gtk calls it before assigned
general = dict( todolabel  = gtk.Label(),
                stop_button    = gtk.Button(),
                encoding       = locale.getpreferredencoding(),
                overwrite_q    = "",
                pic_folder     = "",
                bin_folder     = "",
                dialot2_q      = "",
                viewer         = "",
                mswin          = False,
                stop_progress  = False,
                py2exe         = False,
                sizebox        = True,
                percentbox     = False,
                size_or_not    = True,
                radio_width    = radio_bogus,
                radio_height   = radio_bogus,
                radio_percent  = radio_bogus,
                radio_quality  = radio_bogus,
                window         = gtk.Window(gtk.WINDOW_TOPLEVEL))

if sys.path[0].endswith("\\library.zip"):  #for py2exe
    general["py2exe"] = True
    general["cwd"] = sys.path[0][0:-12] + "/"
else:
    general["cwd"] = sys.path[0] + "/"
gettext.bindtextdomain('cal_pixresizer', general["cwd"] + "locale")

if sys.platform in ["win32", "win16", "win64"]:
    general["mswin"] = True

# imgprocess (global)- data (source) for image processing
imgprocess = dict( ent_prefix  = "",
                   ent_suffix  = "",
                   ent_folder  = "",
                   ftype       = "",
                   files_todo  = [],
                   width       = 9999,
                   height      = 768,
                   percent     = 60,
                   quality     = 94)

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

print "================================================="
print "Calmar's Picture Resizer - a Imagemagick Frontend"
print "================================================="
print

userdata_load()

if __name__ == "__main__":
    main()

#}}}
# vim: foldmethod=marker
