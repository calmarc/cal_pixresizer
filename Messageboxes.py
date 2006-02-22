import gtk
import gettext
from Varhelp import  *

gettext.textdomain('cal_pixresizer')
_ = gettext.gettext

def show_2_dialog(parent_widget, text, button_quit, button_ok):

    mesbox = gtk.Dialog(_("attention:"),
                           parent_widget, 
                           gtk.DIALOG_MODAL,
                           (button_ok, gtk.RESPONSE_OK,
                           button_quit, gtk.RESPONSE_CANCEL))

    mesbox.set_default_response(gtk.RESPONSE_OK)

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

    mesbox.show()
    response = mesbox.run()
    if response == gtk.RESPONSE_OK:
        mesbox.hide()
        mesbox.destroy()
        return True
    else:
        mesbox.hide()
        mesbox.destroy()
        return False

def show_overwrite_dialog(parent, filename, mswin_val, encod):
    mesbox = gtk.Dialog(_("attention:"), 
                           parent , 
                           gtk.DIALOG_MODAL,
                           ( _("skip"), gtk.RESPONSE_NONE,
                             _("quit processing"), gtk.RESPONSE_CLOSE,
                             _("overwrite"), gtk.RESPONSE_YES,
                             _("overwrite ALL"), gtk.RESPONSE_ACCEPT))


    mesbox.set_default_response(gtk.RESPONSE_NONE)
    mesbox.connect("destroy", quit_self, None)
    mesbox.connect("delete_event", quit_self, None)
    mesbox.set_size_request(700,-1)
    vbox = gtk.VBox()
    vbox.show()
    label = gtk.Label()
    label.set_line_wrap(True)
# encoding hack. grr
    if not mswin_val:
        filename = utf8_enc(filename, encod)

    label.set_markup("%s\n\n%s" % (_("Target picture <b>already exists</b>:"), trimlongline(filename ,68)))
    label.show()
    vbox.pack_start(label, True, True, 10)
    align = gtk.Alignment(0.5, 0.0, 0.5, 0.0)
    align.set_padding(5, 5, 20, 20)
    align.show()
    align.add(vbox)
    mesbox.vbox.pack_start(align, True, True, 15)

    mesbox.show()
    response = mesbox.run()
    if response == gtk.RESPONSE_NONE:
        var = "skip"
    elif response == gtk.RESPONSE_CLOSE:
        var = "quit"
    elif response == gtk.RESPONSE_ACCEPT:
        var = "all_overwrite"
    elif response == gtk.RESPONSE_YES:
        var = "overwrite"

    mesbox.hide()
    mesbox.destroy()
    return var

def show_mesbox(parent, text, encod):
    mesbox = gtk.Dialog(_("Calmar's Picture Resizer"), parent, gtk.DIALOG_MODAL,
            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    mesbox.connect("destroy", quit_self)
    mesbox.connect("delete_event", quit_self)
    mesbox.set_size_request(700,-1)

    vbox = gtk.VBox()
    vbox.show()
    label = gtk.Label()
    label.set_line_wrap(True)
# encoding hack. grr
#    if mswin_val:
#        text = utf8_enc(text, encod)
    text = utf8_enc(text, encod)
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
    mesbox.hide()
    mesbox.destroy()
