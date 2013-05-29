# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
from daw_contacts import MyDB
from gi.repository import Gtk, Pango
import daw_tools, daw_araby, daw_customs

# class صفحة التعديل--------------------------------------------------

class Organize(Gtk.Box):
    
    def visible_cb(self, model, itr, data):
        if len(self.theword) == 0: return
        if daw_araby.fuzzy(self.theword[0]) in daw_araby.fuzzy(model.get_value(itr, 1).decode('utf8')):
            return True
        else: return False
        
    def search_cb(self, *a):
        self.theword = [self.search_poets.get_text().decode('utf8')]
        self.modelfilter.refilter()
    
    def visible_cb0(self, model, itr, data):
        if len(self.theword) == 0: return
        if daw_araby.fuzzy(self.theword0[0]) in daw_araby.fuzzy(model.get_value(itr, 1).decode('utf8')):
            return True
        else: return False
        
    def search_on_page(self, text):
        if len(self.store_poems) == 0: return
        self.theword0 = [text]
        self.modelfilter0.refilter()
    
    def near_page(self, v):
        self.size_font += v
        self.view_charh.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.view_nasse.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.view_sabab.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.view_tarjama.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
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
    
    def __init__(self, parent):
        self.parent = parent
        self.db = MyDB()
        self.size_font = int(self.parent.theme.fontch[-2:])
        self.list_modifieds = []
        self .build()
    
    def modify_data(self, *a):
        model, i = self.sel_poem.get_selected()
        id_poem = model.get_value(i,0)
        text = daw_tools.right_space(self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(),
                                                        self.view_nasse_bfr.get_end_iter(), False)).decode('utf8')
        if text == '': daw_customs.erro(self.parent, 'لقد تم مسح القصيدة'); return
        nam = self.nm_poem.get_text().decode('utf8')
        if nam == '' : daw_customs.erro(self.parent, 'ضع اسما للقصيدة\nأو أول شطر منها'); return
        naw3 = daw_customs.value_active(self.naw3)
        if naw3 == None : daw_customs.erro(self.parent, 'حدد نوع القصيدة'); return
        if naw3 == 1:
            baher = daw_customs.value_active(self.baher)
            if baher == None : 
                if self.active_baher.get_active() == False:
                    baher = 0
                else: daw_customs.erro(self.parent, 'حدد بحر القصيدة'); return
            rawi = daw_customs.value_active(self.rawi)
            if rawi == None : 
                if self.active_rawi.get_active() == False:
                    rawi = 0
                else:  daw_customs.erro(self.parent, 'حدد روي القصيدة'); return
            kafia = daw_customs.value_active(self.kafia)
            if kafia == None : 
                if self.active_kafia.get_active() == False:
                    kafia = 0
                else:  daw_customs.erro(self.parent, 'حدد قافية القصيدة'); return
            arodh = daw_customs.value_active(self.arodh)
            if arodh == None : 
                if self.active_arodh.get_active() == False:
                    arodh = 0
                else:  daw_customs.erro(self.parent, 'حدد عروض القصيدة'); return
        elif naw3 == 2:
            baher = daw_customs.value_active(self.baher)
            if baher == None : 
                if self.active_baher.get_active() == False:
                    baher = 0
                else:  daw_customs.erro(self.parent, 'حدد بحر القصيدة'); return
            rawi = 0
            kafia = 0
            arodh = 0
        else:
            baher = 0
            rawi = 0
            kafia = 0
            arodh = 0
        gharadh = daw_customs.value_active(self.gharadh)
        if gharadh == None : 
                if self.active_gharadh.get_active() == False:
                    gharadh = 0
                else:  daw_customs.erro(self.parent, 'حدد غرض القصيدة'); return
        charh = self.view_charh_bfr.get_text(self.view_charh_bfr.get_start_iter(),
                                             self.view_charh_bfr.get_end_iter(), False).decode('utf8')
        sabab = self.view_sabab_bfr.get_text(self.view_sabab_bfr.get_start_iter(),
                                             self.view_sabab_bfr.get_end_iter(), False).decode('utf8')
        label = Gtk.Label()
        label.override_font(Pango.FontDescription('KacstOne 15'))
        if naw3 != 5:
            if arodh in [26, 27, 37, 39, 40]:
                longer_half, n_abiat = daw_tools.longer_half(text, label, 1)
            else:
                longer_half, n_abiat = daw_tools.longer_half(text, label, 0)
        else: longer_half = 0
        msg = daw_customs.sure(self.parent, '''
            هل أنت متأكد بأنك 
            تريد تعديل البيانات ؟
            ''' )
        if msg == Gtk.ResponseType.NO:
            return
        check = self.parent.db.modify_poem(id_poem, nam, text, sabab, charh, n_abiat, 
                                           baher, rawi, kafia, arodh, gharadh, naw3, longer_half)
        if check == None: daw_customs.info(self.parent, 'تم تعديل البيانات بنجاح'); return
    
    def modify_poet_cb(self, *a):
        model, i = self.sel_poet.get_selected()
        id_poet = model.get_value(i,0)
        if id_poet != 0:
            nm = self.nm_poet.get_text().decode('utf8')
            lak = self.lak_poet.get_text().decode('utf8')
            if nm == lak == '': daw_customs.erro(self.parent, 'ضع أسما للشاعر'); return
            if nm == '': nm += lak
            elif lak == '': lak += nm
            age = daw_customs.value_active(self.ages)
            if age == None : daw_customs.erro(self.parent, 'حدد عصر الشاعر\nأو اجعله غير معروف'); return
            balad = daw_customs.value_active(self.lands)
            if self.lands.get_sensitive():
                if balad == None : daw_customs.erro(self.parent, 'حدد بلد الشاعر\nأو اجعله غير معروف'); return
            else: balad = 22
            sex = daw_customs.value_active(self.sexs)
            if sex == None : daw_customs.erro(self.parent, 'حدد جنس الشاعر'); return
            die = self.dh_poet.get_value()
            tarjama = self.view_tarjama_bfr.get_text(self.view_tarjama_bfr.get_start_iter(),
                                                     self.view_tarjama_bfr.get_end_iter(), False).decode('utf8')
            msg = daw_customs.sure(self.parent, '''
                هل أنت متأكد بأنك 
                تريد تعديل بيانات الشاعر ؟
                ''' )
            if msg == Gtk.ResponseType.NO:
                return
            check = self.parent.db.modify_poet(id_poet, nm, lak, tarjama, die, sex, balad, age)
            if check == None: daw_customs.info(self.parent, 'تم تعديل البيانات بنجاح'); return
        else: return
    
    def load_data(self, text_poem='', text_sabab='', 
                  text_charh='', nm_poem='', baher=-1, rawi=-1, gharadh=-1, kafia=-1, naw3=-1, arodh=-1):
        self.view_nasse_bfr.set_text(text_poem)
        self.view_sabab_bfr.set_text(text_sabab)
        self.view_charh_bfr.set_text(text_charh)
        self.nm_poem.set_text(nm_poem)
        self.naw3.set_active(naw3)
        if self.baher.get_visible():
            self.baher.set_active(baher)
        if self.rawi.get_visible():
            self.rawi.set_active(rawi)
        if self.gharadh.get_visible():
            self.gharadh.set_active(gharadh)
        if self.kafia.get_visible():
            self.kafia.set_active(kafia)
        if self.arodh.get_visible():
            if arodh == None: arodh = -1
            self.arodh.set_active(arodh)
    
    # a حذف ديوان
    
    def remove_poet(self,*a):
        model, i = self.sel_poet.get_selected()
        if i:
            id_poet = model.get_value(i,0)
            nm = model.get_value(i,1)
            msg = daw_customs.sure(self.parent, '''
            سيتم حذف ديوان {}"
            مع بيانات الشاعر، هل تريد الاستمرار ؟
            '''.format(nm,))
            if msg == Gtk.ResponseType.YES:
                check = self.parent.db.remove_poet(id_poet)
                if check == None:
                    self.refresh_poets()
    
    # a حذف قصيدة
                    
    def remove_poem(self,*a):
        model, i = self.sel_poem.get_selected()
        if i:
            id_poem = model.get_value(i,0)
            nm = model.get_value(i,1)
            msg = daw_customs.sure(self.parent, '''
            سيتم حذف قصيدة {}
            هل تريد الاستمرار ؟
            '''.format(nm,))
            if msg == Gtk.ResponseType.YES:
                check = self.parent.db.remove_poem(id_poem)
                if check == None:
                    self.ok_poet()
    
    def ok_poem(self, *a):
        self.notebk.set_current_page(1)
        model, i = self.sel_poem.get_selected()
        if i:
            id_poem = model.get_value(i,0)
            text_poem, text_sabab, text_charh, text_ta3lik = self.parent.db.get_poem(id_poem)
            nm_poem = self.parent.db.name_poem(id_poem)
            baher = self.parent.db.get_id_baher(id_poem)-1
            rawi = daw_tools.get_index(daw_tools.elrawi, self.parent.db.rawi_poem(id_poem))
            gharadh = daw_tools.get_index(daw_tools.elgharadh, self.parent.db.gharadh_poem(id_poem))
            kafia = daw_tools.get_index(daw_tools.elkawafi, self.parent.db.kafia_poem(id_poem))
            naw3 = daw_tools.get_index(daw_tools.elnaw3, self.parent.db.naw3_poem(id_poem))
            if baher == -1:
                arodh = -1
            else:
                arodh = daw_tools.get_index_arodh(self.parent.db.get_id_baher(id_poem), 
                                                  self.parent.db.arodh_poem(id_poem))
            self.load_data(text_poem, text_sabab, text_charh, nm_poem, baher, rawi, gharadh,
                            kafia, naw3, arodh)
            self.list_modifieds = []
            self.list_modifieds.append(text_poem)
            self.redo.set_sensitive(False)  
    
    def ok_poet(self, *a):
        model, i = self.sel_poet.get_selected()
        if i:
            id_poet = model.get_value(i,0)
            list_poems, self.text_tarjama = self.parent.db.poems_of_poet(id_poet)
            if id_poet != 0:
                self.grid_poet.set_sensitive(True)
                self.view_tarjama_bfr.set_text(self.text_tarjama)
                self.lak_poet.set_text(self.parent.db.name_poet(id_poet)[1])
                self.nm_poet.set_text(self.parent.db.name_poet(id_poet)[0])
                self.ages.set_active(daw_tools.get_index(daw_tools.age_poet, self.parent.db.age_poet(id_poet)))
                self.lands.set_active(daw_tools.get_index(daw_tools.elbalad, self.parent.db.balad_poet(id_poet)))
                self.sexs.set_active(daw_tools.get_index(daw_tools.sex_poet, self.parent.db.sex_poet(id_poet)))
                self.dh_poet.set_value(float(self.parent.db.death_poet(id_poet)))
            else:
                self.grid_poet.set_sensitive(False)
                self.view_tarjama_bfr.set_text('')
                self.lak_poet.set_text('')
                self.nm_poet.set_text('')
                self.ages.set_active(-1)
                self.lands.set_active(-1)
                self.sexs.set_active(-1)
                self.dh_poet.set_value(0.0)
            self.store_poems.clear()
            self.load_data()
            if len(list_poems) != 0:
                self.names_list0 = []
                self.modelfilter0 = self.store_poems.filter_new()
                for a in list_poems:
                    self.store_poems.append([a[0], a[1]])
                    self.names_list0.append(a[1])
                self.theword0 = self.names_list0[:]
                self.modelfilter0.set_visible_func(self.visible_cb0, self.theword0) 
                self.tree_poems.set_model(self.modelfilter0)
            self.notebk.set_current_page(0)
            
    def change_text(self, *a):
        text = (self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(), self.view_nasse_bfr.get_end_iter(), False)).decode('utf8')
        model, i = self.sel_poem.get_selected()
        if i:
            id_poem = model.get_value(i,0)
            if len(self.list_modifieds) > 0:
                if text != self.list_modifieds[-1]:
                    self.list_modifieds.append(text)
                    self.redo.set_sensitive(True)
    
    def redo_text(self, *a):
        del self.list_modifieds[-1]
        self.view_nasse_bfr.set_text(self.list_modifieds[-1])
        del self.list_modifieds[-1]
        del self.list_modifieds[-1]
        if len(self.list_modifieds) == 1:
            self.redo.set_sensitive(False)      
    
    def change_naw3(self, *a):
        if self.naw3.get_active() == 0:
            self.baher_hb.show_all()
            self.rawi_hb.show_all()
            self.kafia_hb.show_all()
            self.arodh_hb.show_all()
        elif self.naw3.get_active() == 1:
            self.baher_hb.show_all()
            self.rawi_hb.hide()
            self.kafia_hb.hide()
            self.arodh_hb.hide()
        else:
            self.baher_hb.hide()
            self.rawi_hb.hide()
            self.kafia_hb.hide()
            self.arodh_hb.hide()
    
    def a3aridh_elbaher(self, *a):
        model = self.arodh.get_model()
        model.clear()
        baher = daw_customs.value_active(self.baher)
        if baher == None: return
        a3aridh = daw_tools.ela3aridh_in_behor[baher]
        for a in a3aridh:
            nm = daw_tools.get_name(daw_tools.ela3aridh, a)
            model.append([a, nm])
    
    def select_age(self, *a):
        if daw_customs.value_active(self.ages) == 8: self.lands.set_sensitive(True)
        else:
            self.lands.set_active(-1)
            self.lands.set_sensitive(False)
    
    def tashkeel_cb(self, btn, haraka):
        self.view_nasse_bfr.insert_at_cursor(haraka)
    
    def merge_poet_cb(self, *a):
        new_poet = self.poets_entry1.get_text()
        if new_poet == '': return
        poet, sex, balad, age = self.parent.db.id_name_poet(new_poet.decode('utf8'))
        if poet == None: daw_customs.erro(self.parent, 'ضع الاسم الصحيح للشاعر'); return
        model, i = self.sel_poet.get_selected()
        if i:
            poet_old = model.get_value(i,0)
            self.parent.db.merge_poet(poet_old, poet, sex, balad, age)
            daw_customs.info(self.parent, 'تم دمج ديوان {} مع ديوان {}'.format(model.get_value(i,1), new_poet))
    
    def move_poem_cb(self, *a):
        new_poet = self.poets_entry.get_text()
        if new_poet == '': return
        poet, sex, balad, age = self.parent.db.id_name_poet(new_poet.decode('utf8'))
        if poet == None: daw_customs.erro(self.parent, 'ضع الاسم الصحيح للشاعر'); return
        model, i = self.sel_poem.get_selected()
        if i:
            poem = model.get_value(i,0)
            self.parent.db.change_poet(poem, poet, sex, balad, age)
            daw_customs.info(self.parent, 'تم نقل القصيدة {} إلى ديوان {}'.format(model.get_value(i,1), new_poet))
            model.remove(i)
      
    def refresh_poets(self, *a):
        self.store_poet.clear()
        ls = self.db.all_poets()
        self.modelfilter = self.store_poet.filter_new()
        ls.append([0, u'ما لا يعرف قائله', 0, 22, 9])
        self.names_list = []
        for a in ls:
            s_list = []
            self.store_poet.append(a)
            s_list.append(a[2])
            self.names_list.append(s_list)
        self.theword = self.names_list[:]
        self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
        self.tree_poet.set_model(self.modelfilter)
      
    def build(self,*a): 
        Gtk.Box.__init__(self,spacing=7,orientation=Gtk.Orientation.VERTICAL)
        hp1 = Gtk.HPaned()
        self.pack_start(hp1, True, True, 0)
        self.tree_poet = daw_customs.TreeClass()
        self.sel_poet = self.tree_poet.get_selection()
        cell = Gtk.CellRendererText()
        cell.set_property("wrap-mode", Pango.WrapMode.WORD_CHAR)
        cell.set_property("wrap-width", 150)
        kal = Gtk.TreeViewColumn('دواوين الشعراء', cell, text=1)
        self.tree_poet.append_column(kal)
        self.store_poet = Gtk.ListStore(int, str, int, int, int)
        self.refresh_poets()
        self.tree_poet.connect("cursor-changed", self.ok_poet)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poet)
        scroll.set_size_request(150, -1)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        try: self.search_poets = Gtk.SearchEntry()
        except: self.search_poets = Gtk.Entry()
        self.search_poets.set_placeholder_text('بحث عن شاعر')
        self.search_poets.connect('changed', self.search_cb)
        vb.pack_start(self.search_poets, False, False, 0)
        vb.pack_start(scroll, True, True, 0)
        hp1.pack1(vb, False, False)
        
        hp2 = Gtk.HPaned()
        hp1.pack2(hp2, True, True)
        self.store_poems = Gtk.ListStore(int, str)
        self.tree_poems = daw_customs.TreeClass()
        self.tree_poems.set_model(self.store_poems)
        self.sel_poem = self.tree_poems.get_selection()
        self.tree_poems.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        self.tree_poems.connect("cursor-changed", self.ok_poem)
        poems = Gtk.TreeViewColumn('القصائد', Gtk.CellRendererText(), text=1)
        self.tree_poems.append_column(poems)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poems)
        scroll.set_size_request(180, -1)
        hp2.pack1(scroll, False, False)
        
        self.notebk = Gtk.Notebook()
        hp2.pack2(self.notebk, True, True)
        self.notebk.set_show_tabs(False)
        self.nbk1 = Gtk.Notebook()
        self.nbk2 = Gtk.Notebook()
        self.view_nasse  = daw_customs.ViewEdit()
        self.view_nasse.set_justification(Gtk.Justification.CENTER)
        self.view_nasse_bfr = self.view_nasse.get_buffer()
        self.view_nasse_bfr.connect('changed', self.change_text)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_nasse)
        vb = Gtk.VBox(False, 0)
        hb = Gtk.HBox(False, 0)
        lab = Gtk.Label('التشكيل :   ')
        lab.set_alignment(0,0.5)
        hb.pack_start(lab, False, False, 0)
        shadda = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'shadda.png'), 'الشدة', self.tashkeel_cb, daw_araby.SHADDA)
        hb.pack_start(shadda, False, False, 0)
        skon = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'skon.png'), 'السكون',self.tashkeel_cb, daw_araby.SUKUN)
        hb.pack_start(skon, False, False, 0)
        fatha = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'fatha.png'), 'الفتحة',self.tashkeel_cb, daw_araby.FATHA)
        hb.pack_start(fatha, False, False, 0)
        damma = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'damma.png'), 'الضمة',self.tashkeel_cb, daw_araby.DAMMA)
        hb.pack_start(damma, False, False, 0)
        kasra = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'kasra.png'), 'الكسرة',self.tashkeel_cb, daw_araby.KASRA)
        hb.pack_start(kasra, False, False, 0)
        fatha2 = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'fatha2.png'), 'الفتحتين',self.tashkeel_cb, daw_araby.FATHATAN)
        hb.pack_start(fatha2, False, False, 0)
        damma2 = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'damma2.png'), 'الضمتين',self.tashkeel_cb, daw_araby.DAMMATAN)
        hb.pack_start(damma2, False, False, 0)
        kasra2 = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'kasra2.png'), 'الكسرتين',self.tashkeel_cb, daw_araby.KASRATAN)
        hb.pack_start(kasra2, False, False, 0)
        vb.pack_start(scroll, True, True, 0)
        
        self.redo = Gtk.ToolButton(stock_id=Gtk.STOCK_REDO)
        self.redo.set_sensitive(False)
        hb.pack_end(self.redo, False, False, 3)
        self.redo.connect('clicked', self.redo_text)
        vb.pack_start(hb, False, False, 0)
        self.nbk1.append_page(vb, Gtk.Label('القصيدة'))
        
        self.view_charh = daw_customs.ViewEdit()
        self.view_charh_bfr = self.view_charh.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_charh)
        self.nbk1.append_page(scroll, Gtk.Label('الشرح'))
        
        vb = Gtk.VBox(False, 7)
        vb.set_border_width(7)
        hb = Gtk.HBox(False, 7)
        la0 = Gtk.Label('اسم القصيدة')
        la0.set_alignment(0,0.5)
        hb.pack_start(la0, False, False, 0)
        self.nm_poem = Gtk.Entry()
        self.nm_poem.set_placeholder_text('إن لم يكن لها اسم ، اكتب صدر أول بيت بدلا من ذلك')
        hb.pack_start(self.nm_poem, True, True, 0)
        vb.pack_start(hb, False, False, 0)
  
        hb, self.naw3 = daw_customs.combo(daw_tools.elnaw3, u'النوع', 0)
        vb.pack_start(hb, False, False, 0)
        self.naw3.connect('changed', self.change_naw3)
        
        hb, self.gharadh = daw_customs.combo(daw_tools.elgharadh, u'الغرض', 0)
        vb.pack_start(hb, False, False, 0)
        self.active_gharadh = Gtk.CheckButton('')
        self.active_gharadh.set_active(True)
        def active_gharadh_cb(widget, *a):
            if self.active_gharadh.get_active():
                self.gharadh.set_sensitive(True)
            else:
                self.gharadh.set_sensitive(False)
                self.gharadh.set_active(-1)
        self.active_gharadh.connect('toggled', active_gharadh_cb)
        hb.pack_start(self.active_gharadh, False, False, 0)

        self.baher_hb, self.baher = daw_customs.combo(daw_tools.elbehor, u'البحر', 0)
        self.baher.connect('changed', self.a3aridh_elbaher)
        vb.pack_start(self.baher_hb, False, False, 0)
        self.active_baher = Gtk.CheckButton('')
        self.active_baher.set_active(True)
        def active_baher_cb(widget, *a):
            if self.active_baher.get_active():
                self.baher.set_sensitive(True)
            else:
                self.baher.set_sensitive(False)
                self.baher.set_active(-1)
        self.active_baher.connect('toggled', active_baher_cb)
        self.baher_hb.pack_start(self.active_baher, False, False, 0)
        
        self.rawi_hb, self.rawi = daw_customs.combo(daw_tools.elrawi, u'الروي', 0)
        vb.pack_start(self.rawi_hb, False, False, 0)
        self.active_rawi = Gtk.CheckButton('')
        self.active_rawi.set_active(True)
        def active_rawi_cb(widget, *a):
            if self.active_rawi.get_active():
                self.rawi.set_sensitive(True)
            else:
                self.rawi.set_sensitive(False)
                self.rawi.set_active(-1)
        self.active_rawi.connect('toggled', active_rawi_cb)
        self.rawi_hb.pack_start(self.active_rawi, False, False, 0)
        
        self.kafia_hb, self.kafia = daw_customs.combo(daw_tools.elkawafi, u'القافية', 0)
        vb.pack_start(self.kafia_hb, False, False, 0)
        self.active_kafia = Gtk.CheckButton('')
        self.active_kafia.set_active(True)
        def active_kafia_cb(widget, *a):
            if self.active_kafia.get_active():
                self.kafia.set_sensitive(True)
            else:
                self.kafia.set_sensitive(False)
                self.kafia.set_active(-1)
        self.active_kafia.connect('toggled', active_kafia_cb)
        self.kafia_hb.pack_start(self.active_kafia, False, False, 0)
        
        self.arodh_hb, self.arodh = daw_customs.combo([], u'العروض وضربها', 0)
        vb.pack_start(self.arodh_hb, False, False, 0)
        self.active_arodh = Gtk.CheckButton('')
        self.active_arodh.set_active(True)
        def active_arodh_cb(widget, *a):
            if self.active_arodh.get_active():
                self.arodh.set_sensitive(True)
            else:
                self.arodh.set_sensitive(False)
                self.arodh.set_active(-1)
        self.active_arodh.connect('toggled', active_arodh_cb)
        self.arodh_hb.pack_start(self.active_arodh, False, False, 0)
        
        la1 = Gtk.Label('سبب النظم')
        la1.set_alignment(0,1)
        vb.pack_start(la1, False, False, 0)
        self.view_sabab = daw_customs.ViewEdit()
        self.view_sabab_bfr = self.view_sabab.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_sabab)
        vb.pack_start(scroll, True, True, 0)
        self.nbk1.append_page(vb, Gtk.Label('معلوماتها'))
        
        self.view_tarjama = daw_customs.ViewEdit()
        self.view_tarjama_bfr = self.view_tarjama.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_tarjama)
        self.nbk2.append_page(scroll, Gtk.Label('الترجمة'))
        
        self.grid_poet = Gtk.Grid()
        self.grid_poet.set_column_spacing(6)
        self.grid_poet.set_row_spacing(6)
        self.grid_poet.set_border_width(6)

        self.grid_poet.attach(Gtk.Label('الاسم المشتهر'), 1, 1, 1, 1)
        self.lak_poet = Gtk.Entry()
        self.grid_poet.attach(self.lak_poet, 2, 1, 3, 1)
        
        self.grid_poet.attach(Gtk.Label('الاسم الحقيقي'), 1, 2, 1, 1)
        self.nm_poet = Gtk.Entry()
        self.grid_poet.attach(self.nm_poet, 2, 2, 3, 1)
        
        hb, self.ages = daw_customs.combo(daw_tools.age_poet, u'العصر', 0)
        self.ages.connect('changed', self.select_age)
        self.grid_poet.attach(hb, 1, 3, 4, 1)
        
        hb, self.lands = daw_customs.combo(daw_tools.elbalad, u'البلد', 0)
        self.grid_poet.attach(hb, 1, 4, 4, 1)
        
        hb, self.sexs = daw_customs.combo(daw_tools.sex_poet, u'الجنس', 0)
        self.grid_poet.attach(hb, 1, 5, 4, 1)
        
        self.grid_poet.attach(Gtk.Label('الوفاة (هـ)'), 1, 6, 1, 1)
        adj = Gtk.Adjustment(1434, -300, 1434, 1, 5.0, 0.0)
        self.dh_poet = Gtk.SpinButton()
        self.dh_poet.set_adjustment(adj)
        self.dh_poet.set_wrap(True)
        self.grid_poet.attach(self.dh_poet, 2, 6, 1, 1)
        self.nbk2.append_page(self.grid_poet, Gtk.Label('معلومات الشاعر'))
        
        vb = Gtk.VBox(False, 7)
        vb.set_border_width(7)
        hb = Gtk.HBox(False, 7)
        move_poem = daw_customs.ButtonClass('نقل القصيدة الحالية إلى ديوان : ')
        move_poem.connect('clicked', self.move_poem_cb)
        hb.pack_start(move_poem, False, False, 0)
        self.poets_entry = Gtk.Entry()
        self.poets_entry.set_placeholder_text('اكتب حرفا لتحصل على التكملة')
        self.completion03 = Gtk.EntryCompletion()
        self.completion03.set_model(self.parent.dawawinpage.store_poet)
        self.completion03.set_text_column(1)
        self.poets_entry.set_completion(self.completion03)
        hb.pack_start(self.poets_entry, True, True, 0)
        vb.pack_start(hb, False, False, 0)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.del_poem = daw_customs.ButtonClass('حذف قصيدة')
        self.del_poem.connect('clicked',self.remove_poem)
        hbox.pack_start(self.del_poem, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        self.nbk1.append_page(vb, Gtk.Label('متقدم'))
        
        vb = Gtk.VBox(False, 7)
        vb.set_border_width(7)
        hb = Gtk.HBox(False, 7)
        merge_poet = daw_customs.ButtonClass('دمج الشاعر الحالي مع الشاعر : ')
        merge_poet.connect('clicked', self.merge_poet_cb)
        hb.pack_start(merge_poet, False, False, 0)
        self.poets_entry1 = Gtk.Entry()
        self.poets_entry1.set_placeholder_text('اكتب حرفا لتحصل على التكملة')
        self.completion04 = Gtk.EntryCompletion()
        self.completion04.set_model(self.parent.dawawinpage.store_poet)
        self.completion04.set_text_column(1)
        self.poets_entry1.set_completion(self.completion04)
        hb.pack_start(self.poets_entry1, True, True, 0)
        vb.pack_start(hb, False, False, 0)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.del_poet = daw_customs.ButtonClass('حذف ديوان')
        self.del_poet.connect('clicked',self.remove_poet)
        hbox.pack_start(self.del_poet, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        self.nbk2.append_page(vb, Gtk.Label('متقدم'))
        
        vb = Gtk.VBox(False, 7)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.modif_poet = daw_customs.ButtonClass('تعديل الشاعر')
        self.modif_poet.connect('clicked',self.modify_poet_cb)
        vb.pack_start(self.nbk2, True, True, 0)
        vb.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.modif_poet, False, False, 0)
        self.notebk.append_page(vb, Gtk.Label(''))
        
        vb = Gtk.VBox(False, 7)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.modif_poem = daw_customs.ButtonClass('تعديل القصائد')
        self.modif_poem.connect('clicked',self.modify_data)
        vb.pack_start(self.nbk1, True, True, 0)
        vb.pack_start(hbox, False, False, 0)
        hbox.pack_start(self.modif_poem, False, False, 0)
        self.notebk.append_page(vb, Gtk.Label(''))

        self.show_all()
        