# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, dirname, realpath, exists, expanduser
from gi.repository import Gtk, Gdk, Pango
import daw_config, daw_araby
from os import mkdir
import sqlite3

Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)

#a------------------------------------------
version = '0.1.20'
my_return = 1

#a--------------------------------------------------
APP_DIR      = dirname(dirname(realpath(__file__)))
HOME_DIR     = expanduser('~/.dawawin')
if exists('/usr/share/dawawin/dawawin-data/icons/logo.png'):
    DATA_DIR = '/usr/share/dawawin/dawawin-data'
elif exists('/usr/local/share/dawawin/dawawin-data/icons/logo.png'):
    DATA_DIR = '/usr/local/share/dawawin/dawawin-data'
else: 
    DATA_DIR = join(APP_DIR, 'dawawin-data')
ICON_DIR     = join(DATA_DIR, 'icons')
MY_HELP      = join(DATA_DIR, 'Help.db')

#a------------------------------------------
def sure_start(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
    dlg.set_markup(msg)
    db_void = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/dawawin/files/DawawinArab.tar.gz/download",
                                                'تنزيل قاعدة البيانات المفرغة')
    area = dlg.get_content_area()
    area.set_spacing(6)
    hbox = Gtk.HBox(False, 0)
    hbox.pack_end(db_void, False, False, 0)
    area.pack_start(hbox, False, False, 0)
    area.show_all()
    r = dlg.run()
    dlg.destroy()
    return r

