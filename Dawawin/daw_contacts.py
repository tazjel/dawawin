# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import sqlite3
from gi.repository import Gtk
import daw_araby, daw_customs
import random

# a قاعدة بيانات الدواوين----------------------------------
class MyDB(object):
    
    def __init__(self, *a):
        self.con = sqlite3.connect(daw_customs.MY_DATA)
        self.con.create_function('fuzzy', 1, daw_araby.fuzzy_plus)
        self.cur = self.con.cursor()

    # a جميع الشعراء---------------------------------------
    
    def all_poets(self, *a):
        self.cur.execute('SELECT id_poet, lakab, sex, balad, age FROM poets')
        poets = self.cur.fetchall()
        return poets
    
    # a إعادة وأطول شطر في قصيدة---------------------------------------
    
    def length_poem(self, id_poem):
        self.cur.execute('SELECT length FROM infopoem WHERE id_poem=?',(id_poem,))
        length = self.cur.fetchall()
        return length[0][0]
    
    # a إعادة نوع قصيدة---------------------------------------
    
    def naw3_poem(self, id_poem):
        self.cur.execute('SELECT naw3 FROM infopoem WHERE id_poem=?',(id_poem,))
        naw3 = self.cur.fetchall()
        return naw3[0][0]
    
    # a إعادة عروض قصيدة---------------------------------------
    
    def arodh_poem(self, id_poem):
        self.cur.execute('SELECT arodh FROM infopoem WHERE id_poem=?',(id_poem,))
        arodh = self.cur.fetchall()
        return arodh[0][0]
    
    # a إعادة قافية قصيدة---------------------------------------
    
    def kafia_poem(self, id_poem):
        self.cur.execute('SELECT kafia FROM infopoem WHERE id_poem=?',(id_poem,))
        kafia = self.cur.fetchall()
        return kafia[0][0]
    
    # a إعادة عدد الأبيات---------------------------------------
    
    def abiat_poem(self, id_poem):
        self.cur.execute('SELECT abiat FROM infopoem WHERE id_poem=?',(id_poem,))
        abiat = self.cur.fetchall()
        return abiat[0][0]
    
    # a إعادة غرض القصيدة---------------------------------------
    
    def gharadh_poem(self, id_poem):
        self.cur.execute('SELECT gharadh FROM infopoem WHERE id_poem=?',(id_poem,))
        gharadh = self.cur.fetchall()
        return gharadh[0][0]
    
    # a إعادة روي القصيدة---------------------------------------
    
    def rawi_poem(self, id_poem):
        self.cur.execute('SELECT rawi FROM infopoem WHERE id_poem=?',(id_poem,))
        rawi = self.cur.fetchall()
        return rawi[0][0]
    
    # a إعادة نص قصيدة وسبب نظمها وشرحها والتعليق عليها---------------------------------------
    
    def get_poem(self, id_poem):
        self.cur.execute('SELECT nasse, sabab, charh, ta3lik FROM kassaid WHERE id_poem=?',(id_poem,))
        poem = self.cur.fetchall()
        return poem[0][0], poem[0][1], poem[0][2], poem[0][3]
    
    # a أعادة معلومات القصيدة كاملة---------------------------------------
    
    def poem_info(self, id_poem):
        self.cur.execute('SELECT * FROM infopoem WHERE id_poem=?',(id_poem,))
        poems = self.cur.fetchall()
        return poems[0]
    
    # a إعادة اسم شاعر---------------------------------------
    
    def name_poet(self, id_poet):
        if id_poet == 0: return u'أحدهم', u'أحدهم'
        self.cur.execute('SELECT name, lakab FROM poets WHERE id_poet=?',(id_poet,))
        poet = self.cur.fetchall()
        return poet[0][0], poet[0][1]
    
    # a إعادة معرف شاعر مسمى---------------------------------------
    
    def id_name_poet(self, name):
        self.cur.execute('SELECT id_poet, sex, balad, age FROM poets WHERE lakab=?',(name,))
        poets = self.cur.fetchall()
        if len(poets) > 0: id_poet, sex, balad, age = poets[0][0], poets[0][1], poets[0][2], poets[0][3]
        elif name == "ما لا يعرف قائله": id_poet, sex, balad, age = 0, 0, 0, 0
        else: id_poet, sex, balad, age = None, None, None, None
        return id_poet, sex, balad, age
   
    # a إعادة معرف شاعر من القصيدة---------------------------------------
    
    def id_poet(self, id_poem):
        self.cur.execute('SELECT id_poet FROM infopoem WHERE id_poem=?',(id_poem,))
        id_poet = self.cur.fetchall()
        return id_poet[0][0]
    
    # a إعادة وفاة الشاعر---------------------------------------
    
    def death_poet(self, id_poet):
        self.cur.execute('SELECT death FROM poets WHERE id_poet=?',(id_poet,))
        death = self.cur.fetchall()
        return death[0][0]
    
    # a إعادة عصر الشاعر---------------------------------------
    
    def age_poet(self, id_poet):
        self.cur.execute('SELECT age FROM poets WHERE id_poet=?',(id_poet,))
        age = self.cur.fetchall()
        return age[0][0]
    
    # a إعادة بلد الشاعر---------------------------------------
    
    def balad_poet(self, id_poet):
        self.cur.execute('SELECT balad FROM poets WHERE id_poet=?',(id_poet,))
        balad = self.cur.fetchall()
        return balad[0][0]
    
    # a إعادة جنس الشاعر---------------------------------------
    
    def sex_poet(self, id_poet):
        self.cur.execute('SELECT sex FROM poets WHERE id_poet=?',(id_poet,))
        sex = self.cur.fetchall()
        return sex[0][0]
    
    # a إضافة شاعر---------------------------------------
    
    def add_poet(self, nm, lak, tarjama, die, sex, balad, age):
        self.cur.execute('SELECT id_poet FROM poets ORDER BY id_poet')
        poets = self.cur.fetchall()
        if len(poets) == 0: id_poet = 1
        else: id_poet = poets[-1][0]+1
        self.cur.execute('INSERT INTO poets VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                         (id_poet, nm, lak, tarjama, die, sex, balad, age))
        check = self.con.commit()
        if check == None:
            return id_poet, sex, balad, age
        
    # a تعديل شاعر---------------------------------------
    
    def modify_poet(self, id_poet, nm, lak, tarjama, die, sex, balad, age):
        self.cur.execute('UPDATE poets SET name=?, lakab=?, tarjama=?, \
            death=?, sex=?, balad=?, age=? WHERE id_poet=?', 
                         (nm, lak, tarjama, die, sex, balad, age, id_poet))
        self.con.commit()
        self.cur.execute('UPDATE infopoem SET sex=?, balad=?, age=? WHERE id_poet=?', 
                         (sex, balad, age, id_poet))
        check = self.con.commit()
        return check
            
    
    # a إضافة قصيدة---------------------------------------
    
    def add_poem(self, nam, text, sabab, charh, poet, sex, balad, age, abiat, baher, 
                 rawi, kafia, arodh, gharadh, naw3, longer_half):
        self.cur.execute('SELECT id_poem FROM infopoem ORDER BY id_poem')
        poem = self.cur.fetchall()
        if len(poem) == 0: id_poem = 1
        else: id_poem = poem[-1][0]+1
        self.cur.execute('SELECT tartib FROM infopoem ORDER BY tartib')
        tar = self.cur.fetchall()
        if len(tar) == 0: tartib = 1
        else: tartib = tar[-1][0]+1
        self.cur.execute('INSERT INTO infopoem VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                         (id_poem, nam, poet, sex, balad, age, abiat, baher, rawi, 
                          kafia, arodh, gharadh, naw3, tartib, longer_half, 0, 0, u''))
        check = self.con.commit()
        if check == None:
            self.cur.execute('INSERT INTO kassaid VALUES (?, ?, ?, ?, ?)', (id_poem, text, sabab, charh, u''))
            check0 = self.con.commit()
        return check0
    
    # a تعديل قصيدة---------------------------------------
    
    def modify_poem(self, id_poem, nam, text, sabab, charh, abiat, 
                    baher, rawi, kafia, arodh, gharadh, naw3, longer_half):
        self.cur.execute('UPDATE infopoem SET name=?, abiat=?, \
        id_baher=?, rawi=?, kafia=?, arodh=?, gharadh=?, naw3=?, length=? WHERE id_poem=?', 
                         (nam, abiat, baher, rawi, kafia, arodh,  
                          gharadh, naw3, longer_half, id_poem))
        check = self.con.commit()
        if check == None:
            self.cur.execute('UPDATE kassaid SET nasse=?, sabab=?, charh=? WHERE id_poem=?', 
                             (text, sabab, charh, id_poem))
            check0 = self.con.commit()
        return check0
    
    # a تغيير شاعر قصيدة---------------------------------------
    
    def change_poet(self, id_poem, poet, sex, balad, age):
        self.cur.execute('UPDATE infopoem SET id_poet=?, sex=?, balad=?, age=? WHERE id_poem=?', 
                         (poet, sex, balad, age, id_poem))
        check = self.con.commit()
        return check
    
    # a دمج شاعرين معا---------------------------------------
    
    def merge_poet(self, id_poet, poet, sex, balad, age):
        self.cur.execute('UPDATE infopoem SET id_poet=?, sex=?, balad=?, age=? WHERE id_poet=?', 
                         (poet, sex, balad, age, id_poet))
        check0 = self.con.commit()
        if check0 == None:
            check = self.remove_poet(id_poet)
            return check

    # a حذف قصيدة---------------------------------------
    
    def remove_poem(self, id_poem):
        self.cur.execute('DELETE FROM infopoem WHERE id_poem=?', (id_poem,))
        check1 = self.con.commit()
        if check1 == None:
            self.cur.execute('DELETE FROM kassaid WHERE id_poem=?', (id_poem,))
            check = self.con.commit()
        return check
    
    # a حذف الأبيات المفضلة---------------------------------------
    
    def remove_abiaty(self, *a):
        self.cur.execute('DELETE FROM abiat')
        check = self.con.commit()
        return check
    
    # a حذف القصائد المفضلة---------------------------------------
    
    def remove_favory(self, *a):
        self.cur.execute('UPDATE infopoem SET fav = 0 WHERE fav = 1')
        check = self.con.commit()
        return check
    
    # a حذف القصائد المسجلة---------------------------------------
    
    def remove_recite(self, *a):
        self.cur.execute('UPDATE infopoem SET recite = 0 WHERE recite = 1')
        check = self.con.commit()
        return check
    
    # a حذف شاعر مع جميع قصائده---------------------------------------
    
    def remove_poet(self, id_poet):
        ls = self.poems_id(id_poet)
        for a in ls:
            self.remove_poem(a)
        if id_poet == 0:
            return None
        self.cur.execute('DELETE FROM poets WHERE id_poet=?', (id_poet,))
        check = self.con.commit()
        return check
    
    
    # a حذف جميع دواوين عصر ما---------------------------------------
    
    def remove_age(self, age):
        self.cur.execute('SELECT id_poem FROM infopoem WHERE age=?',(age,))
        poems = self.cur.fetchall()
        self.cur.execute('BEGIN;')
        for a in poems:
            self.cur.execute('DELETE FROM infopoem WHERE id_poem=?', (a[0],))
            self.cur.execute('DELETE FROM kassaid WHERE id_poem=?', (a[0],))
        self.con.commit()
        self.cur.execute('DELETE FROM poets WHERE age=?', (age,))
        check = self.con.commit()
        return check
    
    # a قصائد شاعر مع ترجمته---------------------------------------
    
    def poems_of_poet(self, id_poet):
        self.cur.execute('SELECT id_poem, name, abiat, id_baher, rawi, \
        kafia, gharadh, naw3 FROM infopoem WHERE id_poet=?',(id_poet,))
        poems = self.cur.fetchall()
        if id_poet == 0: return poems, u'قسم القصائد غير معروفة النسبة  '
        self.cur.execute('SELECT tarjama FROM poets WHERE id_poet=?',(id_poet,))
        poet = self.cur.fetchall()
        return poems, poet[0][0]
    
    # a معرفات  قصائد شاعر---------------------------------------
    
    def poems_id(self, id_poet):
        self.cur.execute('SELECT id_poem FROM infopoem WHERE id_poet=?',(id_poet,))
        poems = self.cur.fetchall()
        ls = []
        for a in poems:
            ls.append(a[0])
        return ls
    
    # a  معرف بحر قصيدة محددة---------------------------------------
    
    def get_id_baher(self, id_poem):
        self.cur.execute('SELECT id_baher FROM infopoem WHERE id_poem=?',(id_poem,))
        baher = self.cur.fetchall()
        return baher[0][0]
    
    # a  القصائد المقروءة---------------------------------------
    
    def recited_poems(self, *a):
        all_recited = []
        self.cur.execute('SELECT id_poem, name, reciter FROM infopoem WHERE recite=1')
        recited = self.cur.fetchall()
        for a in recited:
            list1 = []
            list1.append(a[0])
            list1.append(a[1])
            list1.append(a[2])
            all_recited.append(list1)
        return all_recited
    
    # a  إضافة قصيدة مقروءة---------------------------------------
    
    def set_recite(self, id_poem, reciter):
        self.cur.execute('UPDATE infopoem SET recite=1, reciter=? WHERE id_poem=?',(reciter, id_poem))
        check = self.con.commit()
        return check
    
    # a  القصائد المفضلة---------------------------------------
    
    def favorite_poems(self, *a):
        all_favorite = []
        self.cur.execute('SELECT id_poem, name FROM infopoem WHERE fav=1')
        recited = self.cur.fetchall()
        for a in recited:
            list1 = []
            list1.append(a[0])
            list1.append(a[1])
            all_favorite.append(list1)
        return all_favorite
    
    # a  اسم القصيدة---------------------------------------
    
    def name_poem(self, id_poem):
        self.cur.execute('SELECT name FROM infopoem WHERE id_poem=?',(id_poem,))
        name = self.cur.fetchall()
        return name[0][0]
    
    # a  وضع تعليق---------------------------------------
    
    def set_ta3lik(self, id_poem, text):
        self.cur.execute('UPDATE kassaid SET ta3lik = ? WHERE id_poem=?',(text, id_poem))
        check = self.con.commit()
        return check
    
    # a  إضافة قصيدة للمفضلة---------------------------------------
    
    def to_favorite(self, id_poem):
        self.cur.execute('UPDATE infopoem SET fav = 1 WHERE id_poem=?',(id_poem,))
        check = self.con.commit()
        return check
    
    # a  إخراج قصيدة من المفضلة---------------------------------------
    
    def out_favorite(self, id_poem):
        self.cur.execute('UPDATE infopoem SET fav = 0 WHERE id_poem=?',(id_poem,))
        check = self.con.commit()
        return check
    
    # a  صفحات الأبيات المفضلة---------------------------------------
    
    def abiaty_pages(self, *a):
        self.cur.execute('SELECT id_verse FROM abiat')
        abiat = self.cur.fetchall()
        return abiat
     
    # a  إضافة الأبيات المفضلة---------------------------------------
    
    def to_abiaty(self, id_poem, text):
        self.cur.execute('SELECT id_verse FROM abiat')
        verse = self.cur.fetchall()
        if len(verse) == 0: id_verse = 1
        else: id_verse = verse[-1][0]+1
        self.cur.execute('INSERT INTO abiat VALUES (?, ?, ?)', (id_verse, id_poem, text))
        check = self.con.commit()  
        if check == None:
            return id_verse 
    
    # a إعادة شاعرين لا على لتعيين---------------------------------------
    
    def two_poet(self, id_poet):
        self.cur.execute('SELECT id_poet FROM poets WHERE id_poet != ?', (id_poet,))
        poets = self.cur.fetchall()
        if len(poets) > 2:
            random.shuffle(poets)
            return poets[0][0], poets[1][0]
        else:
            return 0, 0
    
    # a  تأكد من وجود بيت---------------------------------------
     
    def is_verse(self, verse):
        self.cur.execute('SELECT id_poem FROM kassaid WHERE fuzzy(nasse) LIKE ? OR fuzzy(nasse) LIKE ? LIMIT 1', 
                         (daw_araby.fuzzy_plus('%\n'+verse+'\n%'), daw_araby.fuzzy_plus(verse+'\n%')))
        verses = self.cur.fetchall()
        if len(verses) > 0: return True
        else: return False
    
    # a  بحث عن بيت يبدأ بحرف معين---------------------------------------
     
    def first_in_verse(self, letter):
        n = int(self.n_poems())
        s = n/2000
        if s >= 1: 
            s = random.choice(range(s-1))
        else: s = 0
        self.cur.execute('SELECT id_poem, nasse FROM kassaid WHERE nasse LIKE ? OR nasse LIKE ? LIMIT ?, ?', 
                         ('%\n'+letter+'%', letter+'%', s*2000, 100))
        nasses = self.cur.fetchall()
        verses = []
        for a in nasses:
            ls = a[1].splitlines(1)
            for b in ls:
                if u'*' in b and b[0] == letter:
                    verses.append([b,a[0]])
        return verses
    
            
    # a  أبيات المفضلة---------------------------------------
    
    def get_abiat(self, id_verse):
        self.cur.execute('SELECT id_poem, abiat FROM abiat WHERE id_verse=?', (id_verse,))
        verses = self.cur.fetchall() 
        return verses[0][0], verses[0][1]     

    # a  حذف أبيات من المفضلة---------------------------------------
    
    def del_abiat(self, id_verse):
        self.cur.execute('DELETE FROM abiat WHERE id_verse=?', (id_verse,))
        check = self.con.commit()
        return check
    
    # a  البحث عن نص في قصيدة---------------------------------------
    
    def search(self, id_poem, phrase, ls):
        self.cur.execute('SELECT nasse FROM kassaid WHERE id_poem={} AND {}'.format(id_poem, phrase), ls)
        result = self.cur.fetchall()
        if len(result) > 0: return True
        else: return False
                        
    # a تصفية القصائد---------------------------------------
    
    def filter_poem(self, sex, balad, age, baher, rawi, kafia, arodh, gharadh, naw3):
        condition = []
        data = []
        if sex != 0:
            condition.append(u' sex=?')
            data.append(sex)
        if balad != 0:
            condition.append(u' balad=?')
            data.append(balad)
        if age != 0:
            condition.append(u' age=?')
            data.append(age)
        if baher != 0:
            condition.append(u' id_baher=?')
            data.append(baher)
        if rawi != 0:
            condition.append(' rawi=?')
            data.append(rawi)      
        if kafia != 0:
            condition.append(u' kafia=?')
            data.append(kafia)
        if arodh != 0:
            condition.append(u' arodh=?')
            data.append(arodh)
        if gharadh != 0:
            condition.append(u' gharadh=?')
            data.append(gharadh)
        if naw3 != 0:
            condition.append(u' naw3=?')
            data.append(naw3)
        if condition == []: self.cur.execute('SELECT id_poem FROM infopoem')
        else: 
            txt_cond = ' AND '.join(condition)
            self.cur.execute('SELECT id_poem FROM infopoem WHERE{}'.format(txt_cond,), data)
        poems = self.cur.fetchall()
        poems_id = []
        for a in poems:
            poems_id.append(a[0])
        return poems_id
    
    # a معرفات جميع القصائد---------------------------------------
    
    def all_poems_id(self, *a):
        poems_id = []
        self.cur.execute('SELECT id_poem FROM infopoem')
        poems = self.cur.fetchall()
        for a in poems:
            poems_id.append(a[0])
        return poems_id

    #a استيراد القصائد---------------------------------------------
    
    def is_poem_exists(self, name, sex, balad, age, abiat, baher, rawi, 
                      kafia, arodh, gharadh, naw3, longer_half):
        self.cur.execute('SELECT id_poem FROM infopoem WHERE fuzzy(name)=? AND sex=? AND balad=? AND \
         age=? AND abiat=? AND id_baher=? AND rawi=? AND kafia=? AND arodh=? AND gharadh=? AND naw3=? AND length=?', 
         (daw_araby.fuzzy(name), sex, balad, age, abiat, baher, rawi, kafia, arodh, gharadh, naw3, longer_half))
        poems = self.cur.fetchall()
        return poems
    
    def is_poet_exists(self, lakab_poet, age, balad):
        self.cur.execute('SELECT id_poet FROM poets WHERE fuzzy(lakab)=? AND balad=? AND age=?', 
                         (daw_araby.fuzzy(lakab_poet), balad, age))
        poet = self.cur.fetchall()
        return poet
    
    def add_file_db(self, filename):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        cur.execute('SELECT * FROM infopoem')
        poems = cur.fetchall()
        return poems
        
    def add_poem_from_fileDB(self, id_poem, filename, v=False):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        cur.execute('SELECT * FROM infopoem WHERE id_poem=?', (id_poem,) )
        poem_info = cur.fetchall()
        cur.execute('SELECT * FROM kassaid WHERE id_poem=?', (id_poem,) )
        poem_text = cur.fetchall()
        poet = poem_info[0][2] 
        cur.execute('SELECT * FROM poets WHERE id_poet=?', (poet,) )
        poet_info = cur.fetchall()
        sex = poem_info[0][3] 
        balad = poem_info[0][4] 
        age = poem_info[0][5] 
        nam = poem_info[0][1] 
        text = poem_text[0][1] 
        sabab = poem_text[0][2] 
        charh = poem_text[0][3] 
        abiat = poem_info[0][6] 
        baher = poem_info[0][7] 
        rawi = poem_info[0][8] 
        kafia = poem_info[0][9] 
        arodh = poem_info[0][10] 
        gharadh = poem_info[0][11] 
        naw3 = poem_info[0][12] 
        longer_half = poem_info[0][14]
        if len(poet_info) == 0:
            id_poet = 0
        else:
            name_poet = poet_info[0][1] 
            lakab_poet = poet_info[0][2]
            tardjama = poet_info[0][3] 
            death = poet_info[0][4]
            poet0 = self.is_poet_exists(daw_araby.fuzzy(lakab_poet), age, balad)
            if len(poet0) == 0:
                id_poet, sex, balad, age = self.add_poet(name_poet, lakab_poet, tardjama, death, sex, balad, age)
            else:
                id_poet = poet0[0][0]
        poem = self.is_poem_exists(daw_araby.fuzzy(nam), sex, balad, age, abiat, baher, rawi, kafia, arodh, gharadh, naw3, longer_half)
        if len(poem) > 0:
            if v:
                id_poem = poem[0][0]
                self.modify_poem(id_poem, nam, text, sabab, charh, id_poet, sex, balad, 
                                 age, abiat, baher, rawi, kafia, arodh, gharadh, naw3, longer_half)
            return True
        self.add_poem(nam, text, sabab, charh, id_poet, sex, balad, age, abiat, baher, rawi, 
                      kafia, arodh, gharadh, naw3, longer_half)
        return True
    
    # a دواوين عصر محدد--------------------------------------
    
    def poet_of_age(self, age):
        if age == 0: return [[0,],]
        self.cur.execute('SELECT id_poet, lakab FROM poets WHERE age=?', (age,))
        poets = self.cur.fetchall()
        return poets
    
    # a تصدير قصائد-----------------------------------------
    
    def export_poems(self, new_file, id_v, n):
        con = sqlite3.connect(new_file)
        cur = con.cursor()
        if n == 0:
            cond = 'age=?'
        elif n == 1:
            cond = 'id_poet=?'
        elif n == 2:
            cond = 'id_poem=?'
        self.cur.execute('SELECT * FROM infopoem WHERE {}'.format(cond,), (id_v,))
        poems = self.cur.fetchall()
        cur.execute('BEGIN;')
        for a in poems:
            while (Gtk.events_pending()): Gtk.main_iteration()
            cur.execute('INSERT INTO infopoem VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                             (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], 
                              a[9], a[10], a[11], a[12], a[13], a[14], 0, 0, u''))
