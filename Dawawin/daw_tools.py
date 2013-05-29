# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import re
import daw_config, daw_araby
            
# a قوائم خاصة-----------------------------------------------

sex_poet = [
            [1, u'الرجال'],
            [2, u'النساء']
            ]

elnaw3   = [
            [1, u'قريض'],
            [2, u'أرجوزة'],
            [3, u'مُوشحة'],
            [4, u'رُباعيّة'],
            [5, u'قصيدة نثر'],
            [6, u'مخمّسة'],
            ]

age_poet = [
            [1, u'الجاهلي'],
            [2, u'المخضرمون'],
            [3, u'صدر الإسلام'],
            [4, u'الأموي'],
            [5, u'العباسي'],
            [10, u'الفاطمي'],
            [11, u'الأيوبي'],
            [6, u'المملوكي'],
            [7, u'العثماني'],
            [8, u'الحديث'],
            [9, u'غير معروف'],
            ]

elgharadh = [
            [1, u'وصف'],
            [8, u'تشبيه'], 
            [2, u'فخر'], 
            [3, u'حماسة'], 
            [4, u'نسيب'],
            [6, u'شكوى'],
            [7, u'عتاب'],
            [8, u'اعتذار'],
            [8, u'هجاء'],
            [8, u'وعيد'],
            [9, u'رثاء'], 
            [10, u'مدح'],
            [11, u'اقتضاء'],
            [12, u'علمي'], 
            [13, u'دفاع'], 
            [14, u'مناجاة'], 
            [15, u'زهد'], 
            [16, u'ملحمة'], 
            [17, u'إلغاز'], 
            [18, u'تأريخ'], 
            [19, u'هزل'], 
            [20, u'حكمة'],
            [21, u'قصصي'], 
            [22, u'هِنات'], 
            [23, u'خليط'], 
            ]

elkawafi = [
            [1, u'مطلقة'],
            [2, u'مقيدة']
            ]

elrawi   = [ 
            [1, u"ألف"], 
            [2, u"باء"], 
            [3, u'تاء' ], 
            [4, u'تاء مربوطة' ], 
            [5, u'ثاء' ],
            [6, u'جيم' ], 
            [7, u'حاء' ], 
            [8, u'خاء' ], 
            [9, u'دال' ], 
            [10, u'ذال' ],
            [11, u'راء' ], 
            [12, u'زاي' ], 
            [13, u'سين' ], 
            [14, u'شين' ], 
            [15, u'صاد' ],
            [16, u'ضاد' ], 
            [17, u'طاء' ], 
            [18, u'ظاء' ], 
            [19, u'عين' ], 
            [20, u'غين' ],
            [21, u'فاء' ], 
            [22, u'قاف' ], 
            [23, u'كاف' ], 
            [24, u'لام' ], 
            [25, u'ميم' ],
            [26, u'نون' ], 
            [27, u'هاء' ], 
            [28, u'واو' ], 
            [29, u'ياء' ], 
            [30, u'همزة' ],
            ]

elbalad   = [ 
            [1, u"الجزائر"], 
            [2, u"تونس"], 
            [3, u'المغرب' ], 
            [4, u'موريطانيا' ], 
            [5, u'ليبيا' ],
            [6, u'مصر' ], 
            [7, u'فلسطين' ], 
            [8, u'لبنان' ], 
            [9, u'الأردن' ], 
            [10, u'سوريا' ],
            [11, u'العراق' ], 
            [12, u'السعودية' ], 
            [13, u'الكويت' ], 
            [14, u'البحرين' ], 
            [15, u'قطر' ],
            [16, u'الإمارات' ], 
            [17, u'سلطنة عمان' ], 
            [18, u'اليمن' ], 
            [19, u'السودان' ], 
            [20, u'جيبوتي' ],
            [21, u'الصومال' ],
            [22, u'غير معروف'],
            ]

elbehor = [
            [1, u'الطَّوِيل'], 
            [2, u'المَدِيد'], 
            [3, u'البَسِيط'], 
            [4, u'الوافِر'], 
            [5, u'الكامِل'], 
            [6, u'الهَزَج'], 
            [7, u'الرَجَز'], 
            [8, u'الرَّمَل'], 
            [9, u'السَّريع'], 
            [10, u'المُنْسَرِح'], 
            [11, u'الخفيف'], 
            [12, u'المضارع'], 
            [13, u'المقتضب'], 
            [14, u'المجتث'], 
            [15, u'المتقارب'], 
            [16, u'المتدارك'], 
            ]

