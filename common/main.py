from common.util import *
from common.ui import UI
from common.get_browser_driver import get_driver
import time
import tkinter as tk
import sys
import traceback
from test_login_page import login
from test_account_settings import account
from test_function import *
from test_upload import upload
from test_mysyncfolder import mysyncfolder
from test_backup import backup
from test_markstar import markstar
from test_projectfolder import projectfolder
from test_recently import recently
from test_share import share
from test_trash import trash


class Main:
    def __init__(self):
        self.resultlst = list()
        # checkbox:瀏覽器
        self.browser_list_name = str(config.get('checkbox', 'browser')).split(',')
        self.browser_list_value = list()
        for i in range(len(self.browser_list_name)):
            self.browser_list_value.append(0)
        # checkbox:測試項目
        self.nav_list_name=str(config.get('checkbox','name')).split(',')
        self.nav_list_fun=[login,account,upload,mysyncfolder().main,backup().main,markstar,projectfolder,recently,share,trash]
        self.nav_list_value=list()
        for i in range(len(self.nav_list_fun)):
            self.nav_list_value.append(0)
        self.view = UI(self.main, self.resultlst, self.nav_list_name,self.nav_list_value,self.browser_list_name,self.browser_list_value)
        self.nav_list_value,self.browser_list_value= self.view.main()

    def main(self):
        try:
            self.view.time_label.configure(text='')
            self.view.check = True
            self.view.update_clock()

            if self.view.check != False and self.view.timecount != False:
                self.view.begin_time()
                # 判斷為cathay版本還是通用版本
                check_state(login_config.get('navigate', 'url'))
                # 前置作業-啟動
                browser_count = 0
                for i in range(len(self.browser_list_value)):
                    if self.browser_list_value[i].get() == 1:
                        get_driver(str(self.browser_list_name[i]))
                        browser_count+=1
                print('-----自動測試-----')
                print('創建測試群組...')
                #create_test_group()
                print('創建測試群組...完成')
                print('創建測試帳號...')
                #create_test_account('QTeam_FO')
                print('創建測試帳號...完成')
                # 前置作業-完成
                # 計算執行測項數量
                task_count=0
                task_temp=list()
                for i in range(len(self.nav_list_value)):
                    if self.nav_list_value[i].get()==1:
                        task_count+=1
                        task_temp.append(i)
                print('共有:',task_count,'測項')
                # 進度條單位
                bar_add = 100 / (task_count*browser_count)
                for i in range(len(self.browser_list_value)):
                    if self.browser_list_value[i].get() == 1:
                        browser_type=str(self.browser_list_name[i])
                        t=Test(str(self.browser_list_name[i]),task_temp,self.nav_list_name,self.nav_list_fun,self.view,bar_add)
                        t.main()
                # 測試項目-完成
                print('-----自動測試[完成]-----')
                # 結束
                self.view.timecount = False
                self.view.check = False
                print("測試結束")
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)

class Test:
    def __init__(self,type,task_temp,nav_list_name,nav_list_fun,view,bar_add):
        self.browser_type=type
        self.task_temp=task_temp
        self.nav_list_name=nav_list_name
        self.nav_list_fun=nav_list_fun
        self.view = view
        self.bar_add=bar_add

    def main(self):
        print('-' * 30)
        self.view.resultlst.append('-' * 30)
        self.view.mylist.insert(tk.END, '-' * 30)
        print(self.browser_type + '進行測試...')
        self.view.resultlst.append(self.browser_type + '進行測試...')
        self.view.mylist.insert(tk.END,self.browser_type + '進行測試...')
        for i in self.task_temp:
            # 測試項目-啟動
            try:
                print('@[測試項目]:', self.nav_list_name[i])
                # UI & Report Message
                self.view.resultlst.append('@[測試項目]:' + str(self.nav_list_name[i]))
                self.view.mylist.insert(tk.END, '@[測試項目]:' + str(self.nav_list_name[i]))
                # 測項
                print(self.browser_type)
                self.nav_list_fun[i](self.view,self.browser_type)
                time.sleep(10)
                self.view.n += self.bar_add
                self.view.bar(self.view.n)
            except Exception as e:
                error_class = e.__class__.__name__  # 取得錯誤類型
                detail = e.args[0]  # 取得詳細內容
                cl, exc, tb = sys.exc_info()  # 取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1]
                fileName = lastCallStack[0]  # 取得發生的檔案名稱
                lineNum = lastCallStack[1]  # 取得發生的行號
                funcName = lastCallStack[2]  # 取得發生的函數名稱
                errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                print(errMsg)

        print(self.browser_type + '進行測試...完成')
        self.view.resultlst.append(self.browser_type + '進行測試...完成')
        self.view.mylist.insert(tk.END,self.browser_type + '進行測試...完成')
        print('-' * 30)
        self.view.resultlst.append('-' * 30)
        self.view.mylist.insert(tk.END, '-' * 30)

if __name__ == '__main__':
    t=Main()
    t.main()