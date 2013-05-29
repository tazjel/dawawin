# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, exists
from gi.repository import Gtk, Pango
from daw_player import Mawso3aPlayer
from daw_viewer import ShowPoem
import daw_customs

# class القصائد المقروءة-------------------------------------------------------------------

class RecitePoem(Gtk.HPaned):
    
    def show_poem(self, *a):
        self.player.stop()
        model, i = self.tree_recited.get_selection().get_selected()
        if i:
            id_poem = model.get_value(i,0)
            self.iv.loading(id_poem, self.parent.theme.fontmp)
            self.player.set_sensitive(True)
            file_media = join(daw_customs.AUDIO_DIR,'00'+str(id_poem)+'.ogg')
            self.player.set_media(file_media)
            if not exists(file_media): daw_customs.erro(self.parent, u'لا يوجد ملف صوتي لهذه القصيدة')
            
    def show_info(self, *a):
        model, i = self.sel_recited.get_selected()
        if i:
            self.view_info_bfr.set_text(u'إلقاء : {}'.format(model.get_value(i,2).decode('utf8'),))
    
    def store(self, *a):
        self.store_recited.clear()
        ls = self.parent.db.recited_poems()
        map(self.store_recited.append, ls)
    
    def search_on_page(self, text):
        self.iv.search_on_poem(text) 
    
    def near_page(self, v):
        self.iv.near_poem(v) 
    
    def move_in_page(self, v):
        model, i = self.tree_recited.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_recited.get_selection().select_iter(i1)
            self.tree_recited.scroll_to_cell((p+v,))
        elif len(self.tree_recited.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_recited.get_selection().select_iter(i2)
            self.tree_recited.scroll_to_cell((0,))
        self.show_poem()
    
    def __init__(self, parent):
        self.parent = parent
        Gtk.HPaned.__init__(self)
        self.set_position(150)
        vbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.vbox1= Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.tree_recited = daw_customs.TreeClass()
        self.sel_recited = self.tree_recited.get_selection()
        cell = Gtk.CellRendererText()
        cell.set_property("wrap-mode", Pango.WrapMode.WORD_CHAR)
        self.tree_recited.set_size_request(150, -1)
        kal = Gtk.TreeViewColumn('القصائد المقروءة', cell, text=1)
        self.tree_recited.append_column(kal)
        self.store_recited = Gtk.ListStore(int, str, str)
        self.store()
        self.tree_recited.set_model(self.store_recited)
        self.tree_recited.connect("cursor-changed", self.show_info)
        self.tree_recited.connect("row-activated", self.show_poem)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_recited)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll, True, True, 0)
        
        self.view_info = daw_customs.ViewClass()
        self.view_info.set_right_margin(5)
        self.view_info.set_left_margin(5)
        self.view_info_bfr = self.view_info.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_info)
        scroll.set_size_request(-1, 50)
        vbox.pack_start(scroll, False, False, 0)
        
        self.player = Mawso3aPlayer()
        self.iv = ShowPoem(self.parent)
        self.vbox1.pack_start(self.iv, True, True, 0)
        self.iv.pack_end(self.player, False, False, 0)
        self.vbox1.show_all()
        self.player.set_sensitive(False)
        
        self.pack1(vbox, False, False)
        self.pack2(self.vbox1, True, False)
        self.show_all()
