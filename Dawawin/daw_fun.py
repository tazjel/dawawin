# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk, Pango
from daw_contacts import MyDB
import daw_customs, daw_tools, daw_araby
import random


# class صفحة التسلية-------------------------------------------------------------------    

class MyFun(Gtk.Notebook):
    
    def search_on_page(self, text):
        return
    
    def move_in_page(self, v):
        return
    
    def near_page(self, v):
        return
    
    # a عند الضغط على اعتمد في صفحة المساجلة---------------------------------------
    
    def ok_verse_cb(self, *a):
        all_verse = self.verse_all_bfr.get_text(self.verse_all_bfr.get_start_iter(),
                self.verse_all_bfr.get_end_iter(), False).decode('utf8')
        verse0 = self.verse_prog_bfr.get_text(self.verse_prog_bfr.get_start_iter(),
                self.verse_prog_bfr.get_end_iter(), False).decode('utf8')
        rawi0 = daw_araby.NAMES[daw_tools.rawi_poem(verse0.strip())]
        verse1 = self.verse_usr_bfr.get_text(self.verse_usr_bfr.get_start_iter(),
                self.verse_usr_bfr.get_end_iter(), False).decode('utf8')
        if verse1 == u'' : return
        rawi1 = daw_araby.NAMES[daw_tools.rawi_poem(verse1.strip())]
        first1 = daw_araby.NAMES[verse1.strip()[0]]
        if first1 != rawi0:
            daw_customs.erro(self.parent, 'البيت يبدأ بحرف غير الذي انتهى به الأول\nحاول مجددا .')
            return
        if self.db.is_verse(verse1):
            if daw_araby.fuzzy_plus(verse1) in daw_araby.fuzzy_plus(all_verse):
                daw_customs.erro(self.parent, 'البيت مستخدم مسبقا\nحاول مجددا .')
                return
            else:
                daw_customs.info(self.parent, 'أحسنت')
                self.verse_all_bfr.insert(self.verse_all_bfr.get_end_iter(), u'\nالمستخدم : '+verse1.strip())
                d = int(self.lab_answer_user.get_label())+1
                self.lab_answer_user.set_label(str(d))
                self.next_verse(rawi1)
        else:
            daw_customs.erro(self.parent, 'البيت غير موجود في قاعدة بيانات البرنامج\nحاول مجددا .')
            return
        daw_customs.with_tag(self.verse_all_bfr, self.verse_all_tag, ['البرنامج : ',])
        self.verse_all.scroll_to_iter(self.verse_all_bfr.get_end_iter(), 0, 1, 1, 1)
    
    # a عند الضغط على جديد في صفحة المساجلة---------------------------------------
    
    def skip_verse_cb(self, *a):
        self.new_verse_debate()
    
    # a معالجة التقييم في صفحة من القائل ؟--------------------------------------------
    
    def appraisal_who(self, *a):
        c = int(self.lab_correct_who.get_label())
        f = int(self.lab_false_who.get_label())
        s = int(self.lab_skip_who.get_label())
        if c == 0 and f == 0:
            t = (c*100)/(s+c)
        elif c == 0 and s == 0:
            t = (c*100)/(c+f)
        else:
            t = (((c*100)/(s+c))+((c*100)/(c+f)))/2
        ls_appraisal = [u'سيئ',u'ضعيف',u'متوسط',u'حسن',u'جيد',u'ممتاز']
        if t == 0: t = 15
        self.lab_appraisal_who.set_label(ls_appraisal[(t/15)-1])
    
    # a عند الضغط على أجب في صفحة من القائل ؟-----------------------------------------
    
    def answer_who_cb(self, *a):
        self.choice_1.set_sensitive(False)
        self.choice_2.set_sensitive(False)
        self.choice_3.set_sensitive(False)
        self.answer_who.set_sensitive(False)
        daw_customs.info(self.parent, u'القائل هو {}'.format(self.who_speaker, ))
        d = int(self.lab_skip_who.get_label())+1
        self.lab_skip_who.set_label(str(d))
        self.new_verse_who()
        self.appraisal_who()
    
    # a عند الضغط على جديد في صفحة من القائل ؟----------------------------------------- 
    
    def new_who_cb(self, *a):
        if self.choice_1.get_active() or self.choice_2.get_active() or self.choice_3.get_active():
            pass
        else:
            d = int(self.lab_skip_who.get_label())+1
            self.lab_skip_who.set_label(str(d))
        self.new_verse_who()
        self.appraisal_who()
     
    # a عند الضغط على أجب في صفحة المساجلة---------------------------------------
        
    def answer_verse_cb(self, *a):
        verse = self.verse_prog_bfr.get_text(self.verse_prog_bfr.get_start_iter(),
                self.verse_prog_bfr.get_end_iter(), False).decode('utf8')
        rawi = daw_araby.NAMES[daw_tools.rawi_poem(verse.strip())]
        self.verse_all_bfr.insert(self.verse_all_bfr.get_end_iter(), '\nالمستخدم : لم يجب')
        self.next_verse(rawi)
        daw_customs.with_tag(self.verse_all_bfr, self.verse_all_tag, ['البرنامج : ',])
        self.verse_all.scroll_to_iter(self.verse_all_bfr.get_end_iter(), 0, 1, 1, 1)
    
    # a البيت الجديد الخاص بالبرنامج في صفحة المساجلة---------------------------- 
    
    def next_verse(self, rawi):
        all_verse = self.verse_all_bfr.get_text(self.verse_all_bfr.get_start_iter(),
                self.verse_all_bfr.get_end_iter(), False).decode('utf8')
        if rawi == u'همزة':
            r = u'أ'
        elif rawi == u'ألف':
            r = u'ا'
        else:
            r = rawi[0]
        verses = self.db.first_in_verse(r)
        random.shuffle(verses)
        if len(verses) == 0: 
            daw_customs.erro(self.parent, 'لا يوجد بيت جديد يبدأ بحرف {}'.format(rawi,))
            return
        else:
            for a in verses:
                if daw_araby.fuzzy_plus(a[0]) not in daw_araby.fuzzy_plus(all_verse):
                    self.verse_prog_bfr.set_text(a[0].strip())
                    self.verse_all_bfr.insert(self.verse_all_bfr.get_end_iter(), u'\nالبرنامج : '+a[0].strip())
                    d = int(self.lab_answer_prog.get_label())+1
                    self.lab_answer_prog.set_label(str(d))
                    self.verse_usr_bfr.set_text('')
                    i = self.db.id_poet(a[1])
                    self.lab_speaker0.set_label(self.db.name_poet(i)[1])
                    if a[0] == None: return
                    r = self.db.rawi_poem(a[1])
                    rawi = daw_araby.NAMES[daw_tools.rawi_poem(a[0].strip())]
                    self.lab_rawi.set_label(rawi)
                    return
            daw_customs.erro(self.parent, 'لا يوجد بيت جديد يبدأ بحرف {}'.format(rawi,))
    
    # a معالجة التقييم في صفحة رتب البيت-------------------------------------------- 
    
    def appraisal(self, *a):
        c = int(self.lab_correct.get_label())
        f = int(self.lab_false.get_label())
        s = int(self.lab_skip.get_label())
        if c == 0 and f == 0:
            t = (c*100)/(s+c)
        elif c == 0 and s == 0:
            t = (c*100)/(c+f)
        else:
            t = (((c*100)/(s+c))+((c*100)/(c+f)))/2
        ls_appraisal = [u'سيئ',u'ضعيف',u'متوسط',u'حسن',u'جيد',u'ممتاز']
        if t == 0: t = 15
        self.lab_appraisal.set_label(ls_appraisal[(t/15)-1])
    
    # a عند الضغط على تحقق في صفحة رتب البيت-------------------------------------------- 
    
    def check_verse_cb(self, *a):
        half1 = ''
        half2 = ''
        if self.verse == None : return
        l_v = self.verse.split('*')
        chs1 = self.box_half1.get_children()
        for ch1 in chs1:
            nm = ch1.get_name()
            half1 += nm+" "
        chs2 = self.box_half2.get_children()
        for ch2 in chs2:
            nm = ch2.get_name()
            half2 += nm+" "
        if half1.strip().decode('utf8') == l_v[0].strip() and half2.strip().decode('utf8') == l_v[1].strip():
            daw_customs.info(self.parent, 'أحسنت ..!!!')
            d = int(self.lab_correct.get_label())+1
            self.lab_correct.set_label(str(d))
            self.new_verse_organize()
        else:
            daw_customs.info(self.parent, 'حاول مرة أخرى ..!!!')
            d = int(self.lab_false.get_label())+1
            self.lab_false.set_label(str(d))
        self.appraisal()
    
    # a عند الضغط على جديد في صفحة رتب البيت-------------------------------------------- 
    
    def new_verse_cb(self, *a):
        self.new_verse_organize()
        if self.verse == None : return
        d = int(self.lab_skip.get_label())+1
        self.lab_skip.set_label(str(d))
        self.appraisal()
        self.check_verse.set_sensitive(True)
    
    # a ترتيب البيت آليا في صفحة رتب البيت----------------------------------
    
    def org_verse_cb(self, *a):
        if self.verse == None : return
        lst_verse = self.verse.split('*')
        lst_half1 = lst_verse[0].strip().split(' ')
        lst_half2 = lst_verse[1].strip().split(' ')
        #---------------------
        chs1 = self.box_half1.get_children()
        for ch1 in chs1:
            ch1.destroy()
        for a1 in lst_half1:
            btn = Gtk.Button(a1)
            btn.connect('clicked', self.org_btn, 1)
            label = Gtk.Label()
            label.set_text(a1)
            pangolayout = label.get_layout()
            d1 = pangolayout.get_pixel_size()
            w1 = d1[0]+10
            btn.set_size_request(w1, 50)
            btn.set_name(a1)
            self.box_half1.pack_start(btn, False, False, 0)
        #--------------------------    
        chs2 = self.box_half2.get_children()
        for ch2 in chs2:
            ch2.destroy()
        for a2 in lst_half2:
            btn = Gtk.Button(a2)
            label = Gtk.Label()
            label.set_text(a2)
            pangolayout = label.get_layout()
            d2 = pangolayout.get_pixel_size()
            w2 = d2[0]+10
            btn.set_size_request(w2, 50)
            btn.set_name(a2)
            btn.connect('clicked', self.org_btn, 2)
            self.box_half2.pack_start(btn, False, False, 0)
        self.box_half1.show_all()
        self.box_half2.show_all()
        self.check_verse.set_sensitive(False)
    
    # a عند الضغط على كلمة في صفحة رتب البيت------------------------------------
    
    def org_btn(self, btn, v):
        a1 = btn.get_name()
        btn.destroy()
        btn_new = Gtk.Button(a1)
        label = Gtk.Label()
        label.set_text(a1)
        pangolayout = label.get_layout()
        d1 = pangolayout.get_pixel_size()
        w1 = d1[0]+10
        btn_new.set_size_request(w1, 50)
        btn_new.set_name(a1)
        if v == 1:
            btn_new.connect('clicked', self.org_btn, 1)
            self.box_half1.pack_start(btn_new, False, False, 0)
            self.box_half1.show_all()
        elif v == 2:
            btn_new.connect('clicked', self.org_btn, 2)
            self.box_half2.pack_start(btn_new, False, False, 0)
            self.box_half2.show_all()
    
    # a عند اختيار القائل في صفحة من القائل----------------------------------------
        
    def choice_speaker(self, *a):
        self.choice_1.set_sensitive(False)
        self.choice_2.set_sensitive(False)
        self.choice_3.set_sensitive(False)
        self.answer_who.set_sensitive(False)
        if self.choice_1.get_active() and self.entry_speaker_1.get_text().decode('utf8') == self.who_speaker:
            daw_customs.info(self.parent, u'أحسنت القائل هو {}'.format(self.who_speaker, ))
            d = int(self.lab_correct_who.get_label())+1
            self.lab_correct_who.set_label(str(d))
        elif self.choice_2.get_active() and self.entry_speaker_2.get_text().decode('utf8') == self.who_speaker:
            daw_customs.info(self.parent, u'أحسنت القائل هو {}'.format(self.who_speaker, ))
            d = int(self.lab_correct_who.get_label())+1
            self.lab_correct_who.set_label(str(d))
        elif self.choice_3.get_active() and self.entry_speaker_3.get_text().decode('utf8') == self.who_speaker:
            daw_customs.info(self.parent, u'أحسنت القائل هو {}'.format(self.who_speaker, ))
            d = int(self.lab_correct_who.get_label())+1
            self.lab_correct_who.set_label(str(d))
        else:
            if self.choice_1.get_active() or self.choice_2.get_active() or self.choice_3.get_active():
                daw_customs.erro(self.parent, u'أخطأت !! القائل هو {}'.format(self.who_speaker, ))
                d = int(self.lab_false_who.get_label())+1
                self.lab_false_who.set_label(str(d))
        self.new_verse_who()
        self.appraisal_who()
    
    # a إعادة بيت ومعرف قصيدته بعد اختياره  عشوائيا------------------------------------
        
    def chose_verse(self, *a):
        list_poems_id = self.db.all_poems_id()
        if len(list_poems_id)== 0 : return
        id_poem = random.choice(list_poems_id)
        poem, sb, ch, t3 = self.db.get_poem(id_poem)
        if '*' in poem:
            lst_new = []
            lst_poem = poem.splitlines(1)
            for a in lst_poem:
                if '*' in a:
                    lst_new.append(a)
            verse = random.choice(lst_new)
            return verse, id_poem
        else:
            self.chose_verse()
    
    # a بيت جديد في صفحة من القائل ؟-------------------------------------------- 
            
    def new_verse_who(self, *a):
        try: verse, id_poem = self.chose_verse()
        except: return
        i = self.db.id_poet(id_poem)
        self.who_speaker = self.db.name_poet(i)[1]
        if verse == None: return
        self.verse_who_bfr.set_text(verse.strip())
        i1, i2 = self.db.two_poet(i)
        who_speaker_1 = self.db.name_poet(i1)[1]
        who_speaker_2 = self.db.name_poet(i2)[1]
        ls = [self.who_speaker, who_speaker_1, who_speaker_2]
        random.shuffle(ls)
        self.entry_speaker_1.set_text(ls[0])
        self.entry_speaker_2.set_text(ls[1])
        self.entry_speaker_3.set_text(ls[2])
        self.choice_1.set_active(False)
        self.choice_2.set_active(False)
        self.choice_3.set_active(False)
        self.choice_1.set_sensitive(True)
        self.choice_2.set_sensitive(True)
        self.choice_3.set_sensitive(True)
        self.answer_who.set_sensitive(True)
    
    # a بيت جديد في صفحة المساجلة-------------------------------------------- 
        
    def new_verse_debate(self, *a):
        try: verse, id_poem = self.chose_verse()
        except: return
        i = self.db.id_poet(id_poem)
        self.lab_speaker0.set_label(self.db.name_poet(i)[1])
        if verse == None: return
        r = self.db.rawi_poem(id_poem)
        rawi = daw_araby.NAMES[daw_tools.rawi_poem(verse.strip())]
        self.lab_rawi.set_label(rawi)
        self.verse_prog_bfr.set_text(verse.strip())
        self.verse_all_bfr.set_text(u'البرنامج : '+verse.strip())
        self.verse_usr_bfr.set_text('')
        self.lab_answer_prog.set_label('0')
        self.lab_answer_user.set_label('0')
    
    # a بيت جديد في صفحة رتب البيت--------------------------------------------        
        
    def new_verse_organize(self, *a):
        try: self.verse, id_poem = self.chose_verse()
        except: return
        i = self.db.id_poet(id_poem)
        self.lab_speaker.set_label(self.db.name_poet(i)[1])
        if self.verse == None: return
        lst_verse = self.verse.split('*')
        lst_half1 = lst_verse[0].strip().split(' ')
        lst_half2 = lst_verse[1].strip().split(' ')
        random.shuffle(lst_half1)
        random.shuffle(lst_half2)
        #---------------------
        chs1 = self.box_half1.get_children()
        for ch1 in chs1:
            ch1.destroy()
        for a1 in lst_half1:
            btn = Gtk.Button(a1)
            btn.connect('clicked', self.org_btn, 1)
            label = Gtk.Label()
            label.set_text(a1)
            pangolayout = label.get_layout()
            d1 = pangolayout.get_pixel_size()
            w1 = d1[0]+10
            btn.set_size_request(w1, 50)
            btn.set_name(a1)
            self.box_half1.pack_start(btn, False, False, 0)
        #--------------------------    
        chs2 = self.box_half2.get_children()
        for ch2 in chs2:
            ch2.destroy()
        for a2 in lst_half2:
            btn = Gtk.Button(a2)
            label = Gtk.Label()
            label.set_text(a2)
            pangolayout = label.get_layout()
            d2 = pangolayout.get_pixel_size()
            w2 = d2[0]+10
            btn.set_size_request(w2, 50)
            btn.set_name(a2)
            btn.connect('clicked', self.org_btn, 2)
            self.box_half2.pack_start(btn, False, False, 0)
        self.box_half1.show_all()
        self.box_half2.show_all()
    
    def __init__(self, parent):
        self.parent = parent
        self.db = MyDB()
        Gtk.Notebook.__init__(self)
        
        # a --------------------------------------------
        vb1 = Gtk.VBox(False, 11)
        vb1.set_border_width(11)
        hb = Gtk.HBox(False, 11)
        self.verse_prog = daw_customs.ViewClass()
        self.verse_prog_bfr = self.verse_prog.get_buffer()
        self.verse_prog.override_font(Pango.FontDescription('Simplified Naskh 22'))
        self.verse_prog.set_size_request(-1, 64)
        hb.pack_start(Gtk.Label('البرنامج'), False, False, 0)
        hb.pack_start(self.verse_prog, True, True, 0)
        vb1.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_0 = Gtk.Label('القائل : ')
        lab_0.set_alignment(0, 0.5)
        hb.pack_start(lab_0, False, False, 0)
        self.lab_speaker0 = Gtk.Label()
        hb.pack_start(self.lab_speaker0, False, False, 0)
        lab_1 = Gtk.Label('                     الروي : ')
        lab_1.set_alignment(0, 0.5)
        hb.pack_start(lab_1, False, False, 0)
        self.lab_rawi = Gtk.Label()
        hb.pack_start(self.lab_rawi, False, False, 0)
        vb1.pack_start(hb, False, False, 0)
        
        vb1.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 11)
        self.verse_usr = daw_customs.ViewEdit()
        self.verse_usr_bfr = self.verse_usr.get_buffer()
        self.verse_usr.override_font(Pango.FontDescription('Simplified Naskh 22'))
        self.verse_usr.set_size_request(-1, 64)
        hb.pack_start(Gtk.Label('المستخدم'), False, False, 0)
        hb.pack_start(self.verse_usr, True, True, 0)
        vb1.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 11)
        self.ok_verse = daw_customs.ButtonClass('اعتمدْ')
        self.ok_verse.connect('clicked', self.ok_verse_cb)
        hb.pack_start(self.ok_verse, False, False, 0)
        self.answer_verse = daw_customs.ButtonClass('أجبْ')
        self.answer_verse.connect('clicked', self.answer_verse_cb)
        hb.pack_start(self.answer_verse, False, False, 0)
        self.skip_verse = daw_customs.ButtonClass('جديد')
        self.skip_verse.connect('clicked', self.skip_verse_cb)
        hb.pack_start(self.skip_verse, False, False, 0)
        
        self.lab_answer_user = Gtk.Label(0)
        hb.pack_end(self.lab_answer_user, False, False, 0)
        lab_2 = Gtk.Label('       المستخدم : ')
        lab_2.set_alignment(0, 0.5)
        hb.pack_end(lab_2, False, False, 0)
        
        self.lab_answer_prog = Gtk.Label(0)
        hb.pack_end(self.lab_answer_prog, False, False, 0)
        lab_1 = Gtk.Label('البرنامج : ')
        lab_1.set_alignment(0, 0.5)
        hb.pack_end(lab_1, False, False, 0)
        vb1.pack_start(hb, False, False, 0)
        
        self.verse_all = daw_customs.ViewClass()
        self.verse_all_bfr = self.verse_all.get_buffer()
        self.verse_all_tag = self.verse_all_bfr.create_tag("prog")
        self.verse_all_tag.set_property('foreground', self.parent.theme.coloran) 
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.verse_all)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vb1.pack_start(scroll, True, True, 0)
        self.verse_all.override_font(Pango.FontDescription('Simplified Naskh 14'))
        self.new_verse_debate()
        self.append_page(vb1, Gtk.Label('مساجلة شعرية'))
        
        # a --------------------------------------------
        vb2 = Gtk.VBox(False, 11)
        vb2.set_border_width(11)
        hb = Gtk.HBox(False, 11)
        self.verse_who = daw_customs.ViewClass()
        self.verse_who_bfr = self.verse_who.get_buffer()
        self.verse_who.override_font(Pango.FontDescription('Simplified Naskh 22'))
        self.verse_who.set_size_request(-1, 64)
        hb.pack_start(Gtk.Label('البيت'), False, False, 0)
        hb.pack_start(self.verse_who, True, True, 0)
        vb2.pack_start(hb, False, False, 0)
        
        vb2.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 11)
        self.answer_who = daw_customs.ButtonClass('أجبْ')
        self.answer_who.connect('clicked', self.answer_who_cb)
        hb.pack_start(self.answer_who, False, False, 0)
        self.new_who = daw_customs.ButtonClass('جديد')
        self.new_who.connect('clicked', self.new_who_cb)
        hb.pack_start(self.new_who, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        vb2.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        self.choice_1 = Gtk.CheckButton('')
        hb.pack_start(self.choice_1, False, False, 0)
        self.choice_1.connect('toggled', self.choice_speaker)
        self.entry_speaker_1 = Gtk.Entry()
        self.entry_speaker_1.set_size_request(400,-1)
        self.entry_speaker_1.set_editable(False)
        hb.pack_start(self.entry_speaker_1, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        self.choice_2 = Gtk.CheckButton('')
        hb.pack_start(self.choice_2, False, False, 0)
        self.choice_2.connect('toggled', self.choice_speaker)
        self.entry_speaker_2 = Gtk.Entry()
        self.entry_speaker_2.set_size_request(400,-1)
        self.entry_speaker_2.set_editable(False)
        hb.pack_start(self.entry_speaker_2, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        self.choice_3 = Gtk.CheckButton('')
        hb.pack_start(self.choice_3, False, False, 0)
        self.choice_3.connect('toggled', self.choice_speaker)
        self.entry_speaker_3 = Gtk.Entry()
        self.entry_speaker_3.set_size_request(400,-1)
        self.entry_speaker_3.set_editable(False)
        hb.pack_start(self.entry_speaker_3, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        vb2.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_1 = Gtk.Label('الإجابات الصحيحة : ')
        lab_1.set_alignment(0, 0.5)
        lab_1.set_size_request(180, -1)
        hb.pack_start(lab_1, False, False, 0)
        self.lab_correct_who = Gtk.Label(0)
        hb.pack_start(self.lab_correct_who, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_2 = Gtk.Label('المحاولات الفاشلة : ')
        lab_2.set_alignment(0, 0.5)
        lab_2.set_size_request(180, -1)
        hb.pack_start(lab_2, False, False, 0)
        self.lab_false_who = Gtk.Label(0)
        hb.pack_start(self.lab_false_who, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_3 = Gtk.Label('غير المجاب عنه : ')
        lab_3.set_alignment(0, 0.5)
        lab_3.set_size_request(180, -1)
        hb.pack_start(lab_3, False, False, 0)
        self.lab_skip_who = Gtk.Label(0)
        hb.pack_start(self.lab_skip_who, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_4 = Gtk.Label('التقييم العام : ')
        lab_4.set_alignment(0, 0.5)
        lab_4.set_size_request(180, -1)
        hb.pack_start(lab_4, False, False, 0)
        self.lab_appraisal_who = Gtk.Label('لا شيء')
        hb.pack_start(self.lab_appraisal_who, False, False, 0)
        vb2.pack_start(hb, False, False, 0)
        self.new_verse_who()
        self.append_page(vb2, Gtk.Label('من القائل ؟'))
        
        # a --------------------------------------------
        vb3 = Gtk.VBox(False, 11)
        vb3.set_border_width(11)
        
        hb = Gtk.HBox(False, 3)
        lab_0 = Gtk.Label('القائل : ')
        lab_0.set_alignment(0, 0.5)
        hb.pack_start(lab_0, False, False, 0)
        self.lab_speaker = Gtk.Label(0)
        hb.pack_start(self.lab_speaker, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        
        vb3.pack_start(Gtk.Separator(), False, False, 0)
        
        half1 = Gtk.EventBox()
        half2 = Gtk.EventBox()
        half1.override_background_color(Gtk.StateFlags.NORMAL, daw_customs.rgba(self.parent.theme.colorb)) 
        half2.override_background_color(Gtk.StateFlags.NORMAL, daw_customs.rgba(self.parent.theme.colorb))
        half1.set_size_request(-1,70) 
        half2.set_size_request(-1,70) 
        box_verse = Gtk.HBox(False, 53)
        self.box_half1 = Gtk.HBox(False, 0)
        self.box_half2 = Gtk.HBox(False, 0)
        half1.add(self.box_half1)
        half2.add(self.box_half2)
        box_verse.pack_start(half1, True, True, 0)
        box_verse.pack_start(half2, True, True, 0)
        vb3.pack_start(box_verse, False, False, 0)
        self.new_verse_organize()
        
        vb3.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 11)
        self.check_verse = daw_customs.ButtonClass('تحقّق')
        self.check_verse.connect('clicked', self.check_verse_cb)
        hb.pack_start(self.check_verse, False, False, 0)
        self.new_verse = daw_customs.ButtonClass('جديد')
        self.new_verse.connect('clicked', self.new_verse_cb)
        hb.pack_start(self.new_verse, False, False, 0)
        self.org_verse = daw_customs.ButtonClass('نظّم')
        self.org_verse.connect('clicked', self.org_verse_cb)
        hb.pack_start(self.org_verse, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        
        vb3.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_1 = Gtk.Label('الإجابات الصحيحة : ')
        lab_1.set_alignment(0, 0.5)
        lab_1.set_size_request(180, -1)
        hb.pack_start(lab_1, False, False, 0)
        self.lab_correct = Gtk.Label(0)
        hb.pack_start(self.lab_correct, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_2 = Gtk.Label('المحاولات الفاشلة : ')
        lab_2.set_alignment(0, 0.5)
        lab_2.set_size_request(180, -1)
        hb.pack_start(lab_2, False, False, 0)
        self.lab_false = Gtk.Label(0)
        hb.pack_start(self.lab_false, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_3 = Gtk.Label('غير المجاب عنه : ')
        lab_3.set_alignment(0, 0.5)
        lab_3.set_size_request(180, -1)
        hb.pack_start(lab_3, False, False, 0)
        self.lab_skip = Gtk.Label(0)
        hb.pack_start(self.lab_skip, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 3)
        lab_4 = Gtk.Label('التقييم العام : ')
        lab_4.set_alignment(0, 0.5)
        lab_4.set_size_request(180, -1)
        hb.pack_start(lab_4, False, False, 0)
        self.lab_appraisal = Gtk.Label('لا شيء')
        hb.pack_start(self.lab_appraisal, False, False, 0)
        vb3.pack_start(hb, False, False, 0)
        self.append_page(vb3, Gtk.Label('رتّب البيت'))
        self.show_all()  
        