#            check = con.commit()
            self.cur.execute('SELECT * FROM kassaid WHERE id_poem=?', (a[0],))
            poem = self.cur.fetchall()
            b = poem[0]
            cur.execute('INSERT INTO kassaid VALUES (?, ?, ?, ?, ?)', (b[0], b[1], b[2], b[3], u''))
#                con.commit()
            if n == 2:
                if a[2] != 0:
                    self.cur.execute('SELECT * FROM poets WHERE id_poet=?', (a[2],))
                    poet = self.cur.fetchall()
                    d = poet[0]
                    cur.execute('INSERT INTO poets VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                             (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]))
#                    con.commit()
                return True
        con.commit()
        self.cur.execute('SELECT * FROM poets WHERE {}'.format(cond,), (id_v,))
        poets = self.cur.fetchall()
        cur.execute('BEGIN;')
        for c in poets:
            cur.execute('INSERT INTO poets VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                         (c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
        con.commit()
        return True
    
    def name_poet_newfile(self, id_poet, filename):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        if id_poet == 0: return u'أحدهم', u'أحدهم'
        cur.execute('SELECT name, lakab FROM poets WHERE id_poet=?',(id_poet,))
        poet = cur.fetchall()
        return poet[0][0], poet[0][1]
    
    # a إحصاءات------------------------------------------------
    
    def n_poems_poet(self, id_poet):
        self.cur.execute('SELECT id_poem FROM infopoem WHERE id_poet=?', (id_poet,))
        poems = self.cur.fetchall()
        return str(len(poems))
    
    def n_verses_poet(self, id_poet):
        self.cur.execute('SELECT sum(abiat) FROM infopoem WHERE id_poet=?', (id_poet,))
        abiats = self.cur.fetchall()
        if abiats[0][0] == None: return "  "
        return str(abiats[0][0]) 
    
    def n_dawawin(self, *a):
        self.cur.execute('SELECT id_poet FROM poets')
        poets = self.cur.fetchall()
        return str(len(poets))
    
    def n_poems(self, *a):
        self.cur.execute('SELECT id_poem FROM infopoem')
        poems = self.cur.fetchall()
        return str(len(poems))
    
    def n_verses(self, *a):
        self.cur.execute('SELECT sum(abiat) FROM infopoem')
        abiats = self.cur.fetchall()
        return str(abiats[0][0])
    
    # a انشاء قاعدة بيانات فارغة-------------------------------
    
    def create_db(self, filename):
        con = sqlite3.connect(filename)
        cur = con.cursor()
        cur.execute('CREATE TABLE abiat (id_verse integer primary key, id_poem int, abiat longtext(2000))') 
        cur.execute('CREATE TABLE poets (id_poet integer primary key, \
        name varchar(255), lakab varchar(255), tarjama longtext(20000), \
        death int, sex int, balad int, age int)')
        cur.execute('CREATE TABLE infopoem (id_poem integer primary key, \
        name varchar(255), id_poet int, sex int, balad int, age int, \
        abiat int, id_baher int, rawi int, kafia int, arodh int, gharadh int, \
        naw3 int, tartib int, length int, fav int, recite int, reciter varchar(255))')
        cur.execute('CREATE TABLE kassaid (id_poem integer primary key, \
        nasse longtext(20000), sabab longtext(20000), charh longtext(20000), ta3lik longtext(20000))')

# a قاعدة بيانات الأوزان----------------------------------
        
class AwzanDB(object):
    
    def __init__(self, *a):
        self.con = sqlite3.connect(daw_customs.MY_AWZAN)
        self.cur = self.con.cursor()
    
    def meter_verse(self, text):
        self.cur.execute('SELECT * FROM awzan WHERE wazn=?', (text,))
        result = self.cur.fetchall()
        return result

# a قاعدة بيانات المعجم----------------------------------
      
class DictDB(object):
    
    def firstletter(self, term):
        return term[0]
    
    def __init__(self, *a):
        self.con = sqlite3.connect(daw_customs.MY_DICT)
        self.con.create_function('firstletter', 1, self.firstletter)
        self.cur = self.con.cursor()
    
    def all_index(self, dicte, f_letter):
        self.cur.execute('SELECT term FROM {} WHERE firstletter(term)=? ORDER BY term'.format(dicte, ), (f_letter,))
        terms = self.cur.fetchall()
        return terms
    
    def show_charh(self, term, dicte):
        self.cur.execute('SELECT charh FROM {} WHERE term=?'.format(dicte, ), (term,))
        charh = self.cur.fetchall()
        return charh

# a قاعدة بيانات المساعدة----------------------------------
  
class HelpDB(object):
    
    def __init__(self, *a):
        self.con = sqlite3.connect(daw_customs.MY_HELP)
        self.cur = self.con.cursor()
    
    def titles_help(self, *a):
        self.cur.execute('SELECT id, tit FROM help')
        hlp = self.cur.fetchall()
        return hlp
    
    def show_page_help(self, v):
        self.cur.execute('SELECT nasse FROM help WHERE id=?', (v,))
        txt = self.cur.fetchall() 
        return txt
    
    def titles_mekadimat(self, *a):
        self.cur.execute('SELECT id, tit FROM mekadimat')
        mekadimat = self.cur.fetchall()
        return mekadimat
        
    def show_page_mekadimat(self, v):
        self.cur.execute('SELECT nasse FROM mekadimat WHERE id=?', (v,))
        txt = self.cur.fetchall() 
        return txt 
        
    def titles_behor(self, *a):
        self.cur.execute('SELECT id, tit FROM behor')
        behor = self.cur.fetchall()
        return behor
        
    def show_page_behor(self, v):
        self.cur.execute('SELECT nasse FROM behor WHERE id=?', (v,))
        txt = self.cur.fetchall()
        return txt 
