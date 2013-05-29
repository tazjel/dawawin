# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, exists, basename
import os
from gi.repository import Gtk, GObject
import daw_tools, daw_customs



# class صفحة الاستراد والتصدير-------------------------------------------------------------------    

class ImportExport(Gtk.VBox):
    
    def search_on_page(self, text):
        return
    
    def select_all(self, *a):
        a = 0
        while a in range(len(self.poems_store_import)):
            itr = self.poems_store_import.get_iter((a,))
            if self.all_poems.get_active() == True: self.poems_store_import.set(itr, 1, True)
            else: self.poems_store_import.set(itr, 1, False)
            a += 1
    def select_all_poems(self, *a):
        a = 0
        while a in range(len(self.store_poems)):
            itr = self.store_poems.get_iter((a,))
            if self.all_p.get_active() == True: self.store_poems.set(itr, 1, True)
            else: self.store_poems.set(itr, 1, False)
            a += 1
            
    def select_all_ages(self, *a):
        a = 0
        while a in range(len(self.store_ages)):
            itr = self.store_ages.get_iter((a,))
            if self.all_a.get_active() == True: self.store_ages.set(itr, 1, True)
            else: self.store_ages.set(itr, 1, False)
            a += 1
            
    def select_all_dawawin(self, *a):
        a = 0
        while a in range(len(self.store_poets)):
            itr = self.store_poets.get_iter((a,))
            if self.all_d.get_active() == True: self.store_poets.set(itr, 1, True)
            else: self.store_poets.set(itr, 1, False)
            a += 1
    
    def fixed_toggled(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 1)
        fixed = not fixed
        model.set(itr, 1, fixed)
    
    def add_poems(self, *a):
        open_dlg = Gtk.FileChooserDialog(u'إضافة دوواوين وقصائد جديدة',
                                         self.parent, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        open_dlg.set_select_multiple(True)
        Filter = Gtk.FileFilter()
        Filter.set_name(u"ملفات .dwn")
        Filter.add_pattern("*.[dD][wW][nN]")
        open_dlg.add_filter(Filter)
        
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            for filename in open_dlg.get_filenames():
                ls_poems = self.parent.db.add_file_db(filename)     
                for poem in ls_poems:
                    i = poem[0]
                    name = poem[1]
                    if poem[2] != 0: n_poet, l_poet = self.parent.db.name_poet_newfile(poem[2], filename)
                    else: l_poet = u'أحدهم'
                    if poem[5] != 9: age = daw_tools.get_name(daw_tools.age_poet, poem[5])
                    else: age = u'____'
                    abiat = poem[6]
                    if poem[7] != 0: baher = daw_tools.get_name(daw_tools.elbehor, poem[7])
                    else: baher = u'____'
                    if poem[8] != 0: rawi = daw_tools.get_name(daw_tools.elrawi, poem[8])
                    else: rawi = u'____'
                    if poem[11] != 0: gharadh = daw_tools.get_name(daw_tools.elgharadh, poem[11])
                    else: gharadh = u'____'
                    if poem[12] != 0: naw3 = daw_tools.get_name(daw_tools.elnaw3, poem[12])
                    else: naw3 = u'____'
                    source = basename(filename)
                    self.poems_store_import.append([i, True, name, l_poet, age, naw3, baher, gharadh, rawi, abiat, filename, source])
        open_dlg.destroy()
        self.all_poems.set_active(True)
    
    def import_poems(self, *a):
        self.set_sensitive(False)
        d = len(self.poems_store_import)
        n = 0
        s = 0
        while s < d:
            while (Gtk.events_pending()): Gtk.main_iteration()
            itr = self.poems_store_import.get_iter((n,))
            v = self.poems_store_import.get_value(itr, 1)
            if v == True:
                id_poem = self.poems_store_import.get_value(itr, 0)
                filename = self.poems_store_import.get_value(itr, 10)
                check = self.parent.db.add_poem_from_fileDB(id_poem, filename, 
                                                            self.rb_remplace.get_active())
                if check:
                    self.poems_store_import.remove(itr)
            else: n += 1
            s += 1
        self.parent.dawawinpage.refresh_poets()
        self.parent.dawawinpage.search_cb()
        self.parent.organizepage.refresh_poets()
        self.parent.organizepage.search_cb()
        self.set_sensitive(True)
                
    
    def ok_poet(self, *a):
        model, i = self.sel_poet.get_selected()
        if i:
            id_poet = model.get_value(i,0)
            list_poems, self.text_tarjama = self.parent.db.poems_of_poet(id_poet)
            self.store_poems.clear()
            if len(list_poems) != 0:
                for a in list_poems:
                    self.store_poems.append([a[0], False, a[1]])
    
    def ok_age(self, *a):
        model, i = self.sel_ages.get_selected()
        if i:
            age = model.get_value(i,0)
            list_poet = self.parent.db.poet_of_age(age)
            self.store_poets.clear()
            if len(list_poet) != 0:
                for a in list_poet:
                    self.store_poets.append([a[0], False, a[1]])
            if age == 9:
                self.store_poets.append([0, False, u'ما لا يعرف قائله'])
    
    
    def export_age_cb(self, *a):
        save_dlg = Gtk.FileChooserDialog("تصدير العصور المختارة إلى :", self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            self.my_path = save_dlg.get_filename()
            save_dlg.destroy()
            new_dir = join(self.my_path, u'العصور المصدرة')
            if not exists(new_dir):
                os.mkdir(new_dir)
    #        to_zip = 0
    #        to_one = 0
    #        if self.export_to_one.get_active():
    #            to_one = 1
    #        if self.export_to_zip.get_active():
    #            to_zip = 1
            a = 0
            self.set_sensitive(False)
            while a in range(len(self.store_ages)):
                while (Gtk.events_pending()): Gtk.main_iteration()
                itr = self.store_ages.get_iter((a,))
                v = self.store_ages.get_value(itr, 1)
                name = self.store_ages.get_value(itr, 2)
                if v == True:
                    new_file = join(new_dir, name.decode('utf8')+'.dwn')
                    if exists(new_file): 
                        a += 1
                    else:
                        self.parent.db.create_db(new_file)
                        id_age = self.store_ages.get_value(itr, 0)
                        self.parent.db.export_poems(new_file, id_age, 0)
                a += 1
            self.set_sensitive(True)
        else: save_dlg.destroy()
    
    def export_poet_cb(self, *a):
        save_dlg = Gtk.FileChooserDialog("تصدير الدواوين المختارة إلى :", self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            self.my_path = save_dlg.get_filename()
            save_dlg.destroy()
            new_dir = join(self.my_path, u'الدواوين المصدرة')
            if not exists(new_dir):
                os.mkdir(new_dir)
    #        to_zip = 0
    #        to_one = 0
    #        if self.export_to_one.get_active():
    #            to_one = 1
    #        if self.export_to_zip.get_active():
    #            to_zip = 1
            a = 0
            self.set_sensitive(False)
            while a in range(len(self.store_poets)):
                while (Gtk.events_pending()): Gtk.main_iteration()
                itr = self.store_poets.get_iter((a,))
                v = self.store_poets.get_value(itr, 1)
                name = self.store_poets.get_value(itr, 2)
                if v == True:
                    new_file = join(new_dir, name.decode('utf8')+'.dwn')
                    if exists(new_file): 
                        a += 1
                    else:
                        self.parent.db.create_db(new_file)
                        id_poet = self.store_poets.get_value(itr, 0)
                        self.parent.db.export_poems(new_file, id_poet, 1)
                a += 1
            self.set_sensitive(True)
        else: save_dlg.destroy()
    
    def export_poem_cb(self, *a):
        save_dlg = Gtk.FileChooserDialog("تصدير القصائد المختارة إلى :", self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            self.my_path = save_dlg.get_filename()
            save_dlg.destroy()
            new_dir = join(self.my_path.decode('utf8'), u'القصائد المصدرة')
            if not exists(new_dir):
                os.mkdir(new_dir)
    #        to_zip = 0
    #        to_one = 0
    #        if self.export_to_one.get_active():
    #            to_one = 1
    #        if self.export_to_zip.get_active():
    #            to_zip = 1
            a = 0
            self.set_sensitive(False)
            while a in range(len(self.store_poems)):
                while (Gtk.events_pending()): Gtk.main_iteration()
                itr = self.store_poems.get_iter((a,))
                v = self.store_poems.get_value(itr, 1)
                name = self.store_poems.get_value(itr, 2).decode('utf8')
                if v == True:
                    new_file = join(new_dir, name+u'.dwn')
                    if exists(new_file): 
                        a += 1
                    else:
                        self.parent.db.create_db(new_file)
                        id_poem = self.store_poems.get_value(itr, 0)
                        self.parent.db.export_poems(new_file, id_poem, 2)
                a += 1
            self.set_sensitive(True)
        else: save_dlg.destroy()
    
    def switch(self, *a):
        if self.notebook.get_current_page() == 1:
            self.hb_import.show_all()
            self.hb_export.hide()
        else:
            self.hb_import.hide()
            self.hb_export.show_all()
    
    def near_page(self, v):
        return
    
    def move_in_page(self, v):
        return
    
    def __init__(self, parent):
        self.parent = parent
        self.my_path = daw_customs.HOME_DIR
        Gtk.VBox.__init__(self, False, 7) 
        self.notebook = Gtk.Notebook()
        self.poems_store_import = Gtk.ListStore(int,GObject.TYPE_BOOLEAN,str,str,str,str,str,str,str,int,str,str)
        self.tree_poems_import = Gtk.TreeView()
        self.tree_poems_import.set_model(self.poems_store_import)
        self.sel_poems_import = self.tree_poems_import.get_selection()
        self.tree_poems_import.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntoggle.add_attribute( celltoggle, "active", 1)
        celltoggle.connect('toggled', self.fixed_toggled, self.poems_store_import)
        self.tree_poems_import.append_column(columntoggle)
        poems = Gtk.TreeViewColumn('القصيدة', Gtk.CellRendererText(), text=2)
        self.tree_poems_import.append_column(poems)
        poems.set_max_width(300)
        poets = Gtk.TreeViewColumn('الشاعر', Gtk.CellRendererText(), text=3)
        self.tree_poems_import.append_column(poets)
        poets.set_max_width(300)
        age_poet = Gtk.TreeViewColumn('العصر', Gtk.CellRendererText(), text=4)
        self.tree_poems_import.append_column(age_poet)
        age_poet.set_max_width(100)
        elnaw3 = Gtk.TreeViewColumn('النوع', Gtk.CellRendererText(), text=5)
        self.tree_poems_import.append_column(elnaw3)
        elnaw3.set_max_width(100)
        elbaher = Gtk.TreeViewColumn('البحر', Gtk.CellRendererText(), text=6)
        self.tree_poems_import.append_column(elbaher)
        elbaher.set_max_width(120)
        elgharadh = Gtk.TreeViewColumn('الغرض', Gtk.CellRendererText(), text=7)
        self.tree_poems_import.append_column(elgharadh)
        elgharadh.set_max_width(100)
        elrawi = Gtk.TreeViewColumn('الروي', Gtk.CellRendererText(), text=8)
        self.tree_poems_import.append_column(elrawi)
        elrawi.set_max_width(100)
        verses = Gtk.TreeViewColumn('الأبيات', Gtk.CellRendererText(), text=9)
        self.tree_poems_import.append_column(verses)
        verses.set_max_width(100)
        source = Gtk.TreeViewColumn('المصدر', Gtk.CellRendererText(), text=11)
        self.tree_poems_import.append_column(source)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poems_import)
        self.notebook.append_page(scroll, Gtk.Label('استيراد'))
        
        #a---------------------------------------
        hbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        self.store_ages = Gtk.ListStore(int,GObject.TYPE_BOOLEAN, str)
        for a in daw_tools.age_poet:
            self.store_ages.append([a[0], False, a[1]])
        self.tree_ages = Gtk.TreeView()
        self.tree_ages.set_model(self.store_ages)
        self.sel_ages = self.tree_ages.get_selection()
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntoggle.add_attribute( celltoggle, "active", 1)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_ages)
        self.tree_ages.append_column(columntoggle)
        self.tree_ages.connect("cursor-changed", self.ok_age)
        ages = Gtk.TreeViewColumn('العصور', Gtk.CellRendererText(), text=2)
        self.tree_ages.append_column(ages)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_ages)
        vbox = Gtk.VBox(False, 0)
        self.all_a = Gtk.CheckButton('كل العصور')
        self.all_a.connect('toggled', self.select_all_ages) 
        vbox.pack_start(self.all_a, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        hbox.pack_start(vbox, True, True, 0)
        
        self.store_poets = Gtk.ListStore(int,GObject.TYPE_BOOLEAN, str)
        self.tree_poet = Gtk.TreeView()
        self.sel_poet = self.tree_poet.get_selection()
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntoggle.add_attribute( celltoggle, "active", 1)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_poets)
        self.tree_poet.append_column(columntoggle)
        cell = Gtk.CellRendererText()
        poets = Gtk.TreeViewColumn('الدواوين', cell, text=2)
        self.tree_poet.append_column(poets)
        self.tree_poet.set_model(self.store_poets)
        self.tree_poet.connect("cursor-changed", self.ok_poet)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poet)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.VBox(False, 0)
        self.all_d = Gtk.CheckButton('كل الدواوين')
        self.all_d.connect('toggled', self.select_all_dawawin) 
        vbox.pack_start(self.all_d, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        hbox.pack_start(vbox, True, True, 0)
        
        self.store_poems = Gtk.ListStore(int,GObject.TYPE_BOOLEAN, str)
        self.tree_poems = Gtk.TreeView()
        self.tree_poems.set_model(self.store_poems)
        self.sel_poem = self.tree_poems.get_selection()
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntoggle.add_attribute( celltoggle, "active", 1)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_poems)
        self.tree_poems.append_column(columntoggle)
        poems = Gtk.TreeViewColumn('القصائد', Gtk.CellRendererText(), text=2)
        self.tree_poems.append_column(poems)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_poems)
        vbox = Gtk.VBox(False, 0)
        self.all_p = Gtk.CheckButton('كل القصائد')
        self.all_p.connect('toggled', self.select_all_poems) 
        vbox.pack_start(self.all_p, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        hbox.pack_start(vbox, True, True, 0)
        self.notebook.append_page(hbox, Gtk.Label('تصدير'))
        
        self.hb_import = Gtk.HBox(False, 10)
        self.add_db = daw_customs.ButtonClass('إضافة')
        self.add_db.connect('clicked', self.add_poems)
        self.hb_import.pack_start(self.add_db, False, False, 0)
        self.all_poems = Gtk.CheckButton('الكل')
        self.all_poems.connect('toggled', self.select_all) 
        self.hb_import.pack_start(self.all_poems, False, False, 0)
        self.rb_skep = Gtk.RadioButton.new_with_label_from_widget(None,'تخطى القصائد الموجودة')
        self.rb_remplace = Gtk.RadioButton.new_with_label_from_widget(self.rb_skep,'استبدال القصائد الموجودة')
        self.rb_skep.set_active(True)
        self.hb_import.pack_start(self.rb_skep, False, False, 0)
        self.hb_import.pack_start(self.rb_remplace, False, False, 0)
        self.imp_db = daw_customs.ButtonClass('إستيراد')
        self.imp_db.connect('clicked', self.import_poems)
        self.hb_import.pack_end(self.imp_db, False, False, 0)
        
        self.hb_export = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.export_age = daw_customs.ButtonClass('تصدير عصور')
        self.export_age.connect('clicked', self.export_age_cb)
        self.hb_export.pack_start(self.export_age, False, False, 0)
        self.export_poet = daw_customs.ButtonClass('تصدير دواوين')
        self.export_poet.connect('clicked', self.export_poet_cb)
        self.hb_export.pack_start(self.export_poet, False, False, 0)
        self.export_poem = daw_customs.ButtonClass('تصدير قصائد')
        self.export_poem.connect('clicked', self.export_poem_cb)
        self.hb_export.pack_start(self.export_poem, False, False, 0)
#        self.export_to_zip = Gtk.CheckButton('تصدير إلى ملف مضغوط')
#        self.export_to_zip.connect('toggled', self.select_all) 
#        self.export_to_zip.set_active(True)
#        self.hb_export.pack_start(self.export_to_zip, False, False, 0)
#        self.export_to_one = Gtk.CheckButton('تصدير إلى ملف واحد')
#        self.export_to_one.connect('toggled', self.select_all) 
#        self.export_to_one.set_active(True)
#        self.hb_export.pack_start(self.export_to_one, False, False, 0)
        
        self.hb_prograss = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.progress = Gtk.ProgressBar()
        self.hb_prograss.pack_start(Gtk.Label('التقدم : '), False, False, 0)
        self.hb_prograss.pack_start(self.progress, True, True, 0)

        self.pack_start(self.notebook, True, True, 0)
        self.pack_start(self.hb_import, False, False, 0)
        self.pack_start(self.hb_export, False, False, 0)
        self.pack_start(self.hb_prograss, False, False, 0)
        self.show()
        self.notebook.show_all()
        self.notebook.set_current_page(0)
        self.notebook.connect("switch-page", self.switch)
        self.hb_import.show_all()

        