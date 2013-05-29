# coding: utf-8

# DawawinPlayer 0.6

import sys

try:
    from gi.repository import Gtk, GObject
except ImportError as e:
    print e
    sys.exit(1)

try:
    from gi.repository import Gst
except ImportError as e:
    print e


SECOND = 10.00 ** 9 # (ns)
INTERVAL = 500      # (ms)

class Mawso3aPlayer(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_default_direction(Gtk.TextDirection.RTL)
        
        
        self.is_stopped = True
        self.is_playing = False
        self.is_paused = False
        
        self._player = None
        self._timer_id = None
        
        
        hbox = Gtk.HBox()
        self.pack_start(hbox, False, False, 0)
        
        # Play button
        self._play_btn = Gtk.ToolButton()
        self._play_btn.connect('clicked', self.on_play)
        self._play_btn.set_icon_name('m-play')
        self._play_btn.set_tooltip_text('تشغيل')
        hbox.pack_start(self._play_btn, False, False, 0)
        
        # Pause button
        self._pause_btn = Gtk.ToolButton()
        self._pause_btn.connect('clicked', self.on_pause)
        self._pause_btn.set_icon_name('m-pause')
        self._pause_btn.set_tooltip_text('إيقاف مؤقت')
        hbox.pack_start(self._pause_btn, False, False, 0)
        
        # Stop button
        self._stop_btn = Gtk.ToolButton()
        self._stop_btn.set_icon_name('m-stop')
        self._stop_btn.connect('clicked', self.on_stop)
        self._stop_btn.set_tooltip_text('إيقاف')
        hbox.pack_start(self._stop_btn, False, False, 0)
        
        # Back button
        self._back_btn = Gtk.ToolButton()
        self._back_btn.connect('clicked', self.on_back)
        self._back_btn.set_icon_name('m-backward')
        self._back_btn.set_tooltip_text('5 ثواني للخلف')
        hbox.pack_start(self._back_btn, False, False, 0)
        
        # Forward button
        self._forward_btn = Gtk.ToolButton()
        self._forward_btn.connect('clicked', self.on_forward)
        self._forward_btn.set_icon_name('m-forward')
        self._forward_btn.set_tooltip_text('5 ثواني للأمام')
        hbox.pack_start(self._forward_btn, False, False, 0)
        
        # Repeat button
        self._repeat_btn = Gtk.ToggleToolButton()
        self._repeat_btn.set_icon_name('m-repeat')
        self._repeat_btn.set_tooltip_text('تكرار')
        hbox.pack_start(self._repeat_btn, False, False, 0)
        
        # Sep
        hbox.pack_start(Gtk.VSeparator(), False, False, 7) 
        
        self.img_val = Gtk.Image()
        self.img_val.set_from_icon_name('m-volume-2', Gtk.IconSize.BUTTON)
        hbox.pack_start(self.img_val, False, False, 0)
        
        # Volume scale
        self._volume = Gtk.HScale()
        self._volume.set_size_request(140, 8)
        self._volume.set_value_pos(0)
        self._volume.set_range(0, 100)
        self._volume.set_value(50)
        self._volume.set_draw_value(False)
        self._volume.connect("value-changed", self.on_volume_changed)
        self._volume.set_increments(0, 1)
        self._volume.set_digits(0)
        hbox.pack_start(self._volume, False, False, 0)
        self.val_lab = Gtk.Label('50')
        hbox.pack_start(self.val_lab, False, False, 0)
        hbox.pack_start(Gtk.Label('%'), False, False, 0)

        self.prepare_gst()
        
        # Time (duration)
        self._time_label = Gtk.Label('00:00 ~ 00:00')
        self._time_label.set_padding(10, 0)
        self._time_label.set_use_markup(True)
        hbox.pack_end(self._time_label, False, False, 0)
    
    
    def prepare_gst(self):
        try:
            Gst.init(None)
            self._player = Gst.ElementFactory.make('playbin2', None)
            self._volume.set_value(50)
        except NameError: 
            self.set_sensitive(False)
            
    
    def _set_states(self, playing, paused, stopped):
        self.is_playing = playing
        self.is_paused = paused
        self.is_stopped = stopped
        self._play_btn.set_sensitive(not playing)
        self._stop_btn.set_sensitive(not stopped)
    
    def _get_image(self, path):
        image = Gtk.Image()
        image.set_from_file(path)
        return image
        
    def on_play(self, *args):
        if self._player:
            self._player.set_state(Gst.State.PLAYING)
            self._set_states(True, False, False)
            self._timer_id = GObject.timeout_add(INTERVAL, self.__on_timer)
    
    def on_back(self, *args):
        if self._player:
            start = self._player.query_position(Gst.Format.TIME)[2] - 5 * SECOND
            if start < 0: start = 0
            self._player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, start)
    
    def on_forward(self, *args):
        if self._player:
            start = self._player.query_position(Gst.Format.TIME)[2] + 5 * SECOND
            if start < 0: start = 0
            self._player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, start)
        
    def on_pause(self, *args):
        if self.is_playing and self._player:
            self._player.set_state(Gst.State.PAUSED)
            self._set_states(False, True, False)
    
    def on_stop(self, *args):
        if self.is_playing or self.is_paused:
            self._player.set_state(Gst.State.NULL)
            self._set_states(False, False, True)
            GObject.source_remove(self._timer_id)
    
    
    def on_volume_changed(self, widget):
        self._player.set_property('volume', widget.get_value()/100.0)
        v = int(widget.get_value())
        self.val_lab.set_text(str(v))
        if v == 0: self.img_val.set_from_icon_name('m-volume-0', Gtk.IconSize.BUTTON)
        elif v <= 33: self.img_val.set_from_icon_name('m-volume-1', Gtk.IconSize.BUTTON)
        elif v <= 75: self.img_val.set_from_icon_name('m-volume-2', Gtk.IconSize.BUTTON)
        else: self.img_val.set_from_icon_name('m-volume-3', Gtk.IconSize.BUTTON)
    
    def __on_timer(self):
        position = self.__get_media_position()
        duration = self.__get_media_duration()
        # Invalid media file
        if duration == 0.0:

            self.on_stop()
            return False
        #--- Start Timer
        if (duration - position) > 0.04:
            # Pause
            if self.is_paused:
                return False
            self._time_label.set_text('{} ~ {}'.format(self.to_time(position), self.to_time(duration)))
            return True
        #--- Stop Timer
        self._time_label.set_text('{} ~ {}'.format(self.to_time(0), self.to_time(duration)))
        # Repeat active
        if self._repeat_btn.get_active():
            self.on_stop()
            self.on_play()
            return False
        self.on_stop()
        return False
    
    def __get_media_duration(self):
        dur = self._player.query_duration(Gst.Format.TIME)
        return dur[2] / SECOND
    
    def __get_media_position(self):
        cur = self._player.query_position(Gst.Format.TIME)
        return cur[2] / SECOND
    
    def __get_percent(self):
        cur = self._player.query_position(Gst.Format.PERCENT)
        dur = self._player.query_duration(Gst.Format.PERCENT)
        try:
            percent = float(cur[2]) / dur[2]
        except ZeroDivisionError:
            percent = 1
        return percent
    
    
    #--------------------- Interface ---------------------#
    
    def set_media(self, media_file):
        if self._player:
            self._player.set_state(Gst.State.NULL)
            if media_file.startswith('/'):
                media_file = ''.join(['file://', media_file])
            self._player.set_property('uri', media_file)
    
    def set_volume(self, value):
        if self._player:
            self._player.set_property('volume', float(value))
        
    def get_volume(self):
        if self._player:
            return self._player.get_property('volume')
    
    def stop(self):
        if self._player:
            self._player.set_state(Gst.State.NULL)
    
    
    def get_media_state(self):
        if not self._player:
            return None
        return self._player.get_state(0)
    
    def to_time(self, duration):
        if duration < 0: duration = 0
        if duration < 3600:
            return '{:0d}:{:02d}'.format(int(duration%3600)/60,
                                             int(duration%3600)%60
                                             )
        else:
            return '{:0d}:{:02d}:{:02d}'.format(int(duration/3600),
                                             int(duration%3600)/60,
                                             int(duration%3600)%60
                                             )
