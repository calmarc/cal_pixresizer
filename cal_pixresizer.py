#!/usr/bin/env python
# Copyright (C) 2006 http://www.calmar.ws {{{
# http://www.calmar.ws/resize/COPYING
# }}}
def get_spin_focus(widget, varname): #{{{
    general[varname].set_active(True)
#}}}
def delete_event(widget, event, data=None): #{{{
    gtk.main_quit()
    return False
#}}}
def quit_widget(widget, data): #{{{
    data.hide()
    data.destroy()
#}}}
def quit_self(self, *args): #{{{
    self.hide()
    self.destroy()
#}}}
def setvalue(widget, data): #{{{
    global general
    imgprocess[data[0]] = data[1]
#}}}
def trimlongline(loc_item, size=72): #{{{
    if len(loc_item) >= size:
        loc_item = loc_item[0:size/4] + "..." + loc_item[-1*((size-size/4)-3):]
    return loc_item
#}}}
def update_preview_cb(file_chooser, preview): #{{{
    try:
        filename = file_chooser.get_preview_filename()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 160, 160)
        preview[1].set_from_pixbuf(pixbuf)
        pil_img = Image.open(filename)
        preview[0].set_markup("<b>" + os.path.split(filename)[1] + "</b>\n (" + str(pil_img.size[0]) \
               + " x " + str(pil_img.size[1]) + ")" )
        have_preview = True
    except:
        have_preview = False

    file_chooser.set_preview_widget_active(have_preview)
    return
#}}}
def create_radios(vbox,values,text,ipvar, default): #{{{
    for i in range(len(values)):
        if i == 0: 
            radio = None
        radio = gtk.RadioButton(radio, text[i])
        radio.connect("toggled",setvalue, (ipvar, values[i]))
        vbox.pack_start(radio, True, True, 0)
        if values[i] == default:
            radio.set_active(True)
        radio.show()
    return radio # return last radio thing for spinner
