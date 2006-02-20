#!/usr/bin/env python
# Copyright (C) 2006 http://www.calmar.ws #{{{
# http://www.calmar.ws/resize/COPYING
### little FUNCTIONS 
#              gui related
#}}}
class maingui:
# little gui
    def quit_widget(self, widget, data): #{{{
        data.hide()
        data.destroy()
#}}}
    def quit_self(self, widget, *args): #{{{
        widget.hide()
        widget.destroy()
#}}}
    def delete_event(self, widget, event, data=None): #{{{
        self.userdata_save()
        gtk.main_quit()
        return False
#}}}
    def toggle_percent(self, widget, data): #{{{
        data.show()
        widget.hide()
        self.general["percentbox"].set_sensitive(False)
        self.general["sizebox"].set_sensitive(True)
#}}}
    def toggle_size(self, widget, data): #{{{
        data.show()
        widget.hide()
        self.general["percentbox"].set_sensitive(True)
        self.general["sizebox"].set_sensitive(False)
#}}}
    def get_spin_focus(self, widget, spinname): #{{{
        global general
        self.general[spinname].set_active(True)
#}}}
    def setvalue(self, widget, data): #Radio buttons... #{{{
        global general
        self.imgprocess[data[0]] = data[1]
#}}}
    def entries_cb(self, editable, id_edit): #{{{
        global imgprocess
        posi = editable.get_position()
        char = editable.get_chars(posi, posi+1)
        if char == " ":  # replace spaces with underlines
            editable.delete_text(posi,posi+1)
            editable.insert_text("_", posi)
        self.imgprocess[id_edit] = editable.get_text()
#}}}
    def setcombo(self, combobox): #{{{
        global imgprocess
        model = combobox.get_model()
        active = combobox.get_active()
        if active >= 0:
            self.imgprocess["ftype"]=model[active][0]
#              main label
#}}}
    def label_nopic(self): #{{{
        self.general["todolabel"].set_markup("\n\n  <b>-- %s --</b> \n\n" % _("no pictures selected"))
#}}}
    def label_progress(self, count, tot, text, colorstring): #{{{
        self.general["todolabel"].set_markup("\n\n<b>%s (%s/%s): <span %s>%s</span></b>\n\n" %(
                _("progress"), count, tot, colorstring, text))
#}}}
    def label_files(self, files_todo): #{{{
        labeltext=""
        if len(files_todo) == 1:
            labeltext = "\n\n%s\n\n" % trimlongline(files_todo[0])
        elif len(self.imgprocess["files_todo"]) == 2:
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
                labeltext += "%s\n" % (trimlongline(files_todo[i]))
            labeltext += ".....\n"
            labeltext += trimlongline(files_todo[-1])

# encoding hack. grr
        if mswin:
            self.general["todolabel"].set_text(labeltext)
        else:
            self.general["todolabel"].set_text(utf8_enc(labeltext, encoding))
#              create radios
#}}}
    def create_radios(self, vbox, values, text, id_radio, default): #{{{
        for i in range(len(values)):
            if i == 0: # first should not get other radios as reference
                radio = None
            radio = gtk.RadioButton(radio, text[i])
            radio.connect("toggled", self.setvalue, (id_radio, values[i]))
            vbox.pack_start(radio, True, True, 0)
            if values[i] == default:
                radio.set_active(True)
        return radio # return last radio thing for spinner
#              various
#}}}
# little various
    def stopprogress(self, widget, data): #{{{ bla bla
        global imgprocess
#   callback for setting var while someone presses stop during progress
        self.imgprocess["stop_progress"]=True
#              userdata
#}}}
    def userdata_load(self): #{{{
        global general
        global imgprocess

        filename = cwd + "data_cal_pixresizer.cpd"
        d = shelve.open(filename)
        try:
            for key in ["size_or_not", "viewer", "pic_folder", "bin_folder"]:
                self.general[key] = d[key]
            for key in ["ftype", "files_todo", "width", "height", "percent", "quality",\
                    "ent_prefix", "ent_suffix", "ent_folder"]:
                self.imgprocess[key] = d[key]
        except KeyError:
            print >> sys.stderr, "## %s" % _("no valid userdata found")
        d.close()
