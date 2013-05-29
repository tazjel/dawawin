# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

#a ماذا سأفعل؟
#a تصدير القصائد بصيغة pdf odt
#a خاصية البحث في نفس البيت

from gi.repository import Gtk
from daw_viewer import ShowPoem
import daw_customs

# class القصائد المفضلة-------------------------------------------------------------------

class FavoritePoem(Gtk.HPaned):
    
    def remove_one(self, *a):
        model, i = self.tree_favorite.get_selection().get_selected()
        if i:
            id_poem = model.get_value(i,0)
            check = self.parent.db.out_favorite(id_poem)
            if check == None:
                model.remove(i)
                
    def remove_all(self, *a):
        ls = self.parent.db.favorite_poems()
        for a in ls:
            id_poem = a[0]
            self.parent.db.out_favorite(id_poem)
        self.store_favorite.clear()
    
    def show_poem(self, *a):
        model, i = self.tree_favorite.get_selection().get_selected()
        if i:
            id_poem = model.get_value(i,0)
            self.iv.loading(id_poem, self.parent.theme.fontmp)
    
    def store(self, *a):
        self.store_favorite.clear()
        ls = self.parent.db.favorite_poems()
        map(self.store_favorite.append, ls)
    
    def search_on_page(self, text):
        self.iv.search_on_poem(text)
    
    def near_page(self, v):
        self.iv.near_poem(v) 
    
    def move_in_page(self, v):
        model, i = self.tree_favorite.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_favorite.get_selection().select_iter(i1)
            self.tree_favorite.scroll_to_cell((p+v,))
        elif len(self.tree_favorite.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_favorite.get_selection().select_iter(i2)
            self.tree_favorite.scroll_to_cell((0,))
        self.show_poem()
    
    def __init__(self, parent):
        self.parent = parent
        Gtk.HPaned.__init__(self)
        self.set_position(150)
        vbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.vbox1= Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        
        self.tree_favorite = daw_customs.TreeClass()
        self.tree_favorite.set_size_request(150, -1)
        self.sel_favorite = self.tree_favorite.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('القصائد المفضلة', cell, text=1)
        self.tree_favorite.append_column(kal)
        self.store_favorite = Gtk.ListStore(int, str)
        self.store()
        self.tree_favorite.set_model(self.store_favorite)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_favorite)
        self.tree_favorite.connect("row-activated", self.show_poem)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll, True, True, 0)
        
        remove = daw_customs.ButtonClass("حذف")
        remove.connect('clicked', self.remove_one)
        hbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(remove, True, True, 0)
        remove_all = daw_customs.ButtonClass("مسح")
        remove_all.connect('clicked', self.remove_all)
        hbox.pack_start(remove_all, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        
        self.iv = ShowPoem(self.parent)
        self.vbox1.pack_start(self.iv, True, True, 0)
        self.pack1(vbox, False, False)
        self.pack2(self.vbox1, True, False)
        self.show_all()

