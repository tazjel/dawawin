# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import os.path
from os import mkdir
import ConfigParser

myfile = os.path.expanduser('~/.dawawin/Dawawin.cfg')
config = ConfigParser.RawConfigParser()
config.read(myfile)
section = 'settings'

def load():
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, 'path'):
        config.set(section, 'path', os.path.expanduser('~/DawawinArab/Dawawin.db'))
    if not config.has_option(section, 'open'):
        config.set(section, 'open', 1)
    if not config.has_option(section, 'start'):
        config.set(section, 'start', 0)
    if not config.has_option(section, 'fonttd'):
        config.set(section, 'fonttd', 'KacstOne 15')
    if not config.has_option(section, 'fonttp'):
        config.set(section, 'fonttp', 'KacstOne 15')
    if not config.has_option(section, 'fontmp'):
        config.set(section, 'fontmp', 'Simplified Naskh 22')
    if not config.has_option(section, 'fontch'):
        config.set(section, 'fontch', 'Amiri 18')
    if not config.has_option(section, 'fontan'):
        config.set(section, 'fontan', 'KacstOne 15')
    if not config.has_option(section, 'colortd'):
        config.set(section, 'colortd', '#868609091515')
    if not config.has_option(section, 'colortp'):
        config.set(section, 'colortp', '#202040400000')
    if not config.has_option(section, 'colormp'):
        config.set(section, 'colormp', '#202040400000')
    if not config.has_option(section, 'colorch'):
        config.set(section, 'colorch', '#202040400000')
    if not config.has_option(section, 'coloran'):
        config.set(section, 'coloran', '#868609091515')
    if not config.has_option(section, 'colorb'):
        config.set(section, 'colorb', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'colorfs'):
        config.set(section, 'colorfs', '#ffffffffffff')
    if not config.has_option(section, 'colorbs'):
        config.set(section, 'colorbs', '#9e9ec1c17a7a')
    if not config.has_option(section, 'colorss'):
        config.set(section, 'colorss', '#fe71fab0870b')
    if not config.has_option(section, 'colorbp'):
        config.set(section, 'colorbp', '#fcb2eb47aeb5')
    if not config.has_option(section, 'tr'):
        config.set(section, 'tr','0') # tr = default|custom 4 color&font
    if not config.has_option(section, 'theme'):
        config.set(section, 'theme','0')
    if not config.has_option(section, 'tashkil'):
        config.set(section, 'tashkil', '1')
    if not config.has_option(section, 'help'):
        config.set(section, 'help', '1')
    if not config.has_option(section, 'marks'):
        config.set(section, 'marks', '[]')
    if not config.has_option(section, 'b_abiat'):
        config.set(section, 'b_abiat', 0)
    if not config.has_option(section, 'b_half'):
        config.set(section, 'b_half', 1)
    if not config.has_option(section, 'tarakeb'):
        config.set(section, 'tarakeb', 1)
    if not config.has_option(section, 'tandhid'):
        config.set(section, 'tandhid', 0)
    if not config.has_option(section, 'max_long'):
        config.set(section, 'max_long', 700)
    if not config.has_option(section, 'min_long'):
        config.set(section, 'min_long', 200)
    if not config.has_option(section, 'ornament-file'):
        config.set(section, 'ornament-file', 'fibers.png')
    if not config.has_option(section, 'ornament'):
        config.set(section, 'ornament', '1')
    if not config.has_option(section, 'n_dawawin'):
        config.set(section, 'n_dawawin', ' ')
    if not config.has_option(section, 'n_poems'):
        config.set(section, 'n_poems', ' ')
    if not config.has_option(section, 'n_verses'):
        config.set(section, 'n_verses', ' ')
    with open(myfile, 'wa') as configfile:
        config.write(configfile)

def setv(option, value):
    config.set(section, option, value)
    with open(myfile, 'wa') as configfile:
        config.write(configfile)
   
def getv(option):
    value = config.get(section, option)
    return value

def getn(option):
    value = config.getint(section, option)
    return value

def getf(option):
    value = config.getfloat(section, option)
    return value
  
mydir = os.path.dirname(myfile)
if not os.path.exists(mydir):
    try:  mkdir(mydir)
    except: raise
if not os.path.exists(myfile):
    try: 
        open(myfile,'w+')
    except: raise
load()
