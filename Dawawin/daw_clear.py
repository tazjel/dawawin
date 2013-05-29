# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
from daw_contacts import MyDB
from os.path import join
import os, cPickle
import daw_config, daw_customs, daw_tools

class Clear(Gtk.Dialog):
    
    def remove_cb(self, *a):
        msg = daw_customs.sure(self.parent, "هل تريد مسح جميع البيانات المعلمة")
        if msg == Gtk.ResponseType.YES:
            for btn in self.list_ages_btn:
                if btn.get_active() :
                    self.set_sensitive(False)
                    self.db.remove_age(int(btn.get_name()))
                    btn.set_active(False)
            if self.del_abiaty.get_active():
                self.db.remove_abiaty()
                self.del_abiaty.set_active(False)
            if self.del_favory.get_active():
                self.db.remove_favory()
                self.del_favory.set_active(False)
            if self.del_recite.get_active():
                self.db.remove_recite()
                self.del_recite.set_active(False)
            if self.del_search.get_active():
                list_n = os.listdir(daw_customs.HOME_DIR)
                for v in list_n:
                    if '.pkl' in v:
                        os.remove(join(daw_customs.HOME_DIR, v))
                self.del_search.set_active(False)
            if self.del_mark.get_active():
                daw_config.setv('marks', '[]')
                self.del_mark.set_active(False)
        self.parent.dawawinpage.refresh_poets()
        self.parent.dawawinpage.search_cb()
        self.parent.organizepage.refresh_poets()
        self.parent.organizepage.search_cb()
        self.parent.favorite.store()
        self.parent.recite.store()
        self.set_sensitive(True)
    
    
    def __init__(self, parent):
        self.parent = parent
        self.db = MyDB()
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("Dawawin")
        area = self.get_content_area()
        area.set_spacing(7)
        self.set_title('نافذة المسح')
        self.set_default_size(450, 300)
        vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        vbox.set_border_width(7)
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        self.list_ages = daw_tools.age_poet
        self.list_ages_btn = []
        for a in self.list_ages:
            btn = Gtk.CheckButton(a[1])
            btn.set_name(str(a[0]))
            box.pack_start(btn, False, False, 0)
            self.list_ages_btn.append(btn)
        frame = Gtk.Frame()
        frame.set_label('الدواوين حسب العصور')
        box.set_border_width(6)
        frame.add(box)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        remove_all = daw_customs.ButtonClass("مسح")
        remove_all.connect('clicked', self.remove_cb)
        hb.pack_start(remove_all, False, False, 0)
        clo = daw_customs.ButtonClass("إغلاق")
        clo.connect('clicked',lambda *a: self.destroy())
        hb.pack_end(clo, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)
        hbox.pack_start(frame, True, True, 0)
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        frame = Gtk.Frame()
        frame.set_label('متفرقات')
        box.set_border_width(6)
        frame.add(box)
        self.del_favory = Gtk.CheckButton('القصائد المفضلة')
        box.pack_start(self.del_favory, False, False, 0)
        self.del_recite = Gtk.CheckButton('القصائد المسجلة')
        box.pack_start(self.del_recite, False, False, 0)
        self.del_abiaty = Gtk.CheckButton('أبياتي المفضلة')
        box.pack_start(self.del_abiaty, False, False, 0)
        self.del_search = Gtk.CheckButton('البحوث المحفوظة')
        box.pack_start(self.del_search, False, False, 0)
        self.del_mark = Gtk.CheckButton('المواضع المحفوظة')
        box.pack_start(self.del_mark, False, False, 0)
        hbox.pack_start(frame, True, True, 0)
        vbox.pack_start(hb, False, False, 0)
        area.pack_start(vbox, True, True, 0)