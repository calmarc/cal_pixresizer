import os, gtk, pygtk
import gettext, locale
gettext.textdomain('cal_pixresizer')
_ = gettext.gettext

class mesbox:
    def __init__(self, encoding):
        self.encoding =  encoding
        self.dialog2_q = ""
        self.overwrite_q = ""

    def quit_self(self, widget, *args):
        widget.hide()
        widget.destroy()

    def loc_enc(self, text): 
        obj = unicode(text, 'utf-8')
        return obj.encode( self.encoding)

    def utf8_enc(self, text):
        obj = unicode(text, self.encoding)
        return obj.encode('utf-8')


    def show_2_dialog(self, parent_widget, text, button_quit, button_ok):
        self.dialog2_q == ""
        mesbox = gtk.Dialog(_("attention:"), parent_widget, gtk.DIALOG_MODAL, ())
        mesbox.connect("destroy", self.quit_self, None)
        mesbox.connect("delete_event", self.quit_self, None)
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
        button.connect("clicked", self.dialog_2_destroy, (mesbox,"quit"))
        button.show()
        button = gtk.Button(button_ok)
        mesbox.action_area.pack_start(button, True, True, 0)
        button.connect("clicked", self.dialog_2_destroy, (mesbox,"ok_pressed"))
        button.show()
        button.grab_focus()
        mesbox.show()
        mesbox.run()

    def show_overwrite_dialog(self, parent, filename, mswin):
        mesbox = gtk.Dialog(_("attention:"), parent , gtk.DIALOG_MODAL, ())
        mesbox.connect("destroy", self.quit_self, None)
        mesbox.connect("delete_event", self.quit_self, None)
        mesbox.set_size_request(700,-1)
        vbox = gtk.VBox()
        vbox.show()
        label = gtk.Label()
        label.set_line_wrap(True)
# encoding hack. grr
        if not mswin:
            filename = self.utf8_enc(filename)

        label.set_markup("%s\n\n%s" % (_("Target picture <b>already exists</b>:"), self.trimlongline(filename ,68)))
        label.show()
        vbox.pack_start(label, True, True, 10)
        align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
        align.set_padding(5, 5, 20, 20)
        align.show()
        align.add(vbox)
        mesbox.vbox.pack_start(align, True, True, 15)

        button = gtk.Button(_("quit processing"))
        mesbox.action_area.pack_start(button, True, True, 0)
        button.connect("clicked", self.overwrite_destroy, (mesbox,"cancel"))
        button.show()

        button = gtk.Button(_("skip"))
        mesbox.action_area.pack_start(button, True, True, 0)
        button.connect("clicked", self.overwrite_destroy, (mesbox,"ok_pressed"))
        button.grab_focus()
        button.show()

        button = gtk.Button(_("overwrite"))
        mesbox.action_area.pack_start(button, True, True, 0)
        button.connect("clicked", self.overwrite_destroy, (mesbox,"overwrite"))
        button.show()
        button = gtk.Button(_("ALL overwrite"))
        mesbox.action_area.pack_start(button, True, True, 0)
        button.connect("clicked", self.overwrite_destroy, (mesbox,"all_overwrite"))
        button.show()
        mesbox.show()
        mesbox.run()

    def show_mesbox(self, parent, text):
        mesbox = gtk.Dialog(_("Calmar's Picture Resizer"), parent, gtk.DIALOG_MODAL,
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        mesbox.connect("destroy", self.quit_self)
        mesbox.connect("delete_event", self.quit_self)
        mesbox.set_size_request(700,-1)

        vbox = gtk.VBox()
        vbox.show()
        label = gtk.Label()
        label.set_line_wrap(True)
# encoding hack. grr
#    if mswin:
#        text = utf8_enc(text)
        text = self.utf8_enc(text)
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

    def overwrite_destroy(self, widget, data):
        self.overwrite_q = str(data[1])
        data[0].hide()
        data[0].destroy()

    def dialog_2_destroy(self, widget, data):
        self.dialog2_q = str(data[1])
        data[0].hide()
        data[0].destroy()
