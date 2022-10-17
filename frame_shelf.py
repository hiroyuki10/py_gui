import tkinter
import os
import configparser
import shutil
from tkinter import messagebox
from PIL import Image
from frame_thumbnail import FrameThumbnail

class ShelfListScroll(FrameThumbnail):
    def update_lists(self, _lists):
        images = []
        for name in _lists:
            images.append(self.get_images(name))
        print(images)
        self.update(images, _lists)

    def _bind_button(self, button, _name):
        button.bind("<Button-1>", lambda event, num=len(self.buttons), name=_name: self._callback(event, num, name))
        button.bind("<Button-3>", lambda event, num=len(self.buttons), name=_name: self._callback_2(event, num, name))
        button.bind("<MouseWheel>",  self._on_mousewheel)
        return button

    def _callback_2(self, event, num, name):
        print(event)
        print(num)
        print(name)
        if messagebox.askyesno('警告', name + '\nを削除していいですか？', icon='warning'):
            print("yes")
            shutil.rmtree(name)
        else:
            print("no")

    def get_images(self, _name):
        files = os.listdir(_name)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".jpg":
                _path = os.path.join(_name,file)
                print(_path)
                img = Image.open(_path)
                return img
            if ext == ".png":
                _path = os.path.join(_name,file)
                print(_path)
                img = Image.open(_path)
                return img
        return None

class FrameShelf(tkinter.LabelFrame):
    def __init__(self, master, _callback=None):
        super().__init__(master)
        self.config(text="shelf")
        self.callback = _callback
        self.select_path ='.'

        self.frame_shelf_controller = self.create_controller(self)
        self.frame_shelf_controller.pack(anchor=tkinter.W, fill='x')
        self.frame_list = ShelfListScroll(self)
        self.frame_list.button_size = [300, 300]
        self.frame_list._callback = self.click
        self.frame_list.pack(anchor=tkinter.W)

        self.event_path_update(0)

    def create_controller(self, _master):
        frame = tkinter.LabelFrame(master=_master, text="")
        self.button_path_update = tkinter.Button(master=frame, text="update")
        self.button_path_update.bind("<Button-1>", self.event_path_update)
        self.button_path_update.pack(anchor=tkinter.W)
        self.flag_only_image = tkinter.BooleanVar()
        self.flag_only_image.set(True)
        self.chkbtn_only_image = tkinter.Checkbutton(master=frame, text="only image", variable=self.flag_only_image)
        self.chkbtn_only_image.config(command=lambda : self.event_path_update(0))
        self.chkbtn_only_image.pack(anchor=tkinter.W)
        self.flag_show_thumbnail = tkinter.BooleanVar()
        self.chkbtn_show_thumbnail = tkinter.Checkbutton(master=frame, text="show thumbnail", variable=self.flag_show_thumbnail)
        self.chkbtn_show_thumbnail.config(command=lambda : self.event_path_update(0))
        self.chkbtn_show_thumbnail.pack(anchor=tkinter.W)
        self.entry_path = tkinter.Entry(master=frame)
        self.entry_path.insert(0, self.select_path)
        self.entry_path.bind('<Return>', self.event_path_update)
        self.entry_path.pack(anchor=tkinter.W, fill='x')
        return frame

    def set_size(self, w, h):
        self.frame_shelf_controller.update_idletasks()
        f_cnt_h = self.frame_shelf_controller.winfo_height()
        self.frame_list.set_size(w,h-f_cnt_h)

    def click(self, event, num, name):
        if self.callback:
            print("click")
            print(event)
            print(num)
            print(name)
            self.callback(name)
        else:
            print("callback None...")
            print(event, num, name)

    def get_images(self, name_list, img_dir):
        images = []
        for image_name in name_list:
            images.append(Image.open(img_dir + "/" + image_name))
        return images

    def get_image_files(self, path):
        _list = []
        files = os.listdir(path)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".jpg":
                _list.append(file)
                continue
            if ext == ".png":
                _list.append(file)
                continue
        return _list

    def get_dir_list(self, path):
        tmp_list = []
        all_file = os.listdir(path)
        for file in all_file:
            if os.path.isdir(os.path.join(path,file)):
                tmp_list.append(os.path.join(path,file))
        return tmp_list

    def event_path_update(self, event):
        self.select_path = self.entry_path.get()
        dir_list = self.get_dir_list(self.select_path)
        if self.flag_only_image.get():
            dir_list = self.extract_dir_has_image(dir_list)
        self.frame_list.update_lists(dir_list)

    def extract_dir_has_image(self, _lists):
        image_lists = []
        for path in _lists:
            files = os.listdir(path)
            for file in files:
                name, ext = os.path.splitext(file)
                if ext == ".jpg":
                    image_lists.append(path)
                    break
                if ext == ".png":
                    image_lists.append(path)
                    break
        return image_lists


    def read_conf(self):
        ini_file_name = "setting.ini"
        conf = configparser.ConfigParser()
        conf.read(ini_file_name)
        if conf.has_option("image_list", "dir"):
            self.select_path = conf.get("image_list", "dir")

if __name__ == '__main__' :
    root = tkinter.Tk()
    frame_image_list = FrameShelf(master=root, _callback=None)
    frame_image_list.pack()
    root.mainloop()
