# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

#a ماذا سأفعل؟
#a تصدير القصائد بصيغة pdf odt
#a خاصية البحث في نفس البيت

import daw_customs
if daw_customs.my_return == 0: quit()
from os.path import join
from gi.repository import Gtk, Gdk
from daw_contacts import MyDB
from daw_dawawin import DawawinPage
from daw_recite import RecitePoem
from daw_favorite import FavoritePoem
from daw_viewer import ViewerPoem
from daw_abiat import MyAbiat
from daw_halp import Halper
from daw_filter import FilterPoem
from daw_share import ImportExport
from daw_add import AddPoem
from daw_organize import Organize
from daw_preference import Preference
from daw_search import Searcher, ResultSearch
from daw_dict import Explanatory
from daw_fun import MyFun
from daw_metrics import Metrics
from daw_about import About
from daw_marks import SavedMarks
from daw_result import SavedResult
from daw_theme import MyTheme
from daw_face import MyFace
from daw_count import Count


Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
ACCEL_SHFT_KEY, ACCEL_SHFT_MOD = Gtk.accelerator_parse("<Shift>")
     
# class الرئيس--------------------------------------------------------
        
class DwawinApp(Gtk.Window):
            
    def quit_app(self,*args):
        Gtk.main_quit()       
    
    def refrech(self, *a):
        n = self.main_notebook.get_n_pages()
        r = 0
        while r in range(n):
            ch = self.main_notebook.get_nth_page(r)
            try:
                ch.iv.change_font()
                ch.iv.loading(ch.iv.id_poem, self.theme.fontmp)
            except: pass
            try:
                n2 = ch.get_n_pages()
                r2 = 0
                while r2 in range(n2):
                    ch2 = ch.get_nth_page(r2)
                    ch2.change_font()
                    ch2.loading(ch2.id_poem, self.theme.fontmp)
                    r2 += 1
            except: pass
            try:
                ch.change_font()
                ch.show_page(ch.tree_abiaty, ch.new_font)
            except: pass
            try:
                ch.change_font()
            except: pass
            r += 1
    
    def search_on_page(self, *a):
        text = self.entry_search.get_text().decode('utf8') 
        n = self.main_notebook.get_current_page()
        ch = self.main_notebook.get_nth_page(n)
        ch.search_on_page(text)
        
    def near_page(self, v):
        n = self.main_notebook.get_current_page()
        ch = self.main_notebook.get_nth_page(n)
        ch.near_page(v)
        
    def move_in_page(self, v):
        n = self.main_notebook.get_current_page()
        ch = self.main_notebook.get_nth_page(n)
        ch.move_in_page(v)
            
    def show_win_searh(self, *a):
        self.search_win.show_all()
    
    def hide_btns(self, *a):
        if self.vbox.get_visible():
            self.vbox.hide()
        else:
            self.vbox.show_all()
            
    def full_screen(self, *a):
        if self.full == 1:
            self.unfullscreen()
            self.full = 0
        else:
            self.fullscreen()
            self.full = 1
    
    def show_page(self, btn, title, n_page):
        if btn == None:
            self.detoggled.set_active(False);
            self.main_notebook.set_current_page(n_page)
            self.set_title("دواوين العرب - {}    ({})".format(title,daw_customs.version))
            self.detoggled = Gtk.ToggleButton("")
            return
        if btn.get_active():
            self.detoggled.set_active(False);self.detoggled = btn
            self.set_title("دواوين العرب - {}    ({})".format(title,daw_customs.version))
            self.main_notebook.set_current_page(n_page)
        else:
            self.main_notebook.set_current_page(0)
            self.set_title("دواوين العرب  ({})".format(daw_customs.version,))
            self.detoggled = Gtk.ToggleButton("")
        
    def __init__(self,*a):
        self.full = 0
        self.theme = MyTheme()
        self.db = MyDB()
        Gtk.Window.__init__(self)
        self.axl = Gtk.AccelGroup()
        self.add_accel_group(self.axl)
        self.store = Gtk.TreeStore(int, int, str)
        self.dawawinpage = DawawinPage(self)
        self.viewerpoem = ViewerPoem(self)
        self.favorite = FavoritePoem(self)
        self.recite = RecitePoem(self)
        self.search_win = Searcher(self)
        self.preference_win = Preference(self)
        self.resultsearch = ResultSearch(self)
        self.countpage = Count(self)
        self.dictpage = Explanatory(self)
        self.organizepage = Organize(self)
        self.build()

