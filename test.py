from test_function import *
from common.util import move as u_move ,copy as u_copy,rename as u_rename,delete_file,add_file,add_folder

class mysyncfolder(base_test):
    def __init__(self):
        self.type=0
        self.driver = None
        self.wait = WebDriverWait(self.driver, 15)

    def move(self,wait,driver):
        print('move...')
        u_move()
        return True
    def copy(self,wait,driver):
        print('copy...')
        u_copy()
        return True
    def rename(self,wait,driver):
        print('rename...')
        u_rename()
        return True
    def get_fun_name(self):
        temp = list()
        for i in list(dir(mysyncfolder)):# 取得class name再取所有function name
            if '__' not in i and 'get_fun_name' not in i and 'main' not in i:
                temp.append(i)
        print('msf:',temp)
        return temp

    def main(self, view, browser_type):
        view.resultlst.append('[選單功能測試進行]')
        view.mylist.insert(tk.END, '[選單功能測試進行]')
        for i in self.get_fun_name():
            try:
                if self.type == 0:
                    # 創建檔案
                    delete_file()
                    add_file()
                else:
                    # 創建資料夾
                    delete_file()
                    add_folder()

                self.driver = browser(browser_type)  # 取得driver
                state = login_nav(self.driver, login_config.get('navigate', 'account'),login_config.get('navigate', 'password'))
                time.sleep(1)
                # 15為全選、16為第一個checkbox檔案
                self.driver.find_elements_by_class_name("label-checkbox")[16].click()
                # 執行此operation測試對應方法按鈕
                if state == True:
                    self.wait = WebDriverWait(self.driver, 15)
                    self.wait.until(EC.visibility_of_element_located(
                        (By.XPATH, main_test_config.get('operation_xpath', 'menu_button'))))
                    self.driver.find_element_by_xpath(main_test_config.get('operation_xpath', 'menu_button')).click()
                    time.sleep(1)
                    check = False
                    text = "測試-" + i + ":"
                    message_title(text, view)
                    eval("menu(self.wait, self.driver)."+i+"_click()")
                    check = eval("self." + i)(self.wait, self.driver)
                    if check == True:
                        message_template(text, check, view)
                    else:
                        message_template(text, check, view)

                    time.sleep(1)
                    self.driver.close()

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
                view.resultlst.append(errMsg)
                view.mylist.insert(tk.END, errMsg)
                return False