#}}}
    def userdata_save(self): #{{{
        global general
        global imgprocess

        d = shelve.open(cwd + "data_cal_pixresizer.cpd")
        for key in ["viewer", "pic_folder", "bin_folder"]:
            d[key] = self.general[key]
        for key in ["ftype", "files_todo", "width", "height", "percent", "quality",\
                "ent_prefix", "ent_suffix", "ent_folder"]:
            d[key] = self.imgprocess[key]
        d["size_or_not"] = self.general["sizebox"].get_property("sensitive")
        d.close()
#              encoding stuff
#}}}
#}}}
# converting loop
    def create_subfolder(self, folder, fname): #{{{
        if folder != "" and not os.path.exists(fname + "/" + folder):
            print "## %s: %s (%s/%s)" % (_("create new folder: "), folder,
                         trimlongline(fname, 38), folder)
            try:
                os.mkdir(fname + "/" + folder)
            except OSError, (errno, errstr):
                print >> sys.stderr, ""
                print >> sys.stderr, "## %s" % _("was not able to create target directory: converting will stop")
                print >> sys.stderr, "## %s: %s" % (str(errno), errstr)
                print >> sys.stderr

                text = "<big><b>%s</b></big>\n\n%s/<b>%s</b>\n\n%s\n\n%s: %s" % (
                        _("was not able to create your target folder"),
                        trimlongline(fname ,48), folder,
                        _("please check that issue first"),
                        str(errno), errstr)
                show_mesbox(gtkwindow, text, encoding)
                return False
        else:
            print >> sys.stderr, "## %s" % _("sub-folder exists already")
        return True
#}}}
    def print_settings(self, width, height, percent,  usesize, quality,  folder, prefix, suffix, ftype): #{{{
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
    def get_imgprocess(self): #{{{
        prefix = self.imgprocess["ent_prefix"]
        suffix = self.imgprocess["ent_suffix"]
        folder = self.imgprocess["ent_folder"]
        usesize = True
        if self.general["percentbox"].get_property("sensitive"):
            usesize = False
        if self.imgprocess["width"] == "0": # then, the spinner is selected
            width = str(self.imgprocess["spinWidth"].get_value_as_int())
        else:
            width = str(self.imgprocess["width"])
        if self.imgprocess["height"] == "0":
            height = str(self.imgprocess["spinHeight"].get_value_as_int())
        else:
            height = str(self.imgprocess["height"])
        if self.imgprocess["percent"] == "0":
            percent = str(self.imgprocess["spinPercent"].get_value_as_int())
        else:
            percent = str(self.imgprocess["percent"])
        if self.imgprocess["quality"] == "0":
            quality = str(self.imgprocess["spinQuality"].get_value_as_int())
        else:
            quality = str(self.imgprocess["quality"])
        ftype = self.imgprocess["ftype"]
        return (prefix, suffix, folder, usesize, width, height, percent, quality, ftype)
#}}}
    def no_files_there_selected(self): #{{{
        if not self.imgprocess["files_todo"]:
            show_mesbox(gtkwindow, "<big><b>%s</b></big>" % (
                    _("Select some <b>pics</b> to work on")), encoding)
            return True
#}}}
    def print_stop_message(self, counter, total): #{{{
        self.general["stop_button"].hide()
        self.label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
        print
        print "## %s" % _("stop button pressed: converting has stopped")
        print
        show_mesbox(gtkwindow, "<big><b>%s</b></big>" % _("progress stopped"), encoding)
        self.label_files(self.imgprocess["files_todo"])
