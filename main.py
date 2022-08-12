import vlc
# import time
from time import sleep
import random
from pyradios import RadioBrowser
import tkinter as tk
import tkinter.font as tk_font
import webbrowser
import urllib.parse

SEARCH_ENGINE1 = "https://kagi.com/search?q="
SEARCH_ENGINE2 = "https://duckduckgo.com/?q="
SEARCH_ENGINE3 = "https://www.qwant.com/?q="
SEARCH_ENGINE4 = "https://www.bing.com/search?q="
SEARCH_ENGINE5 = "https://www.google.com/search?q="
SEARCH_ENGINE = SEARCH_ENGINE4

rb = RadioBrowser()
radios = rb.stations()
# radios = rb.search(countrycode="PL")
print(len(radios), "radios downloaded.")

instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
player.audio_set_volume(100)

class App:
    def __init__(self, root):
        # setting title
        root.title("KakaduFM")
        # setting window size
        width = 370
        height = 130
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tk_font.Font(family='Times', size=14)

        self.tk_button_1 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "Play",
                                command = self.tk_button_1_command)
        self.tk_button_1.place(x=10, y=10, width=80, height=50)

        self.tk_button_2 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "Stop",
                                command = self.tk_button_2_command)
        self.tk_button_2.place(x=100, y=10, width=80, height=50)

        self.tk_button_3 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "Info",
                                command = self.tk_button_3_command)
        self.tk_button_3.place(x=190, y=10, width=80, height=50)

        self.tk_button_4 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "Search",
                                command = self.tk_button_4_command)
        self.tk_button_4.place(x=280, y=10, width=80, height=50)

        self.tk_button_1x2 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                       font = ft, justify = "center", text = "Mute",
                                       command = self.tk_button_5_command)
        self.tk_button_1x2.place(x=10, y=70, width=80, height=50)

        self.tk_button_2x2 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "V+",
                                command = self.tk_button_6_command)
        self.tk_button_2x2.place(x=100, y=70, width=80, height=50)

        self.tk_button_3x2 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "V-",
                                command = self.tk_button_7_command)
        self.tk_button_3x2.place(x=190, y=70, width=80, height=50)

        self.tk_button_4x2 = tk.Button(root, bg = "#61b458", fg = "#000000",
                                font = ft, justify = "center", text = "?",
                                command = self.tk_button_8_command)
        self.tk_button_4x2.place(x=280, y=70, width=80, height=50)

        self.rid = 0
        self.url = radios[self.rid]["url"]
        self.media = instance.media_new(self.url)
        self.tmp_title = ''
        self.tmp_vol = 0

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

    def tk_button_1_command(self):
        self.rid = random.randrange(0, len(radios))

# FIX .m3u and .pls not playing on vlc.py
        while self.url[-4:] == '.m3u' or self.url[-4:] == '.pls':
            self.url = self.url[:-4]
            self.rid = random.randrange(0, len(radios))

        self.url = radios[self.rid]["url"]
        meta_list = ['name', 'stationuuid', 'url', 'homepage', 'favicon', 'country', 'countrycode',
                     'language', 'tags', 'bitrate', 'codec', 'votes', 'clickcount']

        print("")
        print(self.rid)
        for i in meta_list:
            if radios[self.rid][i]: print(i + ":", radios[self.rid][i])
        r = rb.click_counter(radios[self.rid]["stationuuid"])
        if r["ok"]:
            print("+1 CLICK")

        self.fade_down()
        self.media = instance.media_new(self.url)
        player.set_media(self.media)
        player.audio_set_volume(0)
        self.tmp_vol = 100
        player.play()
        self.fade_up()

    def tk_button_2_command(self):
        self.fade_down()
        player.stop()

    def tk_button_3_command(self):
        s = self.media.get_meta(12)
        if s and self.tmp_title != s:
            print(s)
            self.tmp_title = s

    def tk_button_4_command(self):
        s = self.media.get_meta(12)
        if s:
            webbrowser.open(SEARCH_ENGINE + urllib.parse.quote(s), new=2)

    def tk_button_5_command(self):
        if player.is_playing():
            player.audio_toggle_mute()
            if player.audio_get_mute() == 0:
                self.tk_button_1x2['text']="UnMute"
            else:
                self.tk_button_1x2['text'] = "Mute"

    def tk_button_6_command(self):
        v0 = player.audio_get_volume()
        v = v0 + 10
        if v > 100:
            v = 100
        for i in range(v0, v + 1):
            sleep(0.01)
            player.audio_set_volume(i)

    def tk_button_7_command(self):
        v0 = player.audio_get_volume()
        v = v0 - 10
        if v < 0:
            v = 0
        for i in range(v0, v - 1, -1):
            sleep(0.01)
            player.audio_set_volume(i)

    def tk_button_8_command(self):
        s = radios[self.rid]["homepage"]
        if s:
            webbrowser.open(s, new=2)
        print(player.audio_get_volume())


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
