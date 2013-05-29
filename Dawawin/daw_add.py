# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
from gi.repository import Gtk, Pango
import daw_tools, daw_araby, daw_customs
import re

# class صفحة إضافة القصيدة-------------------------------------
    
class AddPoem(Gtk.Box):
    
    def write_info(self, item):
        self.nasse_bfr.insert_at_cursor('= '+item.get_label()) 
    
    def populate_popup(self, view, menu):
        c3 = Gtk.SeparatorMenuItem()
        menu.prepend(c3)
        c3.show()
        f1 = Gtk.MenuItem('النوع')
        imenu = Gtk.Menu()
        f1.set_submenu(imenu)
        f1m1 = Gtk.MenuItem(' النوع : قريض')
        imenu.append(f1m1)
        f1m2 = Gtk.MenuItem(' النوع : أرجوزة')
        imenu.append(f1m2)
        f1m3 = Gtk.MenuItem(' النوع : مُوشحة')
        imenu.append(f1m3)
        f1m4 = Gtk.MenuItem(' النوع : رُباعيّة')
        imenu.append(f1m4)
        f1m5 = Gtk.MenuItem(' النوع : قصيدة نثر')
        imenu.append(f1m5)
        f1m6 = Gtk.MenuItem(' النوع : مخمّسة')
        imenu.append(f1m6)
        f1.show_all()

        f2 = Gtk.MenuItem('الغرض')
        imenu = Gtk.Menu()
        f2.set_submenu(imenu)
        f2m1 = Gtk.MenuItem(' الغرض : وصف')
        imenu.append(f2m1)
        f2m2 = Gtk.MenuItem(' الغرض : تشبيه')
        imenu.append(f2m2) 
        f2m3 = Gtk.MenuItem(' الغرض : فخر')
        imenu.append(f2m3) 
        f2m4 = Gtk.MenuItem(' الغرض : حماسة')
        imenu.append(f2m4) 
        f2m5 = Gtk.MenuItem(' الغرض : نسيب')
        imenu.append(f2m5)
        f2m6 = Gtk.MenuItem(' الغرض : شكوى')
        imenu.append(f2m6)
        f2m7 = Gtk.MenuItem(' الغرض : عتاب')
        imenu.append(f2m7)
        f2m8 = Gtk.MenuItem(' الغرض : اعتذار')
        imenu.append(f2m8)
        f2m9 = Gtk.MenuItem(' الغرض : هجاء')
        imenu.append(f2m9)
        f2m10 = Gtk.MenuItem(' الغرض : وعيد')
        imenu.append(f2m10)
        f2m11 = Gtk.MenuItem(' الغرض : رثاء')
        imenu.append(f2m11) 
        f2m12 = Gtk.MenuItem(' الغرض : مدح')
        imenu.append(f2m12)
        f2m13 = Gtk.MenuItem(' الغرض : اقتضاء')
        imenu.append(f2m13)
        f2m14 = Gtk.MenuItem(' الغرض : علمي')
        imenu.append(f2m14) 
        f2m15 = Gtk.MenuItem(' الغرض : دفاع')
        imenu.append(f2m15) 
        f2m16 = Gtk.MenuItem(' الغرض : مناجاة')
        imenu.append(f2m16) 
        f2m17 = Gtk.MenuItem(' الغرض : زهد')
        imenu.append(f2m17) 
        f2m18 = Gtk.MenuItem(' الغرض : ملحمة')
        imenu.append(f2m18) 
        f2m19 = Gtk.MenuItem(' الغرض : إلغاز')
        imenu.append(f2m19) 
        f2m20 = Gtk.MenuItem(' الغرض : تأريخ')
        imenu.append(f2m20) 
        f2m21 = Gtk.MenuItem(' الغرض : هزل')
        imenu.append(f2m21) 
        f2m22 = Gtk.MenuItem(' الغرض : حكمة')
        imenu.append(f2m22)
        f2m23 = Gtk.MenuItem(' الغرض : قصصي')
        imenu.append(f2m23) 
        f2m24 = Gtk.MenuItem(' الغرض : هِنات')
        imenu.append(f2m24)
        f2m25 = Gtk.MenuItem(' الغرض : خليط')
        imenu.append(f2m25)
        f2.show_all() 

        f3 = Gtk.MenuItem('القافية')
        imenu = Gtk.Menu()
        f3.set_submenu(imenu)
        f3m1 = Gtk.MenuItem(' القافية : مطلقة')
        imenu.append(f3m1) 
        f3m2 = Gtk.MenuItem(' القافية : مقيدة')
        imenu.append(f3m2)
        f3.show_all() 

        f4 = Gtk.MenuItem('الروي')
        imenu = Gtk.Menu()
        f4.set_submenu(imenu)
        f4m1 = Gtk.MenuItem(' الروي : ألف')
        imenu.append(f4m1)
        f4m2 = Gtk.MenuItem(' الروي : باء')
        imenu.append(f4m2) 
        f4m3 = Gtk.MenuItem(' الروي : تاء')
        imenu.append(f4m3) 
        f4m4 = Gtk.MenuItem(' الروي : تاء مربوطة')
        imenu.append(f4m4) 
        f4m5 = Gtk.MenuItem(' الروي : ثاء')
        imenu.append(f4m5)
        f4m6 = Gtk.MenuItem(' الروي : جيم')
        imenu.append(f4m6)
        f4m7 = Gtk.MenuItem(' الروي : حاء')
        imenu.append(f4m7)
        f4m8 = Gtk.MenuItem(' الروي : خاء')
        imenu.append(f4m8)
        f4m9 = Gtk.MenuItem(' الروي : دال')
        imenu.append(f4m9)
        f4m10 = Gtk.MenuItem(' الروي : ذال')
        imenu.append(f4m10)
        f4m11 = Gtk.MenuItem(' الروي : راء')
        imenu.append(f4m11) 
        f4m12 = Gtk.MenuItem(' الروي : زاي')
        imenu.append(f4m12)
        f4m13 = Gtk.MenuItem(' الروي : سين')
        imenu.append(f4m13)
        f4m14 = Gtk.MenuItem(' الروي : شين')
        imenu.append(f4m14) 
        f4m15 = Gtk.MenuItem(' الروي : صاد')
        imenu.append(f4m15) 
        f4m16 = Gtk.MenuItem(' الروي : ضاد')
        imenu.append(f4m16) 
        f4m17 = Gtk.MenuItem(' الروي : طاء')
        imenu.append(f4m17) 
        f4m18 = Gtk.MenuItem(' الروي : ظاء')
        imenu.append(f4m18) 
        f4m19 = Gtk.MenuItem(' الروي : عين')
        imenu.append(f4m19) 
        f4m20 = Gtk.MenuItem(' الروي : غين')
        imenu.append(f4m20) 
        f4m21 = Gtk.MenuItem(' الروي : فاء')
        imenu.append(f4m21) 
        f4m22 = Gtk.MenuItem(' الروي : قاف')
        imenu.append(f4m22)
        f4m23 = Gtk.MenuItem(' الروي : كاف')
        imenu.append(f4m23) 
        f4m24 = Gtk.MenuItem(' الروي : لام')
        imenu.append(f4m24)
        f4m25 = Gtk.MenuItem(' الروي : ميم')
        imenu.append(f4m25)
        f4m26 = Gtk.MenuItem(' الروي : نون' )
        imenu.append(f4m26) 
        f4m27 = Gtk.MenuItem(' الروي : هاء' )
        imenu.append(f4m27)
        f4m28 = Gtk.MenuItem(' الروي : واو' )
        imenu.append(f4m28)
        f4m29 = Gtk.MenuItem(' الروي : ياء' )
        imenu.append(f4m29) 
        f4m30 = Gtk.MenuItem(' الروي : همزة' )
        imenu.append(f4m30)
        f4.show_all()

        f5 = Gtk.MenuItem('البحر')
        imenu = Gtk.Menu()
        f5.set_submenu(imenu)
        f5m1 = Gtk.MenuItem(' البحر : الطَّوِيل')
        imenu.append(f5m1) 
        f5m2 = Gtk.MenuItem(' البحر : المَدِيد')
        imenu.append(f5m2) 
        f5m3 = Gtk.MenuItem(' البحر : البَسِيط')
        imenu.append(f5m3) 
        f5m4 = Gtk.MenuItem(' البحر : الوافِر')
        imenu.append(f5m4) 
        f5m5 = Gtk.MenuItem(' البحر : الكامِل')
        imenu.append(f5m5) 
        f5m6 = Gtk.MenuItem(' البحر : الهَزَج')
        imenu.append(f5m6) 
        f5m7 = Gtk.MenuItem(' البحر : الرَجَز')
        imenu.append(f5m7) 
        f5m8 = Gtk.MenuItem(' البحر : الرَّمَل')
        imenu.append(f5m8) 
        f5m9 = Gtk.MenuItem(' البحر : السَّريع')
        imenu.append(f5m9) 
        f5m10 = Gtk.MenuItem(' البحر : المُنْسَرِح')
        imenu.append(f5m10) 
        f5m11 = Gtk.MenuItem(' البحر : الخفيف')
        imenu.append(f5m11) 
        f5m12 = Gtk.MenuItem(' البحر : المضارع')
        imenu.append(f5m12) 
        f5m13 = Gtk.MenuItem(' البحر : المقتضب')
        imenu.append(f5m13) 
        f5m14 = Gtk.MenuItem(' البحر : المجتث')
        imenu.append(f5m14) 
        f5m15 = Gtk.MenuItem(' البحر : المتقارب')
        imenu.append(f5m15) 
        f5m16 = Gtk.MenuItem(' البحر : المتدارك')
        imenu.append(f5m16)
        f5.show_all() 
      
        menu.prepend(f2)
        menu.prepend(f3)
        menu.prepend(f4)
        menu.prepend(f5)
        menu.prepend(f1)
        
        if not self.all_poems.get_active():
            f2.hide()
            f3.hide()
            f4.hide()
            f5.hide()
            f1.hide()
            c3.hide()
        
        f1m1.connect("activate", self.write_info)
        f1m2.connect("activate", self.write_info)
        f1m3.connect("activate", self.write_info)
        f1m4.connect("activate", self.write_info)
        f1m5.connect("activate", self.write_info)
        f1m6.connect("activate", self.write_info)
        f2m1.connect("activate", self.write_info)
        f2m2.connect("activate", self.write_info)
        f2m3.connect("activate", self.write_info)
        f2m4.connect("activate", self.write_info)
        f2m5.connect("activate", self.write_info)
        f2m6.connect("activate", self.write_info)
        f2m7.connect("activate", self.write_info)
        f2m8.connect("activate", self.write_info)
        f2m9.connect("activate", self.write_info)
        f2m10.connect("activate", self.write_info)
        f2m11.connect("activate", self.write_info)
        f2m12.connect("activate", self.write_info)
        f2m13.connect("activate", self.write_info)
        f2m14.connect("activate", self.write_info)
        f2m15.connect("activate", self.write_info)
        f2m16.connect("activate", self.write_info)
        f2m17.connect("activate", self.write_info)
        f2m18.connect("activate", self.write_info)
        f2m19.connect("activate", self.write_info)
        f2m20.connect("activate", self.write_info)
        f2m21.connect("activate", self.write_info)
        f2m22.connect("activate", self.write_info)
        f2m23.connect("activate", self.write_info)
        f2m24.connect("activate", self.write_info)
        f3m1.connect("activate", self.write_info)
        f3m2.connect("activate", self.write_info)
        f4m1.connect("activate", self.write_info)
        f4m2.connect("activate", self.write_info)
        f4m3.connect("activate", self.write_info)
        f4m4.connect("activate", self.write_info)
        f4m5.connect("activate", self.write_info)
        f4m6.connect("activate", self.write_info)
        f4m7.connect("activate", self.write_info)
        f4m8.connect("activate", self.write_info)
        f4m9.connect("activate", self.write_info)
        f4m10.connect("activate", self.write_info)
        f4m11.connect("activate", self.write_info)
        f4m12.connect("activate", self.write_info)
        f4m13.connect("activate", self.write_info)
        f4m14.connect("activate", self.write_info)
        f4m15.connect("activate", self.write_info)
        f4m16.connect("activate", self.write_info)
        f4m17.connect("activate", self.write_info)
        f4m18.connect("activate", self.write_info)
        f4m19.connect("activate", self.write_info)
        f4m20.connect("activate", self.write_info)
        f4m21.connect("activate", self.write_info)
        f4m22.connect("activate", self.write_info)
        f4m23.connect("activate", self.write_info)
        f4m24.connect("activate", self.write_info)
        f4m25.connect("activate", self.write_info)
        f4m26.connect("activate", self.write_info)
        f4m27.connect("activate", self.write_info)
        f4m28.connect("activate", self.write_info)
        f4m29.connect("activate", self.write_info)
        f4m30.connect("activate", self.write_info)
        f5m1.connect("activate", self.write_info)
        f5m2.connect("activate", self.write_info)
        f5m3.connect("activate", self.write_info)
        f5m4.connect("activate", self.write_info)
        f5m5.connect("activate", self.write_info)
        f5m6.connect("activate", self.write_info)
        f5m7.connect("activate", self.write_info)
        f5m8.connect("activate", self.write_info)
        f5m9.connect("activate", self.write_info)
        f5m10.connect("activate", self.write_info)
        f5m11.connect("activate", self.write_info)
        f5m12.connect("activate", self.write_info)
        f5m13.connect("activate", self.write_info)
        f5m14.connect("activate", self.write_info)
        f5m15.connect("activate", self.write_info)
        f5m16.connect("activate", self.write_info)
    
    def search_on_page(self, text):
        return
    
    def is_poet(self, *a):
        if self.present.get_active():
            self.poets.set_sensitive(True)
            self.grd.set_sensitive(False)
            self.tarjama.set_sensitive(False)
        elif self.outsider.get_active():
            self.poets.set_sensitive(False)
            self.grd.set_sensitive(False)
        else:
            self.poets.set_sensitive(False)
            self.grd.set_sensitive(True)
            self.tarjama.set_sensitive(True)
    
    def add_poet(self, *a):
        if self.outsider.get_active():
            msg = daw_customs.sure(self.parent, '''
            هل أنت متأكد من أن 
            قائل هذه الأبيات غير معروف ؟
            ''' )
            if msg == Gtk.ResponseType.NO:
                return 'none', False, False, False
            else:
                return 0, 0, 22, 9
        elif self.present.get_active():
            poet, sex, balad, age = self.parent.db.id_name_poet(self.poets.get_text().decode('utf8'))
            if poet == None:
                daw_customs.erro(self.parent, 'ضع الاسم الصحيح للشاعر'); return
        elif self.nopresent.get_active():
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
            if self.death.get_active(): die = self.dh_poet.get_value()
            else: die = 0
            tarjama = self.tarjama_bfr.get_text(self.tarjama_bfr.get_start_iter(),
                                                self.tarjama_bfr.get_end_iter(), False).decode('utf8')
            poet, sex, balad, age = self.parent.db.add_poet(nm, lak, tarjama, die, sex, balad, age)
        return poet, sex, balad, age
        
    def adding(self, *a):
        if self.all_poems.get_active():
            self.adding_muth()
        else:
            self.adding_one()
        
    def adding_muth(self, *a):
        text = daw_tools.right_space(self.nasse_bfr.get_text(self.nasse_bfr.get_start_iter(),
                                                        self.nasse_bfr.get_end_iter(), False)).decode('utf8')
        if text == '': daw_customs.erro(self.parent, 'ضع القصائد أولا'); return
        gharadh = 0
        baher = 0
        rawi = 0
        kafia = 0
        arodh = 0
        sabab = ""
        charh = ""
        poet, sex, balad, age = self.add_poet()
        if poet == 'none': return
        self.set_sensitive(False)
        list_poems = text.split('#')
        for poem_text in list_poems:
            while (Gtk.events_pending()): Gtk.main_iteration()
            name, poem, naw3, gharadh, baher, rawi, kafia = daw_tools.name_poem(poem_text)
            poem = daw_tools.right_space(poem)
            label = Gtk.Label()
            label.override_font(Pango.FontDescription('KacstOne 15'))
            if naw3 != 5:
                if daw_tools.is_machtor(poem):
                    longer_half, n_abiat = daw_tools.longer_half(poem, label, 1)
                else:
                    longer_half, n_abiat = daw_tools.longer_half(poem, label, 0)
            else: 
                longer_half = 0
                n_abiat = len(poem.splitlines(1))
            self.parent.db.add_poem(name, poem, sabab, charh, poet, sex, balad, age, 
                                 n_abiat, baher, rawi, kafia, arodh, gharadh, naw3, longer_half)
        self.parent.dawawinpage.refresh_poets()
        self.parent.dawawinpage.search_cb()
        self.parent.organizepage.refresh_poets()
        self.parent.organizepage.search_cb()
        daw_customs.info(self.parent, 'تم إضافة جميع القصائد بنجاح')
        self.set_sensitive(True); return
    
    def adding_one(self, *a):
        text = daw_tools.right_space(self.nasse_bfr.get_text(self.nasse_bfr.get_start_iter(),
                                                        self.nasse_bfr.get_end_iter(), False)).decode('utf8')
        if text == '': daw_customs.erro(self.parent, 'ضع القصيدة أولا'); return
        nam = self.name_poem.get_text().decode('utf8')
        if nam == '' : daw_customs.erro(self.parent, 'ضع اسما للقصيدة\nأو أول شطر منها'); return
        naw3 = daw_customs.value_active(self.naw3)
        if naw3 == None : daw_customs.erro(self.parent, 'حدد نوع القصيدة'); return
        if naw3 == 1:
            baher = daw_customs.value_active(self.baher)
            if baher == None : daw_customs.erro(self.parent, 'حدد بحر القصيدة'); return
            rawi = daw_customs.value_active(self.rawi)
            if rawi == None : daw_customs.erro(self.parent, 'حدد روي القصيدة'); return
            kafia = daw_customs.value_active(self.kafia)
            if kafia == None : daw_customs.erro(self.parent, 'حدد قافية القصيدة'); return
            arodh = daw_customs.value_active(self.arodh)
            if arodh == None : daw_customs.erro(self.parent, 'حدد عروض القصيدة'); return
        elif naw3 == 2:
            baher = daw_customs.value_active(self.baher)
            if baher == None : daw_customs.erro(self.parent, 'حدد بحر القصيدة'); return
            rawi = 0
            kafia = 0
            arodh = 0
        else:
            baher = 0
            rawi = 0
            kafia = 0
            arodh = 0
        gharadh = daw_customs.value_active(self.gharadh)
        if gharadh == None : daw_customs.erro(self.parent, 'حدد غرض القصيدة'); return
        poet, sex, balad, age = self.add_poet()
        if poet == 'none': return
        charh = self.charh_bfr.get_text(self.charh_bfr.get_start_iter(),
                                        self.charh_bfr.get_end_iter(), False).decode('utf8')
        sabab = self.sabab_bfr.get_text(self.sabab_bfr.get_start_iter(),
                                        self.sabab_bfr.get_end_iter(), False).decode('utf8')
        label = Gtk.Label()
        label.override_font(Pango.FontDescription('KacstOne 15'))
        if naw3 != 5:
            if daw_tools.is_machtor(text):
                longer_half, n_abiat = daw_tools.longer_half(text, label, 1)
            else:
                longer_half, n_abiat = daw_tools.longer_half(text, label, 0)
        else: 
            longer_half = 0
            n_abiat = len(text.splitlines(1))
        check = self.parent.db.add_poem(nam, text, sabab, charh, poet, sex, balad, age, 
                                 n_abiat, baher, rawi, kafia, arodh, gharadh, naw3, longer_half)
        self.parent.dawawinpage.refresh_poets()
        self.parent.dawawinpage.search_cb()
        self.parent.organizepage.refresh_poets()
        self.parent.organizepage.search_cb()
        if check == None: daw_customs.info(self.parent, 'تم إضافة القصيدة بنجاح'); return
   
    def change_naw3(self, *a):
        if self.naw3.get_active() == 0:
            self.baher.set_sensitive(True)
            self.rawi.set_sensitive(True)
            self.kafia.set_sensitive(True)
            self.arodh.set_sensitive(True)
        elif self.naw3.get_active() == 1:
            self.baher.set_sensitive(True)
            self.rawi.set_active(-1)
            self.kafia.set_active(-1)
            self.arodh.set_active(-1)
            self.rawi.set_sensitive(False)
            self.kafia.set_sensitive(False)
            self.arodh.set_sensitive(False)
        else:
            self.baher.set_active(-1)
            self.rawi.set_active(-1)
            self.kafia.set_active(-1)
            self.arodh.set_active(-1)
            self.baher.set_sensitive(False)
            self.rawi.set_sensitive(False)
            self.kafia.set_sensitive(False)
            self.arodh.set_sensitive(False)
    
    def a3aridh_elbaher(self, *a):
        if self.baher.get_active() == -1: return
        model = self.arodh.get_model()
        model.clear()
        baher = daw_customs.value_active(self.baher)
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
        self.nasse_bfr.insert_at_cursor(haraka)    
    
    def near_page(self, v):
        self.size_font += v
        self.charh.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.nasse.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.sabab.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.tarjama.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        
    def move_in_page(self, v):
        return
    
    def replace_all(self, *a):
        txt1 = self.ent_replace1.get_text().decode('utf8')
        txt2 = self.ent_replace2.get_text().decode('utf8')
        text = daw_tools.right_space(self.nasse_bfr.get_text(self.nasse_bfr.get_start_iter(),
                                                        self.nasse_bfr.get_end_iter(), False)).decode('utf8')
        if self.reg_exp.get_active(): text_new = re.sub(txt1, txt2, text)
        else: text_new = text.replace(txt1, txt2)
        text_new = daw_tools.right_space(text_new)
        self.nasse_bfr.set_text(text_new)
    
    def change_text(self, *a):
        text = (self.nasse_bfr.get_text(self.nasse_bfr.get_start_iter(), self.nasse_bfr.get_end_iter(), False)).decode('utf8')
        self.list_modifieds.append(text)
        if len(self.list_modifieds) > 1:
            self.redo.set_sensitive(True)
    
    def redo_text(self, *a):
        del self.list_modifieds[-1]
        self.nasse_bfr.set_text(self.list_modifieds[-1])
        del self.list_modifieds[-1]
        del self.list_modifieds[-1]
        if len(self.list_modifieds) == 1:
            self.redo.set_sensitive(False)   
    
    def __init__(self, parent):
        self.parent = parent
        self.list_modifieds = []
        self.size_font = int(self.parent.theme.fontch[-2:])
        Gtk.Box.__init__(self,spacing=7, orientation=Gtk.Orientation.VERTICAL)
        self.nbk = Gtk.Notebook()
        
        self.nasse = daw_customs.ViewEdit()
        self.nasse_bfr = self.nasse.get_buffer()
        self.nasse_bfr.connect('changed', self.change_text)
        self.nasse.connect_after("populate-popup", self.populate_popup)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.nasse)
        vb = Gtk.VBox(False, 0)
        hb = Gtk.HBox(False, 0)
        hb.set_border_width(3)
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
        
        self.replace = Gtk.ToolButton(stock_id=Gtk.STOCK_FIND_AND_REPLACE)
        hb.pack_end(self.replace, False, False, 3)
        self.replace.connect('clicked', self.replace_all)
        self.ent_replace2 = Gtk.Entry()
        self.ent_replace2.set_placeholder_text('المُستبدَل به')
        hb.pack_end(self.ent_replace2, False, False, 3)
        self.ent_replace1 = Gtk.Entry()
        self.ent_replace1.set_placeholder_text('المُستبدَل')
        hb.pack_end(self.ent_replace1, False, False, 3)
        
        self.reg_exp = Gtk.CheckButton('استعمل "re"')
        hb.pack_end(self.reg_exp, False, False, 0)
        
        self.redo = Gtk.ToolButton(stock_id=Gtk.STOCK_REDO)
        self.redo.set_sensitive(False)
        hb.pack_end(self.redo, False, False, 3)
        self.redo.connect('clicked', self.redo_text)
        
        vb.pack_start(scroll, True, True, 0)
        vb.pack_start(hb, False, False, 0)
        self.nbk.append_page(vb, Gtk.Label('نص القصيدة'))
        
        self.vb_info = Gtk.VBox(False, 6)
        self.vb_info.set_border_width(6)
        hb = Gtk.HBox(False, 7)
        la0 = Gtk.Label('اسم القصيدة')
        la0.set_alignment(0,0.5)
        hb.pack_start(la0, False, False, 0)
        self.name_poem = Gtk.Entry()
        self.name_poem.set_placeholder_text('إن لم يكن لها اسم ، اكتب صدر أول بيت بدلا من ذلك')
        hb.pack_start(self.name_poem, True, True, 0)
        self.vb_info.pack_start(hb, False, False, 0)
        
        hb, self.naw3 = daw_customs.combo(daw_tools.elnaw3, u'النوع', 0)
        self.vb_info.pack_start(hb, False, False, 0)
        self.naw3.connect('changed', self.change_naw3)
        
        hb, self.gharadh = daw_customs.combo(daw_tools.elgharadh, u'الغرض', 0)
        self.vb_info.pack_start(hb, False, False, 0)
        
        hb, self.baher = daw_customs.combo(daw_tools.elbehor, u'البحر', 0)
        self.baher.connect('changed', self.a3aridh_elbaher)
        self.vb_info.pack_start(hb, False, False, 0)
        
        hb, self.rawi = daw_customs.combo(daw_tools.elrawi, u'الروي', 0)
        self.vb_info.pack_start(hb, False, False, 0)
        
        hb, self.kafia = daw_customs.combo(daw_tools.elkawafi, u'القافية', 0)
        self.vb_info.pack_start(hb, False, False, 0)
        
        hb, self.arodh = daw_customs.combo(daw_tools.ela3aridh, u'العروض وضربها', 0)
        self.vb_info.pack_start(hb, False, False, 0)
        
        la1 = Gtk.Label('سبب النظم')
        la1.set_alignment(0,1)
        self.vb_info.pack_start(la1, False, False, 0)
        
        self.sabab = daw_customs.ViewEdit()
        self.sabab_bfr = self.sabab.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.sabab)
        self.vb_info.pack_start(scroll, True, True, 0)
        self.nbk.append_page(self.vb_info, Gtk.Label('معلومات القصيدة'))
        
        self.charh = daw_customs.ViewEdit()
        self.charh_bfr = self.charh.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.charh)
        self.nbk.append_page(scroll, Gtk.Label('شرح القصيدة'))
        
        vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(6)
        self.outsider = Gtk.RadioButton.new_with_label_from_widget(None,'لا يعرف قائله')
        self.outsider.connect('toggled',self.is_poet,'1')
        hbox.pack_start(self.outsider, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(6)
        self.present = Gtk.RadioButton.new_with_label_from_widget(self.outsider,'موجود في قاعدة البيانات')
        self.present.connect('toggled',self.is_poet,'2')
        self.poets = Gtk.Entry()
        self.poets.set_placeholder_text('اكتب حرفا لتحصل على التكملة')
        self.poets.set_sensitive(False)
        self.completion03 = Gtk.EntryCompletion()
        self.completion03.set_model(self.parent.dawawinpage.store_poet)
        self.completion03.set_text_column(1)
        self.poets.set_completion(self.completion03)
        hbox.pack_start(self.present, False, False, 0)
        hbox.pack_start(self.poets, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(6)
        self.nopresent = Gtk.RadioButton.new_with_label_from_widget(self.outsider,'غير موجود في قاعدة البيانات')
        self.nopresent.connect('toggled',self.is_poet,'3')
        hbox.pack_start(self.nopresent, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.grd = Gtk.Grid()
        self.grd.set_border_width(6)
        self.grd.set_column_spacing(6)
        self.grd.set_row_spacing(6)
        self.grd.set_sensitive(False)
        vbox.pack_start(self.grd, False, False, 0)
        
        self.grd.attach(Gtk.Label('الاسم المشتهر'), 1, 1, 1, 1)
        self.lak_poet = Gtk.Entry()
        self.lak_poet.set_placeholder_text('الفرزدق')
        self.grd.attach(self.lak_poet, 2, 1, 2, 1)
        
        self.grd.attach(Gtk.Label('الاسم الحقيقي'), 4, 1, 1, 1)
        self.nm_poet = Gtk.Entry()
        self.nm_poet.set_placeholder_text('همام بن غالب بن صعصعة التميمي')
        self.grd.attach(self.nm_poet, 5, 1, 4, 1)
        
        hb, self.ages = daw_customs.combo(daw_tools.age_poet, u'العصر', 0)
        self.ages.connect('changed', self.select_age)
        self.grd.attach(hb, 1, 2, 2, 1)
        
        hb, self.lands = daw_customs.combo(daw_tools.elbalad, u'البلد', 0)
        self.grd.attach(hb, 3, 2, 2, 1)
        
        hb, self.sexs = daw_customs.combo(daw_tools.sex_poet, u'الجنس', 0)
        self.grd.attach(hb, 5, 2, 2, 1)
        
        self.death = Gtk.CheckButton('الوفاة (هـ)')
        def is_dh(widget, *a):
            if self.death.get_active():
                self.dh_poet.set_sensitive(True)
            else:
                self.dh_poet.set_sensitive(False)
        self.death.connect('toggled', is_dh)
        self.grd.attach(self.death, 7, 2, 1, 1)
        adj = Gtk.Adjustment(1434, -300, 1434, 1, 5.0, 0.0)
        self.dh_poet = Gtk.SpinButton()
        self.dh_poet.set_sensitive(False)
        self.dh_poet.set_adjustment(adj)
        self.dh_poet.set_wrap(True)
        self.grd.attach(self.dh_poet, 8, 2, 1, 1)
        
        self.tarjama = daw_customs.ViewEdit()
        self.tarjama_bfr = self.tarjama.get_buffer()
        self.tarjama_bfr.set_text('ترجمة الشاعر')
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tarjama)
        vbox.pack_start(scroll, True, True, 0)
        self.tarjama.set_sensitive(False)
        self.nbk.append_page(vbox, Gtk.Label('الشاعر'))
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.accept = daw_customs.ButtonClass('إضافة القصيدة')
        self.accept.connect('clicked',self.adding)
        hbox.pack_start(self.accept, False, False, 0)
        
        self.all_poems = Gtk.CheckButton('نمط إضافة عدة قصائد')
        def all_poems_cb(widget, *a):
            if self.all_poems.get_active():
                self.vb_info.set_sensitive(False)
            else:
                self.vb_info.set_sensitive(True)
        self.all_poems.connect('toggled', all_poems_cb)
        hbox.pack_start(self.all_poems, False, False, 0)

        self.pack_start(self.nbk, True, True, 0)
        self.pack_start(hbox, False, False, 0)
        
        self.show_all()
        