#}}}
def show_mesbox(text): #{{{
    mesbox = gtk.Dialog("Calmar's Picture Resizer", general["window"], gtk.DIALOG_MODAL,\
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
def overwrite_destroy(widget, data): #{{{
    global general
    general["what_todo"] = str(data[1])
    data[0].hide()
    data[0].destroy()
#}}}
def open_filechooser(widget, event, data=None): #{{{
    global general

    dialog = gtk.FileChooserDialog("Calmar's Picture Resizer - Bilder waehlen...",
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

    button = gtk.Button("Alle Bilder auswaehlen")
    button.show()
    button.connect("clicked", lambda w, d: d.select_all(), dialog)
    hbutton_box.add(button)

    label = gtk.Label()
    label.set_markup("<b>Ctrl</b> + linke Maus fuer zusaetzliche Auswahl\n<b>Shift</b> +\
linke Maus fuer Bereiche")
    label.show()
    vbox.pack_start(label, False, False, 0)


    filter = gtk.FileFilter()
    filter.set_name(" Images ")
    filter.add_mime_type("image/jpeg")
    filter.add_pattern("*.jpg")
    filter.add_pattern("*.jpeg")
    filter.add_pattern("*.png")
    filter.add_pattern("*.tif")
    filter.add_pattern("*.bmp")

    dialog.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name(" alles ")
    filter.add_pattern("*")
    dialog.add_filter(filter)

# preview widget
    dialog.set_use_preview_label(False)
    preview = gtk.VBox(False)
    preview.set_size_request(162,162)
    label = gtk.Label()
    label.show()
    preview.pack_start(label, False, False, 10)
    image = gtk.Image()
    image.show()
    preview.pack_start(image, False, False, 10)
    dialog.set_preview_widget(preview)
    dialog.set_preview_widget_active(False)

    dialog.connect("update-preview", update_preview_cb, (label, image))

# starting folder
    if general["pic_folder"] == "":
        if sys.platform == "win32":
          homevar = os.getenv("HOMEDRIVE")
          homevar += "\\" + str(os.getenv("HOMEPATH"))
        else:
          homevar = os.getenv("HOME")
        if homevar != None:
            dialog.set_current_folder(homevar)
    else:
        dialog.set_current_folder(general["pic_folder"])

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
def show_overwrite_dialog(file): #{{{
    global general
    mesbox = gtk.Dialog("Achtung:", general["window"], gtk.DIALOG_MODAL, ()) 
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)    
    label = gtk.Label()
    label.set_markup("Ziel Bild/Datei <b>existiert bereits:</b>\n\n" + trimlongline(file,68))
    mesbox.vbox.pack_start(label, True, True, 10)
    label.show()
    ok_button = gtk.Button("Abbrechen")
    mesbox.action_area.pack_start(ok_button, True, True, 0)
    ok_button.connect("clicked", overwrite_destroy, (mesbox,"cancel"))
    ok_button.show()
    cancel_button = gtk.Button("ueberspringen")
    mesbox.action_area.pack_start(cancel_button, True, True, 0)
    cancel_button.connect("clicked", overwrite_destroy, (mesbox,"skip"))
    cancel_button.show()
    overwrite_button = gtk.Button("ueberschreiben")
    mesbox.action_area.pack_start(overwrite_button, True, True, 0)
    overwrite_button.connect("clicked", overwrite_destroy, (mesbox,"overwrite"))
    overwrite_button.show()
    overwrite_button = gtk.Button("Alle Ueberschreiben")
    mesbox.action_area.pack_start(overwrite_button, True, True, 0)
    overwrite_button.connect("clicked", overwrite_destroy, (mesbox,"all_overwrite"))
    overwrite_button.show()
    mesbox.show()
    mesbox.run()
#}}}
def start_resize(widget, event, data=None): #{{{
    global general
    global imgprocess
    prefix = imgprocess["entry1"].get_text().strip()
    suffix = imgprocess["entry2"].get_text().strip()
    folder = imgprocess["entry3"].get_text().strip()

    if imgprocess["width"] == "0": # then, the spinner is selected finally
        imgprocess["width"] = str(imgprocess["spinWidth"].get_value_as_int())
    if imgprocess["height"] == "0":
        imgprocess["height"] = str(imgprocess["spinHeight"].get_value_as_int())
    if imgprocess["quality"] == "0":
        imgprocess["quality"] = str(imgprocess["spinQuality"].get_value_as_int())


# messagebox when there are no files selexted
    if len(imgprocess["files_todo"]) == 0:
        show_mesbox("  Bitte zuerst <b>Bilder auswaehlen</b>  ")
        return

# messagebox when there is no suff, pre or folder
    if prefix == "" and suffix == "" and folder == "":
        text = """  Mindestens <u>ein</u> von den drei muss angegeben werden:  

             -> <b>Prefix</b>
             -> <b>Suffix</b>
             -> <b>Unterordner</b>

  weil sonst die Original-Bilder ueberschrieben werden wuerden.  """
        show_mesbox(text)
        return

# to get the path
    splitfile = os.path.split(imgprocess["files_todo"][0])

# create folder when needed
    if folder != "" and not os.path.exists(splitfile[0] + "/" +folder):
        print "## Erstelle neuen Ordner: " + folder + "  (" + \
                trimlongline(splitfile[0],38) + "/" + folder + ")"
        print
        os.mkdir(splitfile[0] + "/" + folder)
    else:
        print "# Sub-Ordner existiert bereits"

    if str(imgprocess["width"]) == "99999":
       width_here = "unlimited"
    else:
       width_here = imgprocess["width"]

    if str(imgprocess["height"]) == "99999":
       height_here = "unlimited"
    else:
       height_here = imgprocess["height"]

    print """\
## Erstelle die Bilder: max. Breite: %-s
                        max. Hoehe:  %-s 
                        Qualitaet:   %-s 
                        Ordner:      %-s 
                        Prefix:      %-s 
                        Suffix:      %-s""" %  (width_here, height_here, imgprocess["quality"], folder, prefix, suffix)

    print
    total = len(imgprocess["files_todo"])
    counter=0
    fixed = ""
    fixed2 = ""
    for dofile in imgprocess["files_todo"]:
        counter += 1

        splitfile = os.path.split(dofile)
        resultpath = splitfile[0] + "/"
        if folder != "":
            resultpath += folder + "/" 

        fname,ext=os.path.splitext(splitfile[1]); 
        filetot = resultpath + prefix + fname + suffix + ext

# for py2exe only (looking for the convert.exe in the same dir...)
        if sys.platform == "win32":
            command = general["cwd"] + "convert.exe " + '"' + dofile + '"' + " -resize " + str(imgprocess["width"]) + "x" + str(imgprocess["height"])\
                + " -quality " + str(imgprocess["quality"]) + ' "' + filetot + '"'
        else:
            command = "convert " + '"' + dofile + '"' + " -resize " + str(imgprocess["width"]) + "x" + str(imgprocess["height"])\
                + " -quality " + str(imgprocess["quality"]) + ' "' + filetot + '"'

# wait and update

        while gtk.events_pending():
            gtk.main_iteration(False)

# fixed=(some padding) set already?
        if fixed == "":
            fixed = str(len(splitfile[1]) + 2)
            fixed2 =  len(splitfile[1])

        command_print = "convert: " + "%-" + fixed + "s --> " + \
                trimlongline(filetot,58 - fixed2 )

        general["todolabel"].set_markup("\n\n<b>Progress (" + str(counter) + "/" + \
                str(total) + ")</b>: " + trimlongline(splitfile[1],20) + " -> " + \
                trimlongline(folder,30) + "/" + prefix +\
                fname + suffix + ext + "\n\n" )
        
# check if file exists and may show 'overwrite dialog'
        if os.path.exists(filetot):
            if general["what_todo"] != "all_overwrite":
                show_overwrite_dialog(filetot)
        if general["what_todo"] == "skip":
            general["what_todo"] = ""
            print "# Uebergangen: " + trimlongline(filetot,58)
            continue
        elif general["what_todo"] == "cancel":
            general["what_todo"] = ""
            imgprocess["files_todo"]=[]
            folder=""
            general["todolabel"].set_markup("\n\n  <b>-- keine Bilder ausgewaehlt --</b> \n\n")
            print
            print "# Die Generierung wurde komplett abgebrochen"
            print

            return
        elif general["what_todo"] == "overwrite":
            general["what_todo"] = ""

        print command_print % (splitfile[1])

# the actual work
        exitstatus = os.system(command)
        if exitstatus != 0:
            text = "  Imagemagick beendete mit einem Fehlercode beim  \n\
  Bearbeiten vom Bild: \n  " + dofile + "  \n\n \
  Die weitere Bearbeitung wird ABGEBROCHEN  \n\n \
  (mac@calmar.ws kontaktieren allenfalls)  "
            show_mesbox(text)

    print
    print "# Die Erstellung der Bilder wurde fertiggestellt"
    print "\n"

    general["todolabel"].set_markup("\n\n<b>Progress (" + str(total) + "/" +  str(total) +\
            "): <span color=\"#000060\"> fertig!</span></b>\n\n")
    while gtk.events_pending():
        gtk.main_iteration(False)
    time.sleep(1.4)

    general["what_todo"] = ""
    imgprocess["files_todo"]=[]
    folder=""
    general["todolabel"].set_markup("\n\n  <b>-- keine Bilder ausgewaehlt --</b> \n\n")
#}}}
def main(): #{{{

    global imgprocess

    print "==============================="
    print "Calmar's Picture Resize Utility"
    print "==============================="
    print

    general["window"].set_title("Calmar's Picture Resizer - http://www.calmar.ws")
    general["window"].set_default_size(500,300)
    general["window"].connect("delete_event", delete_event)
    general["window"].set_border_width(15)

    mainbox = gtk.VBox(False, 0)
    general["window"].add(mainbox)

#########################################################################
# buttons  in hbox

    boxh1 = gtk.HBox(False, 0)
    mainbox.pack_start(boxh1, False, False, 0)

    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/calmar.png")
    image.show()
    boxh1.pack_start(image, False, False , 0)

    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/exit.png")
    image.show()
    but_quit = gtk.Button()
    hbox=gtk.HBox()
    hbox.pack_end(image, False, False, 0)
    but_quit.add(hbox)
    label = gtk.Label(" Exit ")
    label.show()
    hbox.pack_end(label, False, False, 0)

    hbox.show()
    but_quit.connect("clicked", delete_event, None)
    boxh1.pack_end(but_quit, False, False, 0)

#########################################################################
# separator

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)
    separator.show()

