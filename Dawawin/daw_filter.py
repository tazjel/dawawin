# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
from daw_viewer import ShowPoem
from daw_tablabel import TabLabel
import daw_tools, daw_customs, daw_araby


# class صفحة المصفاة-------------------------------------------------------------------    
    
class FilterPoem(Gtk.HBox):
    
    def visible_cb(self, model, itr, data):
        if len(self.theword) == 0: return
        if daw_araby.fuzzy(self.theword[0]) in daw_araby.fuzzy(model.get_value(itr, 1).decode('utf8')):
            return True
        else: return False
        
    def search_on_page(self, text):
        self.theword = [text]
        self.modelfilter.refilter()
    
    def near_page(self, v):
        return
    
    def move_in_page(self, v):
        model, i = self.tree_poems.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_poems.get_selection().select_iter(i1)
            self.tree_poems.scroll_to_cell((p+v,))
        elif len(self.tree_poems.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_poems.get_selection().select_iter(i2)
            self.tree_poems.scroll_to_cell((0,))
    
    def select_page(self, btn):
        n = int(btn.get_name())
        self.load_poems(n)
    
    def a3aridh_elbaher(self, *a):
        #self.refresh(self.select_page, 9)
        model = self.arodh.get_model()
        model.clear()
        baher = daw_customs.value_active(self.baher)
        model.append([0, 'الكل'])
        if baher == 0:
            for a in daw_tools.ela3aridh:
                model.append(a)
            self.arodh.set_active(0)
            return
        a3aridh = daw_tools.ela3aridh_in_behor[baher]
        for a in a3aridh:
            nm = daw_tools.get_name(daw_tools.ela3aridh, a)
            model.append([a, nm])
        self.arodh.set_active(0)
    
    def toggled_cb(self, btn):
        if btn.get_active():
            for a in self.list_btn:
                if a.get_name() != btn.get_name():
                    a.set_active(False)
    
    def next_cb(self, *a):
        self.r += 1
        self.add_btn()
        self.prev_p.set_sensitive(True)
        if self.r > (self.n_pages-1)/10:
            self.next_p.set_sensitive(False)
            
    
    def prev_cb(self, *a):
        self.r -= 1
        self.add_btn()
        self.next_p.set_sensitive(True)
        if self.r == 1:
            self.prev_p.set_sensitive(False)
    
    def add_btn(self, *a):
        de = self.hb_btn.get_children()
        for a in de:
            self.hb_btn.remove(a)
        self.list_btn = []
        for a in range(10*(self.r-1),(10*self.r)):
            if a < self.n_pages:
                btn = Gtk.ToggleButton(str(a+1))
                btn.set_size_request(50, 24)
                btn.set_name(str(a))
                btn.connect('toggled', self.toggled_cb)
                btn.connect('toggled', self.select_page)
                if a == 0 : btn.set_active(True)
                self.hb_btn.pack_start(btn, False, False, 0)
                self.list_btn.append(btn)
        self.btns_pages.show_all()
    
    def refresh(self, n):
        de = self.btns_pages.get_children()
        for a in de:
            self.btns_pages.remove(a)
        self.r = 1
        self.n_pages = n
        self.hb_btn = Gtk.HBox(False, 1) 
        self.btns_pages.pack_start(Gtk.Label('الصفحات {} : '.format(str(self.n_pages),)), False, False, 0)
        self.prev_p = daw_customs.ButtonClass(' < ')
        self.prev_p.connect('clicked', self.prev_cb)
        self.prev_p.set_sensitive(False)
        self.btns_pages.pack_start(self.prev_p, False, False, 0)
        self.btns_pages.pack_start(self.hb_btn, False, False, 0)
        self.next_p = daw_customs.ButtonClass(' > ')
        if self.n_pages <= 10: self.next_p.set_sensitive(False)
        self.next_p.connect('clicked', self.next_cb)
        self.btns_pages.pack_start(self.next_p, False, False, 0)
        self.add_btn()
    
    def change_filter(self, *a):
        age = daw_customs.value_active(self.ages)
        balad = daw_customs.value_active(self.lands)
        sex = daw_customs.value_active(self.sexs)
        baher = daw_customs.value_active(self.baher)
        rawi = daw_customs.value_active(self.rawi)
        kafia = daw_customs.value_active(self.kafia)
        arodh = daw_customs.value_active(self.arodh)
        naw3 = daw_customs.value_active(self.naw3)
        gharadh = daw_customs.value_active(self.gharadh)
        self.poems_id = self.parent.db.filter_poem(sex, balad, age, baher, rawi, kafia, arodh, gharadh, naw3)
        self.list_filtereds()
    
    def list_filtereds(self, *a):
        if len(self.poems_id) == 0: v = 0
        else: v = len(self.poems_id)/50+1
        self.refresh(v)
        self.load_poems(0)
        
    def load_poems(self, v):
        self.poems_store.clear()
        self.names_list = []
        self.modelfilter = self.poems_store.filter_new()
        if len(self.poems_id) != 0:
            for a in range(v*50, (v+1)*50):
                if a < len(self.poems_id):
                    ls = self.parent.db.poem_info(self.poems_id[a])
                    i = self.poems_id[a]
                    name = ls[1]
                    if ls[2] != 0: n_poet, l_poet = self.parent.db.name_poet(ls[2])
                    else: l_poet = u'أحدهم'
                    abiat = ls[6]
                    if ls[7] != 0: baher = daw_tools.get_name(daw_tools.elbehor, ls[7])
                    else: baher = u'____'
                    if ls[8] != 0: rawi = daw_tools.get_name(daw_tools.elrawi, ls[8])
                    else: rawi = u'____'
                    if ls[11] != 0: gharadh = daw_tools.get_name(daw_tools.elgharadh, ls[11])
                    else: gharadh = u'____'
                    if ls[12] != 0: naw3 = daw_tools.get_name(daw_tools.elnaw3, ls[12])
                    else: naw3 = u'____'
                    self.poems_store.append([i, name, l_poet, naw3, baher, gharadh, rawi, abiat])
                    self.names_list.append(name)
        self.theword = self.names_list[:]
        self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
        self.tree_poems.set_model(self.modelfilter)
    
    def on_button_press(self, widget, event):
        if event.button == 3:
            self.popup.show_all()
            self.popup.popup(None, None, None, None, 3,
                             Gtk.get_current_event_time())
        elif event.button == 1 and event.get_click_count()[1] == 2:
            self.show_poem_cb()
                
    def modify_poem_cb(self, *a):
        model, i = self.tree_poems.get_selection().get_selected()
        if i:
            nm_poem = model.get_value(i,1)
            nm_poet = model.get_value(i,2)
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
            text = model.get_value(i,1)
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
    
    def __init__(self, parent):
        self.parent = parent
        self.poems_id = self.parent.db.all_poems_id()
        Gtk.HBox.__init__(self, False, 7)
        self.vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.vbox.set_border_width(6)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.vbox)
        scroll.set_size_request(220, -1)
        self.pack_start(scroll, False, False, 0)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        lab = Gtk.Label('\nالتصفية بحسب :\n')
        lab.set_alignment(0,0.5)
        self.vbox.pack_start(lab, False, False, 0)
        
        hb, self.ages = daw_customs.combo(daw_tools.age_poet, u'العصر', 1)
        self.ages.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.lands = daw_customs.combo(daw_tools.elbalad, u'البلد', 1)
        self.lands.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.sexs = daw_customs.combo(daw_tools.sex_poet, u'الجنس', 1)
        self.sexs.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.baher = daw_customs.combo(daw_tools.elbehor, u'البحر', 1)
        self.baher.connect('changed', self.a3aridh_elbaher)
        self.baher.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.rawi = daw_customs.combo(daw_tools.elrawi, u'الروي', 1)
        self.rawi.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.kafia = daw_customs.combo(daw_tools.elkawafi, u'القافية', 1)
        self.kafia.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.arodh = daw_customs.combo(daw_tools.ela3aridh, u'العروض', 1)
        self.arodh.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.naw3 = daw_customs.combo(daw_tools.elnaw3, u'النوع', 1)
        self.naw3.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        hb, self.gharadh = daw_customs.combo(daw_tools.elgharadh, u'الغرض', 1)
        self.gharadh.connect('changed', self.change_filter)
        self.vbox.pack_start(hb, False, False, 0)
        
        self.poems_store = Gtk.ListStore(int,str,str,str,str,str,str,int)
        self.tree_poems = daw_customs.TreePoem()
        self.tree_poems.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        self.tree_poems.connect("button-press-event", self.on_button_press)
        poems = Gtk.TreeViewColumn('القصيدة', Gtk.CellRendererText(), text=1)
        self.tree_poems.append_column(poems)
        poems.set_max_width(300)
        poets = Gtk.TreeViewColumn('الشاعر', Gtk.CellRendererText(), text=2)
        self.tree_poems.append_column(poets)
        poets.set_max_width(300)
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
        if len(self.parent.db.all_poems_id()) == 0: v = 0
        else: v = (len(self.parent.db.all_poems_id())/50)+1
        self.load_poems(0)
        self.btns_pages = Gtk.HBox(False, 3)
        self.refresh(v)
        self.btns_pages.set_border_width(2)
        vbox2.pack_start(self.btns_pages, False, False, 0)
        vbox2.pack_start(scroll, True, True, 0)
        self.pack_start(vbox2, True, True, 0)
        self.show_all()
        
        #--- Popup menu
        self.popup = Gtk.Menu()
        show_poem = Gtk.ImageMenuItem('اعرض القصيدة')
        show_poem.connect('activate', self.show_poem_cb)
        self.popup.append(show_poem)
        
        modify_poem = Gtk.ImageMenuItem('عدّل القصيدة')
        modify_poem.connect('activate', self.modify_poem_cb)
        self.popup.append(modify_poem)
        self.popup.show_all()
        