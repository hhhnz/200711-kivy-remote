#!/usr/bin/python2.7 python2.7
# -*- coding: utf-8 -*-

# kivy modules first, if not Kivy may cause problems
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('1.10.0')


# common modules
import sys
import signal
from multiprocessing import Process


# Flask & similar modules
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import eventlet
from eventlet import wsgi


# async server setup
app = Flask(__name__)
api = Api(app)


def start_Flask():
    print("Starting server...")
    # start an eventlet WSGI server on port 5000
    wsgi.server(eventlet.listen(('', 5000)), app)


def signal_handler(signal, frame):
    # for fetching CTRL+C and relatives
    print (" CTRL + C detected, exiting ... ")
    exit(1)


# Kivy screen class
class MainScreen(Screen):
    def __init__(self, **kwargs):
        self.name="MAIN SCREEN"
        super(Screen, self).__init__(**kwargs)


# Kivy app class
class Kivy(App):
    w_MessageBox10_1 = "MAIN SCREEN"
    w_MessageBox10_2 = "One golden glance of what should be"
    w_MessageBox30_2 = "CHORUS"
    w_MessageBox30_3 = "EXIT"


    # exit button action
    def exit(self):
        print ("exiting... one shaft of light will show the way...")
        p1.terminate()  # terminate Flask by pressing on cancel
        exit(1)


    # do magic button action
    def do_magic(self):
        # your code goes here or maybe not
        print ("***** it's a kind of magic *************************")


    # Kivy UI builder file
    def build(self):
        sm = Builder.load_string("""

ScreenManager
    MainScreen:
        size_hint: 1, .7
        auto_dismiss: False
        title: app.w_MessageBox10_1       
        title_align: "center"

        BoxLayout:
            orientation: "vertical"
            Label:
                text: app.w_MessageBox10_2
            BoxLayout:
                orientation: "horizontal"
                spacing: 10
                size_hint: 1, .5
                Button:
                    text: app.w_MessageBox30_2  # DO MAGIC
                    on_press:
                        app.do_magic()
                Button:
                    text: app.w_MessageBox30_3  # EXIT
                    on_press:
                        app.exit()


        """)

        return sm


if __name__ == '__main__':

    # #CTRL+C signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    global p1
    p1 = Process(target=start_Flask)    # assign Flask to a process
    p1.start()                          # run Flask as process
    Kivy().run()                        # run Kivy UI