#########################################################################
#  vbox for radios below

    boxh2 = gtk.HBox(False, 0)
    mainbox.pack_start(boxh2, False, False, 0)

#### width

    vbox = gtk.VBox(False, 0)
    boxh2.pack_start(vbox, False, False, 20)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>max. Breite</b></span>')
    vbox.pack_start(label, False, False, 0)
    label.show()

    text = [ "kein Limit", "1600 x ...", "1280 x ...", "1024 x ...", "800 x ...", "640 x ...",\
            "480 x ...", "120 x ...", "spezifisch:" ]
    values = [ "99999", "1600", "1280", "1024", "800", "640", "480", "120" ,"0"]
    default = "99999"
    general["radio_width"] = create_radios(vbox, values, text, "width", default)
    imgprocess["width"] = 99999

    imgprocess["spinWidth"].show()
    imgprocess["spinWidth"].set_wrap(False)
    vbox.pack_start(imgprocess["spinWidth"], False, False, 0)


## height

    vbox = gtk.VBox(False, 0)
    boxh2.pack_start(vbox, False, False, 20)
    
    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>max. Hoehe</b></span>')
    vbox.pack_start(label, False, False, 0)
    label.show()

    text = [ "kein Limit", "... x 1200", "...x 1024",  "... x 768", "... x 600", "... x 480",\
             "... x 320", "... x 80", "spezifisch:" ]
    values = [ "99999", "1200", "1024", "768", "600", "480", "320", "80", "0"]
    default = "768"
    general["radio_height"] = create_radios(vbox, values, text, "height", default)
    imgprocess["height"] = 768

    imgprocess["spinHeight"].show()
    imgprocess["spinHeight"].set_wrap(False)
    vbox.pack_start(imgprocess["spinHeight"], False, False, 0)