#a------------------------------------------------
def change_path_db():
        open_dlg = Gtk.FileChooserDialog(u'تحديد مسار قاعدة البيانات',
                                         None, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        Filter = Gtk.FileFilter()
        Filter.set_name(u"قاعدة البيانات")
        Filter.add_pattern("Dawawin.db")
        open_dlg.add_filter(Filter)
        
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            daw_config.setv('path', open_dlg.get_filenames()[0])          
            open_dlg.destroy()
        else:
            open_dlg.destroy()
            quit()

#a------------------------------------------
if not exists(daw_config.getv('path')): 
    res = sure_start(None, '''
    لم يتمكن البرنامج من الاتصال بقاعدة البيانات،
    إذا كنت قد نزلتها بالفعل فربما لم تربطها بالبرنامج، 
    أو قد يكون القرص الموجود عليه القاعدة غير مضموم،
    هل تريد تحديد مسار قاعدة البيانات ؟''')
    if res == Gtk.ResponseType.YES:
        change_path_db()
        MY_DATA = daw_config.getv('path')
        MY_DIR = dirname(MY_DATA)
        MY_DICT = join(MY_DIR, 'Dict.db')
        MY_AWZAN = join(MY_DIR, 'Awzan.db')
        AUDIO_DIR = join(MY_DIR, 'Audio')
        ORNAMENT = join(MY_DIR, 'Ornament')
    elif res == Gtk.ResponseType.NO:
        my_return = 0
        quit()
else:
    MY_DATA = daw_config.getv('path')
    MY_DIR = dirname(MY_DATA)
    MY_DICT = join(MY_DIR, 'Dict.db')
    MY_AWZAN = join(MY_DIR, 'Awzan.db')
    AUDIO_DIR = join(MY_DIR, 'Audio')
    ORNAMENT = join(MY_DIR, 'Ornament')
    
if not exists(MY_DICT):
    con2 = sqlite3.connect(MY_DICT)
    cur2 = con2.cursor()
    cur2.execute('CREATE TABLE lisan (id_term int, term varchar(255) primary key, charh longtext(2000))') 
try:
    con2 = sqlite3.connect(MY_DICT)
    cur2 = con2.cursor()
    cur2.execute('CREATE TABLE taje (id_term int, term varchar(255) primary key, charh longtext(2000))') 
    cur2.execute('CREATE TABLE assas (id_term int, term varchar(255) primary key, charh longtext(2000))') 
    cur2.execute('CREATE TABLE mekhtar (id_term int, term varchar(255) primary key, charh longtext(2000))') 
except: pass
    
if not exists(MY_AWZAN):
    con0 = sqlite3.connect(MY_AWZAN)
    cur0 = con0.cursor()
    cur0.execute('CREATE TABLE awzan (id_wazn integer primary key, id_baher int, wazn varchar(255),\
                 tafa3il  varchar(255), takti3 varchar(255), arodh varchar(255), t_arodh varchar(255), \
                 dharb varchar(255), t_dharb varchar(255), taf3ila1 varchar(255), t_taf3ila1 varchar(255), \
                 taf3ila2 varchar(255), t_taf3ila2 varchar(255), taf3ila3 varchar(255), \
                 t_taf3ila3 varchar(255), taf3ila4 varchar(255), t_taf3ila4 varchar(255), \
                 taf3ila5 varchar(255), t_taf3ila5 varchar(255), taf3ila6 varchar(255), \
                 t_taf3ila6 varchar(255))')
    
if not exists(AUDIO_DIR):
    mkdir(AUDIO_DIR)
    
if not exists(ORNAMENT):
    mkdir(ORNAMENT)
    
#a--------------------------------------------------
try: greet = Gtk.Window(Gtk.WindowType.POPUP)
except: 
    greet = Gtk.Window()
    greet.set_title("مرحبا !")
greet.set_border_width(15)
greet.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
greet.set_size_request(400,300)
vb = Gtk.VBox(False, 10)
img_greet = Gtk.Image()
img_greet.set_from_file(join(ICON_DIR,"greet.png"))
vb.pack_start(img_greet, False, False, 0)
vb.pack_start(Gtk.Label('الإصدار {}\nجاري تحميل برنامج دواوين العرب....'.format(version, ))
              , False, False, 0)
greet.add(vb)
greet.show_all()
while (Gtk.events_pending()): Gtk.main_iteration()

#a------------------------------------------
def rgba(value):
    value = value.lstrip('#')
    v = len(value)/3
    R = int(value[0:v], 16)/15.999**v
    G = int(value[v:2*v], 16)/15.999**v
    B = int(value[2*v:3*v], 16)/15.999**v
    A = 1.0
    return Gdk.RGBA(R, G, B, A)

#a-------------------------------------------
def rgb(value):
    value = value.lstrip('#')
    v = len(value)/3
    R = int(value[0:v], 16)/16**(v-2)
    G = int(value[v:2*v], 16)/16**(v-2)
    B = int(value[2*v:3*v], 16)/16**(v-2)
    return  'rgb({}, {}, {})'.format(R, G, B)

#a------------------------------------------
def tool_button(icon_file, tooltip, function, data=None):
        ''' Build custom toolbutton '''
        toolbtn = Gtk.ToolButton()
        widget = Gtk.Image.new_from_file(join(APP_DIR, icon_file))
        toolbtn.set_icon_widget(widget)
        toolbtn.set_tooltip_text(tooltip)
        toolbtn.connect('clicked', function, data)
        return toolbtn

#a------------------------------------------
def combo(ls, name, v):
    new_ls = []
    new_ls.extend(ls)
    hb = Gtk.HBox(False, 6) 
    store = Gtk.ListStore(int, str)
    cmt = Gtk.ComboBox.new_with_model(store)
    if v == 1:
        new_ls.insert(0, [0, u'الكل'])
    map(store.append, new_ls)
    renderer_text = Gtk.CellRendererText()
    renderer_text.set_property("ellipsize-set", True)
#    renderer_text.set_property("max-width-chars",10)
    renderer_text.set_property("weight",14)
    renderer_text.set_property("ellipsize", Pango.EllipsizeMode.END)
    cmt.pack_start(renderer_text, True)
    cmt.add_attribute(renderer_text, "text", 1)
    lab = Gtk.Label(name)
    lab.set_alignment(0,0.5)
    if v == 3:
        lab.set_size_request(200, 8)
    else:
        lab.set_size_request(50, 8)
    cmt.set_size_request(140, 30)
    hb.pack_start(lab, False, False, 0)
    hb.pack_start(cmt, False, False, 0)
    if v == 1:
        cmt.set_active(0)
    return hb, cmt

#a------------------------------------------
def value_active(combo):
    if combo.get_active() == -1: return None
    v = combo.get_active_iter()
    model = combo.get_model()
    value = model.get_value(v, 0)
    return value

#a------------------------------------------
def text_active(combo):
    if combo.get_active() == -1: return None
    v = combo.get_active_iter()
    model = combo.get_model()
    value = model.get_value(v, 1)
    return value

#a------------------------------------------
def search_and_mark(text_buff, text_tag, text, start):
    end = text_buff.get_end_iter()
    match = start.forward_search(text, 0, end)
    if match != None:
        match_start, match_end = match
        text_buff.apply_tag(text_tag, match_start, match_end)
        search_and_mark(text_buff, text_tag, text, match_end)
        
def with_tag(text_buff, text_tag, ls):
    for text in ls:
        cursor_mark = text_buff.get_insert()
        start = text_buff.get_iter_at_mark(cursor_mark)
        if start.get_offset() == text_buff.get_char_count():
            start = text_buff.get_start_iter()
        search_and_mark(text_buff, text_tag, text, start)

#a------------------------------------------           
def tashkil(text):
    if daw_config.getv('tashkil') == '0': return daw_araby.stripTashkeel(text)
    else: return text

#a------------------------------------------
def info(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def erro(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def sure(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
    dlg.set_markup(msg)                         
    r = dlg.run()
    dlg.destroy()
    return r

#a------------------------------------------
class ViewPoem(Gtk.TextView):
    __gtype_name__ = 'MyView'
    def __init__(self, *a):
        Gtk.TextView.__init__(self)
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_right_margin(20)
        self.set_left_margin(20)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        
#a------------------------------------------
class ViewClass(Gtk.TextView):
    __gtype_name__ = 'View'
    def __init__(self, *a):
        Gtk.TextView.__init__(self)
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_right_margin(10)
        self.set_left_margin(10)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
                
#a------------------------------------------
class ButtonClass(Gtk.Button):
    __gtype_name__ = 'button'
    def __init__(self, name):
        Gtk.Button.__init__(self, name)
        label = Gtk.Label()
        label.set_text(name)
        pangolayout = label.get_layout()
        d = pangolayout.get_pixel_size()
        w = ((d[0]/25)+2)*25
        self.set_size_request(w, 30)

#a------------------------------------------
class CustomsButton(Gtk.ToggleButton):
    __gtype_name__ = 'mytogglebutton'
    def __init__(self, name):
        Gtk.ToggleButton.__init__(self, name)
        self.set_size_request(150, -1)
      
#a------------------------------------------
class ViewEdit(Gtk.TextView):
    __gtype_name__ = 'View-editable'
    def __init__(self, *a):
        Gtk.TextView.__init__(self)
        self.set_right_margin(20)
        self.set_left_margin(20)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        
#a------------------------------------------
class TreePoem(Gtk.TreeView):
    __gtype_name__ = 'Treepoem'
    def __init__(self, *a):
        Gtk.TreeView.__init__(self)
        
#a------------------------------------------
class TreeClass(Gtk.TreeView):
    __gtype_name__ = 'Tree'
    def __init__(self, *a):
        Gtk.TreeView.__init__(self)

#a------------------------------------------        
class ScrollClass(Gtk.ScrolledWindow):
    __gtype_name__ = 'Myscroll'
    def __init__(self, *a):
        Gtk.ScrolledWindow.__init__(self)
        
#a------------------------------------------        
class ToggleButtonClass(Gtk.ToggleButton):
    __gtype_name__ = 'Togglebutton'
    def __init__(self, name):
        Gtk.ToggleButton.__init__(self, name) 
        
#a------------------------------------------
class SpinnerClass(Gtk.Dialog):

    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, parent=parent)
        self.set_title(title)
        self.set_size_request(300, 160)
        area = self.get_content_area()
        area.set_spacing(6)
        lab = Gtk.Label('\nانتظر قليلاً من فضلك ...\n')
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        vb = Gtk.VBox(False, 6)
        vb.pack_start(lab, False, False, 0)
        vb.pack_start(self.spinner,  True, True, 0)
        area.pack_start(vb, True, True, 0)
        self.show_all()

    def close(self, *a):
        self.destroy()
