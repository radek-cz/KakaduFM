import vlc
import random
import time
import calendar
import re
from io import BytesIO
from datetime import datetime
from time import sleep
from pyradios import RadioBrowser
from PIL import Image, ImageTk
# from tkinter import *
#from tkinter import ttk
import tkinter as tk
# import tkinter.font as tk_font
# from tkinter import messagebox
import webbrowser
import urllib.parse
import pathlib
import pygubu
import requests

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"
VER_TK = tk.Tcl().eval('info patchlevel')
SEARCH_ENGINE1 = "https://kagi.com/search?q="
SEARCH_ENGINE2 = "https://duckduckgo.com/?q="
SEARCH_ENGINE3 = "https://www.qwant.com/?q="
SEARCH_ENGINE4 = "https://www.bing.com/search?q="
SEARCH_ENGINE5 = "https://www.google.com/search?q="
SEARCH_ENGINE = SEARCH_ENGINE4
MAXL_NAME = 24

rb = RadioBrowser()
# radios = rb.stations()
radios = rb.search(countrycode="PL")

# FIX some .m3u and .pls not playing on vlc.py
try:
    for i in range(len(radios)):
        url = radios[i]["url"]
        if url.find('.m3u') > -1 or url.find('.pls') > -1:
            radios.pop(i)
except:
    pass

# Deduplicate
url0 = radios[0]["url"]
try:
    for i in range(1, len(radios)):
        url = radios[i]["url"]
        if url == url0:
            radios.pop(i)
        url0 = radios[i]["url"]
except:
    pass

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

        self.dialog1 = builder.get_object("dialog1", self.mainwindow)
        self.dialog2 = builder.get_object("dialog2", self.mainwindow)
        # self.stations = builder.get_object("toplevel2", self.mainwindow)
        # self.history = builder.get_object("toplevel3", self.mainwindow)

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

    def update_info(self):
        meta_list = ['name', 'stationuuid', 'url', 'homepage', 'favicon', 'country', 'countrycode',
                     'language', 'tags', 'bitrate', 'codec', 'votes', 'clickcount']

        meta_data = {
            'name': 'label_name',
            'country': 'label_country',
            'countrycode': 'label_countrycode',
            'language': 'label_language',
            'tags': 'label_tags',
            'bitrate': 'label_bitrate',
            'codec': 'label_codec',
            'votes': 'label_votes',
            'clickcount': 'label_clickcount',
        }

        for i in meta_data:
            widget = self.builder.get_object(meta_data[i])
            txt = radios[self.rid][i]
            if str(type(txt)) == "<class 'str'>":
                txt = txt.strip()
                txt = re.sub(r"[\n\t]*", "", txt)
            if str(type(txt)) == "<class 'str'>" and len(txt) > MAXL_NAME and i == 'name':
                txt = txt[:MAXL_NAME] + '...'
            if str(type(txt)) == "<class 'str'>" and len(txt) > (2*MAXL_NAME) and i == 'tags':
                txt = txt[:(2*MAXL_NAME)] + '...'
            widget.configure(text=txt)

        widget = self.builder.get_object('label_rid')
        widget.configure(text=str(self.rid))

        widget = self.builder.get_object('button_homepage')
        if radios[self.rid]['homepage']:
            widget.configure(state="normal")
        else:
            widget.configure(state="disabled")

        widget = self.builder.get_object('button_nowplaying')
        if self.media.get_meta(12):
            widget.configure(state="normal")
        else:
            widget.configure(state="disabled")

        widget = self.builder.get_object('entry_dialogbox')
        widget.configure(state="normal")
        widget.delete (0, last=len(widget.get()))
        widget.insert(0,self.url)
        widget.configure(state="readonly")

        fi = radios[self.rid]["favicon"]
        widget = self.builder.get_object('label_icon')
        if fi and (fi.find('.jpg') > -1 or fi.find('.jpeg') > -1 or fi.find('.png') > -1 or fi.find('.ico') > -1):
            response = requests.get(fi)

            img = Image.open(BytesIO(response.content))
            size = 300, 300
            # img.thumbnail(size)
            img = img.resize(size)
            favicon = ImageTk.PhotoImage(img)

            widget.configure(image=favicon)
            widget.image=favicon
        else:
            img = Image.open("kakadu.png")
            favicon = ImageTk.PhotoImage(img)
            widget.configure(image=favicon)
            widget.image=favicon
            pass

        # print("")
        # for i in meta_list:
        #     if radios[self.rid][i]: print(i + ":", radios[self.rid][i])

    def shuffle(self):
        self.rid = random.randrange(0, len(radios))
        self.url = radios[self.rid]["url"]

        self.update_info()

        r = rb.click_counter(radios[self.rid]["stationuuid"])

        self.fade_down()
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        # self.tmp_vol = 100
        player.play()
        self.fade_up()

    def play(self):
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        player.play()
        self.fade_up()
        self.tmp_stop = 0
        widget = self.builder.get_object('button_stop')
        widget.configure(state="normal")
        self.update_info()

    def stop(self):
        self.fade_down()
        player.stop()
        self.tmp_stop = 1
        widget = self.builder.get_object('button_stop')
        widget.configure(state="disabled")

    def mute(self):
        if player.is_playing():
            player.audio_toggle_mute()
            if player.audio_get_mute() == 0:
                widget = self.builder.get_object('button_mute')
                widget.configure(text="UnMute")
            else:
                widget = self.builder.get_object('button_mute')
                widget.configure(text="Mute")

    def prev_station(self):
        if self.rid > 0:
            self.rid -= 1
        else:
            self.rid = len(radios) - 1
        self.url = radios[self.rid]["url"]

        self.update_info()

        r = rb.click_counter(radios[self.rid]["stationuuid"])

        self.fade_down()
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        # self.tmp_vol = 100
        player.play()
        self.fade_up()

    def next_station(self):
        if self.rid < len(radios) - 1:
            self.rid += 1
        else:
            self.rid = 0
        self.url = radios[self.rid]["url"]

        self.update_info()

        r = rb.click_counter(radios[self.rid]["stationuuid"])

        self.fade_down()
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        # self.tmp_vol = 100
        player.play()
        self.fade_up()

    def config(self):
        pass

    def stationurl(self):
        self.dialog1.run()

    def nowplaying(self):
        song = self.media.get_meta(12)
        if song:
            widget = self.builder.get_object('entry_song')
            widget.configure(state="normal")
            widget.delete (0, last=len(widget.get()))
            widget.insert(0,song)
            widget.configure(state="readonly")
            self.dialog2.run()

    def homepage(self):
        s = radios[self.rid]["homepage"]
        if s:
            webbrowser.open(s, new=2)

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

    def search_song(self):
        s = self.media.get_meta(12)
        if s:
            webbrowser.open(SEARCH_ENGINE + urllib.parse.quote(s), new=2)

    def vol_up(self):
        v0 = player.audio_get_volume()
        v = v0 + 10
        if v > 100:
            v = 100
        for i in range(v0, v + 1):
            sleep(0.01)
            player.audio_set_volume(i)

    def vol_down(self):
        v0 = player.audio_get_volume()
        v = v0 - 10
        if v < 0:
            v = 0
        for i in range(v0, v - 1, -1):
            sleep(0.01)
            player.audio_set_volume(i)

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

    def clear_filterlist(self):
        pass

    def add_filter(self):
        pass

if __name__ == "__main__":
    app = GuiApp()
    app.run()
