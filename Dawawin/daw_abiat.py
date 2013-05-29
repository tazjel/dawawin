# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join
from gi.repository import Gtk, Pango
from daw_viewer import ShowPoem
from daw_tablabel import TabLabel
import daw_tools, daw_customs, daw_araby


# class صفحة أبياتي المفضلة----------------------------------------------------

class MyAbiat(Gtk.HBox):
    
    def change_font(self, *a):
        self.search_poem_tag.set_property('foreground', self.parent.theme.colortp)
        self.search_poem_tag.set_property('background', self.parent.theme.colorss)
        self.new_font = self.parent.theme.fontmp
    
    
    def rm_bayt(self, btn, *a):
        id_verse = int(btn.get_name())
        msg = daw_customs.sure(self.parent, '''
            هل أنت متأكد من أنك 
            تريد حذف هذا الموضع ؟
            ''' )
        if msg == Gtk.ResponseType.YES:
            self.parent.db.del_abiat(id_verse)
            de = self.btns_pages.get_children()
            ch = de[2].get_children()
            for a in ch:
                if a.get_active():
                    self.select_page(a)
    
    def to_poet(self, btn, *a):
        nm_poet = btn.get_name()
        if nm_poet == u'أحدهم': return
        self.parent.set_title("دواوين العرب - الدواوين ")
        self.parent.main_notebook.set_current_page(1)
        self.parent.dawawin_page.set_active(True)
        self.parent.dawawinpage.search_poets.set_text(nm_poet)
        self.parent.dawawinpage.show_all()
        self.parent.dawawinpage.notebook.set_current_page(0)
        self.parent.dawawinpage.sel_poet.select_path((0,))
        self.parent.dawawinpage.ok_poet()
        self.parent.dawawinpage.search_poets.set_text('')
            
    def to_poem(self, btn, *a):
        id_poem = int(btn.get_name())
        nm_poem = self.parent.db.name_poem(id_poem)
        self.parent.set_title("دواوين العرب - القصائد")
        self.parent.main_notebook.set_current_page(2)
        self.parent.poems_page.set_sensitive(True)
        self.parent.poems_page.set_active(True)
        n = self.parent.viewerpoem.get_n_pages()
        for s in range(n):
            ch = self.parent.viewerpoem.get_nth_page(s)
            if self.parent.viewerpoem.get_tab_label(ch).nm == nm_poem:
                self.parent.viewerpoem.set_current_page(s)
                return
        sr = ShowPoem(self.parent)
        sr.loading(id_poem, self.parent.theme.fontmp)
        self.parent.viewerpoem.append_page(sr,TabLabel(sr, nm_poem))
        self.parent.viewerpoem.show_all()
        self.parent.viewerpoem.set_current_page(-1)
    
    def show_page(self, new_font=None):
        lst_abiat = []
        if new_font == None:
            new_font = self.new_font
        text_page = u''
        self.view_abiat_bfr.set_text('')
        self.view_abiat.override_font(Pango.FontDescription(self.new_font))
        for s in self.list_abiat:
            lst_abiat.append(s) 
        lst_abiat.reverse()
        for a in lst_abiat:
            id_poem, abiat = self.parent.db.get_abiat(a)
            try: id_poet = self.parent.db.id_poet(id_poem)
            except: id_poet = 0
            name_poet, lakab_poet = self.parent.db.name_poet(id_poet)
            speaker = lakab_poet
            
            itr = self.view_abiat_bfr.get_iter_at_offset(0)
            anchor = self.view_abiat_bfr.create_child_anchor(itr)
            if (anchor and not anchor.get_deleted()):
                box = Gtk.HBox(False, 0)
                img1 = Gtk.Image()
                img1.set_from_file(join(daw_customs.ICON_DIR, 'clear.png'))
                widget1 = Gtk.Button()
                widget1.set_image(img1)
                widget1.connect('clicked', self.rm_bayt)
                widget1.set_tooltip_text('احذف من المفضلة')
                widget1.set_name(str(a))
                img2 = Gtk.Image()
                img2.set_from_file(join(daw_customs.ICON_DIR, 'to_poem.png'))
                widget2 = Gtk.Button()
                widget2.set_image(img2)
                widget2.connect('clicked', self.to_poem)
                widget2.set_tooltip_text('اعرض القصيدة الأصلية')
                widget2.set_name(str(id_poem))
                widget3 = daw_customs.ButtonClass(speaker)
                widget3.connect('clicked', self.to_poet)
                widget3.set_name(speaker)
                box.pack_start(widget1, False, False, 0)
                box.pack_start(widget2, False, False, 0)
                box.pack_start(widget3, False, False, 0)
                self.view_abiat.add_child_at_anchor(box, anchor)
                box.show_all()
                
            size = self.parent.get_size()
            self.width_window = size[0]-240
            if self.view_abiat.get_allocated_width() > 100:
                self.width_window = self.view_abiat.get_allocated_width()
            size_font = int(new_font[-2:])
            label = Gtk.Label()
            label.override_font(Pango.FontDescription(new_font))
            length, n_abiat = daw_tools.longer_half(abiat, label, 0)
            r_abiat, t = daw_tools.length_Half(abiat, label, length, size_font, self.width_window, 0)
            text_page = u'\n'+r_abiat+'\n'
            itr = self.view_abiat_bfr.get_iter_at_offset(1)
            self.view_abiat_bfr.insert(itr, text_page, -1)
    
    def select_page(self, btn):
        self.list_abiat = []
        n = int(btn.get_name())
        abiat = self.parent.db.abiaty_pages()
        if (n+1)*10 < len(abiat): v = (n+1)*10
        else: v = len(abiat)
        for a in range(n*10, v):
            self.list_abiat.append(abiat[a][0])
        self.show_page(self.new_font)
    
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
                self.hb_btn.pack_start(btn, False, False, 0)
                self.list_btn.append(btn)
        self.btns_pages.show_all()
    
    def pages(self, *a):
        abiat = self.parent.db.abiaty_pages()
        de = self.btns_pages.get_children()
        for a in de:
            self.btns_pages.remove(a)
        self.r = 1
        if len(abiat) == 0: v = 0
        else: v = (len(abiat)-1)/10+1
        self.n_pages = v
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
    
    def search_and_mark2(self, text, start):
        end = self.view_abiat_bfr.get_end_iter()
        match = start.forward_search(text, 0, end)
        if match != None:
            match_start, match_end = match
            self.view_abiat_bfr.apply_tag(self.search_poem_tag, match_start, match_end)
            self.search_and_mark2(text, match_end)
            if match_start and (not self.i_min or self.i_min.compare(match_start) > 0): 
                self.i_min = match_start
            if self.i_min:
                self.view_abiat.scroll_to_iter(self.i_min, 0.0, True, 0.5, 0.5)
                
    def mark_on_poem(self, text, cursive=False): 
        self.i_min = None
        text = daw_araby.fuzzy(text)
        ls = text.split()
        ln = len(ls)
        list_search = []
        text_page0 = self.view_abiat_bfr.get_text(self.view_abiat_bfr.get_start_iter(),
                                        self.view_abiat_bfr.get_end_iter(), False).decode('utf8')
        self.text_page = daw_araby.stripTatweel(text_page0)
        ls_poem, nw = daw_tools.n_words(self.text_page)
        list_word = text_page0.split()
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
            cursor_mark = self.view_abiat_bfr.get_insert()
            start = self.view_abiat_bfr.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.view_abiat_bfr.get_char_count():
                start = self.view_abiat_bfr.get_start_iter()
                self.search_and_mark2(txt, start)
    
    def search_on_page(self, text): 
        self.i_min = None      
        self.show_page(self.new_font)
        if len(text) > 0:
            self.mark_on_poem(text, False) 
    
    def near_page(self, v):
        font = self.new_font[:-2]
        sz = int(self.new_font[-2:])
        new_sz = sz+v
        if new_sz < 10: return
        self.new_font = font+str(new_sz)
        self.show_page(self.new_font)
    
    def move_in_page(self, v):
        return
    
    def __init__(self, parent):
        self.parent = parent
        self.list_abiat = []
        self.new_font = self.parent.theme.fontmp
        Gtk.HBox.__init__(self, False, 6)
        vbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        self.vbox1= Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        
        self.btns_pages = Gtk.HBox(False, 3)
        self.btns_pages.set_border_width(2)
        self.vbox1.pack_start(self.btns_pages, False, False, 0)
        
        self.view_abiat = daw_customs.ViewPoem()
        self.view_abiat.set_justification(Gtk.Justification.CENTER)
        self.view_abiat_bfr = self.view_abiat.get_buffer()
        self.title_tag = self.view_abiat_bfr.create_tag("title")
        self.search_poem_tag = self.view_abiat_bfr.create_tag("search")
        scroll = daw_customs.ScrollClass()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_abiat)
        self.vbox1.pack_start(scroll, True, True, 0)
        
        self.pack_start(vbox, False, False, 0)
        self.pack_start(self.vbox1, True, True, 0)
        self.pages()
        self.show_all()
        self.change_font()