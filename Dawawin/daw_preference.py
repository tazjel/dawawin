# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join, dirname, exists
import os
from shutil import copyfile
from daw_clear import Clear
from daw_contacts import MyDB
from gi.repository import Gtk, Pango
from gi.repository.GdkPixbuf import Pixbuf
import daw_config, daw_customs



# class نافذة التفضيلات----------------------------------------------------------       
        
class Preference(Gtk.Dialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = MyDB()
        self.build()        
        
    def specified(self, *a):
        if self.dfo.get_active():
            self.frame.set_sensitive(False)
            daw_config.setv('tr', '0')
        else:
            self.frame.set_sensitive(True)
            daw_config.setv('tr', '1')
        
    def ch_font(self, btn):
        nconf = btn.get_name()
        dialog = Gtk.FontChooserDialog("اختر خطا")
        dialog.set_font(daw_config.getv(nconf))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            font = dialog.get_font()
            daw_config.setv(nconf, font)
        dialog.destroy()
        self.parent.theme.refrech()
        
#FIXME change 'get_current_color' to 'get_current_rgba'-------------
    def ch_color(self, btn):
        nconf = btn.get_name()
        dialog = Gtk.ColorSelectionDialog("اختر لونا")
        colorsel = dialog.get_color_selection()
        colorsel.set_current_rgba(daw_customs.rgba(daw_config.getv(nconf)))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            color = colorsel.get_current_color().to_string()
            daw_config.setv(nconf, color)
        dialog.destroy()
        self.parent.theme.refrech()
    
    def change_vls(self, btn, nm):
        v = btn.get_active()
        daw_config.setv(nm, v)
    
    def sel_ORNAMENT(self, icv, path):
        model = icv.get_model()
        name = model[path][1]
        daw_config.setv('ornament-file', name)
        self.parent.theme.refrech()
    
    def has_mytheme(self, *a):
        if self.sel_theme.get_active():
            daw_config.setv('theme', '1')
            self.parent.theme.refrech()
        else:
            daw_config.setv('theme', '0')
            self.parent.theme.refrech()
    
    def has_ornament(self, *a):
        if self.sel_ornament.get_active():
            daw_config.setv('ornament', '1')
            self.parent.theme.refrech()
        else:
            daw_config.setv('ornament', '0')
            self.parent.theme.refrech()
    
    def change_path_db(self, *a):
        open_dlg = Gtk.FileChooserDialog(u'تغيير مسار قاعدة البيانات',
                                         self.parent, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        Filter = Gtk.FileFilter()
        Filter.set_name(u"قاعدة البيانات")
        Filter.add_pattern("Dawawin.db")
        open_dlg.add_filter(Filter)
        
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            self.e_dest.set_text(open_dlg.get_filenames()[0].decode('utf8')) 
            daw_config.setv('path', open_dlg.get_filenames()[0])          
        open_dlg.destroy()
    
    def new_db(self,*a): 
        save_dlg = Gtk.FileChooserDialog(u'مسار قاعدة البيانات الجديدة', self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            new_dir = join(save_dlg.get_filename().decode('utf8'), u'دواوين العرب')
            if os.path.exists(join(new_dir,'Dawawin.db')):
                daw_customs.erro(self.parent, u'يوجد قاعدة بيانات في هذا الدليل بالفعل')
            else:
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                if not os.path.exists(join(new_dir,u'Audio')):
                    os.mkdir(join(new_dir,u'Audio'))
                if not os.path.exists(join(new_dir,u'Ornament')):
                    os.mkdir(join(new_dir,u'Ornament'))
                list_f = os.listdir(daw_customs.ORNAMENT)
                for v in list_f:
                    copyfile(join(daw_customs.ORNAMENT,v), join(new_dir,u'Ornament',v))
                self.parent.db.create_db(join(new_dir,'Dawawin.db'))
                copyfile(daw_customs.MY_AWZAN, join(new_dir,'Awzan.db'))
                copyfile(daw_customs.MY_HELP, join(new_dir,'Help.db'))
                copyfile(daw_customs.MY_DICT, join(new_dir,'Dict.db'))
                daw_customs.info(self.parent, u'تم إضافة قاعدة بيانات جديدة')
        save_dlg.destroy()
    
    def count_cb(self, *a):
        n_dawawin = self.db.n_dawawin()
        n_poems = self.db.n_poems()
        n_verses = self.db.n_verses()
        daw_config.setv('n_dawawin', n_dawawin)
        daw_config.setv('n_poems', n_poems)
        daw_config.setv('n_verses', n_verses)
        self.n_dawawin.set_text('عدد الدواوين : '+n_dawawin)
        self.n_poems.set_text('عدد القصائد : '+n_poems)
        self.n_verses.set_text('عدد الأبيات : '+n_verses)
    
    def del_all_cb(self, *a):
        Clear(self.parent).show_all()
        self.hide()
    
    def show_count(self, *a):
        self.parent.show_page(None, 'الإحصاء', 15)
        self.parent.countpage.make_text()
        self.hide()
              
    def build(self,*a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("Dawawin")
        self.set_title("التفضيلات")
        self.resize(500, 300)
        area = self.get_content_area()
        area.set_spacing(6)
        self.connect('delete-event', lambda w,*a: w.hide() or True)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        lab_info = Gtk.Label('بعض الخيارات قد تحتاج إلى إعادة تشغيل البرنامج')
        lab_info.override_background_color(Gtk.StateFlags.NORMAL, daw_customs.rgba('#FFF14E'))
        lab_info.override_color(Gtk.StateFlags.NORMAL, daw_customs.rgba('#E90003'))
        lab_info.override_font(Pango.FontDescription("8"))
        
        self.notebook = Gtk.Notebook()
        self.box0 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box00 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box1 = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)
        self.box2 = Gtk.Box(spacing=4,orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(spacing=40,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(self.box1, False, False, 0)
        hbox.pack_start(self.box2, False, False, 0)
        self.frame = Gtk.Frame()
        self.frame.add(hbox)
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.dfo = Gtk.RadioButton.new_with_label_from_widget(None, 'افتراضي')
        self.cos = Gtk.RadioButton.new_with_label_from_widget(self.dfo,'مخصص')
        self.dfo.connect('toggled',self.specified,'0')
        self.cos.connect('toggled',self.specified,'1')
        hbox.pack_start(self.dfo, False, False, 0)
        hbox.pack_start(self.cos, False, False, 0)
        self.sel_theme = Gtk.CheckButton('تلوين النافذة')
        hbox.pack_end(self.sel_theme, False, False, 0)
        if daw_config.getv('theme') == '1': self.sel_theme.set_active(True)
        else: self.sel_theme.set_active(False)
        self.sel_theme.connect("toggled", self.has_mytheme)
        hbox.set_border_width(5)
        self.box0.pack_start(hbox, False, False, 0)
        self.box0.pack_start(self.frame, True, True, 0)
       
        list_w1 = [[u'القوائم الجانبية','td'], [u'قائمة القصائد','tp'], [u'متن القصيدة','mp'], 
                   [u'الشرح والترجمة','ch'], [u'العناوين','an']]
        list_w2 = [[u'لون خلفية العرض','b'], [u'لون خط التحديد','fs'], [u'لون خلفية التحديد','bs'], 
                   [u'لون تحديد البحث','ss'], [u'لون خلفية خاص','bp']]
        for a in list_w1:
            hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn1 = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_FONT)
            btn1.set_name('font'+a[1])
            btn1.connect('clicked',self.ch_font)
            btn2 = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_COLOR)
            btn2.set_name('color'+a[1])
            btn2.connect('clicked',self.ch_color)
            hbox.pack_start(btn2, False, False, 0)
            hbox.pack_start(btn1, False, False, 0)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            self.box1.pack_start(hbox, False, False, 0)
            
        for a in list_w2:
            hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_COLOR)
            btn.set_name('color'+a[1])
            btn.connect('clicked',self.ch_color)
            hbox.pack_start(btn, False, False, 0)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            self.box2.pack_start(hbox, False, False, 0)
        self.notebook.append_page(self.box0, Gtk.Label('خط ولون'))
        
        vb = Gtk.VBox(False, 6)
        vb.set_border_width(6)
        ls = [[0, u'ضيق'],
            [1, u'وسط'],
            [2, u'واسع']]
        hb, self.bayn_abiat = daw_customs.combo(ls, u'المسافة بين الأبيات', 3)
        self.bayn_abiat.set_active(daw_config.getn('b_abiat'))
        self.bayn_abiat.connect('changed', self.change_vls, u'b_abiat')
        vb.pack_start(hb, False, False, 0)
        
        ls = [[0, u'ضيق'],
            [1, u'وسط'],
            [2, u'واسع']]
        hb, self.bayn_shater = daw_customs.combo(ls, u'المسافة بين شطري البيت', 3)
        self.bayn_shater.set_active(daw_config.getn('b_half'))
        self.bayn_shater.connect('changed', self.change_vls, u'b_half')
        vb.pack_start(hb, False, False, 0)
        
        ls = [[0, u'دوما'],
            [1, u'للحاجة']]
        hb, self.tarakeb = daw_customs.combo(ls, u'تراكب شطري البيت', 3)
        self.tarakeb.set_active(daw_config.getn('tarakeb'))
        self.tarakeb.connect('changed', self.change_vls, u'tarakeb')
        vb.pack_start(hb, False, False, 0)
        
        ls = [[0, u'بالتطويلات'],
            [1, u'بالمسافات']]
        hb, self.tandhid = daw_customs.combo(ls, u'تعديل طول الشطر', 3)
        self.tandhid.set_active(daw_config.getn('tandhid'))
        self.tandhid.connect('changed', self.change_vls, u'tandhid')
        vb.pack_start(hb, False, False, 0)
        
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        lab = Gtk.Label('أدنى طول للشطر بالبكسلات')
        lab.set_alignment(0,0.5)
        hbox.pack_start(lab, False, False, 0)
        adj = Gtk.Adjustment(150, 100, 700, 1, 5, 0)
        self.min_long = Gtk.SpinButton()
        self.min_long.set_adjustment(adj)
        self.min_long.set_wrap(True)
        self.min_long.set_value(daw_config.getf('min_long'))
        def change_min(widget, *a):
            v = self.min_long.get_value()
            daw_config.setv('min_long', v)
        self.min_long.connect('value-changed', change_min)
        hbox.pack_start(self.min_long, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        lab = Gtk.Label('التراكب إذا تجاوز طول الشطر')
        lab.set_alignment(0,0.5)
        hbox.pack_start(lab, False, False, 0)
        adj = Gtk.Adjustment(350, 300, 1000, 1, 5, 0)
        self.max_long = Gtk.SpinButton()
        self.max_long.set_adjustment(adj)
        self.max_long.set_wrap(True)
        self.max_long.set_value(daw_config.getf('max_long'))
        def change_max(widget, *a):
            v = self.max_long.get_value()
            daw_config.setv('max_long', v)
        self.max_long.connect('value-changed', change_max)
        hbox.pack_start(self.max_long, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        self.notebook.append_page(vb, Gtk.Label('تخطيط'))
        
        vb = Gtk.VBox(False, 6)
        vb.set_border_width(6)
        
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.del_all = daw_customs.ButtonClass('مسح عام')
        self.del_all.connect('clicked', self.del_all_cb)
        hbox.pack_start(self.del_all, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.add_db = daw_customs.ButtonClass('أنشاء قاعدة بيانات جديدة')
        self.add_db.connect('clicked', self.new_db)
        hbox.pack_start(self.add_db, False, False, 0)
        if not exists(dirname(daw_config.getv('path'))): self.add_db.set_sensitive(False)
        vb.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        self.e_dest = Gtk.Entry()
        self.e_dest.set_text(daw_config.getv('path').decode('utf8'))
        self.b_dest = daw_customs.ButtonClass('تغيير المسار')
        self.b_dest.connect('clicked', self.change_path_db)  
        hbox.pack_start(self.b_dest, False, False, 0)
        hbox.pack_start(self.e_dest, True, True, 0)
        vb.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        db_void = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/dawawin/files/",
                                                'صفحة البرنامج على النت')
        hbox.pack_start(db_void, False, False, 0)
        vb.pack_start(hbox, False, False, 0)
        self.notebook.append_page(vb, Gtk.Label('خيارات'))
        
        vb = Gtk.VBox(False, 6)
        vb.set_border_width(6)
        self.n_dawawin = Gtk.Label('عدد الدواوين : '+daw_config.getv('n_dawawin'))
        self.n_dawawin.set_alignment(0,0.5)
        vb.pack_start(self.n_dawawin, False, False, 0)
        self.n_poems = Gtk.Label('عدد القصائد : '+daw_config.getv('n_poems'))
        self.n_poems.set_alignment(0,0.5)
        vb.pack_start(self.n_poems, False, False, 0)
        self.n_verses = Gtk.Label('عدد الأبيات : '+daw_config.getv('n_verses'))
        self.n_verses.set_alignment(0,0.5)
        vb.pack_start(self.n_verses, False, False, 0)
        hbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        self.rapid_count = daw_customs.ButtonClass('إحصاء سريع')
        self.rapid_count.connect('clicked', self.count_cb)
        self.detail_count = daw_customs.ButtonClass('إحصاء مفصل')
        self.detail_count.connect('clicked', self.show_count)
        self.web_count = daw_customs.ButtonClass('صفحة ويب')
        self.web_count.connect('clicked', lambda *a: self.parent.countpage.make_html())
        hbox.pack_start(self.rapid_count, False, False, 0)
        hbox.pack_start(self.detail_count, False, False, 0)
        hbox.pack_start(self.web_count, False, False, 0)
        vb.pack_end(hbox, False, False, 0)
        self.notebook.append_page(vb, Gtk.Label('إحصاء'))
        
        vbox = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.sel_ornament = Gtk.CheckButton('اعتمد زخرفة الخلفية')
        hbox.pack_start(self.sel_ornament, False, False, 0)
        if daw_config.getv('ornament') == '1': self.sel_ornament.set_active(True)
        else: self.sel_ornament.set_active(False)
        self.sel_ornament.connect("toggled", self.has_ornament)
        vbox.pack_start(hbox, False, False, 0)
        
        liststore = Gtk.ListStore(Pixbuf, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_reorderable(True)
        list_icons = os.listdir(daw_customs.ORNAMENT)
        iconview.set_columns(6)
        iconview.connect('item-activated', self.sel_ORNAMENT)
        for a in list_icons:
            try:
                pixbuf = Pixbuf.new_from_file_at_size(join(daw_customs.ORNAMENT, a), 64, 64 )
                liststore.append([pixbuf, a])
            except: pass
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(iconview)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll, True, True, 0)
        self.notebook.append_page(vbox, Gtk.Label('الزخرفة'))
        
        self.box.pack_start(self.notebook, True, True, 0)
        self.box.pack_start(lab_info, False, False, 0)
        
        clo = daw_customs.ButtonClass("إغلاق")
        clo.connect('clicked',lambda *a: self.hide())
        ref = daw_customs.ButtonClass("تحديث الواجهة")
        ref.connect('clicked',lambda *a: self.parent.theme.refrech())
        ref.connect('clicked',lambda *a: self.parent.refrech())
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(5)
        hbox.pack_start(ref, False, False, 0)
        hbox.pack_end(clo, False, False, 0)
        self.box.pack_start(hbox, False, False, 0)
        if daw_config.getv('tr') == '1':
            self.cos.set_active(True)
        else:
            self.frame.set_sensitive(False)
            self.dfo.set_active(True)
        area.pack_start(self.box, True, True, 0)