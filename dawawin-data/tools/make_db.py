#!/usr/bin/python
# -*- coding: utf-8 -*-

#a#      "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"

import sqlite3
con = sqlite3.connect('Dawawin.db')
cur = con.cursor()

con0 = sqlite3.connect('Awzan.db')
cur0 = con0.cursor()

con1 = sqlite3.connect('Help.db')
cur1 = con1.cursor()

con2 = sqlite3.connect('Dict.db')
cur2 = con2.cursor()

cur2.execute('CREATE TABLE lisan (id_term int, term varchar(255) primary key, charh longtext(2000))') 

cur1.execute('CREATE TABLE help (id integer primary key, tit varchar(255), nasse varchar(255))') 
cur1.execute('CREATE TABLE mekadimat (id integer primary key, tit varchar(255), nasse varchar(255))') 
cur1.execute('CREATE TABLE behor (id integer primary key, tit varchar(255), nasse varchar(255))') 

cur0.execute('CREATE TABLE awzan (id_wazn integer primary key, id_baher int, wazn varchar(255), tafa3il  varchar(255), \
takti3 varchar(255), arodh varchar(255), t_arodh varchar(255), dharb varchar(255), t_dharb varchar(255), \
taf3ila1 varchar(255), t_taf3ila1 varchar(255), taf3ila2 varchar(255), t_taf3ila2 varchar(255), \
taf3ila3 varchar(255), t_taf3ila3 varchar(255), taf3ila4 varchar(255), t_taf3ila4 varchar(255), \
taf3ila5 varchar(255), t_taf3ila5 varchar(255), taf3ila6 varchar(255), t_taf3ila6 varchar(255))') 

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
