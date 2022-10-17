import tkinter
import threading
import time

class PushPopGUI(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.entry = tkinter.Entry(master=self)
        self.entry.pack(fill='x')
        self.button_push = tkinter.Button(master=self, text='push')
        self.button_push.pack(anchor=tkinter.W)
        self.button_pop = tkinter.Button(master=self, text='pop')
        self.button_pop.pack(anchor=tkinter.W)
        
        self.entry.bind("<Return>", self.event_push)
        self.button_push.bind("<Button-1>", self.event_push)
        self.button_pop.bind("<Button-1>", self.event_pop)

        self.t1_flag = False
        self.t1_end_flag = False
        self.t1_endless_flag = True
        self.move_ex_list = True
    
        self.green = '#80FF80'
        self.red = '#FF8080'
        self.off = '#F0F0ED'

    def event_push(self, event):
        push = self.entry.get()
        self.entry.delete(0, tkinter.END)
        if not push == '':
            with open("push.txt", 'a', encoding='utf-8') as f:
                f.write(push+'\n')

    def event_pop(self, event):
        if self.t1_end_flag:
            print("already t1 end flag")
            return
        if self.t1_flag:
            print("t1 end flag assert")
            self.button_pop['bg'] = self.red
            self.t1_end_flag = True
            return
        print("t1 start")
        self.button_pop['bg'] = self.green
        self.t1_flag = True
        t1  = threading.Thread(target=lambda:self.th())
        t1.start()

    def th_end(self):
        self.t1_flag = False
        self.t1_end_flag = False
        self.button_pop['bg'] = self.off

    def th(self):
        if self.t1_end_flag:
            print("t1_end_flag is True")
            self.th_end()
            return

        # popするための情報を入手
        push_lines = self.get_text_list("push.txt")
        
        if push_lines == []:
            print("push.txt is empty file")
            self.th_end()
            return

        print(push_lines)
        # popしたリストを入手
        pop_lines= self.get_text_list("pop.txt")

        # 重複はpopせず無視する
        l = push_lines.pop(0)
        if l in pop_lines:
            print( l, " is already exist in pop.txt")
        else:
            try:
                self.mycommand(l)
                # 成功したら最後に書き込む
                with open("pop.txt", 'a', encoding='utf-8') as f:
                    f.write(l+'\n')
            except Exception as e:
                print(e)
                if not self.move_ex_list:
                    # 移動しないと無限ループになるので終わる
                    self.th_end()
                    return
                else:
                    with open("push_error.txt", 'a', encoding='utf-8') as f:
                            f.write(l+'\n')

        # ひとつpopしたので戻す
        # command実行中にpushされてると逃すので、改めてリードする
        push_lines = self.get_text_list("push.txt")
        push_lines.pop(0)
        with open("push.txt", 'w', encoding='utf-8') as f:
            for l in push_lines:
                f.write(l+'\n')
        
        if self.t1_endless_flag:
            self.th()
        else:
            self.th_end()

    def get_text_list(self, file_name):
        _list = []
        with open(file_name, 'r', encoding='utf-8') as f:
            for l in f.read().split():
                _list.append(l)
        return _list
    
    def mycommand(self, l):
        print("pop : ", l)
        if int(l)%2==0:
            raise ValueError("Error")
        time.sleep(1)
    

if __name__ == '__main__':
    root = tkinter.Tk()
    app = PushPopGUI(root)
    app.pack()
    root.mainloop()
                