# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import sqlite3
import daw_araby, daw_customs
from os.path import join
from daw_contacts import MyDB
from subprocess import call
from gi.repository import Gtk, Pango


class Count(Gtk.Box):
    
    def __init__(self, parent):
        self.parent = parent
        self.size_font = int(self.parent.theme.fontch[-2:])
        self.con = sqlite3.connect(daw_customs.MY_DATA)
        self.db = MyDB()
        self.con.create_function('fuzzy', 1, daw_araby.fuzzy)
        self.cur = self.con.cursor()
        Gtk.Box.__init__(self,spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.view_count = daw_customs.ViewClass()
        self.view_count_bfr = self.view_count.get_buffer()
        self.view_count_tag = self.view_count_bfr.create_tag("title")
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_count)
        self.pack_start(scroll, True, True, 0)
        self.show_all()
   
    def near_page(self, v):
        self.size_font += v
        self.view_count.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
   
    def move_in_page(self, v):
        return
     
    def n_dawawin(self, sex, age):
        self.cur.execute('SELECT id_poet FROM poets WHERE sex=? AND age=?', (sex, age))
        poets = self.cur.fetchall()
        return len(poets)
    
    def n_poems(self, sex, age):
        self.cur.execute('SELECT id_poem FROM infopoem WHERE sex=? AND age=?', (sex, age))
        poems = self.cur.fetchall()
        return len(poems)
    
    def n_verses(self, sex, age):
        self.cur.execute('SELECT sum(abiat) FROM infopoem WHERE sex=? AND age=?', (sex, age))
        abiats = self.cur.fetchall()
        if abiats[0][0] == None: return 0
        return abiats[0][0] 
       
    def refresh(self, *a):
        self.v_f_1 = self.n_verses(2, 1)
        self.v_m_1 = self.n_verses(1, 1)
        self.p_f_1 = self.n_poems(2, 1)
        self.p_m_1 = self.n_poems(1, 1)
        self.d_f_1 = self.n_dawawin(2, 1)
        self.d_m_1 = self.n_dawawin(1, 1)

        self.v_f_2 = self.n_verses(2, 2)
        self.v_m_2 = self.n_verses(1, 2)
        self.p_f_2 = self.n_poems(2, 2)
        self.p_m_2 = self.n_poems(1, 2)
        self.d_f_2 = self.n_dawawin(2, 2)
        self.d_m_2 = self.n_dawawin(1, 2)

        self.v_f_3 = self.n_verses(2, 3)
        self.v_m_3 = self.n_verses(1, 3)
        self.p_f_3 = self.n_poems(2, 3)
        self.p_m_3 = self.n_poems(1, 3)
        self.d_f_3 = self.n_dawawin(2, 3)
        self.d_m_3 = self.n_dawawin(1, 3)

        self.v_f_4 = self.n_verses(2, 4)
        self.v_m_4 = self.n_verses(1, 4)
        self.p_f_4 = self.n_poems(2, 4)
        self.p_m_4 = self.n_poems(1, 4)
        self.d_f_4 = self.n_dawawin(2, 4)
        self.d_m_4 = self.n_dawawin(1, 4)

        self.v_f_5 = self.n_verses(2, 5)
        self.v_m_5 = self.n_verses(1, 5)
        self.p_f_5 = self.n_poems(2, 5)
        self.p_m_5 = self.n_poems(1, 5)
        self.d_f_5 = self.n_dawawin(2, 5)
        self.d_m_5 = self.n_dawawin(1, 5)

        self.v_f_10 = self.n_verses(2, 10)
        self.v_m_10 = self.n_verses(1, 10)
        self.p_f_10 = self.n_poems(2, 10)
        self.p_m_10 = self.n_poems(1, 10)
        self.d_f_10 = self.n_dawawin(2, 10)
        self.d_m_10 = self.n_dawawin(1, 10)

        self.v_f_11 = self.n_verses(2, 11)
        self.v_m_11 = self.n_verses(1, 11)
        self.p_f_11 = self.n_poems(2, 11)
        self.p_m_11 = self.n_poems(1, 11)
        self.d_f_11 = self.n_dawawin(2, 11)
        self.d_m_11 = self.n_dawawin(1, 11)

        self.v_f_6 = self.n_verses(2, 6)
        self.v_m_6 = self.n_verses(1, 6)
        self.p_f_6 = self.n_poems(2, 6)
        self.p_m_6 = self.n_poems(1, 6)
        self.d_f_6 = self.n_dawawin(2, 6)
        self.d_m_6 = self.n_dawawin(1, 6)

        self.v_f_7 = self.n_verses(2, 7)
        self.v_m_7 = self.n_verses(1, 7)
        self.p_f_7 = self.n_poems(2, 7)
        self.p_m_7 = self.n_poems(1, 7)
        self.d_f_7 = self.n_dawawin(2, 7)
        self.d_m_7 = self.n_dawawin(1, 7)

        self.v_f_8 = self.n_verses(2, 8)
        self.v_m_8 = self.n_verses(1, 8)
        self.p_f_8 = self.n_poems(2, 8)
        self.p_m_8 = self.n_poems(1, 8)
        self.d_f_8 = self.n_dawawin(2, 8)
        self.d_m_8 = self.n_dawawin(1, 8)
         
        self.v_f_9 = self.n_verses(2, 9)
        self.v_m_9 = self.n_verses(1, 9)
        self.p_f_9 = self.n_poems(2, 9)
        self.p_m_9 = self.n_poems(1, 9)
        self.d_f_9 = self.n_dawawin(2, 9)
        self.d_m_9 = self.n_dawawin(1, 9)
        self.p_n_9 = self.n_poems(0, 9)
        self.v_n_9 = self.n_verses(0, 9)
    
    def make_html(self, *a):
        self.refresh()
        template  = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>إحصاءات دواوين العرب</title>
        </head>
        <body>
        <table
        style="vertical-align: middle; text-align: center; width: 800px; height: 700px; margin-left: auto; margin-right: auto;"
        border = 1"1" cellpadding = 1"2" cellspacing = 1"2">
        <caption style="caption-side: right;"><br>
        </caption><tbody>
        <tr>
        <td style="background-color: rgb(204, 51, 204);">أبيات الشواعر<br>
        </td>
        <td style="background-color: rgb(204, 51, 204);">أبيات الشعراء<br>
        </td>
        <td style="background-color: rgb(204, 51, 204);">قصائد الشواعر<br>
        </td>
        <td style="background-color: rgb(204, 51, 204);">قصائد الشعراء<br>
        </td>
        <td style="background-color: rgb(204, 51, 204);">دواوين الشواعر<br>
        </td>
        <td style="background-color: rgb(204, 51, 204);">دواوين الشعراء<br>
        </td>
        <td style="background-color: rgb(51, 204, 255);">العصور</td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">الجاهلي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">المخضرمون<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">صدر اﻹسلام<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">الأموي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">العباسي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">الفاطمي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">الأيوبي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">المملوكي<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">العثماني<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">الحديث<br>
        </td>
        </tr>
        <tr>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td>{}<br>
        </td>
        <td style="background-color: rgb(255, 190, 94);">غير معروف<br>
        </td>
        </tr>
        </tbody>
        </table>
        <br>
        <br>
        </body>
        </html>'''.format(self.v_f_1, self.v_m_1, self.p_f_1, self.p_m_1, self.d_f_1, self.d_m_1,
                          self.v_f_2, self.v_m_2, self.p_f_2, self.p_m_2, self.d_f_2, self.d_m_2,
                          self.v_f_3, self.v_m_3, self.p_f_3, self.p_m_3, self.d_f_3, self.d_m_3,
                          self.v_f_4, self.v_m_4, self.p_f_4, self.p_m_4, self.d_f_4, self.d_m_4,
                          self.v_f_5, self.v_m_5, self.p_f_5, self.p_m_5, self.d_f_5, self.d_m_5,
                          self.v_f_10, self.v_m_10, self.p_f_10, self.p_m_10, self.d_f_10, self.d_m_10,
                          self.v_f_11, self.v_m_11, self.p_f_11, self.p_m_11, self.d_f_11, self.d_m_11,
                          self.v_f_6, self.v_m_6, self.p_f_6, self.p_m_6, self.d_f_6, self.d_m_6,
                          self.v_f_7, self.v_m_7, self.p_f_7, self.p_m_7, self.d_f_7, self.d_m_7,
                          self.v_f_8, self.v_m_8, self.p_f_8, self.p_m_8, self.d_f_8, self.d_m_8,
                          self.v_f_9, self.v_m_9, self.p_f_9, self.p_m_9, self.d_f_9, self.d_m_9)
        
        file_html = join(daw_customs.HOME_DIR, 'count.html')
        file_count = open(file_html, 'w')
        file_count.write(template)
        file_count.close()
        call(['xdg-open', file_html])
        
    def make_text(self, *a):
        self.refresh()
        new_text = '''
        صفحة إحصاء الدواوين والقصائد والأبيات الملحقة بقاعدة بيانات برنامج دواوين العرب :
        عدد الدواوين الإجمالي : {} ،
        عدد القصائد الإجمالي : {} ،
        عدد الأبيات الإجمالي : {} ،
        ،============================================،
        
        العصر الجاهلي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        عصر المخضرمين :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر الإسلامي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر الأموي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر العباسي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر الفاطمي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر الأيوبي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر المملوكي :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر العثماني :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        العصر الحديث :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        غير المعروف عصره :
        الشعراء :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الشواعر :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        الكل :
        عدد الدواوين : {} ،
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        ...................................
        غير المعروف قائله :
        عدد القصائد : {} ،
        عدد الأبيات : {} ،
        '''.format(self.db.n_dawawin(), self.db.n_poems(), self.db.n_verses(),
                      self.d_m_1, self.p_m_1, self.v_m_1, self.d_f_1, self.p_f_1, self.v_f_1,
                      self.d_m_1+self.d_f_1 ,self.p_m_1+self.p_f_1, self.v_m_1+self.v_f_1,
                      self.d_m_2, self.p_m_2, self.v_m_2, self.d_f_2, self.p_f_2, self.v_f_2,
                      self.d_m_2+self.d_f_2 , self.p_m_2+self.p_f_2, self.v_m_2+self.v_f_2,
                      self.d_m_3, self.p_m_3, self.v_m_3, self.d_f_3, self.p_f_3, self.v_f_3,
                      self.d_m_3+self.d_f_3 ,self.p_m_3+self.p_f_3, self.v_m_3+self.v_f_3,
                      self.d_m_4, self.p_m_4, self.v_m_4, self.d_f_4, self.p_f_4, self.v_f_4,
                      self.d_m_4+self.d_f_4 ,self.p_m_4+self.p_f_4, self.v_m_4+self.v_f_4,
                      self.d_m_5, self.p_m_5, self.v_m_5, self.d_f_5, self.p_f_5, self.v_f_5,
                      self.d_m_5+self.d_f_5, self.p_m_5+self.p_f_5, self.v_m_5+self.v_f_5,
                      self.d_m_10, self.p_m_10, self.v_m_10, self.d_f_10, self.p_f_10, self.v_f_10,
                      self.d_m_10+self.d_f_10 ,self.p_m_10+self.p_f_10, self.v_m_10+self.v_f_10,
                      self.d_m_11, self.p_m_11, self.v_m_11, self.d_f_11, self.p_f_11, self.v_f_11,
                      self.d_m_11+self.d_f_11 ,self.p_m_11+self.p_f_11, self.v_m_11+self.v_f_11,
                      self.d_m_6, self.p_m_6, self.v_m_6, self.d_f_6, self.p_f_6, self.v_f_6,
                      self.d_m_6+self.d_f_6 ,self.p_m_6+self.p_f_6, self.v_m_6+self.v_f_6,
                      self.d_m_7, self.p_m_7, self.v_m_7, self.d_f_7, self.p_f_7, self.v_f_7,
                      self.d_m_7+self.d_f_7 ,self.p_m_7+self.p_f_7, self.v_m_7+self.v_f_7,
                      self.d_m_8, self.p_m_8, self.v_m_8, self.d_f_8, self.p_f_8, self.v_f_8,
                      self.d_m_8+self.d_f_8 ,self.p_m_8+self.p_f_8, self.v_m_8+self.v_f_8,
                      self.d_m_9, self.p_m_9, self.v_m_9, self.d_f_9, self.p_f_9, self.v_f_9,
                      self.d_m_9+self.d_f_9 ,self.p_m_9+self.p_f_9, self.v_m_9+self.v_f_9,
                      self.p_n_9, self.v_n_9)
        self.view_count_bfr.set_text(new_text)