#}}}
    def go_on_source_is_equal_target(self, counter, total): #{{{
        print >> sys.stderr, "## " + _("source and target are the same!")
        text = "%s\n\n%s" % (_("<b>source</b> and <b>target</b> are the same!"),
                _("(...cowardly refuses to overwrite)"))
        if not show_2_dialog(gtkwindow, text, _("quit processing"), _("skip and go on...")):
            self.general["stop_button"].hide()
            self.label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
            while gtk.events_pending():
                gtk.main_iteration(False)
            time.sleep(2.0)
            print
            print "## %s" % _("converting has stopped")
            print
            self.label_files(self.imgprocess["files_todo"])
            return False
        else:
            return True
#}}}
    def start_resize(self, widget, event, data=None): #{{{
        global general
        global imgprocess

        if self.no_files_there_selected():
            return
# get imgprocess data
        prefix, suffix, folder, usesize, width, height, percent, quality, ftype = self.get_imgprocess()

# messagebox when there is no suff, pre or folder
        if prefix == "" and suffix == "" and folder == "" and ftype == "":
                text = _("""  At least <u>one</u> must be set:

                  -> <b>Prefix</b>
                  -> <b>Suffix</b>
                  -> <b>subfolder to create pics in</b>
                  -> <b>picture type</b>

     in order to prevent overwriting the original pictures""")
                show_mesbox(gtkwindow, text, encoding)
                return

# to get the path of sample (first) file
        splitfile = os.path.split(self.imgprocess["files_todo"][0])

# create folder when needed
        if not self.create_subfolder(folder, splitfile[0]):
            return
# just some konsole messages
        self.print_settings(width, height, percent, usesize, quality, folder, prefix, suffix, ftype)

# loop preparations
        total = len(self.imgprocess["files_todo"])
        counter = 0
        dist = ""
        self.imgprocess["stop_progress"] = False
        self.general["stop_button"].show()
        self.general["stop_button"].grab_focus()
        overwrite_retval = ""  # reset  'overwrite all' flag
#######################################################################
# begin the loop
#######################################################################
        for sourcefile in self.imgprocess["files_todo"]:
            while gtk.events_pending():
                gtk.main_iteration(False)
# check if stop got pressed
            if self.imgprocess["stop_progress"]:
                self.print_stop_message(counter, total)
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
            self.label_progress(str(counter), str(total), text,"")
            print command_print % (splitfile[1][-1*(dist-1):]) # initial file lenght (dist-1)

# source und target the same?  continue or stop?
            if sourcefile == targetfile:
                if self.go_on_source_is_equal_target(counter, total):
                    continue
                else:
                    return
