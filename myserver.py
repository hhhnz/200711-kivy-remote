#!/usr/bin/env python
#import for system and time function
import sys
import time
from datetime import timedelta
#this is for encode
import ctypes
import secrets

#import flask pkg
from flask import Flask, request, send_file, render_template, url_for,flash, redirect,session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_login import LoginManager, UserMixin, login_user,login_required,current_user,logout_user
from flask_bcrypt import Bcrypt
#import for grab image
from PIL import ImageGrab
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from io import BytesIO

#import gui kivy package
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
#from kivy.uix.popup import Popup
#import tkinter as tk
import threading

import random
import string
from requests import get
#import for url handling on client side
import pycurl
from io import BytesIO
#dataase handling
import sqlite3

# from multiprocessing import Process
# http://msdn.microsoft.com/en-us/library/windows/desktop/ms646260%28v=vs.85%29.aspx
MOUSEEVENTF_LEFTDOWN = 2
MOUSEEVENTF_LEFTUP = 4
###FLASK#######################################
app = Flask(__name__)
app.config['SECRET_KEY']='35a60fe01bbe505d2597abda0cfbab26' #key for cookie
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #local library for


randomURL=secrets.token_urlsafe(16) #this is to generate random nubers for shut down routing
db = SQLAlchemy(app) #db is the database
bcrypt = Bcrypt(app) #encrupyt fucntion for slask
#from models import User
# class User(db.Model):
#     id = 1
#**************login manager***************
#step 2. add login manager to routes
login_manager = LoginManager(app)
login_manager.login_view = 'desktop'
login_manager.login_view = 'click'
login_manager.login_view = 'indexscript'

def shutdown_server(): #this is for shution down the server discuss later
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
@app.before_request #session management discusss later
def make_session_permanent():
    session.permanent = True
    #app.permanent_session_lifetime = timedelta(seconds=10)
    app.permanent_session_lifetime = timedelta(minutes=1)
    return
@app.route('/',methods=['GET','POST']) # log in page
def index():
    if current_user.is_authenticated:
        return redirect(url_for('desktop')) #if user logged in direct to desktop
    #return 'Hello, Flask' #app.send_static_file('index.html')
    form=LoginForm()
    if form.validate_on_submit():
        user = load_user(1)#just one suer
        #login_user(user,remember=form.remember.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):#compare password with in database
            login_user (user, remember=form.remember.data)#log in the user, flask will take care session control
            return redirect(url_for('indexscript'))#after login, direct to show desktop
        else:#if with wrong password
            flash('Login Unsuccessful. Please check password','danger')
            #login.html is template
    return render_template ('login.html', title = 'Login', form = form)#show login page

# @app.route('/register', methods=['GET','POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f"Account created for {form.username.data}!",'success')
#         return redirect (url_for('about'))
#     return render_template('register.html', title='Register', form=form)
# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Login', form=form)
# @app.route('/about')
# def about():
#     return render_template('about.html', title='about')
@app.route('/indexscript')#sending click to server
@login_required #step 3 add login_required to each route
def indexscript():
    return app.send_static_file('index.html')
    #return "indexscript"
@app.route('/desktop.jpeg')
@login_required
def desktop():
    #return 'desktop jpg'
    screen = ImageGrab.grab()
    buf = BytesIO()
    screen.save(buf, 'JPEG', quality=50)
    buf.seek(0)
    return send_file(buf, mimetype='image/jpeg')
    # if current_user:
    #     return current_user.username
    # else:
    #     return "no current user"

@app.route('/click')
@login_required
def click():
    try:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
    except:
        return 'error'
    user32 = ctypes.windll.user32
    user32.SetCursorPos(x, y)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    return 'done'