ela3aridh = [
        [1, u'عروض تامّة مقبوضة وضرب صحيح',],
        [2, u'عروض تامّة مقبوضة وضرب مقبوض',],
        [3, u'عروض تامّة مقبوضة وضرب محذوف',],
        [4, u'عروض مجزوءة صحيحة وضرب صحيح'],
        [5, u'عروض مجزوءة محذوفة وضرب محذوف'],
        [6, u'عروض مجزوءة محذوفة وضرب مقصور'],
        [7, u'عروض مجزوءة محذوفة وضرب أبتر'],
        [8, u'عروض مجزوءة مخبونة محذوفة وضرب مخبون محذوف'],
        [9, u'عروض مجزوءة مخبونة محذوفة وضرب أبتر'],
        [10, u'عروض مشطورة صحيحة وضرب صحيح'],
        [11, u'عروض تامّة مخبونة وضرب مخبون'],
        [12, u'عروض تامّة مخبونة وضرب مقطوع'],
        [13, u'عروض مجزوءة صحيحة وضرب مذال'],
        [14, u'عروض مجزوءة صحيحة وضرب مقطوع'],
        [15, u'عروض مجزوءة مقطوعة وضرب مقطوع'],
        [16, u'عروض مخلّعة مكبولة وضرب مكبول'],
        [17, u'عروض تامّة مقطوفة وضرب مقطوف'],
        [18, u'عروض مجزوءة صحيحة وضرب أعصب'],
        [19, u'عروض تامّة صحيحة وضرب صحيح'],
        [20, u'عروض تامّة صحيحة وضرب مقطوع'],
        [21, u'عروض تامّة صحيحة وضرب مضمر أحذّ'],
        [22, u'عروض تامّة حذّاء وضرب أحذّ'],
        [23, u'عروض تامّة حذّاء وضرب مضمر أحذّ'],
        [24, u'عروض مجزوءة صحيحة وضرب مرفّل'],
        [25, u'عروض مجزوءة صحيحة وضرب محذوف'],
        [26, u'عروض مشطورة صحيحة وهي الضرب نفسه'],
        [27, u'عروض منهوكة صحيحة وهي الضرب نفسه'],
        [28, u'عروض تامّة محذوفة وضرب صحيح'],
        [29, u'عروض تامّة محذوفة وضرب محذوف'],
        [30, u'عروض تامّة محذوفة وضرب مقصور'],
        [31, u'عروض مجزوءة صحيحة وضرب مسبّغ'],
        [32, u'عروض تامّة مكسوفة مطويّة وضرب مكسوف مطويّ'],
        [33, u'عروض تامّة مكسوفة مطويّة وضرب مطويّ موقوف'],
        [34, u'عروض تامّة مكسوفة مطويّة وضرب أصلم'],
        [35, u'عروض تامّة مكسوفة مخبولة وضرب مكسوف مخبول'],
        [36, u'عروض تامّة مكسوفة مخبولة وضرب أصلم'],
        [37, u'عروض مشطورة موقوفة وهي الضرب نفسه'],
        [38, u'عروض تامّة صحيحة وضرب مطويّ'],
        [39, u'عروض منهوكة موقوفة وهي الضرب نفسه'],
        [40, u'عروض منهوكة مكسوفة وهي الضرب نفسه'],
        [41, u'عروض تامّة صحيحة وضرب محذوف'],
        [42, u'عروض مجزوءة صحيحة وضرب مخبون مقصور'],
        [43, u'عروض مجزوءة مطويّة وضرب مطويّ'],
        [44, u'عروض تامّة صحيحة وضرب مقصور'],
        [45, u'عروض تامّة صحيحة وضرب أبتر'],
        ]

ela3aridh_in_behor = {
        1:[1, 2, 3],
        2:[4, 5, 6, 7, 8, 9, 10],
        3:[11, 12, 4, 13, 14, 15, 16],
        4:[17, 4, 18],
        5:[19, 20, 21, 22, 23, 4, 13, 24, 14],
        6:[4, 25],
        7:[19, 20, 4, 26, 27],
        8:[28, 29, 30, 4, 31, 25],
        9:[32, 33, 34, 35, 36, 37],
        10:[38, 20, 39, 40],
        11:[19, 41, 29, 4, 42],
        12:[4,],
        13:[43,],
        14:[4,],
        15:[19, 44, 41, 45, 5, 7],
        16:[19, 4, 13, 24],
        }