# check if file exists and may show 'overwrite dialog'
            if os.path.exists(targetfile):
                if overwrite_retval != "all_overwrite":
                    overwrite_retval = show_overwrite_dialog(gtkwindow, targetfile, mswin, encoding)
                    while gtk.events_pending():
                        gtk.main_iteration(False)
                    if overwrite_retval == "skip":
                        print _("# skipped: ") + trimlongline(targetfile,58)
                        continue
                    elif overwrite_retval == "quit":
                        overwrite_retval = ""
                        self.general["stop_button"].hide()
                        self.label_progress(str(counter),str(total),_("stopped!"),"color='#550000'")
                        while gtk.events_pending():
                            gtk.main_iteration(False)
                        time.sleep(2.0)
                        print
                        print _("# converting has stopped ")
                        print
                        self.label_files(self.imgprocess["files_todo"])
                        return
                    elif overwrite_retval == "overwrite":
                        overwrite_retval = ""

            pre = ""
            if py2exe:
                pre = cwd
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
                pipe = subprocess.Popen(tot, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=False)
                err_output = pipe.stderr.read()
            except OSError, (errno, errstr):
                print >> sys.stderr, "## %s" % _("error while trying to convert the picture")
                print >> sys.stderr, "## %s: %s" % (str(errno), errstr)
                text = "%s\n\n%s\n\n%s: %s\n\n%s" % (
                        _("catched an <b>error</b> while working on:"),
                        sourcefile, str(errno), errstr,
                        _("(may contact mac@calmar.ws)"))
                if not show_2_dialog(gtkwindow, text, _("quit processing"), _("skip and go on...")):
                    self.general["stop_button"].hide()
                    self.label_progress(str(counter),str(total), _("canceled!"),"color='#550000'")
                    while gtk.events_pending():
                        gtk.main_iteration(False)
                    time.sleep(2.4)
                    print
                    print "## %s" % _("converting has stopped")
                    print
                    self.label_files(self.imgprocess["files_todo"])
                    return
                else:
                    continue

            if err_output != "" : # an error, since not empty or so
                print >> sys.stderr, "## %s" % _("ERROR while working on that picture")
                print >> sys.stderr, "## %s" % err_output
                print
                if os.path.exists(targetfile) and os.path.getsize(targetfile) == 0 : # del bogus
                    try:
                        os.remove(targetfile)
                    except OSError,  (errno, errstr):
                        print >> sys.stderr, "## %s" % _(" there is a currupt (filesize == 0 bytes) generated file")
                        print >> sys.stderr, "## %s" % targetfile
                        print >> sys.stderr, "## %s" % _("trying to delete, didn't succeed")
                        print >> sys.stderr, "## %s: %s" % (str(errno), errstr)
                        print >> sys.stderr, "## %s" % _("please check that issue yourself as well")

                text = "%s\n\n%s\n<b>%s</b>\n\n%s" % (
                        _("imagemagick terminated with an <b>error</b> while working on:"),
                        sourcefile, err_output, _("(may contact mac@calmar.ws)"))
                if not show_2_dialog(gtkwindow, text, _("quit processing"), _("skip and go on...")):
                    self.general["stop_button"].hide()
                    self.label_progress(str(counter),str(total), _("canceled!"),"color='#550000'")
                    while gtk.events_pending():
                        gtk.main_iteration(False)
                    time.sleep(2.4)
                    #self.label_nopic()
                    # self.imgprocess["files_todo"]=[]
                    print
                    print _("# converting has stopped ")
                    print
                    self.label_files(self.imgprocess["files_todo"])
                    return

        print
        print "## %s" % _("progress finished")
        print

        self.general["stop_button"].hide()
        self.label_progress(str(total),str(total), _("finish!"),"color='#000070'")

        while gtk.events_pending():
            gtk.main_iteration(False)
        time.sleep(2.0)

        self.label_files(self.imgprocess["files_todo"])
### major GUI
#}}}
# main and gui
    def open_filechooser_func(self, widget, acgroup): #{{{
        global general
        fcgui = Filechoosegui.filechoose(widget, 
                                         acgroup, 
                                         gtkwindow,
                                         self.general["pic_folder"], 
                                         mswin,
                                         cwd,
                                         py2exe,
                                         self.general["bin_folder"],
                                         self.general["viewer"],
                                         encoding)

        self.general["pic_folder"] = fcgui.pic_dir
        self.general["bin_folder"] = fcgui.bin_dir
        self.general["viewer"] = fcgui.viewer

        if fcgui.files:
            self.imgprocess["files_todo"] = fcgui.files
        self.label_files(self.imgprocess["files_todo"])

        counter=0
        print "## Die Bilder Auswahl:"
        print
        for filename in self.imgprocess["files_todo"]:
            counter += 1
            string = "%3s: " + trimlongline(filename,65)
            print string % (str(counter))
#}}} 
    def gui_todo_box(self, mainbox): #{{{
        box = gtk.HBox(False, 0)
        mainbox.pack_start(box, False, False, 0)

        if self.imgprocess["files_todo"] != []:
            self.label_files(self.imgprocess["files_todo"])
            counter=0
            print "## Die Bilder Auswahl:"
            print
            for fname in self.imgprocess["files_todo"]:
                counter += 1
                string = "%3s: " + trimlongline(fname,66)
                print string % (str(counter))
            print
        else:
            self.label_nopic()

        box.pack_start(self.general["todolabel"], False, False , 0)

        separator = gtk.HSeparator()
        mainbox.pack_start(separator, False, False, 5)
