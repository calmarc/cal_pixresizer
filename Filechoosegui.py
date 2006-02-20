# filechooser Class
import os, subprocess  #{{{
import gtk, gobject, Image
#import pygtk
import gettext
from Messageboxes import *
from Varhelp import *
gettext.textdomain('cal_pixresizer')
_ = gettext.gettext
#}}}
class filechoose:
    def __init__(self, widget, acgroup, mainwindow, pic_dir, #{{{
                 mswin, cwd, py2exe, bin_dir, viewer, encoding):
        self.files = []
        self.pic_dir = pic_dir
        self.mswin = mswin
        self.cwd = cwd
        self.py2exe = py2exe
        self.bin_dir = bin_dir
        self.viewer = viewer
        self.encoding = encoding

        self.dialog = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                       mainwindow,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        self.dialog.set_default_response(gtk.RESPONSE_OK)
        self.dialog.set_select_multiple(True)
        self.dialog.set_size_request(700,500)

        self.dialog.add_accel_group(acgroup)
# main vbox overall there
        vbox = gtk.VBox()
        vbox.show()

# set main widget
        self.dialog.set_extra_widget(vbox)

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
        button.connect("clicked", self.dialog_delete)
        table.attach(button, 1, 2, 0, 1, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#00008a" size="larger">' +
                _("select <b><u>a</u></b>ll images") + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.add_accelerator('clicked', acgroup, ord('a'), 0, gtk.ACCEL_VISIBLE )
        button.connect("clicked", lambda w, d: d.select_all())
        table.attach(button, 2, 3, 0, 1, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#002a00" size="larger">' +
                _("pre<b><u>v</u></b>iew pictures") + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.connect("clicked", self.dialog_viewpics)
        button.add_accelerator('clicked', acgroup, ord('v'), 0, gtk.ACCEL_VISIBLE )
        table.attach(button, 3, 4, 0, 1, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#402a20" size="larger">' +
                _("rotate l<b><u>e</u></b>ft") + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.connect("clicked", self.dialog_rotate, "-90")
        button.add_accelerator('clicked', acgroup, ord('e'), 0, gtk.ACCEL_VISIBLE )
        table.attach(button, 1, 2, 1, 2, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#402a20" size="larger">' +
                _("rotate <b><u>r</u></b>ight") + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.connect("clicked", self.dialog_rotate, "+90")
        button.add_accelerator('clicked', acgroup, ord('r'), 0, gtk.ACCEL_VISIBLE )
        table.attach(button, 2, 3, 1, 2, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#405a30" size="larger">' + _("choose viewer") + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.connect("clicked", self.dialog_setupviewer)
        table.attach(button, 3, 4, 1, 2, gtk.FILL)

        label = gtk.Label()
        label.set_markup('<span color="#610e4d" size="larger">' +
                _('edit e<b><u>x</u></b>if comment') + '</span>')
        label.show()
        button = gtk.Button()
        button.add(label)
        button.show()
        button.add_accelerator('clicked', acgroup, ord('x'), 0, gtk.ACCEL_VISIBLE )
        button.connect("clicked", self.dialog_exif_cb)
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

        self.dialog.add_filter(filefilter)
        filefilter = gtk.FileFilter()
        filefilter.set_name(_(" all files           "))
        filefilter.add_pattern("*")
        self.dialog.add_filter(filefilter)

# preview widget
        self.dialog.set_use_preview_label(False)
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
        self.dialog.set_preview_widget(preview)
        self.dialog.set_preview_widget_active(True)

# could also 'remove the tupble thing there'
        self.dialog.connect("update-preview", self.update_preview_cb, (image, label, label2, label3), exiflabel)

# starting folder
        if self.pic_dir == "":
            if self.mswin:
              homevar = os.getenv("HOMEDRIVE")
              homevar += "\\" + str(os.getenv("HOMEPATH"))
              if os.path.exists(homevar + "\My Documents"):
                  homevar += "\My Documents"
              elif os.path.exists(homevar + "\Eigene Dateien"):
                 homevar += "\Eigene Dateien"
            else:
              homevar = os.getenv("HOME")
            if os.path.exists(homevar):
                self.dialog.set_current_folder(homevar)
        else:
            self.dialog.set_current_folder(self.pic_dir)
# dialog run
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.pic_dir = self.dialog.get_current_folder()
            self.files = self.dialog.get_filenames() 
            self.dialog.destroy()
        elif response == gtk.RESPONSE_CANCEL:
            self.dialog.destroy()
#}}}
    def update_preview_cb(self, file_chooser, preview, exiflabel ): #{{{
        filename = str(file_chooser.get_preview_filename())  # str needed once on M$
        comment = self.get_jhead_exif(filename)
        if comment != "":
            exiflabel.set_text(trimlongline(comment,55))
        else:
            exiflabel.set_text("")
        path, filen = os.path.split(filename)
        if file != "":
# encoding hack. grr
            if self.mswin:
                preview[1].set_markup("<b>" + filen + "</b>")
            else:
                preview[1].set_markup("<b>" + self.utf8_enc(filen) + "</b>")
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
                        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.cwd +
                                "bilder/file.png", 96, 96)
                        preview[0].set_from_pixbuf(pixbuf)
                        preview[2].set_markup(bytes)
                        preview[3].set_markup("")
                    except (gobject.GError, TypeError, IOError): # file but not viewable
                        pass
            else: # is dir (or so, hm)
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.cwd +
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
    def dialog_delete(self, widget): # needs more work #{{{
        text = "<big>%s</big>" % _("are you sure you want to <b>delete</b> selected items - forever?")
        if not show_2_dialog(self.dialog, text, _("cancel"), _("yes")):
            return
        for item in self.dialog.get_filenames():
            if os.path.isdir(item):
                try:
                    os.rmdir(item)
                    print "## %s: %s" % ( _("folder removed:"), trimlongline(item,40))
                    self.dialog.set_current_folder(self.dialog.get_current_folder())
                except OSError,  (errno, errstr):
                    print "## %s" %  _("error while trying to delete")
                    print "## %s: %s" % (str(errno), errstr)
                    self.dialog_delete_error(item,
                            _('sorry, could not remove directory:'), errno, errstr)
            else:
                try:
                    os.remove(item)
                    print "## %s: %s" % (_("file removed:"), trimlongline(item,40))
                    self.dialog.set_current_folder(self.dialog.get_current_folder())
                except OSError,  (errno, errstr):
                    print "## %s" %  _("error while trying to delete")
                    print "## %s: %s" % (str(errno), errstr)
                    self.dialog_delete_error(item,
                            _('sorry, could not remove file:'), errno, errstr)
#}}}
    def dialog_delete_error(self, item, text, errno, errstr): #{{{
        print "## %s" % text
        print "## %s" % item
        print "## %s: %s" % (str(errno), errstr)
        message = "<big><b>%s</b></big>\n\n%s\n\n%s: %s" % (_("sorry, could not remove file:"),
                                                item, str(errno), errstr)
        show_mesbox(self.dialog, message, self.encoding)
#             exif comments
#}}}
    def get_jhead_exif(self, file): #{{{
        if not os.path.isfile(file):
            return ""
        fname,ext=os.path.splitext(file);  # file itself
        if ext != ".jpg" and ext != ".jpeg" and ext != ".tif" \
                and ext != ".tiff" and ext != ".tiff24" \
                and ext != ".JPG" and ext != ".JPEG" and ext != ".TIF" \
                and ext != ".TIFF" and ext != ".TIFF24":
            return ""
        pre = ""
        if self.py2exe:
            pre = self.cwd
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
        return self.utf8_enc(comment)
#}}}
    def show_exif_dialog(self, text, button_quit, button_ok, file): #{{{
        mesbox = gtk.Dialog(_("attention:"),
                               self.dialog, 
                               gtk.DIALOG_MODAL,
                               (button_ok, gtk.RESPONSE_OK,
                               button_quit, gtk.RESPONSE_CANCEL))

        mesbox.set_default_response(gtk.RESPONSE_OK)

        mesbox.connect("destroy", self.quit_self, None)
        mesbox.connect("delete_event", self.quit_self, None)

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
        comment = self.get_jhead_exif(file).strip()
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

        mesbox.show()

        textview.grab_focus()

#        mesbox.action_area.set_focus_chain((button, button1))

        response = mesbox.run()
        if response == gtk.RESPONSE_OK:
            print "OK"
            mesbox.hide()
            mesbox.destroy()
            text = textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(), True)
            return (True, text)
        else:
            mesbox.hide()
            mesbox.destroy()
            return (False, "")
#}}}
    def dialog_exif_cb(self, widget): #{{{
        files =  self.dialog.get_filenames()
        if not files:
            return
        filen = files[0]

        if os.path.isdir(filen):
            print "## " + _("can not yet set Exif comments to a directory :P")
            show_mesbox(self.dialog, "<big><b>%s</b></big>" % (
                     _("can not yet set Exif comments to a directory :P")), self.encoding)
            return
        fname,ext=os.path.splitext(filen);  # file itself
        if ext != ".jpg" and ext != ".jpeg" and ext != ".tif" \
                and ext != ".tiff" and ext != ".tiff24" \
                and ext != ".JPG" and ext != ".JPEG" and ext != ".TIF" \
                and ext != ".TIFF" and ext != ".TIFF24":
            print "## jhead: %s" %  _("does not seem to be a jpg or tiff picture?")
            show_mesbox(self.dialog, "<big><b>%s</b></big>" %
                        _("does not seem to be a .jpg picture?"), self.encoding)
            return

        labeltext = "<big><b>%s</b></big>\n%s" % (_("Exif Comment Editing:"),
                                                  _("(see output details on the console)"))
        ok_or_not, ret_text = self.show_exif_dialog(labeltext, _("cancel"),
                                                    _("OK, save that"), filen)

        if ok_or_not: # ok pressed
            pre = ""
            if self.py2exe:
                pre = self.cwd
            tot = [pre + "jhead"]
            tot.append("-cl")

            newcomment = ret_text.strip()
# reverse encoding here, hm, only win2000?
            newcomment = self.loc_enc(newcomment)

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
                show_mesbox(self.dialog, "<big><b>%s</b></big>\n\n%s: %s" % (
                    _("error while trying to set Exif comment:"), str(errno), errstr), self.encoding)
                return ""
            if err_output != "": # does not reach here unfortunately
                print "## jhead (ERROR): %s" % err_output
                return ""

            print "## jhead: %s" % trimlongline(std_output.replace("\n",""),62)

#        check of correct output, modified... ?
            self.dialog.emit("update-preview")
            return
        else:
            return

#}}}
    def dialog_rotate(self, widget, direction): #{{{
        try:
            filen = self.dialog.get_filenames()[0]  # can be 'None' ?
            if len(self.dialog.get_filenames()) > 1:
                show_mesbox(self.dialog, "<big>%s</big>" % _("please select only <b>one</b> pic for rotating"), self.encoding)
                return
            if os.path.isdir(filen):
                show_mesbox(self.dialog, "<big>%s</big>" % _("don't know how to rotate a folder :P"), self.encoding)
                return
        except IndexError:
            return

        fileext = os.path.splitext(filen)
        targetfile = filen + "_rot" + fileext[1]
        pre = ""
        if self.py2exe:
            pre = self.cwd
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
            show_mesbox(self.dialog,text, self.encoding)
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

                    show_mesbox(self.dialog, text, self.encoding)
                    self.dialog.set_current_folder(self.dialog.get_current_folder())
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
                        show_mesbox(self.dialog, text, self.encoding)

            except OSError, (errno, errstr):
               print "## %s" % _("ERROR while trying to replace your file with the rotated one")
               print "## %s: %s" % (str(errno), errstr)
               print "## %s" % _("you find the rotated file now at:")
               print "## %s" % trimlongline(targetfile, 65)
               text = "<big><b>%s</b></big>\n\n%s\n<b>%s: %s</b>\n\n%s:\n\n%s\n%s" % (
                           _("replacing your original file didn't succeed on:"),
                           filen, str(errno), errstr, _("you find your file now at:"),
                           targetfile, _("(may contact mac@calmar.ws)"))
               show_mesbox(self.dialog, text, self.encoding)
        else:
            print "## %s" % _("Error while tyring to rotate the file")
            print "## %s" % std_output
            text = "<big><b>%s</b></big>\n\n%s\n\n%s\n\n%s" % (
                    _("rotating didn't succeed on:"), filen, std_output,
                    _("(may contact mac@calmar.ws)"))
            show_mesbox(self.dialog, text, self.encoding)

        self.dialog.emit("update-preview")
#             view pics
#}}}
    def dialog_viewpics(self, widget): #{{{
        if self.viewer == "":
            if self.mswin:
                print "## %s" % _("select first your viewer (whatever you have) and then try again")
                self.dialog_setupviewer() #### hmmm
                return
            else:
                self.viewer == "display" # for not windows platorms
        try:   # Probably when a folder is selected. Should change later
            filen = self.dialog.get_filenames()[0]
        except IndexError:
            return
        files = self.dialog.get_filenames()
        file_show = []
        for filen in files:
            if os.path.isfile(filen):
                file_show.append(filen)
        if not file_show:
            show_mesbox(self.dialog, "<big><b>%s</b></big>" % _("can not display anything, sorry"), self.encoding)
            return

        tot = [self.viewer]
        if self.mswin:
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
            show_mesbox(self.dialog, text, self.encoding)
            return

        if err_output != "" :
            print _("## error while trying to display the picture(s)")
            print "## (ERROR): %s" % err_output
            text = "<big><b>%s</b></big>\n\n%s" % (
                    _("Error while trying to display the pictures(s)"), err_output )
            show_mesbox(self.dialog, text, self.encoding)
#}}}
    def dialog_setupviewer(self): #{{{
        dialog_sw = gtk.FileChooserDialog(_("Calmar's Picture Resizer - select pictures..."),
                                       self.dialog,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog_sw.set_default_response(gtk.RESPONSE_OK)
        dialog_sw.set_select_multiple(False)

        align = gtk.Alignment(xalign=0.5, yalign=0.0, xscale=0.0, yscale=0.0)
        align.set_padding(0, 0, 0, 0)
        align.show()

        dialog_sw.set_extra_widget(align)

        label = gtk.Label()

        text = "\n%s\n\n" % _("<b>Select</b> your <b>previewer</b> for your images - e.g:")
        if self.mswin:
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
        dialog_sw.add_filter(filefilter)

        filefilter = gtk.FileFilter()
        filefilter.set_name(_(" MS-Win executables "))
        filefilter.add_pattern("*.exe")
        dialog_sw.add_filter(filefilter)

# preview widget
        dialog_sw.set_use_preview_label(False)

# starting folder
        if self.bin_dir != "":
            dialog_sw.set_current_folder(self.bin_dir)

        response = dialog_sw.run()

        if response == gtk.RESPONSE_OK:
            self.bin_dir = dialog_sw.get_current_folder()
            try:   # Probably when folder is selected, should do in a different way, so
                self.viewer = dialog_sw.get_filenames()[0]
            except IndexError:
                print "## %s" % _("no binary selected? May try again")
                return
        dialog_sw.destroy()
#}}}
    def loc_enc(self, text): #{{{
        obj = unicode(text, 'utf-8')
        return obj.encode( self.encoding)
#}}}
    def utf8_enc(self, text): #{{{
        obj = unicode(text, self.encoding)
        return obj.encode('utf-8')
#}}}
    def quit_self(self, widget, *args): #{{{
        widget.hide()
        widget.destroy()
#}}}
# vim: foldmethod=marker
