# 各介面方法寫在此
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter.ttk import Progressbar
import time
import threading
import configparser
import os
from tkinter import Checkbutton
from common.util import *

class UI:
    def __init__(self, run, resultlst, cb_name_nav, cb_value_nav,browser_name_nav,browser_value_nav):
        self.resultlst = resultlst
        self.window = tk.Tk()
        self.time_label = "" # 時間
        self.begintime_label = "" # 初始時間
        self.run = run # 執行測試方法
        self.scrollbar = "" # 滑軌
        self.mylist = "" # 訊息
        self.progressbar = "" # 進度
        self.config=config
        self.login_config=login_config
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.check = False
        self.timecount = True
        self.url_text = ""
        self.n = 0 # 進度條初始
        self.bar_interval = 3
        self.run_button=""
        self.cb_name_nav=cb_name_nav
        self.cb_value_nav=cb_value_nav
        self.browser_name_nav=browser_name_nav
        self.browser_value_nav=browser_value_nav
        self.check=[]
        self.check_nav=[]

    def create(self):
        print('視窗建立...')
        self.window.title(self.config.get('test','title_name'))
        self.window.geometry(self.config.get('test','size_width')+'x'+self.config.get('test','size_length'))
        self.window.resizable(width=False,height=False)
        self.window.configure(background='white')
        self.option() # 選單欄
        self.component() # 元件
        print('視窗建立完成...')

    def component(self):
        title_frame = tk.Frame(self.window,bg = 'white')
        title_frame.pack(side = tk.TOP)
        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        title_label=tk.Label(title_frame, text=self.config.get('test','name'), font=fontStyle, bg='white')
        title_label.pack()
        url_frame = tk.Frame(self.window,bg = 'white')
        url_frame.pack(side=tk.TOP)
        url_label= tk.Label(url_frame, text="測試網址:"+str(self.login_config.get('navigate', 'url')).split('.com')[0]+'.com',bg='white')
        url_label.pack(side = tk.LEFT)
        temp = []
        for i in range(len(self.browser_name_nav)):
            if i % 5 == 0:
                temp.append(tk.Frame(self.window, bg='white'))
                temp[len(temp) - 1].pack(side=tk.TOP)
                if i == 0:
                    browserLabel = tk.Label(temp[len(temp) - 1], text='BROWSER', bg='white')
                    browserLabel.pack(side=tk.LEFT)
            self.browser_value_nav[i] = tk.IntVar()
            self.check_nav.append(
                Checkbutton(temp[len(temp) - 1], text=self.browser_name_nav[i], variable=self.browser_value_nav[i]).pack(side=tk.LEFT))

        temp=[]
        for i in range(len(self.cb_name_nav)):
            if i%5==0:
                temp.append(tk.Frame(self.window, bg='white'))
                temp[len(temp)-1].pack(side=tk.TOP)
                if i==0:
                    navLabel = tk.Label(temp[len(temp)-1], text='NAVIGATE', bg='white')
                    navLabel.pack(side=tk.LEFT)
            self.cb_value_nav[i] = tk.IntVar()
            self.check_nav.append(
                Checkbutton(temp[len(temp)-1], text=self.cb_name_nav[i], variable=self.cb_value_nav[i]).pack(side=tk.LEFT))

        begin_frame = tk.Frame(self.window, bg='white')
        begin_frame.pack(side=tk.TOP)
        self.begintime_label= tk.Label(begin_frame, text='', font=fontStyle, bg='white')
        self.begintime_label.pack()
        time_frame = tk.Frame(self.window, bg='white')
        time_frame.pack(side=tk.TOP)
        self.time_label = tk.Label(time_frame, text="按下按鈕開始測驗", fg="red", bg="white", font=('Arial', 17))
        self.time_label.pack()
        button_frame = tk.Frame(self.window, bg='white')
        button_frame.pack(side=tk.TOP)
        self.run_button=tk.Button(button_frame,text='開始測試',command=lambda :self.thread_it(self.run))
        self.run_button.pack()
        progress_frame = tk.Frame(self.window, bg='white')
        progress_frame.pack(side=tk.TOP)
        self.progress = Progressbar(progress_frame, orient=tk.HORIZONTAL, length=self.config.get('test','size_width'), mode='determinate')
        self.progress.pack()
        scrollbar_frame = tk.Frame(self.window, bg='white')
        scrollbar_frame.pack(side=tk.TOP)
        self.scrollbar = tk.Scrollbar(scrollbar_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mylist = tk.Listbox(scrollbar_frame, width=str(int(int(self.config.get('test','size_width'))*0.2)), height=str(int(int(self.config.get('test','size_length'))*0.03)), yscrollcommand=self.scrollbar.set)
        self.mylist.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.mylist.yview)

    def option(self):
        # 選單欄設定
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.window.config(menu=menubar)

    def save_file(self):
        # 存取方法
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        for result in self.resultlst:
            f.write(str(result) + '\n')
        f.close()

    def begin_time(self):
        localtime = time.asctime(time.localtime(time.time()))
        self.resultlst.append('開始測試時間:' + str(localtime))
        timee = '開始測試時間:' + str(localtime)
        self.begintime_label.configure(text=timee)

    def update_clock(self):
        self.sec+=1
        if(self.sec==60):
            self.sec=0
            self.min+=1
        if(self.min==60):
            self.hour=0
            self.hour+=1
        if(self.check == True):
            now = '[測試開始]\n測試時間:' +str("%02d" % self.hour) + ":" + str("%02d" % self.min) + ":" + str("%02d" % self.sec)
            #print("update clock:"+str("%02d" % self.hour) + ":" + str("%02d" % self.min) + ":" + str("%02d" % self.sec))
            self.time_label.configure(text=now)
            self.window.after(1000, self.update_clock)

        elif(self.check == False and self.timecount == False):
            self.resultlst.append('總共測試時間:' + str("%02d" % self.hour)+":"+str("%02d" % self.min)+":"+str("%02d" % self.sec))
            self.time_label.configure(text='[測試結束]\n總共測試時間:' + str("%02d" % self.hour)+":"+str("%02d" % self.min)+":"+str("%02d" % self.sec))
            self.run_button.configure(text = "結束測驗", command=self.quit)

    def quit(self):
        quit = tkinter.messagebox.askokcancel("提示","確定離開視窗?")
        if quit == True:
            self.window.quit()

    def thread_it(self,func, *args):
        # 避免tkinter沒回應，故開多執行緒
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def bar(self,n):
        self.progress['value'] = n
        self.window.update_idletasks()

    def main(self):
        self.create()
        self.window.mainloop()
        return self.cb_value_nav,self.browser_value_nav