#}}}
    def gui_top_box(self, mainbox): #{{{
        box = gtk.HBox(False, 0)
        mainbox.pack_start(box, False, False, 0)

        image = gtk.Image()
        image.set_from_file(cwd + "bilder/calmar.png")
        box.pack_start(image, False, False , 0)

        image = gtk.Image()
        image.set_from_file(cwd + "bilder/exit.png")
        but_quit = gtk.Button()
        hbox=gtk.HBox()
        hbox.pack_end(image, False, False, 0)
        but_quit.add(hbox)
        label = gtk.Label(_("exit"))
        hbox.pack_end(label, False, False, 0)

        but_quit.connect("clicked", self.delete_event, None)
        box.pack_end(but_quit, False, False, 0)

        separator = gtk.HSeparator()
        mainbox.pack_start(separator, False, False, 5)

#}}}
    def gui_last_box(self, mainbox, acgroup): #{{{
        box = gtk.HBox(False, 0)
        mainbox.pack_start(box, False, False, 0)

        hbox=gtk.HBox()
        image = gtk.Image()
        image.set_from_file(cwd + "bilder/go.png")
        hbox.pack_end(image, False, False, 0)
        label = gtk.Label(_("start converting  "))
        hbox.pack_end(label, False, False, 0)
        button = gtk.Button()
        button.add(hbox)
        button.connect("clicked", self.start_resize, None)
        box.pack_end(button, False, False, 0)

        hbox=gtk.HBox()
        image = gtk.Image()
        image.set_from_file(cwd + "bilder/open.png")
        hbox.pack_end(image, False, False, 0)
        label = gtk.Label(_("select pictures...  "))
        hbox.pack_end(label, False, False, 0)
        button = gtk.Button()
        button.add(hbox)
        button.connect("clicked", self.open_filechooser_func, acgroup)

        align = gtk.Alignment(xalign=1.0, yalign=1.0, xscale=1.0, yscale=1.0)
        align.set_padding(0, 0, 5, 15)
        align.add(button)
        box.pack_end(align, False, False, 0)

        button.grab_focus()

        hbox=gtk.HBox()
        image = gtk.Image()
        image.set_from_file(cwd + "bilder/stop.png")
        hbox.pack_end(image, False, False, 0)
        label = gtk.Label(_("STOP "))
        hbox.pack_end(label, False, False, 0)
        self.general["stop_button"].add(hbox)
        self.general["stop_button"].connect("clicked", self.stopprogress, None)
        box.pack_end(self.general["stop_button"], False, False, 0)
#}}}
    def gui_setting_box(self, mainbox): #{{{
        table = gtk.Table(rows=6, columns=2, homogeneous=False)
        mainbox.pack_start(table, False, False, 0)

# over hbox for sizes

        self.general["sizebox"] = gtk.HBox(True, 0)
        table.attach(self.general["sizebox"], 0, 2, 0, 1, gtk.EXPAND)
        self.general["sizebox"].set_sensitive(self.general["size_or_not"])

# width

        vbox = gtk.VBox(False, 0)
        self.general["sizebox"].pack_start(vbox, False, False, 5)

        label = gtk.Label()
        label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("width"))
        vbox.pack_start(label, False, False, 0)

        text = [ _("no limit"), "1600x", "1280x", "1024x", "800x", "640x",\
                "480x", _("specific:") ]
        values = [ "9999", "1600", "1280", "1024", "800", "640", "480", "0"]
        default = self.imgprocess["width"]
        self.general["radio_width"] = self.create_radios(vbox, values, text, "width", default)

        self.imgprocess["spinWidth"].set_wrap(False)
        vbox.pack_start(self.imgprocess["spinWidth"], False, False, 0)


# height

        vbox = gtk.VBox(False, 0)
        self.general["sizebox"].pack_start(vbox, False, False, 5)

        label = gtk.Label()
        label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("height"))
        vbox.pack_start(label, False, False, 0)

        text = [ _("no limit"), "x1200", "x1024",  "x768", "x600", "x480",\
                 "x320", _("specific:") ]
        values = [ "9999", "1200", "1024", "768", "600", "480", "320", "0"]
        default = self.imgprocess["height"]
        self.general["radio_height"] = self.create_radios(vbox, values, text, "height", default)

        self.imgprocess["spinHeight"].set_wrap(False)
        vbox.pack_start(self.imgprocess["spinHeight"], False, False, 0)

