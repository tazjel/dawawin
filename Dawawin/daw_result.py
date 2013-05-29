# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join
import os, cPickle
from gi.repository import Gtk
from daw_search import ShowResult
from daw_tablabel import TabLabel
import daw_config, daw_customs

class SavedResult(Gtk.Dialog):
    
    def ok_m(self,*a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        if i :
            nm = model.get_value(i,0)
            self.set_title("دواوين العرب - نتائج البحث")
            self.parent.main_notebook.set_current_page(10)
            self.parent.search_result_page.set_sensitive(True)
            self.parent.search_result_page.set_active(True)
            sr = ShowResult(self.parent)
            self.parent.resultsearch.append_page(sr,TabLabel(sr, nm))
            self.parent.resultsearch.set_current_page(-1)
            store = cPickle.load(file(join(daw_customs.HOME_DIR, nm+".pkl")))
            sr.results_list = store
            for a in store:
                sr.results_store.append(a)
            self.destroy()
                
    def remove_iter(self, *a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        if i :
            res_self = daw_customs.sure(self, " هل ترغب في حذف النتيجة المحددة ؟")
            if res_self:
                nm = model.get_value(i,0)
                os.remove(join(daw_customs.HOME_DIR, nm+'.pkl'))
                self.store_sav.remove(i)
                
    def remove_iters(self, *a):
        res_self = daw_customs.sure(self, " هل ترغب في حذف جميع النتائج الموجودة ؟")
        if res_self:
            for a in self.list_n:
                os.remove(join(daw_customs.HOME_DIR, a))
            self.store_sav.clear()
    
    def __init__(self, parent):
        self.parent = parent
        self.list_marks = eval(daw_config.getv('marks'))
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("Dawawin")
        area = self.get_content_area()
        area.set_spacing(6)
        self.set_title('نتائج البحوث المحفوظة')
        self.set_default_size(350, 300)
        box = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.store_sav = Gtk.ListStore(str)
        self.list_n = os.listdir(daw_customs.HOME_DIR)
        self.store_sav.clear()
        for v in self.list_n:
            if '.pkl' in v:
                nm = v.replace('.pkl', '')
                self.store_sav.append([nm])
        self.tree_sav = daw_customs.TreeClass()
        self.tree_sav.connect("row-activated", self.ok_m)
        column = Gtk.TreeViewColumn('اسم الموضع',Gtk.CellRendererText(),text = 0)
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