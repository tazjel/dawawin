# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
from gi.repository import Gtk
import daw_customs


# class عنوان الصفحة-------------------------------------------------------------------    
    
class TabLabel(Gtk.Box):
    close_img=None
    
    def __init__(self, child, nm):
        self.nm = nm
        self.child=child
        if not self.close_img:
            self.close_img=Gtk.Image()
            self.close_img.set_from_file(join(daw_customs.ICON_DIR, 'tab.png'))
        Gtk.Box.__init__(self,orientation=Gtk.Orientation.HORIZONTAL)
        self.close=Gtk.Button()
        self.close.set_tooltip_text('اغلق هذه الصفحة')
        self.close.add(self.close_img)
        self.close.set_focus_on_click(False)
        self.close.connect('clicked',self.close_tab)
        self.close.set_relief(Gtk.ReliefStyle(2))
        self.lab = Gtk.Label(self.nm)
        self.pack_start(self.lab, True, True,0)
        self.pack_start(self.close, False, False,0)
        self.show_all()

    def close_tab(self, widget):
        n = self.get_parent()
        i = n.page_num(self.child)
        if i < 0: return
        w = n.get_nth_page(i)
        n.remove_page(i)
        w.destroy()