# overbox finish

# over hbox for percent

        self.general["percentbox"] = gtk.HBox(False, 0)
        table.attach(self.general["percentbox"], 2, 3, 0, 1, gtk.EXPAND)
        self.general["percentbox"].set_sensitive(not self.general["size_or_not"])


# percent

        vbox = gtk.VBox(False, 0)
        self.general["percentbox"].pack_start(vbox, False, False, 5)

        label = gtk.Label()
        label.set_markup("<span foreground=\"#000060\"><b>%s</b></span>" % _("size in %"))
        vbox.pack_start(label, False, False, 0)

        text = [ "100%", "90%", "80%", "70%", "60%", "50%", "40%", _("specific:") ]
        values = [ "100", "90", "80", "70", "60", "50", "40", "0"]
        default = self.imgprocess["percent"]
        self.general["radio_percent"] = self.create_radios(vbox, values, text, "percent", default)

        self.imgprocess["spinPercent"].set_wrap(False)
        vbox.pack_start(self.imgprocess["spinPercent"], False, False, 0)

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

        but1.connect("clicked", self.toggle_percent, but2)
        table.attach(align1, 0, 2, 1, 2, gtk.FILL)

        but2.connect("clicked", self.toggle_size, but1)
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
        default = self.imgprocess["quality"]
        self.general["radio_quality"] = self.create_radios(vbox, values, text, "quality", default)

        self.imgprocess["spinQuality"].set_wrap(False)
        vbox.pack_start(self.imgprocess["spinQuality"], False, False, 0)

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
        entry.set_text(self.imgprocess["ent_prefix"])
        entry.connect('changed', self.entries_cb, "ent_prefix")
        vbox.pack_start(entry, False, False, 0)

        label = gtk.Label()
        label.set_markup('\nfile<span foreground="#000060"><b>&lt;%s&gt;</b></span>.jpg' % _("SUFFIX"))
        vbox.pack_start(label, False, False, 0)
        entry = gtk.Entry(60)
        entry.set_alignment(0.49)
        entry.set_text(self.imgprocess["ent_suffix"])
        entry.connect('changed', self.entries_cb, "ent_suffix")
        vbox.pack_start(entry, False, False, 0)

        label = gtk.Label()
        label.set_markup('\n<span foreground="#000060"><b>%s</b></span>, %s' % (_("sub-folder"),
                                            _("for\nthe <u>new</u> pics")))
        vbox.pack_start(label, False, False, 0)
        entry = gtk.Entry(60)
        entry.set_alignment(0.49)
        entry.set_text(self.imgprocess["ent_folder"])
        entry.connect('changed', self.entries_cb, "ent_folder")
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
        combo.set_active(ext_list.index(self.imgprocess["ftype"]))
        vbox.pack_start(combo, False, False, 0)
        combo.connect('changed', self.setcombo)

        separator = gtk.HSeparator()
        mainbox.pack_start(separator, False, False, 5)
        return but1, but2
#}}}
    def __init__(self): #{{{

        self.radio_bogus = gtk.RadioButton() #radio_ must be radio, gtk calls it before assigned
        self.general = dict( todolabel = gtk.Label(),
                        stop_button    = gtk.Button(),
                        pic_folder     = "",
                        bin_folder     = "",
                        viewer         = "",
                        mswin          = False,
                        stop_progress  = False,
                        sizebox        = True,
                        percentbox     = False,
                        size_or_not    = True,
                        radio_width    = self.radio_bogus,
                        radio_height   = self.radio_bogus,
                        radio_percent  = self.radio_bogus,
                        radio_quality  = self.radio_bogus)