# a البناء-------------------------------------------------------------------- 
    
    def build(self,*a):
        self.detoggled = Gtk.ToggleButton("")
        self.set_title("دواوين العرب  ({})".format(daw_customs.version,))
        self.set_icon_name('dawawin')
        self.maximize()
        self.connect("delete_event", self.quit_app)
        self.connect("destroy", self.quit_app)
        self.agr = Gtk.AccelGroup()
        self.add_accel_group(self.agr)
        #self.set_size_request(900,600)
        self.box = Gtk.Box(spacing=0, orientation=Gtk.Orientation.VERTICAL)
        self.hbox = Gtk.Box(spacing=7, orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_border_width(7)
        self.hb = Gtk.Box(spacing=7, orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        self.vbox.set_size_request(150, -1)
        
        img = Gtk.Image()
        self.img_item = Gtk.ToolItem.new()
        self.img_item.add(img)
        self.img_item.set_size_request(160, -1)
        img.set_from_file(join(daw_customs.ICON_DIR, 'title.png'))
        
        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        self.toolbar.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)

        self.box.pack_start(self.toolbar, False, False, 0)
        
        self.toolbar.insert(self.img_item, 0)
        
        self.prev = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'prev.png'), 'السابق\nاستعمل التحكم والسهم الأيمن', lambda *a: self.move_in_page(-1))
        self.toolbar.insert(self.prev, 1)
        self.prev.add_accelerator("clicked",self.axl, Gdk.KEY_Right, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        
        self.next = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'next.png'), 'التالي\nاستعمل التحكم والسهم الأيسر', lambda *a: self.move_in_page(1))
        self.toolbar.insert(self.next, 2)
        self.next.add_accelerator("clicked",self.axl, Gdk.KEY_Left, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 3)
        
        self.near = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'near.png'), 'كبّر الخط\nاستعمل التحكم وعلامة الجمع', lambda *a: self.near_page(1))
        self.toolbar.insert(self.near, 4)
        self.near.add_accelerator("clicked",self.axl,Gdk.KEY_equal, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        self.near.add_accelerator("clicked",self.axl,Gdk.KEY_plus, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        self.near.add_accelerator("clicked",self.axl,Gdk.KEY_KP_Add, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        
        self.far = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'far.png'), 'صغّر الخط\nاستعمل التحكم وعلامة الطرح', lambda *a: self.near_page(-1))
        self.toolbar.insert(self.far, 5)
        self.far.add_accelerator("clicked",self.axl,Gdk.KEY_minus, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        self.far.add_accelerator("clicked",self.axl,Gdk.KEY_KP_Subtract, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 6)
        
        try: self.entry_search = Gtk.SearchEntry()
        except: self.entry_search = Gtk.Entry()
        self.entry_search.set_placeholder_text('بحث ضبابي')
        self.entry_search_item = Gtk.ToolItem.new()
        self.entry_search_item.add(self.entry_search)
        self.entry_search.connect('changed', self.search_on_page)
        self.entry_search.connect('activate', self.search_on_page)
        self.toolbar.insert(self.entry_search_item, 7)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 8)
        
        self.mark = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'marks.png'), 'تصفح المواضع المحفوظة', lambda *a: SavedMarks(self))
        self.toolbar.insert(self.mark, 9)
        
        self.save_result = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'save_result.png'), 'نتائج البحث المحفوظة', lambda *a: SavedResult(self))
        self.toolbar.insert(self.save_result, 10)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 11)
        
        self.search = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'search.png'), 'نافذة البحث', self.show_win_searh)
        self.toolbar.insert(self.search, 12)
        
        self.pref = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'pref.png'), 'تفضيلات', 
                                     lambda *a: self.preference_win.show_all())
        self.toolbar.insert(self.pref, 13)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 14)
        
        self.about = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'about.png'), 'لمحة عن البرنامج', lambda *a: About(self))
        self.toolbar.insert(self.about, 15)
        
        self.toolbar.insert(Gtk.SeparatorToolItem(), 16)
        
        self.close = daw_customs.tool_button(join(daw_customs.ICON_DIR, 'close.png'), 'إغلاق البرنامج', self.quit_app)
        self.toolbar.insert(self.close, 17)
        
        self.dawawin_page = daw_customs.ToggleButtonClass('الدواوين')
        self.vbox.pack_start(self.dawawin_page, True, True, 0)
        self.dawawin_page.connect("toggled", self.show_page, "الدواوين",1)
        
        self.poems_page = daw_customs.ToggleButtonClass('القصائد')
        self.vbox.pack_start(self.poems_page, True, True, 0)
        self.poems_page.connect("toggled", self.show_page, "القصائد", 2)
        self.poems_page.set_sensitive(False)
        
        self.filter_page = daw_customs.ToggleButtonClass('التصفية')
        self.vbox.pack_start(self.filter_page, True, True, 0)
        self.filter_page.connect("toggled", self.show_page, "التصفية", 3)
        
        self.fav_page = daw_customs.ToggleButtonClass('المفضلة')
        self.vbox.pack_start(self.fav_page, True, True, 0)
        self.fav_page.connect("toggled", self.show_page, "المفضلة", 4)
        
        self.abiaty_page = daw_customs.ToggleButtonClass('أبياتي')
        self.vbox.pack_start(self.abiaty_page, True, True, 0)
        self.abiaty_page.connect("toggled", self.show_page, "أجمل الأبيات", 5)
        
        self.recite_page = daw_customs.ToggleButtonClass('التسجيلات')
        self.vbox.pack_start(self.recite_page, True, True, 0)
        self.recite_page.connect("toggled", self.show_page, "التسجيلات", 6)
        
        self.dicty_page = daw_customs.ToggleButtonClass('المعاجم')
        self.vbox.pack_start(self.dicty_page, True, True, 0)
        self.dicty_page.connect("toggled", self.show_page, "المعجم", 7)
        
        self.wazn_page = daw_customs.ToggleButtonClass('العَروض')
        self.vbox.pack_start(self.wazn_page, True, True, 0)
        self.wazn_page.connect("toggled", self.show_page, "العروض", 8)
        
        self.fun_page = daw_customs.ToggleButtonClass('التسلية')
        self.vbox.pack_start(self.fun_page, True, True, 0)
        self.fun_page.connect("toggled", self.show_page, "التسلية",9)
        
        self.search_result_page = daw_customs.ToggleButtonClass('البحوث')
        self.vbox.pack_start(self.search_result_page, True, True, 0)
        self.search_result_page.connect("toggled", self.show_page, "نتائج البحث", 10)
        self.search_result_page.set_sensitive(False)
        
        self.reg_page = daw_customs.ToggleButtonClass('التعديل')
        self.vbox.pack_start(self.reg_page, True, True, 0)
        self.reg_page.connect("toggled", self.show_page, "التعديل",11)
        
        self.addpoem_page = daw_customs.ToggleButtonClass('الإضافة')
        self.vbox.pack_start(self.addpoem_page, True, True, 0)
        self.addpoem_page.connect("toggled", self.show_page, "إضافة قصيدة", 12)
        
        self.in_out_page = daw_customs.ToggleButtonClass('المشاركة')
        self.vbox.pack_start(self.in_out_page, True, True, 0)
        self.in_out_page.connect("toggled", self.show_page, "استيراد وتصدير", 13)
        
        self.help_page = daw_customs.ToggleButtonClass('المساعدة')
        self.vbox.pack_start(self.help_page, True, True, 0)
        self.help_page.connect("toggled", self.show_page, "المساعدة", 14)
        
        self.main_notebook = Gtk.Notebook()
        self.box.pack_start(self.hbox, True, True, 0)
        self.hbox.pack_start(self.vbox, False, False, 0)
        self.hbox.pack_start(self.main_notebook, True, True, 0)
        self.main_notebook.set_scrollable(True)
        self.main_notebook.set_show_tabs(False)
        
        self.main_notebook.append_page(MyFace(self), Gtk.Label("الواجهة"))
        self.main_notebook.append_page(self.dawawinpage,Gtk.Label("دواوين"))
        self.main_notebook.append_page(self.viewerpoem, Gtk.Label("قصائد"))
        self.main_notebook.append_page(FilterPoem(self), Gtk.Label('صفحة التصفية'))
        self.main_notebook.append_page(self.favorite, Gtk.Label('المفضلة'))
        self.main_notebook.append_page(MyAbiat(self), Gtk.Label('أبياتي'))
        self.main_notebook.append_page(self.recite, Gtk.Label('التسجيلات'))
        self.main_notebook.append_page(self.dictpage, Gtk.Label('المعجم'))
        self.main_notebook.append_page(Metrics(self), Gtk.Label('صفحة العروض'))
        self.main_notebook.append_page(MyFun(self), Gtk.Label('التسلية'))
        self.main_notebook.append_page(self.resultsearch, Gtk.Label('نتائج البحث'))
        self.main_notebook.append_page(self.organizepage, Gtk.Label('صفحة التعديل'))
        self.main_notebook.append_page(AddPoem(self), Gtk.Label('إضافة قصيدة'))
        self.main_notebook.append_page(ImportExport(self), Gtk.Label('استيراد'))
        self.main_notebook.append_page(Halper(self), Gtk.Label('صفحة المساعدة'))
        self.main_notebook.append_page(self.countpage, Gtk.Label('صفحة الإحصاء'))
        
        self.axl.connect(Gdk.KEY_F1, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.help_page.set_active(True))
        self.axl.connect(Gdk.KEY_F9, 0, Gtk.AccelFlags.VISIBLE, self.hide_btns)
        self.axl.connect(Gdk.KEY_F11, 0, Gtk.AccelFlags.VISIBLE, self.full_screen)
        self.axl.connect(Gdk.KEY_F5, 0, Gtk.AccelFlags.VISIBLE, self.refrech)
        self.axl.connect(Gdk.KEY_F6, 0, Gtk.AccelFlags.VISIBLE, self.show_win_searh)
        self.axl.connect(Gdk.KEY_F8, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.preference_win.show_all())
        
        self.add(self.box)
        self.vbox.show_all()
        self.toolbar.show_all()
        self.main_notebook.show()
        self.hbox.show()
        self.box.show()
        self.show()
        daw_customs.greet.destroy()
#----------------------------------------------------

Dwa = DwawinApp()
def main(): 
    Gtk.main()

if __name__ == "__main__":
    main()
