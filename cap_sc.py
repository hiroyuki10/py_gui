import tkinter
import threading
import time
import numpy as np
from PIL import Image
from PIL import ImageGrab

class Core:
    def __init__(self):
        self.i = 0
        self.old_img = None
    
    def sc(self):
        try:
            img = ImageGrab.grabclipboard()
        except OSError:
            print("OSError")
            return
        if isinstance(img, Image.Image):
            self.save(img)

    def save(self, img):
        np_img = np.array(img)
        if np.array_equal(np_img, self.old_img):
            return
        self.old_img = np_img
        save_name = str(self.i) + ".png"
        print("save : ", save_name)
        img.save(save_name)
        self.i += 1

class CapScreen(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.button = tkinter.Button(master=self, text='start')
        self.button.pack(anchor=tkinter.W)
        self.button.bind("<Button-1>", self.event_call)

        self.core = Core()
        self.t1_flag = False
        self.t1_end_flag = False
        self.t1_endless_flag = True
    
        self.green = '#80FF80'
        self.red = '#FF8080'
        self.off = '#F0F0ED'

    def event_call(self, event):
        if self.t1_end_flag:
            print("already t1 end flag")
            return
        if self.t1_flag:
            print("t1 end flag assert")
            self.button['bg'] = self.red
            self.t1_end_flag = True
            return
        print("t1 start")
        self.button['bg'] = self.green
        self.t1_flag = True
        t1  = threading.Thread(target=lambda:self.th())
        t1.start()

    def th_end(self):
        self.t1_flag = False
        self.t1_end_flag = False
        self.button['bg'] = self.off

    def th(self):
        if self.t1_end_flag:
            print("t1_end_flag is True")
            self.th_end()
            return
        self.core.sc()
        print("sleep ... ")
        time.sleep(0.5)
        self.th()


if __name__ == '__main__':
    root = tkinter.Tk()
    app = CapScreen(root)
    app.pack()
    root.mainloop()
                