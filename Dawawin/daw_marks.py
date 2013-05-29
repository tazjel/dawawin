# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
from daw_viewer import ShowPoem
from daw_tablabel import TabLabel
import daw_config, daw_customs

class SavedMarks(Gtk.Dialog):
    
    def ok_m(self,*a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        self.destroy()
        id_poem = model.get_value(i,0)
        text = model.get_value(i,1)
        sr = ShowPoem(self.parent)
        sr.loading(id_poem, self.parent.theme.fontmp)
        self.parent.viewerpoem.append_page(sr,TabLabel(sr, text))
        self.parent.viewerpoem.set_current_page(-1)
        self.parent.viewerpoem.show_all()
        sr.search_half(text)
        self.parent.set_title("دواوين العرب - القصائد")
        self.parent.main_notebook.set_current_page(2)
        self.parent.poems_page.set_sensitive(True)
        self.parent.poems_page.set_active(True)
    
    def remove_iter(self, *a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        id_poem = model.get_value(i,0)
        for a in self.list_marks:
            if a[0] == id_poem :
                s = self.list_marks.index(a)
                self.list_marks.pop(s)
                model.remove(i)
                marks = repr(self.list_marks)
                daw_config.setv('marks', marks)
    
    def remove_iters(self, *a):
        daw_config.setv('marks', '[]')
        self.list_marks = []
        self.store_sav.clear()
    
    def __init__(self, parent):
        self.parent = parent
        self.list_marks = eval(daw_config.getv('marks'))
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("Dawawin")
        area = self.get_content_area()
        area.set_spacing(6)
        self.set_title('المواضع المحفوظة')
        self.set_default_size(350, 300)
        box = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.store_sav = Gtk.ListStore(int, str)
        map(self.store_sav.append, self.list_marks)
        self.tree_sav = daw_customs.TreeClass()
        self.tree_sav.connect("row-activated", self.ok_m)
        column = Gtk.TreeViewColumn('اسم الموضع',Gtk.CellRendererText(),text = 1)
        self.tree_sav.append_column(column)
        self.tree_sav.set_model(self.store_sav)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_sav)
        remove = daw_customs.ButtonClass("حذف")
        remove.connect('clicked', self.remove_iter)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(remove, False, False, 0)
        remove_all = daw_customs.ButtonClass("مسح")
        remove_all.connect('clicked', self.remove_iters)
        hb.pack_start(remove_all, False, False, 0)
        clo = daw_customs.ButtonClass("إغلاق")
        clo.connect('clicked',lambda *a: self.destroy())
        hb.pack_end(clo, False, False, 0)
        box.pack_start(scroll, True, True, 0)
        box.pack_start(hb, False, False, 0)
        area.pack_start(box, True, True, 0)
        self.show_all()