## quality

    vbox = gtk.VBox(False, 0)
    boxh2.pack_start(vbox, False, False, 20)

    label = gtk.Label()
    label.set_markup('<span foreground="#000060"><b>Qualitaet</b></span>')
    vbox.pack_start(label, False, False, 0)
    label.show()

    text = [ "100%", "97%", "94%", "90%", "85%", "80%", "70%", "50%", "spezifisch"]
    values = [ "100", "97", "94", "90", "85", "80", "70", "50", "0"]
    default = "94"
    general["radio_quality"] = create_radios(vbox, values, text, "quality", default)
    imgprocess["quality"] = 94

    imgprocess["spinQuality"].show()
    imgprocess["spinQuality"].set_wrap(False)
    vbox.pack_start(imgprocess["spinQuality"], False, False, 0)

#### prefix/suffix/folder

    vbox = gtk.VBox(False, 0)
    boxh2.pack_start(vbox, False, False, 20)

    label = gtk.Label()
    label.set_markup("\n<b>PREFIX</b>orig-name.jpg")
    vbox.pack_start(label, False, False, 0)
    label.show()
    imgprocess["entry1"].set_alignment(0)
#    entry1.set_text("_")
    vbox.pack_start(imgprocess["entry1"], False, False, 0)
    imgprocess["entry1"].show()

    label = gtk.Label()
    label.set_markup("\norig-name<b>SUFFIX</b>.jpg")

    vbox.pack_start(label, False, False, 0)
    label.show()
    imgprocess["entry2"].set_alignment(0)
    vbox.pack_start(imgprocess["entry2"], False, False, 0)
    imgprocess["entry2"].show()

    label = gtk.Label()
    label.set_markup("\n<b>Unterordner</b>, fuer\ndie <u>neuen</u> Bilder")
    vbox.pack_start(label, False, False, 0)
    label.show()
    imgprocess["entry3"].set_alignment(0)
    vbox.pack_start(imgprocess["entry3"], False, False, 0)
    imgprocess["entry3"].show()

