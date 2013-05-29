# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from shutil import copyfile
from os.path import join, exists
from os import mkdir
from gi.repository import Gtk, Pango
#from gi.repository import WebKit
import daw_config, daw_customs

fontan  = 'KacstOne 15'
colormp = '#202040400000'
coloran = '#868609091515'
colorb  = '#fdfdfdfdd7d7'

#wv = WebKit.WebView()

class Exporter(object):
    
    def __init__(self, parent, name_poem, name_poet, text_poem, font):
        self.parent = parent
        self.background_image = daw_config.getv('ornament-file')
        if daw_config.getv('tr') == '1':
            self.colorb = daw_customs.rgb(daw_config.getv('colorb'))
            self.colormp = daw_customs.rgb(daw_config.getv('colormp'))
            self.coloran = daw_customs.rgb(daw_config.getv('coloran'))
            self.fontan = daw_config.getv('fontan')
        else:
            self.colorb = daw_customs.rgb(colorb)
            self.colormp = daw_customs.rgb(colormp)
            self.coloran = daw_customs.rgb(coloran)
            self.fontan = fontan
            
        self.name_poem = name_poem
        self.name_poet = name_poet
        self.text_poem = text_poem
        fdmp = Pango.FontDescription(font)
        self.fontmp_family = fdmp.get_family()
        self.fontmp_size = font[-2:]+'px'
        fdan = Pango.FontDescription(self.fontan)
        self.fontan_family = fdan.get_family()
        self.fontan_size = self.fontan[-2:]+'px'

    def make_html(self, *a):
        if daw_config.getv('ornament') == '1': background = 'background-image: url({});'.format(self.background_image,)
        else: background = 'background-color: {};'.format(self.colorb,)
                
        html_text = self.text_poem.replace('\n', '\n<br>').replace(' ', '&nbsp;')
        template = [
                    u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', 
                    u'"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', 
                    u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">', 
                    u'<head>', 
                    u'<title>{}</title>'.format(self.name_poem,), 
                    u'<meta http-equiv="content-type" content="text/html; charset=utf-8" />', 
                    u'<style type="text/css">', 
                    u'body {', 
                    u'text-align: center; ', 
                    u'{}'.format(background,), 
                    u'}', 
                    u'span.speaker{', 
                    u'font-family: {};'.format(self.fontan_family,), 
                    u'font-size: {};'.format(self.fontan_size,), 
                    u'color: {};'.format(self.coloran,), 
                    u'}', 
                    u'span.nasse{', 
                    u'font-family: {};'.format(self.fontmp_family,), 
                    u'font-size: {};'.format(self.fontmp_size,), 
                    u'color: {};'.format(self.colormp,), 
                    u'}', 
                    u'</style>', 
                    u'</head>', 
                    u'<body dir="rtl">', 
                    u'<span class="speaker">{}</span><br>'.format(self.name_poet,), 
                    u'<span class="nasse">{}</span>'.format(html_text,), 
                    u'</body>', 
                    u'</html>']
        text =  '\n'.join(template)
        return text.encode('utf-8')
    
    def dlg_dest(self):
        dir_save = None
        save_dlg = Gtk.FileChooserDialog("اختر المجلد الذي تريد التصدير إليه", self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            dir_save = save_dlg.get_filename()
        save_dlg.destroy()
        return dir_save
    
    def export_html(self, *a):    
        template = self.make_html()
        dir_save = self.dlg_dest()
        if dir_save == None: return
        if not exists(join(dir_save, self.name_poem.encode('utf-8'))):
            try:  mkdir(join(dir_save, self.name_poem))
            except: raise
        file_save = open(join(dir_save, self.name_poem, self.name_poem+'.html'), 'w')
        file_save.write(template)
        file_save.close()
        if daw_config.getv('ornament') == '1':
            copyfile(join(daw_customs.ORNAMENT,self.background_image), join(dir_save, self.name_poem, self.background_image))
            
    def export_txt(self, *a):    
        template = self.text_poem
        dir_save = self.dlg_dest()
        if dir_save == None: return
        if not exists(join(dir_save, self.name_poem.encode('utf-8'))):
            try:  mkdir(join(dir_save, self.name_poem))
            except: raise
        file_save = open(join(dir_save, self.name_poem, self.name_poem+'.txt'), 'w')
        file_save.write(template.encode('utf-8'))
        file_save.close()
     
    def print_pdf(self, action, *a, **kw):
        """
        html = self.make_html()
        wv.load_html_string(html,'file:///')
        return getattr(wv, action)(*a,**kw)
        """
