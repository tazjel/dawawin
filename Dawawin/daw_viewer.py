# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, exists, basename
from gi.repository import Gtk, Pango, Gdk
from shutil import copyfile
from daw_export import Exporter
import daw_config, daw_tools, daw_araby, daw_customs, daw_stemming


# class صفحة القصائد-------------------------------------------------------------------

class ViewerPoem(Gtk.Notebook):
   
    def move_in_page(self, v):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.move_in_page(v) 
   
    def search_on_page(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_poem(text) 
   
    def near_page(self, v):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.near_poem(v) 
   
    def __init__(self, parent):
        self.parent = parent
        Gtk.Notebook.__init__(self)
        self.set_scrollable(True)
        def eee(widget,*a):
            if self.get_n_pages() == 0:
                self.parent.main_notebook.set_current_page(0)
                self.parent.poems_page.set_sensitive(False)
        self.connect("page-removed",eee)
        self.show_all()

# class عرض القصيدة-------------------------------------------------------------------

class ShowPoem(Gtk.Box):
    
    __gtype_name__ = 'showpoem'
    
    def change_font(self, *a):
        self.speaker_poem_tag.set_property('foreground', self.parent.theme.coloran) 
        self.speaker_poem_tag.set_property('font', self.parent.theme.fontan)
        self.search_poem_tag.set_property('foreground', self.parent.theme.colortp)
        self.search_poem_tag.set_property('background', self.parent.theme.colorss)
        self.new_font = self.parent.theme.fontmp

    def copy_sel(self, *a):
        sel = self.view_poem_bfr.get_selection_bounds()
        sel_text = self.view_poem_bfr.get_text(sel[0], sel[1],True)
        self.clipboard.set_text(sel_text, -1)

    def populate_popup(self, view, menu):
        for a in menu.get_children():
            a.destroy()
        buff = view.get_buffer()
        f1 = Gtk.MenuItem('شرح المفردة في القواميس')
        f1.add_accelerator("activate", self.axl, Gdk.KEY_D, self.ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        menu.append(f1)
        f1.set_sensitive(False)
        f1.show()
        c1 = Gtk.SeparatorMenuItem()
        menu.append(c1)
        c1.show()
        f4 = Gtk.MenuItem('نسخ')
        menu.append(f4)
        f4.set_sensitive(False)
        f4.show()
        c3 = Gtk.SeparatorMenuItem()
        menu.append(c3)
        c3.show()
        f2 = Gtk.MenuItem('تعليم البيت للرجوع إليه')
        menu.append(f2)
        f2.set_sensitive(False)
        f2.show()
        f3 = Gtk.MenuItem('إضافة الأبيات المحددة إلى أبياتي')
        menu.append(f3)
        f3.set_sensitive(False)
        f3.show()
        f5 = Gtk.MenuItem('إرسال البيت المحدد لتقطيعه عروضيا')
        menu.append(f5)
        f5.set_sensitive(False)
        f5.show()
        c4 = Gtk.SeparatorMenuItem()
        menu.append(c4)
        c4.show()
        f6 = Gtk.MenuItem('ضم القصيدة إلى المفضلة')
        menu.append(f6)
        f6.show()
        f7 = Gtk.MenuItem('إضافة ملف صوتي للقصيدة')
        menu.append(f7)
        f7.show()
        f8 = Gtk.MenuItem('تصدير القصيدة إلى ملف')
        imenu = Gtk.Menu()
        f8.set_submenu(imenu)
        menu.append(f8)
        fm1 = Gtk.MenuItem('pdf')
        #imenu.append(fm1)
        fm2 = Gtk.MenuItem('odt')
        #imenu.append(fm2)
        fm3 = Gtk.MenuItem('html')
        imenu.append(fm3)
        fm4 = Gtk.MenuItem('text')
        imenu.append(fm4)
        f8.show_all()
        c5 = Gtk.SeparatorMenuItem()
        menu.append(c5)
        c5.show()
        f9 = Gtk.MenuItem('شرح القصيدة')
        f9.add_accelerator("activate",self.axl, Gdk.KEY_F4, 0, Gtk.AccelFlags.VISIBLE)
        menu.append(f9)
        f9.show()
        f10 = Gtk.MenuItem('التعليق على القصيدة')
        f10.add_accelerator("activate",self.axl, Gdk.KEY_F3, 0, Gtk.AccelFlags.VISIBLE)
        menu.append(f10)
        f10.show()
        f11 = Gtk.MenuItem('نبذة عن القصيدة')
        f11.add_accelerator("activate",self.axl, Gdk.KEY_F2, 0, Gtk.AccelFlags.VISIBLE)
        menu.append(f11)
        f11.show()
        c6 = Gtk.SeparatorMenuItem()
        menu.append(c6)
        c6.show()
        f12 = Gtk.MenuItem('تعديل القصيدة')
        menu.append(f12)
        f12.show()
        if buff.get_has_selection():
            f1.set_sensitive(True)
            f2.set_sensitive(True)
            f3.set_sensitive(True)
            f4.set_sensitive(True)
            f5.set_sensitive(True)
        f1.connect("activate", self.explain_term)
        f4.connect("activate", self.copy_sel)
        f11.connect("activate", self.show_nabdha)
        f12.connect("activate", self.modify_poem_cb)
        f9.connect("activate", self.show_charh)
        f10.connect("activate", self.show_ta3lik)
        f6.connect("activate", self.save_tafdil)
        f2.connect("activate", self.save_ta3lim)
        f7.connect("activate", self.set_recite)
        f3.connect("activate", self.save_abiaty)
        f5.connect("activate", self.scan_verse)
        fm1.connect("activate", self.export_pdf)
        fm2.connect("activate", self.export_odt)
        fm3.connect("activate", self.export_html)
        fm4.connect("activate", self.export_text)

    def modify_poem_cb(self, *a):
        self.parent.set_title("دواوين العرب - التعديل")
        self.parent.main_notebook.set_current_page(11)
        if self.nm_poet == u"أحدهم": self.nm_poet = u'ما لا يعرف قائله'
        self.parent.organizepage.search_poets.set_text(self.nm_poet)
        self.parent.organizepage.sel_poet.select_path((0,))
        self.parent.organizepage.ok_poet()
        self.parent.entry_search.set_text(self.nm_poem)
        self.parent.reg_page.set_active(True)

    def show_nabdha(self, *a):
        self.vp.pack2(self.vbox_charh, False, False)
        self.view_charh_bfr.set_text(self.text_nabdha)
        self.vbox_charh.show_all()
        self.save_charh.hide()
        self.view_charh.set_cursor_visible(False)
        self.view_charh.set_editable(False)
        self.lab_charh.set_label("نبذة عن القصيدة")
    
    def show_charh(self, *a):
        self.vp.pack2(self.vbox_charh, False, False)
        self.view_charh_bfr.set_text(self.text_charh)
        self.vbox_charh.show_all()
        self.save_charh.hide()
        self.view_charh.set_cursor_visible(False)
        self.view_charh.set_editable(False)
        self.lab_charh.set_label("شرح القصيدة")
    
    def show_ta3lik(self, *a):
        self.text_ta3lik = self.parent.db.get_poem(self.id_poem)[3]
        self.view_charh.set_cursor_visible(True)
        self.view_charh.set_editable(True)
        self.vp.pack2(self.vbox_charh, False, False)
        self.view_charh_bfr.set_text(self.text_ta3lik)
        self.vbox_charh.show_all()
        self.lab_charh.set_label("التعليق على القصيدة")
        
    def save_ta3lik(self, *a):
        text = daw_tools.right_space(self.view_charh_bfr.get_text(self.view_charh_bfr.get_start_iter(),
                                                             self.view_charh_bfr.get_end_iter(), False))
        self.parent.db.set_ta3lik(self.id_poem, text.decode('utf8'))

    def search_and_mark(self, text, start):
        end = self.view_poem_bfr.get_end_iter()
        match = start.forward_search(text, 0, end)
        if match != None:
            match_start, match_end = match
            self.view_poem_bfr.apply_tag(self.search_poem_tag, match_start, match_end)
            self.search_and_mark(text, match_end)
            if match_start and (not self.i_min or self.i_min.compare(match_start) > 0): 
                self.i_min = match_start
            if self.i_min:
                self.view_poem.scroll_to_iter(self.i_min, 0.0, True, 0.5, 0.5)
                
    def mark_on_poem(self, text, cursive=False): 
        self.i_min = None
        text = daw_araby.fuzzy(text)
        ls = text.split()
        ln = len(ls)
        list_search = []
        ls_poem, nw = daw_tools.n_words(self.text_poem)
        list_word = self.new_poem.split()
        if cursive == False:
            for n in range(nw):
                for k in range(len(ls)): 
                    if ls[k] in daw_araby.fuzzy(ls_poem[n]) or ls[k] in ls_poem[n]:
                        list_search.append(daw_customs.tashkil(list_word[n]))
        else:
            for n in range(nw):
                ntext = daw_araby.fuzzy(' '.join(ls_poem[n:n+ln]))
                if text in ntext:
                    list_search.append(daw_customs.tashkil(' '.join(list_word[n:n+ln])))
        for txt in list_search:
            cursor_mark = self.view_poem_bfr.get_insert()
            start = self.view_poem_bfr.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.view_poem_bfr.get_char_count():
                start = self.view_poem_bfr.get_start_iter()
                self.search_and_mark(txt, start)
       
    def search_on_poem(self, text): 
        self.i_min = None      
        try: 
            self.build(self.new_font)
            if len(text) > 0:
                self.mark_on_poem(text, False)         
        except: pass 
               
    def search_half(self, text):
        self.i_min = None
        text = text.decode('utf8')
        list_search = []        
        self.build(self.new_font)
        ls_poem = self.new_poem.splitlines(1)
        for a in ls_poem:
            if daw_araby.fuzzy(text) in daw_araby.fuzzy(a) :
                list_search.append(daw_customs.tashkil(a))
        for txt in list_search:
            cursor_mark = self.view_poem_bfr.get_insert()
            start = self.view_poem_bfr.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.view_poem_bfr.get_char_count():
                start = self.view_poem_bfr.get_start_iter()
            self.search_and_mark(txt, start)
            
    def near_poem(self, v):
        font = self.new_font[:-2]
        sz = int(self.new_font[-2:])
        new_sz = sz+v
        if new_sz < 10: return
        self.new_font = font+str(new_sz)
        self.build(self.new_font)
        
    def move_in_page(self, v):
        dx = self.list_id_poem.index(self.id_poem)
        new_dx = dx+v
        if new_dx >= len(self.list_id_poem): return
        if new_dx == -1: return
        new_id_poem = self.list_id_poem[new_dx]
        self.id_poem = new_id_poem
        self.loading(new_id_poem, self.new_font)
        name_poem = self.parent.db.name_poem(new_id_poem)
        self.parent.viewerpoem.get_tab_label(self).lab.set_text(name_poem)
  
    def get_nabdha(self, id_poem):
        text = u'\n\
        - الشاعر : {} \n\
        - القصيدة : {} \n\
        - الأبيات : {} \n\
        - الغرض : {} \n\
        - البحر : {} \n\
        - سبب النظم : {} \n' .format(
        self.name_poet, 
        self.parent.db.name_poem(id_poem), 
        self.parent.db.abiat_poem(id_poem), 
        daw_tools.get_name(daw_tools.elgharadh, self.parent.db.gharadh_poem(id_poem)),
        daw_tools.get_name(daw_tools.elbehor, self.parent.db.get_id_baher(id_poem)), 
        self.text_sabab)
        return text
    
    def save_ta3lim(self, *a):
        if self.view_poem_bfr.get_has_selection():
            sel = self.view_poem_bfr.get_selection_bounds()
            sel_text = self.view_poem_bfr.get_text(sel[0], sel[1],True)
            text = daw_tools.one_half(sel_text.decode('utf8'))
            list_marks = eval(daw_config.getv('marks'))
            list_marks.append([self.id_poem, text])
            marks = repr(list_marks)
            daw_config.setv('marks', marks)
            daw_customs.info(self.parent, u'تم تعليم الموضع')
        else:
            daw_customs.erro(self.parent, u'حدد شطرا واحدا من البيت الذي تريد الرجوع إليه')
            
    def save_abiaty(self, *a):
        if self.view_poem_bfr.get_has_selection():
            sel = self.view_poem_bfr.get_selection_bounds()
            v1 = sel[0].get_line() 
            v2 = sel[1].get_line()
            abiaty = daw_tools.get_abiat(self.text_poem, v1, v2, self.t)
            if abiaty == None: return daw_customs.erro(self.parent, u'لا يمكن إضافة هذه الأبيات إلى المفضلة')
            id_verse = self.parent.db.to_abiaty(self.id_poem, abiaty)
            if id_verse > 0:
                daw_customs.info(self.parent, u'تم إضافة هذا البيت للأبيات المفضلة')
                n = self.parent.main_notebook.get_n_pages()
                for s in range(n):
                    ch = self.parent.main_notebook.get_nth_page(s)
                    if self.parent.main_notebook.get_tab_label_text(ch) == 'أبياتي':
                        ch.pages()
                        return
        else:
            daw_customs.erro(self.parent, u'''
            حدد البيت أو الأبيات التي تريد 
            إضافتها إلى أبياتك المفضلة
            ''')
        
    def scan_verse(self, *a):
        if self.view_poem_bfr.get_has_selection():
            sel = self.view_poem_bfr.get_selection_bounds()
            v1 = sel[0].get_line() 
            v2 = v1
            verse = daw_tools.get_abiat(self.text_poem, v1, v2, self.t)
            if verse == None: return daw_customs.erro(self.parent, u'لا يمكن تقطيع هذا البيت')
            self.parent.main_notebook.set_current_page(8)
            self.parent.wazn_page.set_active(True)
            n = self.parent.main_notebook.get_current_page()
            ch = self.parent.main_notebook.get_nth_page(n)
            ch.set_current_page(0)
            txt = verse.replace(u'*', u'     ')
            ch.verse_dictation_bfr.set_text(txt.strip())
            ch.view_scan_bfr.set_text('')
        else:
            daw_customs.erro(self.parent, u'''
            حدد البيت أو الأبيات التي تريد 
            إضافتها إلى أبياتك المفضلة
            ''')
        
    def save_tafdil(self, *a):
        check = self.parent.db.to_favorite(self.id_poem)
        self.parent.favorite.store()
        if check == None:
            daw_customs.info(self.parent, u'تم إضافة هذه القصيدة للمفضلة')
    
    def explain_term(self, *a):
        if self.view_poem_bfr.get_has_selection():
            sel = self.view_poem_bfr.get_selection_bounds()
            sel_text = self.view_poem_bfr.get_text(sel[0], sel[1],True)
            text = daw_araby.stripTatweel(sel_text.decode('utf8'))
            text = daw_tools.first_term(text)
            if len(text) >= 3:
                all_root, all_term = daw_stemming.get_root(u''+text)
                if len(all_root['taje'])+len(all_root['assas'])+len(all_root['lisan'])+len(all_root['mekhtar']) == 0:
                    daw_customs.erro(self.parent, 'لا يوجد نتيجة'); return
                self.parent.dictpage.tree_dict.collapse_all()
                self.parent.dictpage.store_dict.clear()
                self.parent.dictpage.view_dict_bfr.set_text('')
                if len(all_root['taje'])+len(all_root['assas'])+len(all_root['lisan'])+len(all_root['mekhtar']) == 0:
                        daw_customs.erro(self.parent, 'لا يوجد نتيجة'); return
                if len(all_root['lisan']) != 0: 
                    a1 = self.parent.dictpage.store_dict.append(None, ['لسان العرب', 'lisan'])
                    for text in all_root['lisan']:
                        self.parent.dictpage.store_dict.append(a1, [text, 'lisan'])
                if len(all_root['taje']) != 0: 
                    a2 = self.parent.dictpage.store_dict.append(None, ['تاج العروس', 'taje'])
                    for text in all_root['taje']:
                        self.parent.dictpage.store_dict.append(a2, [text, 'taje'])
                if len(all_root['assas']) != 0: 
                    a3 = self.parent.dictpage.store_dict.append(None, ['أساس البلاغة', 'assas'])
                    for text in all_root['assas']:
                        self.parent.dictpage.store_dict.append(a3, [text, 'assas'])
                if len(all_root['mekhtar']) != 0: 
                    a4 = self.parent.dictpage.store_dict.append(None, ['مختار الصحاح', 'mekhtar'])
                    for text in all_root['mekhtar']:
                        self.parent.dictpage.store_dict.append(a4, [text, 'mekhtar'])
                self.parent.dictpage.all_term = all_term
                self.parent.main_notebook.set_current_page(7)
                self.parent.dicty_page.set_active(True)
    
            
    def export_pdf(self, *a):
        myexpoty = Exporter(self.parent, self.parent.db.name_poem(self.id_poem), 
                            self.lakab_poet, self.new_poem, self.new_font)
        myexpoty.export_html()
        
    def export_odt(self, *a):
        myexpoty = Exporter(self.parent, self.parent.db.name_poem(self.id_poem), 
                            self.lakab_poet, self.new_poem, self.new_font)
        myexpoty.export_html()
        
    def export_html(self, *a):
        myexpoty = Exporter(self.parent, self.parent.db.name_poem(self.id_poem), 
                            self.lakab_poet, self.new_poem, self.new_font)
        myexpoty.export_html()
        
    def export_text(self, *a):
        myexpoty = Exporter(self.parent, self.parent.db.name_poem(self.id_poem), 
                            self.lakab_poet, self.new_poem, self.new_font)
        myexpoty.export_txt()
    
    def set_recite(self, *a):
        open_dlg = Gtk.FileChooserDialog("أضف ملفا صوتيا للقصيدة", self.parent,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        Filter = Gtk.FileFilter()
        Filter.set_name("ملفات OGG")
        Filter.add_pattern("*.[Oo][Gg][Gg]")
        open_dlg.add_filter(Filter)
        
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            old_file = open_dlg.get_filename()
            old_name = basename(old_file)
            new_name = u'00'+str(self.id_poem)+u'.ogg'
            new_file = join(daw_customs.AUDIO_DIR, new_name)
            if new_file == old_file:
                daw_customs.erro(self.parent, u'الملف موجود بالفعل لايمكنك استيراده') 
            else:
                ent_dlg = Gtk.Dialog("أدخل اسم الملقي", open_dlg, Gtk.DialogFlags.MODAL)
                entry = Gtk.Entry()
                entry.show()
                btn = daw_customs.ButtonClass('نعم')
                btn.show()
                ent_dlg.add_action_widget(entry, 0)
                ent_dlg.add_action_widget(btn, 1)
                res_ent = ent_dlg.run()
                if res_ent == 1:
                    reciter = entry.get_text().decode('utf8')
                    ent_dlg.destroy()
                    if exists(new_file):
                        replace = u'واستبداله بالملف القديم'
                    else:
                        replace = u''
                    msg = daw_customs.sure(self.parent, u'''
                    سوف يقوم البرنامج بنسخ الملف {} 
                    إلى المجلد {}
                    بعد تسميته بـ {}
                    {} 
                    ''' .format(
                    old_name, 
                    daw_customs.AUDIO_DIR, 
                    new_name, 
                    replace))
                    if msg == Gtk.ResponseType.YES:
                        copyfile(old_file, new_file)
                        check = self.parent.db.set_recite(self.id_poem, reciter)
                        self.parent.recite.store()
                        if check == None: daw_customs.info(self.parent, 'تم إضافة ملف صوتي لهذه القصيدة') 
                        open_dlg.destroy()
                else:
                    ent_dlg.destroy()
        open_dlg.destroy()
    
    def print_poem(self, *a):
        myexpoty = Exporter(self.parent, self.parent.db.name_poem(self.id_poem), 
                            self.lakab_poet, self.new_poem, self.new_font)
        myexpoty.print_pdf("execute_script", 'window.print();')
        print 'طباعة الصفحة'
     
    def __init__(self, parent):
        self.ACCEL_CTRL_KEY, self.ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
        self.ACCEL_SHFT_KEY, self.ACCEL_SHFT_MOD = Gtk.accelerator_parse("<Shift>")
        self.parent = parent
        self.t = 1
        self.long_verse = None
        self.long_tatwil = None
        self.long_space = None
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        Gtk.Box.__init__(self,spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.vp = Gtk.VPaned()
        self.view_poem = daw_customs.ViewPoem()
        self.view_poem.set_justification(Gtk.Justification.CENTER)
        self.view_poem.set_cursor_visible(False)
        self.view_poem.set_editable(False)
        self.view_poem.set_right_margin(10)
        self.view_poem.set_left_margin(10)
        self.view_poem_bfr = self.view_poem.get_buffer()
        self.speaker_poem_tag = self.view_poem_bfr.create_tag("speaker")
        self.search_poem_tag = self.view_poem_bfr.create_tag("search")
        scroll = daw_customs.ScrollClass()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_poem)
        self.vp.pack1(scroll, False, False)
        
        self.vbox_charh = Gtk.VBox(False, 0)
        self.lab_charh = Gtk.Label()
        self.close_charh = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'tab.png'),
                                                "إخفاء", lambda *a: self.vbox_charh.hide())
        self.save_charh = Gtk.Button("حفظ")
        self.save_charh.connect("clicked", self.save_ta3lik)
        hb = Gtk.HBox(False,7)
        hb.set_border_width(7)
        hb.pack_start(self.lab_charh, False, False, 0)
        hb.pack_end(self.close_charh, False, False, 0)
        hb.pack_end(self.save_charh, False, False, 0)
        self.view_charh = daw_customs.ViewEdit()
        self.view_charh.set_right_margin(5)
        self.view_charh.set_left_margin(5)
        self.view_charh.set_cursor_visible(False)
        self.view_charh.set_editable(False)
        self.view_charh_bfr = self.view_charh.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_charh)
        scroll.set_size_request(-1, 200)
        self.vbox_charh.pack_start(hb, False, False, 0)
        self.vbox_charh.pack_start(scroll, True, True, 0)
        self.pack_start(self.vp, True, True, 0)
        self.change_font()
        
    def loading(self, id_poem, font='Simplified Naskh 18'):
        self.view_poem.connect_after("populate-popup", self.populate_popup)
        id_poet = self.parent.db.id_poet(id_poem)
        self.list_id_poem = self.parent.db.poems_id(id_poet)
        self.id_poem = id_poem
        self.text_poem, self.text_sabab, self.text_charh, self.text_ta3lik = self.parent.db.get_poem(id_poem)
        if self.text_charh == u'': self.text_charh = u'لا يوجد شرح لهذه القصيدة'
        self.length = self.parent.db.length_poem(id_poem)
        self.naw3 = self.parent.db.naw3_poem(id_poem)
        self.a3aridh = self.parent.db.arodh_poem(id_poem)
        self.new_poem = self.text_poem
        id_poet = self.parent.db.id_poet(id_poem)
        self.name_poet, self.lakab_poet = self.parent.db.name_poet(id_poet)
        self.speaker = self.lakab_poet+u' :\n'
        self.text_nabdha = self.get_nabdha(id_poem)
        self.build(font)
        self.nm_poet = self.lakab_poet
        self.nm_poem = self.parent.db.name_poem(id_poem)
        self.axl = Gtk.AccelGroup()
        self.parent.add_accel_group(self.axl)
        self.axl.connect(Gdk.KEY_D, self.ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.explain_term)
        self.axl.connect(Gdk.KEY_F2, 0, Gtk.AccelFlags.VISIBLE, self.show_nabdha)
        self.axl.connect(Gdk.KEY_F3, 0, Gtk.AccelFlags.VISIBLE, self.show_ta3lik)
        self.axl.connect(Gdk.KEY_F4, 0, Gtk.AccelFlags.VISIBLE, self.show_charh)
        self.axl.connect(Gdk.KEY_Escape, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.vbox_charh.hide())
        
    def build(self, font='Simplified Naskh 18'):
        size = self.parent.get_size()
        self.width_window = size[0]-240
        if self.view_poem.get_allocated_width() > 100:
            self.width_window = self.view_poem.get_allocated_width()
        b_a = daw_config.getn('b_abiat')*2
        self.font = font
        self.size_font = int(self.font[-2:])
        label = Gtk.Label()
        label.override_font(Pango.FontDescription(self.font))
        if self.naw3 != 5: 
            if daw_tools.is_machtor(self.text_poem): arodh = 1
            else: arodh = 0
            self.new_poem, self.t = daw_tools.length_Half(self.text_poem, label, self.length, self.size_font, self.width_window, arodh)
        poem = self.new_poem
        poem = self.speaker+poem
        self.view_poem_bfr.set_text(poem)
        daw_customs.with_tag(self.view_poem_bfr, self.speaker_poem_tag, [self.speaker,])
        self.view_poem.override_font(Pango.FontDescription(self.font))
        self.view_poem.set_pixels_below_lines((self.size_font*b_a)/3)
        self.view_poem.set_pixels_above_lines((self.size_font*b_a)/3)