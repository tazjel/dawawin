# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk, Pango
import daw_customs, daw_scan, daw_araby, daw_tools
from daw_contacts import HelpDB
from os.path import join

Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)

# class صفحة العروض-------------------------------------------------------------------

class Metrics(Gtk.Notebook):
   
    def search_on_page(self, text):
        return
   
    def near_page(self, v):
        self.size_font += v
        self.view_info.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.view_scan.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.prescript.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
        self.zihaf_info.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
   
    def move_in_page(self, v):
        n = self.get_current_page()
        if n == 1:
            model, i = self.tree_mekaddima.get_selection().get_selected()
            if i:
                p = model.get_path(i).get_indices()[0]
                if p+v == -1 or p+v == len(model): return
                i1 = model.get_iter((p+v,))
                self.tree_mekaddima.get_selection().select_iter(i1)
                self.tree_mekaddima.scroll_to_cell((p+v,))
            elif len(self.tree_mekaddima.get_model()) == 0: return
            else:
                i2 = model.get_iter((0,))
                self.tree_mekaddima.get_selection().select_iter(i2)
                self.tree_mekaddima.scroll_to_cell((0,))
            self.show_page_mekadimat()
        elif n == 2:
            model, ii = self.tree_behor.get_selection().get_selected()
            if ii:
                p = model.get_path(ii).get_indices()[0]
                if p+v == -1 or p+v == len(model): return
                ii1 = model.get_iter((p+v,))
                self.tree_behor.get_selection().select_iter(ii1)
                self.tree_behor.scroll_to_cell((p+v,))
            elif len(self.tree_behor.get_model()) == 0: return
            else:
                ii2 = model.get_iter((0,))
                self.tree_behor.get_selection().select_iter(ii2)
                self.tree_behor.scroll_to_cell((0,))
            self.show_page_behor()
   
    def __init__(self, parent):
        self.parent = parent
        self.myhelp = HelpDB()
        self.size_font = int(self.parent.theme.fontch[-2:])
        Gtk.Notebook.__init__(self)
        self.build()
    
    def scan_cb(self, *a):
        v = 0
        if self.ishbaa_m.get_active(): v = 1
        text = self.verse_dictation_bfr.get_text(self.verse_dictation_bfr.get_start_iter(),
                                self.verse_dictation_bfr.get_end_iter(), False).decode('utf8')
        if text != '':
            wazn = daw_scan.writing_wazn(text, v)
            ls_awzan = daw_scan.meter_verse(wazn)
            text1 = daw_scan.writing_spoken(text, v)
            if len(ls_awzan) == 0:
                daw_customs.erro(self.parent, u'''
لم يستطع البرنامج تحديد بحر هذا البيت
هل جميع الأحرف المنطوقة مكتوبة في الكتابة العروضية ؟
إن لم تكن ، فقد يكون الخطأ في التشكيل !.''')
                takti31= daw_scan.writing_scan(text, v)
                result = u'الكتابة العروضية :     '+text1+'\n'
                result += u'الكتابة التقطيعية :     '+takti31+'\n'
            else:
                result = u'الكتابة العروضية :     '+text1+'\n'
                result += u'الكتابة التقطيعية :     '+ls_awzan[0][4]+'\n'
                s = 1
                if len(ls_awzan) > 1: result += u'هذا الوزن ينتمي لأكثر من بحر فقد يكون : \n'.format(str(s),) 
                for a in ls_awzan:
                    t = a[3].split(' ')
                    if s > 1: result += u'وقد يكون : *****************************************\n'.format(str(s),) 
                    result += u'البحر :     '+daw_scan.Elbehor[a[1]]+'\n'
                    result += u'الكتابة التفعيلية :     '+a[3]+'\n'
                    if a[7] != u'':
                        result += u'******* الصدر *******\n'
                    result += u'التفعيلة الأولى :     '+a[10]+'\n'
                    if len(t) != 5 and len(t) != 2:
                        result += u'التفعيلة الثانية :     '+a[12]+'\n'
                    if len(t) == 9:
                        result += u'التفعيلة الثالثة :     '+a[14]+'\n'
                    result += u'العروض :     '+a[6]+'\n'
                    if a[7] != u'':
                        result += u'******* العجز *******\n'
                        if len(t) == 5:
                            result += u'التفعيلة الأولى :     '+a[12]+'\n'
                        elif len(t) == 7:
                            result += u'التفعيلة الأولى :     '+a[14]+'\n'
                            result += u'التفعيلة الثانية :     '+a[16]+'\n'
                        elif len(t) == 9:
                            result += u'التفعيلة الأولى :     '+a[16]+'\n'
                            result += u'التفعيلة الثانية :     '+a[18]+'\n'
                            result += u'التفعيلة الثالثة :     '+a[20]+'\n'
                    if a[7] != u'':
                        result += u'الضرب :     '+a[8]+'\n'
                    s += 1
            self.view_scan_bfr.set_text(result)
            daw_customs.with_tag(self.view_scan_bfr, self.title_tag2, 
                             [u'الكتابة العروضية :',u'الكتابة التقطيعية :', 
                              u'البحر :', u'الكتابة التفعيلية :', u'العروض :', u'الضرب :',
                              u'******* العجز *******', u'التفعيلة الأولى : ', u'التفعيلة الثانية :', 
                              u'التفعيلة الثالثة :', u'******* الصدر *******'])
    
    def tashkeel_cb(self, btn, haraka):
        self.verse_dictation_bfr.insert_at_cursor(haraka)
    
    def show_page_mekadimat(self, *a):
        model, i = self.sel_mekaddima.get_selected()
        if i:
            v = model.get_value(i,1)
            txt = self.myhelp.show_page_mekadimat(v)
            self.prescript_bfr.set_text(txt[0][0])
    
    def show_page_behor(self, *a):
        model, i = self.sel_behor.get_selected()
        if i:
            v = model.get_value(i,1)
            txt = self.myhelp.show_page_behor(v)
            self.view_info_bfr.set_text(txt[0][0])
    
    def change_taf3ila(self, *a):
        if self.taf3ila.get_active() == -1: return
        model1 = self.takiir.get_model()
        model2 = self.sabab.get_model()
        model1.clear()
        model2.clear()
        taf3ila = daw_customs.value_active(self.taf3ila)
        for a in daw_scan.Changes[taf3ila].keys():
            if a in daw_scan.Zihafat_ta3rif.keys():
                model1.append([a, daw_scan.Changes[taf3ila][a]])
                model2.append([a, daw_scan.Zihafat_ta3rif[a][0]])
   
    def change_sabab(self, *a):
        sabab= daw_customs.value_active(self.sabab)
        model = self.takiir.get_model()
        ls = []
        for a in model:
            ls.append(a)
        idx = daw_tools.get_index(ls, sabab)
        if idx == None: return
        self.takiir.set_active(idx)
        self.zihaf_info_bfr.set_text(daw_scan.Zihafat_ta3rif[sabab][1])
                
    def change_takiir(self, *a):
        takiir= daw_customs.value_active(self.takiir)
        model = self.sabab.get_model()
        ls = []
        for a in model:
            ls.append(a)
        idx = daw_tools.get_index(ls, takiir)
        if idx == None: return
        self.sabab.set_active(idx) 
        self.zihaf_info_bfr.set_text(daw_scan.Zihafat_ta3rif[takiir][1]) 
        
    def build(self, *a):
        
        #a صفحة تقطيع الأبيات الشعرية--------------------------------------------
        vb3 = Gtk.VBox(False, 3)
        info = '''
        - يجب تشكيل البيت شكلا تاما
        - الحرف العاري عن التشكيل يعتبر ساكنا
        - يجب حذف جميع الرموز والأعداد
        - الكتابة العروضية هي كتابة الأحرف الملفوظة
        - الحرف إن كان ملفوظا ولم يكن في الكتابة العروضية
           فهو خطأ قديكون بسبب عدم تشكيله إن كان متحركا
           أوعدم تشكيل الحرف الذي يليه إن كان ساكنا 
        - قد يشبع البرنامج ما لا يستحق الإشباع لذلك ينصح
           باختيار الإشباع يدويا وتقوم بزيادة حرف المد
           إلى ما يستحق الإشباع دون غيره
        '''
        hb = Gtk.HBox(False, 10)
        vbox = Gtk.VBox(False, 1)
        self.verse_dictation = daw_customs.ViewEdit()
        self.verse_dictation_bfr = self.verse_dictation.get_buffer()
        self.verse_dictation.override_font(Pango.FontDescription('Simplified Naskh 22'))
        self.verse_dictation.set_size_request(-1, 64)
        hb.pack_start(self.verse_dictation, True, True, 0)
        scan_btn = daw_customs.ButtonClass('تقطيع البيت')
        scan_btn.connect('clicked', self.scan_cb)
        vbox.pack_start(scan_btn, False, False, 0)
        info_btn = daw_customs.ButtonClass('إرشادات')
        info_btn.connect('clicked', lambda *a: self.view_scan_bfr.set_text(info))
        vbox.pack_start(info_btn, False, False, 0)
        hb.pack_start(vbox, False, False, 0)
        vb3.pack_start(hb, False, False, 3)
        
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
        
        self.ishbaa_m = Gtk.CheckButton('معالجة إشباع ميم وهاء الضمير يدويا')
        hb.pack_start(self.ishbaa_m, False, False, 15)
        vb3.pack_start(hb, False, False, 3)
        
        self.view_scan = daw_customs.ViewClass()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.view_scan)
        self.view_scan_bfr = self.view_scan.get_buffer()
        self.view_scan_bfr.set_text(info)
        self.title_tag2 = self.view_scan_bfr.create_tag("title")
        self.title_tag2.set_property('foreground', self.parent.theme.coloran) 
        vb3.pack_start(scroll, True, True, 0)
        self.append_page(vb3, Gtk.Label("تقطيع الأبيات"))
        
        #a صفحة المقدمات العروضية--------------------------------------
        self.store_mekaddima = Gtk.ListStore(str, int)
        mekadimat = self.myhelp.titles_mekadimat()
        for a in mekadimat:
            self.store_mekaddima.append([a[1], a[0]])
        hp0 = Gtk.HPaned()
        self.tree_mekaddima = daw_customs.TreeClass()
        self.sel_mekaddima = self.tree_mekaddima.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('الفهرس', cell, text=0)
        self.tree_mekaddima.append_column(kal)
        self.tree_mekaddima.set_model(self.store_mekaddima)
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(200, -1)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.tree_mekaddima)
        self.tree_mekaddima.connect("cursor-changed", self.show_page_mekadimat)
        hp0.pack1(scroll, False, False)
        self.prescript = daw_customs.ViewClass()
        self.prescript_bfr = self.prescript.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.prescript)
        hp0.pack2(scroll, True, True)
        self.append_page(hp0, Gtk.Label("مقدمات مهمة"))
        
        #a صفحة البحور الشعرية--------------------------------------------
        hb1 = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        self.tree_behor = daw_customs.TreeClass()
        self.sel_behor = self.tree_behor.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('البحور', cell, text=0)
        self.tree_behor.append_column(kal)
        self.store_behor = Gtk.ListStore(str, int)
        behor = self.myhelp.titles_behor()
        for a in behor:
            self.store_behor.append([a[1], a[0]])
        self.tree_behor.set_model(self.store_behor)
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(150, -1)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.tree_behor)
        self.tree_behor.connect("cursor-changed", self.show_page_behor)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        hb1.pack_start(scroll, False, False, 0)
        self.view_info = daw_customs.ViewClass()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add_with_viewport(self.view_info)
        self.view_info_bfr = self.view_info.get_buffer()
        hb1.pack_start(scroll, True, True, 0)
        self.append_page(hb1, Gtk.Label("بحور الشعر"))
        
        #a صفحة الزحافات والعلل--------------------------------------------
        vb4 = Gtk.VBox(False, 0)    
        hbox = Gtk.HBox(False, 12)
        ls = [] 
        for a in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
            ls.append([a, daw_scan.Taf3ilat[a]])
        hb, self.taf3ila = daw_customs.combo(ls, u'التفعيلة', 0)
        hbox.pack_start(hb, False, False, 0)
        self.taf3ila.connect('changed', self.change_taf3ila)

        self.ls_takiir = [] 
        hb, self.takiir = daw_customs.combo(self.ls_takiir, u'التغيير', 0)
        hbox.pack_start(hb, False, False, 0)
        self.takiir.connect('changed', self.change_takiir)

        self.ls_sabab = [] 
        hb, self.sabab = daw_customs.combo(self.ls_sabab, u'السبب', 0)
        hbox.pack_start(hb, False, False, 0)
        self.sabab.connect('changed', self.change_sabab)
        
        self.zihaf_info = daw_customs.ViewClass()
        self.zihaf_info_bfr = self.zihaf_info.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.zihaf_info)
        vb4.pack_start(hbox, False, False, 7)
        vb4.pack_start(scroll, True, True, 0)
        self.append_page(vb4, Gtk.Label("الزحافات والعلل"))
        
        self.show_all()