# a أخذ الرقم وإعادة الاسم-----------------------------------------

def get_name(ls, n):
    if n == 0: return u'لا شيء'
    for a in ls:
        if n == a[0]:
            return a[1]
        
# a أخذ الاسم وإعادة الرقم-----------------------------------------

def get_int(ls, nm):
    nm = nm.strip()
    for a in ls:
        if nm in a[1]:
            return a[0]
        
# a أخذ الرقم وإعادة الموضع---------------------------------------

def get_index(ls, n):
    if n == 0: return -1
    for a in ls:
        if n == a[0]:
            idx = ls.index(a)
            return idx

# a أخذ الرقم وإعادة موضع العروض----------------------------------

def get_index_arodh(b, a):
    if a == 0: return -1
    for c in ela3aridh_in_behor[b]:
        if c == a:
            idx = ela3aridh_in_behor[b].index(a)
            return idx

# a أخذ الحرف وإعادة رقم الروي----------------------------------

def get_int_rawi(h):
    if h == u'ى': h = u'ا'
    rawi = daw_araby.NAMES[h]
    return get_int(elrawi, rawi)


# a حذف المسافات الزائدة والأسطر الفارغة---------------------------
    
def right_space(text):
    text = text.expandtabs(1)
    text = re.sub(' +', ' ', text)
    text = re.sub('\n \n', '\n', text)
    text = re.sub('\n ', '\n', text)
    text = re.sub(' \n', '\n', text)
    text = re.sub('\n+', '\n', text)
    txt = text.strip()
    return txt

# a تحديد شطر أو جزء منه فقط------------------------------------

def one_half(text):
    ls = text.split('  ')
    txt = daw_araby.stripTatweel(ls[0])
    return txt

# a الكلمة الأولى فقط--------------------------------------------

def first_term(text):
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    ls = text.split(' ')
    txt = daw_araby.stripTatweel(ls[0])
    return txt

# a تقسيم القصيدة المدخلة إلى أبيات-----------------------------
    
def my_split(text, a3aridh):
    list_abiat = []
    text = right_space(text)
    l_abiat = text.splitlines(1)
    n = 0
    for a in l_abiat:
        if '*' in a and len(a) > 15:
            half = a.split('*')
            h1 = half[0].strip()
            h2 = half[1].strip()
            list_abiat.append([h1, h2])
            n += 1
        else:
            if a3aridh == 1:
                list_abiat.append([a, 'half']) 
                n += 1
            else:
                list_abiat.append([a, 'title']) 
    return list_abiat, n

# a تحديد نوع قصيدة القريض أمشطور أم تام----------------------
    
def is_machtor(text):
    mashtor = True
    if '*' in text:
        mashtor = False
    return mashtor

# a إعادة روي القصيدة بعد تخمينه-----------------------------
    
def rawi_poem(text):
    if is_machtor(text):
        list_poem, n = my_split(text, 1)
    else:
        list_poem, n = my_split(text, 0)
    if len(list_poem) == 1:
        txt = daw_araby.stripTashkeel(text)
        if txt[-1] == u'ا':
            if txt[-2] == u'و':
                return txt[-3]
            else:
                return txt[-2]
        if text[-2:] == u'هْ':
            return txt[-2]
        elif text[-1] in [u'ي', u'و', u'ه']:
            return txt[-2]
        elif txt[-1] == u'ة':
            return u'ت'
        elif txt[-1] == u'ى':
            return u'ا'
        else:
            return txt[-1]
    elif len(list_poem) > 1:
        n = 0
        ls = []
        for a in list_poem:
            if n == 2: break
            if a[1] == 'half':
                ls.append(a[0])
                n += 1
            elif a[1] == 'title':
                continue
            else:
                ls.append(a[1])
                n += 1 
        txt1 = daw_araby.stripTashkeel(ls[0])
        txt2 = daw_araby.stripTashkeel(ls[1])
        h11 = txt1[-1]
        h12 = txt1[-2]
        h13 = txt1[-3]
        h21 = txt2[-1]
        h22 = txt2[-2]
        h23 = txt2[-3]
        if h11 == u'ا' and h12 == u'ه':
            if h13 == h23: return h13
            else: return h12
        if h11 in [u'ا', u'ى', u'ه', u'ة', u'و', u'ي']:
            if h12 == h22 or h12 == h21: return h12
            else: return h11
        else: return h11
        
