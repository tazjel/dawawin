# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk, Pango
import daw_customs, daw_araby
from daw_contacts import HelpDB

# class صفحة المساعدة والتعريف-------------------------------------------------------------------    
    
class Halper(Gtk.Box):
    
    def show_page_help(self, *a):
        model, i = self.sel_help.get_selected()
        if i:
            v = model.get_value(i,1)
            txt = self.myhelp.show_page_help(v)
            self.prescript_bfr.set_text(txt[0][0])
    
    def search_on_page(self, text):
        self.show_page_help()
        search_tokens = []
        nasse = self.prescript_bfr.get_text(self.prescript_bfr.get_start_iter(), 
                                            self.prescript_bfr.get_end_iter(),True).split()
        if text != u'': 
            txt = daw_araby.fuzzy(text)
            for term in nasse: 
                if txt in daw_araby.fuzzy(term.decode('utf8')):
                    search_tokens.append(term)
        daw_customs.with_tag(self.prescript_bfr, self.search_tag, search_tokens)
    
    def near_page(self, v):
        self.size_font += v
        self.prescript.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
    def move_in_page(self, v):
        model, i = self.tree_help.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_help.get_selection().select_iter(i1)
            self.tree_help.scroll_to_cell((p+v,))
        elif len(self.tree_help.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_help.get_selection().select_iter(i2)
            self.tree_help.scroll_to_cell((0,))
        self.show_page_help()
    
    def __init__(self, parent):
        self.parent = parent
        self.size_font = int(self.parent.theme.fontch[-2:])
        Gtk.Box.__init__(self,spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.store_help = Gtk.ListStore(str, int)
        self.myhelp = HelpDB()
        for a in self.myhelp.titles_help():
            self.store_help.append([a[1], a[0]])
        self.tree_help = daw_customs.TreeClass()
        self.sel_help = self.tree_help.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('الفهرس', cell, text=0)
        self.tree_help.append_column(kal)
        self.tree_help.set_model(self.store_help)
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(200, -1)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.tree_help)
        self.tree_help.connect("cursor-changed", self.show_page_help)
        self.pack_start(scroll, False, False, 0)
        
        self.prescript = daw_customs.ViewClass()
        self.prescript_bfr = self.prescript.get_buffer()
        self.search_tag = self.prescript_bfr.create_tag("search")
        self.search_tag.set_property('background', self.parent.theme.colorss) 
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(-1, 100)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.prescript)
        self.pack_start(scroll, True, True, 0)
        self.show_all()
