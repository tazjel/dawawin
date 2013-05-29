# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
from os.path import join
import daw_customs


class MyFace(Gtk.HBox):
    
    def search_on_page(self, text):
        return
    
    def near_page(self, v):
        return
    
    def move_in_page(self, v):
        return
    
    def __init__(self, parent):
        Gtk.HBox.__init__(self, False, 0)
        img_face = Gtk.Image()
        img_face.set_from_file(join(daw_customs.ICON_DIR,"logo.png"))
        self.pack_start(img_face, True, True, 0)
        self.show_all()
