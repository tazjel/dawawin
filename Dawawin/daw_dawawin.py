# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk, Pango
from daw_contacts import MyDB
from daw_viewer import ShowPoem
from daw_tablabel import TabLabel
import daw_config, daw_tools, daw_araby, daw_customs


     
# class صفحة الدواوين--------------------------------------------------------
        
class DawawinPage(Gtk.HPaned):
    
    def change_font(self, *a):
        self.tarjama_tag.set_property('foreground', self.parent.theme.coloran) 
        self.tarjama_tag.set_property('font', self.parent.theme.fontan)
    
    def search_on_page(self, text):
        if len(self.poems_store) == 0: return
        self.notebook.set_current_page(1)
        self.theword0 = [text]
        self.modelfilter0.refilter()
    
    def near_page(self, v):
        self.notebook.set_current_page(0)
        self.size_font += v
        self.tarjama.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
    def move_in_page(self, v):
        model, i = self.tree_poet.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_poet.get_selection().select_iter(i1)
            self.tree_poet.scroll_to_cell((p+v,))
        elif len(self.tree_poet.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_poet.get_selection().select_iter(i2)
            self.tree_poet.scroll_to_cell((0,))
        self.ok_poet()
    
    def on_button_press(self, widget, event):
        if event.button == 3:
            self.popup.show_all()
            self.popup.popup(None, None, None, None, 3,
                             Gtk.get_current_event_time())
        elif event.button == 1 and event.get_click_count()[1] == 2:
            self.show_poem_cb()
                
    def modify_poem_cb(self, *a):
        model0, i0 = self.tree_poet.get_selection().get_selected()
        model, i = self.tree_poems.get_selection().get_selected()
        if i and i0:
            nm_poem = model.get_value(i, 2)
            nm_poet = model0.get_value(i0, 1)
            if nm_poet == u"أحدهم": nm_poet = u'ما لا يعرف قائله'
            self.parent.set_title("دواوين العرب - التعديل")
            self.parent.main_notebook.set_current_page(11)
            self.parent.organizepage.search_poets.set_text(nm_poet)
            self.parent.organizepage.sel_poet.select_path((0,))
            self.parent.organizepage.ok_poet()
            self.parent.entry_search.set_text(nm_poem)
            self.parent.reg_page.set_active(True)
    
    def show_poem_cb(self, *a):
        model, i = self.tree_poems.get_selection().get_selected()
        if i:
            id_poem = model.get_value(i,0)
            text = model.get_value(i,2)
            self.parent.set_title("دواوين العرب - القصائد")
            self.parent.main_notebook.set_current_page(2)
            self.parent.poems_page.set_sensitive(True)
            self.parent.poems_page.set_active(True)
            n = self.parent.viewerpoem.get_n_pages()
            for s in range(n):
                ch = self.parent.viewerpoem.get_nth_page(s)
                if self.parent.viewerpoem.get_tab_label(ch).nm == text:
                    self.parent.viewerpoem.set_current_page(s)
                    return
            sr = ShowPoem(self.parent)
            sr.loading(id_poem, self.parent.theme.fontmp)
            self.parent.viewerpoem.append_page(sr,TabLabel(sr, text))
            self.parent.viewerpoem.show_all()
            self.parent.viewerpoem.set_current_page(-1)
    
    def visible_cb0(self, model, itr, data):
        if len(self.theword0) == 0: return
        if daw_araby.fuzzy(self.theword0[0]) in daw_araby.fuzzy(model.get_value(itr, 2).decode('utf8')):
            return True
        else: return False
        
    def ok_poet(self, *a):
        model, i = self.sel_poet.get_selected()
        if i:
            id_poet = model.get_value(i,0)
            list_poems, tarjama = self.db.poems_of_poet(id_poet)
            self.tarjama_bfr.set_text(tarjama)
            ls = [tarjama.splitlines(1)[0],]
            daw_customs.with_tag(self.tarjama_bfr, self.tarjama_tag, ls)
            self.poems_store.clear()
            n = self.notebook.get_current_page()
            if n > 1:
                self.notebook.set_current_page(daw_config.getn('open'))
            if len(list_poems) != 0:
                self.names_list0 = []
                self.modelfilter0 = self.poems_store.filter_new()
                for a in list_poems:
                    i = a[0]
                    rakm = list_poems.index(a, )+1
                    name = a[1]
                    abiat = a[2]
                    if a[3] != 0: baher = daw_tools.get_name(daw_tools.elbehor, a[3])
                    else: baher = u'____'
                    if a[4] != 0: rawi = daw_tools.get_name(daw_tools.elrawi, a[4])
                    else: rawi = u'____'
                    if a[6] != 0: gharadh = daw_tools.get_name(daw_tools.elgharadh, a[6])
                    else: gharadh = u'____'
                    if a[7] != 0: naw3 = daw_tools.get_name(daw_tools.elnaw3, a[7])
                    else: naw3 = u'____'
                    self.poems_store.append([i, rakm, name, naw3, baher, gharadh, rawi, abiat])
                    self.names_list0.append(name)
                self.theword0 = self.names_list0[:]
                self.modelfilter0.set_visible_func(self.visible_cb0, self.theword0) 
                self.tree_poems.set_model(self.modelfilter0)
            lab = '  .: {} :.    عدد القصائد : {} ، عدد الأبيات : {}'.format((self.db.name_poet(id_poet)[1]).encode('utf8'),
                                                          self.db.n_poems_poet(id_poet).decode('utf8'),
                                                          self.db.n_verses_poet(id_poet).decode('utf8'))
            self.lab_count.set_label(lab)

    
    def visible_cb(self, model, itr, data):
        if len(self.theword) == 0: return
        if daw_araby.fuzzy(self.theword[0][0]) in daw_araby.fuzzy(model.get_value(itr, 1).decode('utf8')) and\
        (self.theword[0][1] == model.get_value(itr, 2) or self.theword[0][1] == 0) and\
        (self.theword[0][2] == model.get_value(itr, 3) or self.theword[0][2] == 0) and\
        (self.theword[0][3] == model.get_value(itr, 4) or self.theword[0][3] == 0):
            return True
        else: return False
        
    def search_cb(self, *a):
        self.theword = [[self.search_poets.get_text().decode('utf8'), 
        daw_customs.value_active(self.sexs),daw_customs.value_active(self.lands),  daw_customs.value_active(self.ages)]]
        self.modelfilter.refilter()
        
    def select_age(self, *a):
        if daw_customs.value_active(self.ages) == 8: self.lands.set_sensitive(True)
        else:
            self.lands.set_active(0)
            self.lands.set_sensitive(False)
            
    def refresh_poets(self, *a):
        self.store_poet.clear()
        self.modelfilter = self.store_poet.filter_new()
        ls = self.db.all_poets()
        ls.append([0, u'ما لا يعرف قائله', 0, 22, 9])
        self.names_list = []
        for a in ls:
            s_list = []
            self.store_poet.append(a)
            s_list.append(a[1])
            s_list.append(a[2])
            s_list.append(a[3])
            s_list.append(a[4])
            self.names_list.append(s_list)
        self.theword = self.names_list[:]
        self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
        self.tree_poet.set_model(self.modelfilter)
    
    def __init__(self, parent):
        self.parent = parent
        self.db = MyDB()
        self.size_font = int(self.parent.theme.fontch[-2:])
        Gtk.HPaned.__init__(self)
        
        self.vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        
        hb, self.ages = daw_customs.combo(daw_tools.age_poet, u'العصر', 1)
        self.vbox.pack_start(hb, False, False, 0)
        self.ages.connect('changed', self.search_cb)
        self.ages.connect('changed', self.select_age)
        
        hb, self.lands = daw_customs.combo(daw_tools.elbalad, u'البلد', 1)
        self.lands.set_sensitive(False)
        self.vbox.pack_start(hb, False, False, 0)
        self.lands.connect('changed', self.search_cb)
        
        hb, self.sexs = daw_customs.combo(daw_tools.sex_poet, u'الجنس', 1)
        self.vbox.pack_start(hb, False, False, 0)
        self.sexs.connect('changed', self.search_cb)
        
        try: self.search_poets = Gtk.SearchEntry()
        except: self.search_poets = Gtk.Entry()
        self.search_poets.set_placeholder_text('بحث عن شاعر')
        self.search_poets.connect('changed', self.search_cb)
        hbox = Gtk.HBox(False, 2)
#        self.btn_refresh = Gtk.ToolButton(Gtk.STOCK_REFRESH)
#        self.btn_refresh.set_tooltip_text('تحديث قائمة الدواوين')
#        self.btn_refresh.connect('clicked', self.refresh_poets)
#        hbox.pack_start(self.btn_refresh, False, False, 0)
        hbox.pack_start(self.search_poets, True, True, 0)
        self.vbox.pack_start(hbox, False, False, 0)
        
        self.tree_poet = daw_customs.TreeClass()
        cell = Gtk.CellRendererText()
        cell.set_property("wrap-mode", Pango.WrapMode.WORD_CHAR)
        cell.set_property("wrap-width", 200)
        kal = Gtk.TreeViewColumn('دواوين الشعراء', cell, text=1)
        self.tree_poet.append_column(kal)
        self.store_poet = Gtk.ListStore(int, str, int, int, int)
        self.refresh_poets()
#        self.store_poet.clear()
#        ls = self.db.all_poets()
#        ls.append([0, u'ما لا يعرف قائله', 0, 22, 9])
#        self.names_list = []
#        for a in ls:
#            s_list = []
#            self.store_poet.append(a)
#            s_list.append(a[1])
#            s_list.append(a[2])
#            s_list.append(a[3])
#            s_list.append(a[4])
#            self.names_list.append(s_list)
#        self.theword = self.names_list[:]
#        self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
#        self.tree_poet.set_model(self.modelfilter)
        self.sel_poet = self.tree_poet.get_selection()
        self.tree_poet.connect("cursor-changed", self.ok_poet)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poet)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.vbox.pack_start(scroll, True, True, 0)
        #self.tree_poet.scroll_to_cell(0, kal, False, 1.0, 1.0)
        
        vbox2 = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.tarjama = daw_customs.ViewClass()
        self.tarjama_bfr = self.tarjama.get_buffer()
        self.tarjama_tag = self.tarjama_bfr.create_tag("title")
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tarjama)
        self.notebook.append_page(scroll, Gtk.Label("الترجمة"))
        self.notebook.set_current_page(-1)
        
        self.poems_store = Gtk.ListStore(int,int,str,str,str,str,str,int)
        
        self.tree_poems = daw_customs.TreePoem()
        
        vbox = Gtk.VBox(False, 2)
        self.lab_count = Gtk.Label('  .:   :.    عدد القصائد :   ، عدد الأبيات :  ')
        self.lab_count.set_alignment(0, 0.5)
        vbox.pack_start(self.lab_count, False, False, 0)
        self.tree_poems.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        self.tree_poems.connect("button-press-event", self.on_button_press)
        raq = Gtk.TreeViewColumn('الرقم', Gtk.CellRendererText(), text=1)
        raq.set_max_width(30)
        self.tree_poems.append_column(raq)
        poems = Gtk.TreeViewColumn('القصيدة', Gtk.CellRendererText(), text=2)
        self.tree_poems.append_column(poems)
        poems.set_max_width(300)
        elnaw3 = Gtk.TreeViewColumn('النوع', Gtk.CellRendererText(), text=3)
        self.tree_poems.append_column(elnaw3)
        elnaw3.set_max_width(100)
        elbaher = Gtk.TreeViewColumn('البحر', Gtk.CellRendererText(), text=4)
        self.tree_poems.append_column(elbaher)
        elbaher.set_max_width(120)
        elgharadh = Gtk.TreeViewColumn('الغرض', Gtk.CellRendererText(), text=5)
        self.tree_poems.append_column(elgharadh)
        elgharadh.set_max_width(80)
        elrawi = Gtk.TreeViewColumn('الروي', Gtk.CellRendererText(), text=6)
        self.tree_poems.append_column(elrawi)
        elrawi.set_max_width(50)
        verses = Gtk.TreeViewColumn('عدد الأبيات', Gtk.CellRendererText(), text=7)
        self.tree_poems.append_column(verses)
        verses.set_max_width(50)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poems)
        vbox.pack_start(scroll, True, True, 0)
        self.notebook.append_page(vbox, Gtk.Label("القصائد"))
        self.notebook.set_current_page(-1)
        
        def switch(widget, *a):
            n = self.notebook.get_current_page()
            daw_config.setv('open', n)
        self.notebook.connect('set-focus-child', switch)
        
        vbox2.pack_start(self.notebook, True, True, 0)
        self.pack1(self.vbox, False, False)
        self.pack2(vbox2, True, False)
        self.show_all()
        self.change_font()
        self.notebook.set_current_page(daw_config.getn('open'))
        
        #--- Popup menu
        self.popup = Gtk.Menu()
        show_poem = Gtk.ImageMenuItem('اعرض القصيدة')
        show_poem.connect('activate', self.show_poem_cb)
        self.popup.append(show_poem)
        
        modify_poem = Gtk.ImageMenuItem('عدّل القصيدة')
        modify_poem.connect('activate', self.modify_poem_cb)
        self.popup.append(modify_poem)
        self.popup.show_all()