#########################################################################
# separator

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)
    separator.show()


#########################################################################
# label 

    boxh3 = gtk.HBox(False, 0)
    mainbox.pack_start(boxh3, False, False, 0)

    general["todolabel"].set_markup("\n\n  <b>-- keine Bilder ausgewaehlt --</b> \n\n")
    boxh3.pack_start(general["todolabel"], False, False , 0)

#########################################################################
# separator

    separator = gtk.HSeparator()
    mainbox.pack_start(separator, False, False, 5)
    separator.show()

#########################################################################
# buttons  in letzter box


    boxhend = gtk.HBox(False, 0)
    mainbox.pack_start(boxhend, False, False, 0)

    hbox=gtk.HBox()
    hbox.show()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/open.png")
    image.show()
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label("Bilder auswaehlen  ")
    label.show()
    hbox.pack_end(label, False, False, 0)
    but_files = gtk.Button()
    but_files.add(hbox)
    but_files.connect("clicked", open_filechooser, None)
    boxhend.pack_start(but_files, False, False, 0)

    but_files.grab_focus()

    hbox=gtk.HBox()
    hbox.show()
    image = gtk.Image()
    image.set_from_file(general["cwd"] + "bilder/go.png")
    image.show()
    hbox.pack_end(image, False, False, 0)
    label = gtk.Label("Starten  ")
    label.show()
    hbox.pack_end(label, False, False, 0)
    but_start = gtk.Button()
    but_start.add(hbox)
    but_start.connect("clicked", start_resize, None)
    boxhend.pack_end(but_start, False, False, 0)

#########################################################################
# show

    font_desc = pango.FontDescription("Courier")
    if font_desc:
        general["todolabel"].modify_font(font_desc)


    general["window"].show_all()

    gtk.main()
    return 0      
#}}}
# for pyexe only: comment out: #pygtk.require('2.0' #{{{
import pygtk, glob, os, sys, pango, time
#pygtk.require('2.0')
import gtk
# PIL needs some help, when py2exe-d
import Image
import PngImagePlugin
import JpegImagePlugin

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,4,0):
   print "PyGtk 2.4.0 or later required for this example"
   raise SystemExit

# global: general - used on many function
radio_bogus = gtk.RadioButton() #radio_ must be radioB, gtk calls it or so
general = { "todolabel" : gtk.Label(), 
            "what_todo" : "",
            "pic_folder": "",
            "radio_width" : radio_bogus,
            "radio_height" : radio_bogus,
            "radio_quality" : radio_bogus,
            "window" : gtk.Window(gtk.WINDOW_TOPLEVEL)}

if sys.path[0][-12:] == "\library.zip":
    general["cwd"] = sys.path[0][0:-12] + "/"  #for py2exe only
else:
    general["cwd"] = sys.path[0] + "/"

# global: imgprocess - data (source) for image processing
imgprocess = { "entry1" : gtk.Entry(15),
               "entry2" : gtk.Entry(15),
               "entry3" : gtk.Entry(25),
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