@app.route(('/shutdown'+randomURL), methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
#########MODEL DATA BASE#############################
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@login_manager.unauthorized_handler #message when unauthorized action
def unauthorized_handler():
    flash("Please Log in first!")
    return redirect(url_for('index'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False) #do not need email only 1 user
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self): #return a presentation
        return f"User('{self.username}', '{self.password}')"
####GUI Kivy################################################################################
class MyGrid(Widget):
    # initialize property to link back to kv file
    #txtServerIP = ObjectProperty(None)
    #butServerCheckIp = ObjectProperty(None)
    txtStatus = ObjectProperty(None)
    txtPw=ObjectProperty(None)
    txtPort=ObjectProperty(None)
    txtLicense=ObjectProperty(None)
    butStopServer=ObjectProperty(None)
    flagFlaskStarted = False
    #flagIPget=False
    flagPWget=False
    flagButStopServerEnabled = False

    # def getIP(self):
    #     self.txtStatus.text='check computer ip address...'
    #
    #     try:
    #         ip = get('https://api.ipify.org').text
    #     except:
    #         self.txtStatus.text = 'computer ip address retrieve failed'
    #     else:
    #         self.txtServerIP.text=ip
    #         self.flagIPget = True
    #     self.txtStatus.text = 'computer ip address received'
    def genPW(self):
        global gPassword
        self.txtPw.text = self.get_random_alphanumeric_string(4,4)
        gPassword = self.txtPw.text
        self.flagPWget=True
        hashed_password = bcrypt.generate_password_hash(gPassword).decode('utf-8')
        try:
            sqliteConnection = sqlite3.connect('site.db')
            c = sqliteConnection.cursor()
            c.execute("Update User set password = (:pw) where id = 1",{'pw':hashed_password})
            #sql_update_query='''Update User set password = '''+str(gPassword)+''' where id =1'''
            #username freeRemoteUser571894635218
            sqliteConnection.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        self.txtStatus.text = 'password generated'


    def get_random_alphanumeric_string(self, letters_count, digits_count):
        sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
        sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

        # Convert string to list and shuffle it to mix letters and digits
        sample_list = list(sample_str)
        random.shuffle(sample_list)
        final_string = ''.join(sample_list)
        return final_string
    def runFlask(self,):
        app.run(host='0.0.0.0', port=int(self.txtPort.text), debug=False,ssl_context='adhoc')
    def startServer(self):
        if self.flagPWget: #check if passward has been generated
            self.t=threading.Thread(target=self.runFlask) #run flask under kivy as a thread
            self.t.start()
            time.sleep(2)
            self.butStartServer.disabled=True #disable start server button
            self.butStopServer.disabled=False #enable stop server button
            self.txtStatus.text = 'Server started' #show in status bar
            self.flagButStopServerEnabled = True
        else:
            self.txtStatus.text = "Please get public IP and generate Password before start Server." #if no password


    def stopServer(self):
        buffer = BytesIO()
        c = pycurl.Curl() #use pycurl to send message to server
        c.setopt(c.URL, 'https://127.0.0.1:'+self.txtPort.text+'/shutdown'+randomURL) #use shutdown url to shut down server on server machine
        c.setopt(c.WRITEDATA, buffer)
        #for self certificate
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.perform()
        c.close()
        body = buffer.getvalue()
        self.txtStatus.text=body.decode('iso-8859-1')#show message in status
        time.sleep(2)
        self.t.join()
        self.butStartServer.disabled=False #enable start server
        self.butStopServer.disabled=True #disable stop server button
        self.flagButStopServerEnabled=False

class ServerApp(App):#kivy app
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        self.my = MyGrid()
        return self.my

    def on_request_close(self, *args):
        if self.my.flagButStopServerEnabled == True:
            self.my.stopServer()
        exit()
        return True


if __name__ == '__main__':
    arg = sys.argv[1:]
    if arg.__len__()!=0:
        if arg[0] == "test":
            app.run(host='0.0.0.0', port=7080, debug=True, ssl_context='adhoc') #debug mode
    else:#running with GUI
        kivyApp = ServerApp()
        kivyApp.run()