# a إعادة اسم القصيدة ونصها ومعلوماتها-------------------------
    
def name_poem(text):
    new_text = u''
    n = 0
    naw3 = 1
    gharadh = 0
    baher = 0
    kafia = 0
    text = right_space(text)
    h = rawi_poem(text)
    rawi = get_int_rawi(h)
    l_abiat = text.splitlines(1)
    for a in l_abiat:
        if u'=' in a:
            n += 1
            d = a.split(' ')
            if u'النوع' in a:
                try: naw3 = get_int(elnaw3, d[-1])
                except: naw3 = 1
            if u'الغرض' in a:
                try: gharadh = get_int(elgharadh, d[-1])
                except: gharadh = 0
            if u'القافية' in a:
                try: kafia = get_int(elkawafi, d[-1])
                except: kafia = 0
            if u'الروي' in a:
                try: rawi = get_int(elrawi, d[-1])
                except: 
                    h = rawi_poem(text)
                    rawi = get_int_rawi(h)
            if u'البحر' in a:
                try: baher = get_int(elbehor, d[-1])
                except: baher = 0
        else:
            new_text += a+'\n'
    if '*' in l_abiat[n]:
        half = l_abiat[n].split('*')
        name = half[0]
    else:
        name = l_abiat[n]
    name = re.sub('\n+', '', name)
    return name, new_text, naw3, gharadh, baher, rawi, kafia

# a قائمة بكلمات القصيدة وعددها-----------------------------
    
def n_words(text):
    txt = re.sub('\*', '', text)
    text = right_space(txt)
    ls = text.split()
    return ls, len(ls)

# a إعادة أبيات محددة من القصيدة-----------------------------
    
def get_abiat(text, v1, v2, t):
    l_abiat = text.splitlines(1)
    lst = []
    for a in range(len(l_abiat)):
        if u'*' in l_abiat[a] and len(l_abiat[a]) > 15 and t == 2:
            lst.append(l_abiat[a])
        lst.append(l_abiat[a])
    x = v1-1
    y = v2
    ls = lst[x: y]
    ll = []
    for a in range(len(ls)):
        if u'*' in ls[a] and len(ls[a]) > 15:
            ll.append(ls[a])
    ls = []
    for a in ll:
        if a not in ls:
            ls.append(a)
    if len(ls) > 0:
        return '\n'.join(ls)
    else: return None

# a إعادة موضع أطول شطر في القصيدة-----------------------------
    
def longer_half(text, label, a3aridh):
    l_abiat, n_abiat = my_split(text, a3aridh)
    s = 0
    i = 0
    c = 0
    for a in l_abiat:
        if a[1] != 'title':
            label.set_text(a[0])
            pangolayout = label.get_layout()
            d = pangolayout.get_pixel_size()
            if d[0] > s :
                s = d[0]
                c = 0
                i = l_abiat.index(a, )
            if a[1] != 'half':
                label.set_text(a[1])
                pangolayout = label.get_layout()
                d1 = pangolayout.get_pixel_size()
                if d1[0] > s :
                    s = d1[0]
                    c = 1
                    i = l_abiat.index(a, )
    return (i*2)+c, n_abiat

# a حساب طول أطول شطر بالبكسلات-----------------------------
    
def length_Half(poem, label, length, size_font, width_window, a3aridh):
    list_verses, n_abiat = my_split(poem, a3aridh)
    a1 = length/2
    a2 = length%2
    lengther = list_verses[a1][a2]
    label.set_text(lengther)
    pangolayout = label.get_layout()
    d = pangolayout.get_pixel_size()
    label.set_text(u'حــــب')
    pangolayout = label.get_layout()
    t = pangolayout.get_pixel_size()
    label.set_text(u'حب')
    pangolayout = label.get_layout()
    s = pangolayout.get_pixel_size()
    label.set_text(u' ')
    pangolayout = label.get_layout()
    e = pangolayout.get_pixel_size()
    long_verse = d[0]+10
    long_tatwil = (t[0]-s[0])/4
    long_space = e[0]
    return load_poem(label, list_verses, long_verse, 
                     long_tatwil, long_space, size_font, width_window)

