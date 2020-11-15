import tkinter as tk
from tkinter import ttk


class View:
    def __init__(self, parent):  # initialize class/object
        self.container = parent  # parent is the gui entry point given
        self.setup()

    def setup(self):
        self.frame=tk.Frame(self.container)
        self.b1Start = tk.Button(self.frame, text="Start Server", command = self.startServer, width = 20, height =1)
        self.frame.pack(fill=tk.BOTH)
        self.b1Start.pack(side=tk.TOP)

    def startServer(self):
        print ("starting Flask as process...")
        #global p1
        #p1 = Process(target=self.startFlask)# assign Flask to a process
        #p1.daemon = True
        #p1.start()  # launch Flask as separate process
        #self.startFlask()
    def startFlask(self):
        print ("inside start flask method...")
        #app.run(host='0.0.0.0', port=7080, debug=True)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7080, debug=True)
    mainwin = tk.Tk()  # tk instance created in operating system
    WIDTH = 800
    HEIGHT = 600
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    mainwin.title("Remote Desk Server")
    view = View(mainwin)  # give reference of mainwin to view object
    mainwin.mainloop()