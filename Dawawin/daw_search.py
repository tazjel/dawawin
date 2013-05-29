# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
import os
from gi.repository import Gtk, GObject
import daw_tools, daw_araby, daw_customs
from daw_viewer import ShowPoem
from daw_tablabel import TabLabel
import cPickle

# class صفحة نتائج البحث-------------------------------------------------------------------

class ResultSearch(Gtk.Notebook):
   
    def search_on_page(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_poem(text) 
    
    def near_page(self, v):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.showpoem.near_poem(v)
        
    def move_in_page(self, v):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.move_in_page(v) 
   
    def __init__(self, parent):
        self.parent = parent
        Gtk.Notebook.__init__(self)
        self.set_scrollable(True)
        def eee(widget,*a):
            if self.get_n_pages() == 0:
                self.parent.main_notebook.set_current_page(0)
                self.parent.search_result_page.set_sensitive(False)
        self.connect("page-removed",eee)
        self.show_all()
        
# class عارض نتائج البحث-------------------------------------------------------------------

class ShowResult(Gtk.Box):
   
    def search_on_poem(self, text):
        self.showpoem.search_on_poem(text)
   
    def move_in_page(self, v):
        model, i = self.tree_results.get_selection().get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_results.get_selection().select_iter(i1)
            self.tree_results.scroll_to_cell((p+v,))
        elif len(self.tree_results.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_results.get_selection().select_iter(i2)
            self.tree_results.scroll_to_cell((0,))
        self.show_result()
   
    def __init__(self, parent):
        self.parent = parent
        self.showpoem = ShowPoem(self.parent)
        self.text = ''
        self.cursive = False
        self.results_list = []
        self.build()
    
    def show_result(self, *a):
        model, i = self.sel_result.get_selected()
        if i:
            id_poem = model.get_value(i,0)
            self.showpoem.loading(id_poem, self.parent.theme.fontmp)
            self.showpoem.mark_on_poem(self.text, self.cursive)
    
    def search(self, text, dict_perf, selected_list):
        self.text = text
        self.cursive = dict_perf['cursive']
        text = text.replace('"','')
        text = text.replace("'","")
        ls_term = []
        if dict_perf['with_tachkil'] == True: 
            cond = 'nasse LIKE ?'
        else:
            cond = 'fuzzy(nasse) LIKE ?'
            text = daw_araby.fuzzy_plus(text)
        if dict_perf['identical'] == True:  pfx, sfx = '% ', ' %'
        else: pfx, sfx = '%', '%'
        if dict_perf['cursive'] == True:
            self.condition = 'fuzzy(nasse) LIKE ?'
            ls_term.append(pfx+text+sfx)
        else: 
            for a in text.split(u' '):
                ls_term.append(pfx+a+sfx)
            #if dict_perf['one_verse'] == True:
            #    self.condition = u'fuzzy(nasse) LIKE ?'
            #    ls_term = ['%'+u'%[.+]%'.join(text.split(u' '))+u'%',]
            #else:
            if dict_perf['one_term'] == True:
                self.condition = ' OR '.join([cond]*len(ls_term))
            else :
                self.condition = ' AND '.join([cond]*len(ls_term))
        n = 0
        for a in selected_list:
            ls = self.parent.db.poems_id(a)
            for b in ls:
                check = self.parent.db.search(b, self.condition, ls_term)
                if check == True:
                    n += 1
                    self.results_store.append([b, n, self.parent.db.name_poem(b),
                                               self.parent.db.name_poet(self.parent.db.id_poet(b))[1],
                                               daw_tools.get_name(daw_tools.elbehor, self.parent.db.get_id_baher(b)),
                                               daw_tools.get_name(daw_tools.elgharadh, self.parent.db.gharadh_poem(b)),
                                               daw_tools.get_name(daw_tools.elrawi, self.parent.db.rawi_poem(b)),])
                    self.results_list.append([b, n, self.parent.db.name_poem(b),
                                               self.parent.db.name_poet(self.parent.db.id_poet(b))[1],
                                               daw_tools.get_name(daw_tools.elbehor, self.parent.db.get_id_baher(b)),
                                               daw_tools.get_name(daw_tools.elgharadh, self.parent.db.gharadh_poem(b)),
                                               daw_tools.get_name(daw_tools.elrawi, self.parent.db.rawi_poem(b)),])
                else: pass
        if len(self.results_list)>0:
            output = open(join(daw_customs.HOME_DIR,'آخر بحث.pkl'), 'wb')
            cPickle.dump(self.results_list, output)
            output.close()
   
    def sav_result_cb(self, *a):
        nm = self.sav_result_entry.get_text()
        if nm == "":
            daw_customs.erro(self.parent, "أدخل الاسم أولا.")
        elif nm in os.listdir(daw_customs.HOME_DIR): 
            daw_customs.erro(self.parent, "يوجد بحث محفوظ بنفس الاسم !!")
        else:
            output = open(join(daw_customs.HOME_DIR, nm+'.pkl'), 'wb')
            cPickle.dump(self.results_list, output)
            output.close()
        self.sav_result_entry.set_text("")
        
    def build(self, *a):
        Gtk.Box.__init__(self,spacing=7,orientation=Gtk.Orientation.VERTICAL)
        hb = Gtk.HBox(False, 7)
        self.sav_result_btn = Gtk.ToolButton(Gtk.STOCK_SAVE)
        hb.pack_start(self.sav_result_btn, False, False, 0)
        self.sav_result_btn.connect('clicked', self.sav_result_cb)
        self.sav_result_entry = Gtk.Entry()
        hb.pack_start(self.sav_result_entry, False, False, 0)
        self.showpoem.pack_end(hb, False, False, 0)
        self.pack_start(self.showpoem, True, True, 0)
        self.results_store = Gtk.ListStore(int,int,str,str,str,str,str)
        self.tree_results = daw_customs.TreeClass()
        self.tree_results.set_model(self.results_store)
        self.sel_result = self.tree_results.get_selection()
        self.tree_results.connect("cursor-changed", self.show_result)
        self.tree_results.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        raq = Gtk.TreeViewColumn('الرقم', Gtk.CellRendererText(), text=1)
        raq.set_max_width(50)
        self.tree_results.append_column(raq)
        poems = Gtk.TreeViewColumn('القصيدة', Gtk.CellRendererText(), text=2)
        self.tree_results.append_column(poems)
        poems.set_max_width(300)
        eldimwan = Gtk.TreeViewColumn('الشاعر', Gtk.CellRendererText(), text=3)
        self.tree_results.append_column(eldimwan)
        eldimwan.set_max_width(300)
        elbaher = Gtk.TreeViewColumn('البحر', Gtk.CellRendererText(), text=4)
        self.tree_results.append_column(elbaher)
        elbaher.set_max_width(120)
        elgharadh = Gtk.TreeViewColumn('الغرض', Gtk.CellRendererText(), text=5)
        self.tree_results.append_column(elgharadh)
        elgharadh.set_max_width(80)
        elrawi = Gtk.TreeViewColumn('الروي', Gtk.CellRendererText(), text=6)
        self.tree_results.append_column(elrawi)
        elrawi.set_max_width(50)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_results)
        scroll.set_size_request(-1, 200)
        self.pack_start(scroll, False, False, 0)
        self.show_all()
        
# class نافذة البحث-------------------------------------------------------------------

class Searcher(Gtk.Dialog):
   
    def __init__(self, parent):
        self.parent = parent
        self.showpoem = ShowPoem(self.parent)
        self.selected_list = []
        self.build()
        
    def search_cb(self, *a):
        return
        
    def select_age(self, btn):
        v = int(btn.get_name())
        a = 0
        while a in range(len(self.store_poets)):
            while (Gtk.events_pending()): Gtk.main_iteration()
            itr = self.store_poets.get_iter((a,))
            if self.store_poets.get_value(itr, 3) == v:
                if btn.get_active():
                    self.store_poets.set(itr, 2, True)
                else: self.store_poets.set(itr, 2, False)
                self.add_to_list(self.store_poets, itr, btn.get_active())
            a += 1
    
    def select_all(self, *a):
        for a in self.list_ages_btn:
            if self.all_poets.get_active() == True: a.set_active(True)
            else: a.set_active(False)
            
    def deselect_all(self, *a):
        for a in self.list_ages_btn:
            a.set_active(False)
            self.select_age(a)
        self.all_poets.set_active(False)
        
            
    def select_perf(self, btn):
        nm = btn.get_name()
        self.dict_perf[nm] = btn.get_active()
    
    def fixed_toggled(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 2)
        fixed = not fixed
        model.set(itr, 2, fixed)
        self.add_to_list(model, itr, fixed)
        
    def add_to_list(self, model, itr, fixed):
        id_poet = model.get_value(itr, 0)
        if fixed: 
            if id_poet not in self.selected_list:
                self.selected_list.append(id_poet)
        else:
            if id_poet in self.selected_list:
                idx = self.selected_list.index(id_poet, )
                self.selected_list.pop(idx)
    
    def search(self, *a):
        text = self.entry_search.get_text().decode('utf8')
        if text == u'':
            daw_customs.erro(self.parent, 'أدخل النص المراد البحث عنه')
        elif self.selected_list == []:
            daw_customs.erro(self.parent, 'أنت لم تحدد أين ستبحث')
        else:
            self.parent.set_title("دواوين العرب - نتائج البحث")
            self.parent.main_notebook.set_current_page(10)
            self.parent.search_result_page.set_sensitive(True)
            self.parent.search_result_page.set_active(True)
            sr = ShowResult(self.parent)
            self.parent.resultsearch.append_page(sr,TabLabel(sr, text))
            self.parent.resultsearch.set_current_page(-1)
            sr.search(text, self.dict_perf, self.selected_list)
            self.hide()
        
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_border_width(6)
        self.set_icon_name("Dawawin")
        area = self.get_content_area()
        area.set_spacing(6)
        self.set_title("نافذة البحث")
        self.set_size_request(700,450)
        self.connect('delete-event', lambda w,*a: w.hide() or True)
        self.vbox0 = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.list_ages = daw_tools.age_poet
        self.list_ages_btn = []
        for a in self.list_ages:
            btn = Gtk.CheckButton(a[1])
            btn.set_name(str(a[0]))
            btn.connect('toggled', self.select_age)
            box.pack_start(btn, False, False, 0)
            self.list_ages_btn.append(btn)
        frame = Gtk.Frame()
        frame.set_label('العصور')
        box.set_border_width(6)
        frame.add(box)
        self.hbox.pack_start(frame, False, False, 0)
        self.store_poets = Gtk.ListStore(int, GObject.TYPE_STRING,GObject.TYPE_BOOLEAN, int)
        self.tree_poets = Gtk.TreeView()
        ls = self.parent.db.all_poets()
        ls.append([0, u'ما لا يعرف قائله', None, 0, 9])
        for a in ls:
            self.store_poets.append([a[0], a[1], None, a[4]])
        self.tree_poets.set_model(self.store_poets)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poets)
        scroll.set_size_request(200, -1)
        celltext = Gtk.CellRendererText()
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntext = Gtk.TreeViewColumn("الديوان", celltext, text = 1 )
        columntoggle.add_attribute( celltoggle, "active", 2)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_poets)
        self.tree_poets.append_column(columntoggle)
        self.tree_poets.append_column(columntext)
        self.hbox.pack_start(scroll, True, True, 0)
             
        frame = Gtk.Frame()
        frame.set_label('خيارات البحث')
        self.dict_perf = {}
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(6)
        for a in [[u'بدون لواصق', u'identical'],
        [u'عبارة متصلة', u'cursive'], 
        [u'إحدى الكلمات', u'one_term'], 
        #[u'في نفس البيت', u'one_verse'], 
        [u'مع التشكيل', u'with_tachkil']]:
            btn = Gtk.CheckButton(a[0])
            btn.set_name(a[1])
            box.pack_start(btn, False, False, 0)
            btn.connect('toggled', self.select_perf)
            self.dict_perf[a[1]] = False
        frame.add(box)
        self.hbox.pack_start(frame, False, False, 0)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.null_all = daw_customs.ButtonClass('إلغاء التحديد')
        self.null_all.connect('clicked', self.deselect_all)
        hbox.pack_start(self.null_all, False, False, 0)
        self.all_poets = Gtk.CheckButton('جميع الدواوين')
        self.all_poets.connect('toggled', self.select_all) 
        hbox.pack_start(self.all_poets, False, False, 0)
        try: self.search_poet = Gtk.SearchEntry()
        except: self.search_poet = Gtk.Entry()
        self.search_poet.set_placeholder_text('بحث عن ديوان')
        self.search_poet.connect('changed', self.search_cb)
        hbox.pack_end(self.search_poet, False, False, 0)
        
        self.vbox0.pack_start(self.hbox, True, True, 0)
        self.vbox0.pack_start(hbox, False, False, 0)
        area.pack_start(self.vbox0, True, True, 0)
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        try: self.entry_search = Gtk.SearchEntry()
        except: self.entry_search = Gtk.Entry()
        self.entry_search.set_placeholder_text('أدخل النص المراد البحث عنه')
        self.btn_search = daw_customs.ButtonClass('بحث')
        self.btn_search.connect('clicked', self.search)
        hbox.pack_start(self.btn_search, False, False, 0)
        hbox.pack_start(self.entry_search, True, True, 0)
        self.btn_close = daw_customs.ButtonClass('إغلاق')
        self.btn_close.connect('clicked', lambda *a: self.hide() or True)
        hbox.pack_end(self.btn_close, False, False, 0)
        area = self.get_content_area()
        area.pack_start(hbox, False, False, 0)
        area.set_spacing(6)