# imgprocess (global)- data (source) for image processing
        self.imgprocess = dict( ent_prefix  = "",
                           ent_suffix  = "",
                           ent_folder  = "",
                           ftype       = "",
                           files_todo  = [],
                           width       = "9999",
                           height      = "768",
                           percent     = "60",
                           quality     = "94")

        adj = gtk.Adjustment(1024, 10, 2000, 1, 100, 0)
        adj.connect("value_changed", self.get_spin_focus, "radio_width" )
        self.imgprocess["spinWidth"] = gtk.SpinButton(adj, 1.0, 0)
        self.imgprocess["spinWidth"].set_numeric(True)  #spinnervalue needed later
        adj = gtk.Adjustment(768, 10, 2000, 1, 100, 0)
        adj.connect("value_changed", self.get_spin_focus, "radio_height" )
        self.imgprocess["spinHeight"] = gtk.SpinButton(adj, 1.0, 0)
        self.imgprocess["spinHeight"].set_numeric(True)
        adj = gtk.Adjustment(60, 10, 400, 1, 30, 0)
        adj.connect("value_changed", self.get_spin_focus, "radio_percent" )
        self.imgprocess["spinPercent"] = gtk.SpinButton(adj, 1.0, 0)
        self.imgprocess["spinPercent"].set_numeric(True)
        adj = gtk.Adjustment(90, 10, 100, 1, 10, 0)
        adj.connect("value_changed", self.get_spin_focus, "radio_quality" )
        self.imgprocess["spinQuality"] = gtk.SpinButton(adj,0.1, 0)
        self.imgprocess["spinQuality"].set_numeric(True)

        print "================================================="
        print "Calmar's Picture Resizer - a Imagemagick Frontend"
        print "================================================="
        print

        self.userdata_load()

        gtkwindow.set_title("Calmar's Picture Resizer - http://www.calmar.ws")
        gtkwindow.set_default_size(500,300)
        gtkwindow.connect("delete_event", self.delete_event)
        gtkwindow.set_border_width(10)

        acgroup = gtk.AccelGroup()  # not needed actually.
        gtkwindow.add_accel_group(acgroup)

        mainbox = gtk.VBox(False, 0)
        gtkwindow.add(mainbox)

        self.gui_top_box(mainbox)
        but1, but2 = self.gui_setting_box(mainbox)
        self.gui_todo_box(mainbox)
        self.gui_last_box(mainbox, acgroup)

# show
        font_desc = pango.FontDescription("Courier")
        if font_desc:
            self.general["todolabel"].modify_font(font_desc)

        gtkwindow.show_all()

# if showing depends on size_or_not boolean / needs to be at the end or so
        if self.general["size_or_not"]:
            but1.hide()
            but2.show()
            self.general["percentbox"].set_sensitive(False)
            self.general["sizebox"].set_sensitive(True)
        else:
            but2.hide()
            but1.show()
            self.general["percentbox"].set_sensitive(True)
            self.general["sizebox"].set_sensitive(False)

        self.general["stop_button"].hide()
#}}}
def main(): #{{{
    maingui()
    gtk.main()
    return 0
#}}}
### imports, head (at the bottom :) #{{{
#imports... vars...
import os, sys,  time, string, shelve, subprocess
import gtk, pango
#import pygtk
import gettext, locale

# for pyexe 
# PIL needs some help, when py2exe'd
import dbhash
import Image, PngImagePlugin, JpegImagePlugin

# classes
import Filechoosegui
from Messageboxes import *
from Varhelp import *

# globals/konstants - used on many function
gettext.textdomain('cal_pixresizer')
_ = gettext.gettext

if sys.path[0].endswith("\\library.zip"):  #for py2exe
    py2exe = True
    cwd = sys.path[0][0:-12] + "/"
else:
    py2exe = False
    cwd = sys.path[0] + "/"


if sys.platform in ["win32", "win16", "win64"]:
    mswin = True
else:
    mswin = False

gettext.bindtextdomain('cal_pixresizer', cwd + "locale")
locale.setlocale(locale.LC_ALL, "")

encoding = locale.getpreferredencoding()

gtkwindow  = gtk.Window(gtk.WINDOW_TOPLEVEL)


if __name__ == "__main__":
    main()

#}}}
# vim: foldmethod=marker