# a إيجاد موضع لزيادة التطويل---------------------------------

def my_re(labeltext):
    for s in daw_araby.tatwil_locations:
        if u''.join(s) in labeltext:
            return u''.join(s)

# a زيادة التطويلات لتعديل طول الأبيات---------------------------

def ta3dil_by_tatweel(text, label, long_verse, long_tatwil):
    min_v = int(daw_config.getf('min_long'))
    if long_verse > min_v: pass
    else: long_verse = min_v
    label.set_text(text)
    pangolayout = label.get_layout()
    s = pangolayout.get_pixel_size()
    if long_tatwil == 0 : return text
    rn = ((long_verse-s[0])/long_tatwil)
    re_text = my_re(text)
    tatwil = u'\u0640'*rn
    new_text = text.replace(re_text, re_text[:-1]+tatwil+re_text[-1], 1)
    return new_text

# a زيادة المسافات لتعديل طول الأبيات---------------------------

def ta3dil_by_space(text, label, long_verse, long_space):
    min_v = int(daw_config.getf('min_long'))
    if long_verse > min_v: pass
    else: long_verse = min_v
    label.set_text(text)
    pangolayout = label.get_layout()
    s = pangolayout.get_pixel_size()
    list_text = text.split()
    n_all = (long_verse-s[0])/long_space
    n_one = n_all/((len(list_text))-1)
    n_add = n_all%((len(list_text))-1)
    if n_all <= 0 : return text
    new_text = ''
    for a in list_text:
        if a == list_text[-1]: new_text += a
        else:
            new_text += a+' '+' '*n_one
            if n_add > 0:
                new_text += " "
                n_add -= 1
    return new_text

def ta3dil(text, label, long_verse, long_tatwil, long_space):
    if daw_config.getf('tandhid') == 0:
        return ta3dil_by_tatweel(text, label, long_verse, long_tatwil)
    else: 
        return ta3dil_by_space(text, label, long_verse, long_space)

# a تعديل الأشطر وجمعها------------------------------------------

def load_poem(label, list_verses, long_verse, long_tatwil, long_space, size_font, width_window):
    poem = u''
    max_v = int(daw_config.getf('max_long'))
    min_v = int(daw_config.getf('min_long'))
    b_h = (daw_config.getn('b_half')+1)*2
    half_space = (width_window-30)/2
    if half_space >= long_verse*5/6: v = (long_verse*2)/3
    else: v = (2*half_space)-long_verse
    if daw_config.getf('tarakeb') == 0 or long_verse > max_v or \
    long_verse > half_space-((size_font*b_h)/2) or min_v > half_space-((size_font*b_h)/2):
        t = 2
        for a in list_verses:
            if a[1] == 'title':
                poem += right_space(a[0])+'\n'
            elif a[1] == 'half':
                poem += re.sub('\n\n', '\n', ta3dil(a[0], label, long_verse, long_tatwil, long_space)+'\n')
            else:
                h1 = ta3dil(a[0], label, long_verse, long_tatwil, long_space)
                h2 = ta3dil(a[1], label, long_verse, long_tatwil, long_space)
                poem += h1+u' '*(v/long_space)+u'\n'
                poem += u' '*(v/long_space)+h2+u'\n'
    else:
        t = 1
        for a in list_verses:
            if a[1] == 'title':
                poem += right_space(a[0])+'\n'
            elif a[1] == 'half':
                poem += re.sub('\n\n', '\n', ta3dil(a[0], label, long_verse, long_tatwil, long_space)+'\n')
            else:
                h1 = ta3dil(a[0], label, long_verse, long_tatwil, long_space)
                h2 = ta3dil(a[1], label, long_verse, long_tatwil, long_space)
                poem += h1
                poem += u' '*(size_font*b_h/long_space)
                poem += h2+u'\n'
    return poem, t
#ddd = u'''
#هَلِ البابُ مَفروجٌ فَأنظر نظرةً * بِعينيَ أَرضاً عزّ عندي مرامها
#فَيا حبّذا الدهنا وَطيبُ تُرابِها * وَأَرضٌ فضاءٌ يصدح الليلُ هامها
#'''
#print rawi_poem(ddd)