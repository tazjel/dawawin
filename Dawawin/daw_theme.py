# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, exists
from gi.repository import Gtk, Gdk
import daw_config, daw_customs

#a----------------------------------------------------------------------       


class MyTheme(object):
    
    def apply_preference(self, *a):
        if daw_config.getv('tr') == '1':
            self.fonttd = daw_config.getv('fonttd')
            self.fonttp = daw_config.getv('fonttp')
            self.fontmp = daw_config.getv('fontmp')
            self.fontch = daw_config.getv('fontch')
            self.fontan = daw_config.getv('fontan')
            self.colortd = daw_config.getv('colortd')
            self.colortp = daw_config.getv('colortp')
            self.colormp = daw_config.getv('colormp')
            self.colorch = daw_config.getv('colorch')
            self.coloran = daw_config.getv('coloran')
            self.colorb = daw_config.getv('colorb')
            self.colorfs = daw_config.getv('colorfs')
            self.colorbs = daw_config.getv('colorbs')
            self.colorss = daw_config.getv('colorss')
            self.colorbp = daw_config.getv('colorbp')
        else:
            self.fonttd = 'KacstOne 15'
            self.fonttp = 'KacstOne 13'
            self.fontmp = 'Simplified Naskh 22'
            self.fontch = 'Amiri 18'
            self.fontan = 'KacstOne 15'
            self.colortd = '#868609091515'
            self.colortp = '#202040400000'
            self.colormp = '#202040400000'
            self.colorch = '#202040400000'
            self.coloran = '#868609091515'
            self.colorb = '#fdfdfdfdd7d7'
            self.colorfs = '#ffffffffffff'
            self.colorbs = '#9e9ec1c17a7a'
            self.colorss = '#fe71fab0870b'
            self.colorbp = '#fcb2eb47aeb5'
    
    def __init__(self):
        self.refrech()
        
    def refrech(self, *a):
        self.apply_preference()
        ornament = daw_config.getv('ornament-file')
        p = join(daw_customs.ORNAMENT, ornament)
        bg0 = join(daw_customs.ICON_DIR, 'bg1.png')
        bg1 = join(daw_customs.ICON_DIR, 'bg0.png')
        if daw_config.getv('ornament') == '1': background = 'background-image: url("{}");'.format(p,)
        else: background = 'background-color: {};'.format(daw_customs.rgb(self.colorb),)
        if not exists(p): background = 'background-color: {};'.format(daw_customs.rgb(self.colorb),)
        css_data = '''
            * {
            -GtkPaned-handle-size: 7;
            }
            View-editable:selected,
            View:selected,
            MyView:selected,
            Treepoem:selected,
            Tree:selected  {
            background-color: '''+daw_customs.rgb(self.colorbs)+''';
            background-image: none;
            color: '''+daw_customs.rgb(self.colorfs)+''';
            }
            View-editable {
            background-color: '''+daw_customs.rgb(self.colorb)+''';
            background-image: none;
            color: '''+daw_customs.rgb(self.colorch)+''';
            font: Simplified Naskh 15;
            }
            View {
            background-color: '''+daw_customs.rgb(self.colorb)+''';
            background-image: none;
            color: '''+daw_customs.rgb(self.colorch)+''';
            font: '''+self.fontch+''';
            }
            Tree {
            background-color: '''+daw_customs.rgb(self.colorbp)+''';
            background-image: none;
            color: '''+daw_customs.rgb(self.colortd)+''';
            font: '''+self.fonttd+''';
            }
            Treepoem {
            background-color: '''+daw_customs.rgb(self.colorb)+''';
            background-image: none;
            color: '''+daw_customs.rgb(self.colortp)+''';
            font: '''+self.fonttp+''';
            }
            Myscroll, MyView {
            color: '''+daw_customs.rgb(self.colormp)+''';
            font: '''+self.fontmp+''';
            }
            Myscroll, MyView {
            '''+background+'''
            } '''
            
        css_data1 = '''
            GtkToolbar {
            background-image: url("'''+bg1+'''");
            }
            GtkEventbox, GtkWindow, GtkNotebook,
            GtkPaned {
            background-image: url("'''+bg0+'''");
            }
            GtkNotebook tab {
            background-image: none;
            }
            Togglebutton {
            background-image: url("'''+bg1+'''");
            color: #ffffff;
            text-shadow: black 5px 5px 5px;
            border: 1px solid grey;
            }
            Togglebutton:active {
            background-color: grey;
            background-image: none;
            border: 2px solid #555555;
            }
            '''+css_data
            
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        context = Gtk.StyleContext()
        try: 
            if daw_config.getv('theme') == '1': css_provider.load_from_data(css_data1)
            else: css_provider.load_from_data(css_data)
        except: css_provider.load_from_data(css_data)
        context.add_provider_for_screen(screen, css_provider,
                                         Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
