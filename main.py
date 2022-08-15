import vlc
import random
import time
import calendar
from datetime import datetime
from time import sleep
from pyradios import RadioBrowser
# from tkinter import *
#from tkinter import ttk
import tkinter as tk
# import tkinter.font as tk_font
# from tkinter import messagebox
import webbrowser
import urllib.parse
import pathlib
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"
VER_TK = tk.Tcl().eval('info patchlevel')
SEARCH_ENGINE1 = "https://kagi.com/search?q="
SEARCH_ENGINE2 = "https://duckduckgo.com/?q="
SEARCH_ENGINE3 = "https://www.qwant.com/?q="
SEARCH_ENGINE4 = "https://www.bing.com/search?q="
SEARCH_ENGINE5 = "https://www.google.com/search?q="
SEARCH_ENGINE = SEARCH_ENGINE4

rb = RadioBrowser()
# radios = rb.stations()
radios = rb.search(countrycode="PL")
print(len(radios), "radios downloaded.")

instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
player.audio_set_volume(100)


class GuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        # CENTER WINDOW
        # screenwidth = self.mainwindow.winfo_screenwidth()
        # screenheight = self.mainwindow.winfo_screenheight()
        # alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        # # root.geometry(alignstr)
        # self.mainwindow.geometry(alignstr)

        # self.mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
        #
        # self.mainwindow.after(1000, task)

        self.rid = 0
        self.url = radios[self.rid]["url"]
        self.media = instance.media_new(self.url)
        self.tmp_title = ''
        self.tmp_vol = 100
        self.tmp_stop = 0

    def run(self):
        self.mainwindow.mainloop()

    def favorite_station(self):
        pass

    def shuffle(self):
        self.rid = random.randrange(0, len(radios))
        self.url = radios[self.rid]["url"]

        # FIX .m3u and .pls not playing on vlc.py
        while self.url.find('.m3u') > -1 or self.url.find('.pls') > -1:
            self.rid = random.randrange(0, len(radios))
            self.url = radios[self.rid]["url"]

        meta_list = ['name', 'stationuuid', 'url', 'homepage', 'favicon', 'country', 'countrycode',
                     'language', 'tags', 'bitrate', 'codec', 'votes', 'clickcount']

        print("")
        for i in meta_list:
            if radios[self.rid][i]: print(i + ":", radios[self.rid][i])
        r = rb.click_counter(radios[self.rid]["stationuuid"])
        # if r["ok"]:
        #     print("+1 CLICK")

        self.fade_down()
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        # self.tmp_vol = 100
        player.play()
        self.fade_up()

    def play(self):
        pass

    def stop(self):
        if self.tmp_stop == 0:
            self.fade_down()
            player.stop()
            self.button_21['text'] = "Continue"
            self.tmp_stop = 1
        else:
            self.media = instance.media_new(self.url)
            player.set_media(self.media)
            player.audio_set_volume(0)
            player.play()
            self.fade_up()
            self.button_21['text'] = "Stop"
            self.tmp_stop = 0

    def mute(self):
        if player.is_playing():
            player.audio_toggle_mute()
            if player.audio_get_mute() == 0:
                self.button_12['text'] = "UnMute"
            else:
                self.button_12['text'] = "Mute"

    def prev_station(self):
        pass

    def next_station(self):
        pass

    def config(self):
        pass

    def fade_down(self):
        v0 = player.audio_get_volume()
        self.tmp_vol = v0
        v1 = 0
        for v in range(v0, v1 - 1, -2):
            sleep(0.01)
            if v < 0:
                v = 0
                break
            player.audio_set_volume(v)

    def fade_up(self):
        v0 = player.audio_get_volume()
        v1 = self.tmp_vol
        self.tmp_vol = v0
        for v in range(v0, v1 + 2):
            sleep(0.01)
            if v > 100:
                v = 100
                break
            player.audio_set_volume(v)

    def button_info(self):
        s = self.media.get_meta(12)
        if s and self.tmp_title != s:
            date_time = datetime.fromtimestamp(calendar.timegm(time.gmtime()))
            str_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S >> ")
            print(str_date_time, s)
            self.tmp_title = s

    def button_search(self):
        s = self.media.get_meta(12)
        if s:
            webbrowser.open(SEARCH_ENGINE + urllib.parse.quote(s), new=2)

    def button_volinc(self):
        v0 = player.audio_get_volume()
        v = v0 + 10
        if v > 100:
            v = 100
        for i in range(v0, v + 1):
            sleep(0.01)
            player.audio_set_volume(i)

    def button_voldec(self):
        v0 = player.audio_get_volume()
        v = v0 - 10
        if v < 0:
            v = 0
        for i in range(v0, v - 1, -1):
            sleep(0.01)
            player.audio_set_volume(i)

    def button_homepage(self):
        s = radios[self.rid]["homepage"]
        if s:
            webbrowser.open(s, new=2)
        print(player.audio_get_volume())

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.app_quit()
            root.destroy()

    def task():
        app.button_info()
        root.after(1000, task)  # reschedule event in 2 seconds

    def app_quit(self):
        self.fade_down()
        player.stop()


if __name__ == "__main__":
    app = GuiApp()
    app.run()
