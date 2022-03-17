from test_function import *
from common.util import move as u_move ,copy as u_copy,rename as u_rename,delete_file,add_file,add_folder,browser,login_nav,login_config,cloud_to_trash

def move_to_cloud():
    driver = browser('chrome')
    state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
    time.sleep(1)
    # 15為全選、16為第一個checkbox檔案
    driver.find_elements_by_class_name("label-checkbox")[16].click()
    if state == True:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('operation_xpath', 'menu_button'))))
        driver.find_element_by_xpath(main_test_config.get('operation_xpath', 'menu_button')).click()
        time.sleep(1)
        wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'move'))))
        driver.find_element_by_xpath(main_test_config.get('menu', 'move')).click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[16]/div/div/bs-modal-body/div/div/div/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node[2]/div/tree-node-wrapper/div/tree-node-expander/span/span').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[16]/div/div/bs-modal-body/div/div/div/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node[2]/div/tree-node-children/div/tree-node-collection/div/tree-node/div/tree-node-wrapper/div/div/tree-node-content/span').click()
        driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[16]/div/div/bs-modal-footer/div/button[2]').click()
        driver.close()

class backup(base_test):
    def __init__(self):
        self.type=None
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
        for i in list(dir(backup)):# 取得class name再取所有function name
            if '__' not in i and 'get_fun_name' not in i and 'main' not in i:
                temp.append(i)
        print('msf:',temp)
        return temp

    def main(self, view, browser_type):
        # 選單-檔案測試
        print('檔案測試')
        view.resultlst.append('檔案測試')
        view.mylist.insert(tk.END, '檔案測試')
        self.type=0
        view.resultlst.append('[選單功能測試進行]')
        view.mylist.insert(tk.END, '[選單功能測試進行]')
        for i in self.get_fun_name():
            try:
                if self.type == 0:
                    # 創建檔案
                    delete_file()
                    cloud_to_trash()
                    add_file()
                    move_to_cloud()
                else:
                    # 創建資料夾
                    delete_file()
                    cloud_to_trash()
                    add_folder()
                    move_to_cloud()

                self.driver = browser(browser_type)  # 取得driver
                state = login_nav(self.driver, login_config.get('navigate', 'account'),login_config.get('navigate', 'password'))
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/a').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/div/a[1]').click()
                # 15為全選、16為第一個checkbox檔案
                time.sleep(3)
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

        # 選單-資料夾測試
        print('資料夾測試')
        view.resultlst.append('資料夾測試')
        view.mylist.insert(tk.END, '資料夾測試')
        self.type=1
        view.resultlst.append('[選單功能測試進行]')
        view.mylist.insert(tk.END, '[選單功能測試進行]')
        for i in self.get_fun_name():
            try:
                if self.type == 0:
                    # 創建檔案
                    delete_file()
                    cloud_to_trash()
                    add_file()
                    move_to_cloud()
                else:
                    # 創建資料夾
                    delete_file()
                    cloud_to_trash()
                    add_folder()
                    move_to_cloud()

                self.driver = browser(browser_type)  # 取得driver
                state = login_nav(self.driver, login_config.get('navigate', 'account'),
                                  login_config.get('navigate', 'password'))
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/a').click()
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    '//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/div/a[1]').click()
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
                    eval("menu(self.wait, self.driver)." + i + "_click()")
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

        # 右鍵-檔案測試
        print('檔案測試')
        view.resultlst.append('檔案測試')
        view.mylist.insert(tk.END, '檔案測試')
        self.type = 0
        view.resultlst.append('[右鍵功能測試進行]')
        view.mylist.insert(tk.END, '[右鍵功能測試進行]')
        for i in self.get_fun_name():
            try:
                if self.type == 0:
                    # 創建檔案
                    delete_file()
                    cloud_to_trash()
                    add_file()
                    move_to_cloud()
                else:
                    # 創建資料夾
                    delete_file()
                    cloud_to_trash()
                    add_folder()
                    move_to_cloud()

                self.driver = browser(browser_type)  # 取得driver
                state = login_nav(self.driver, login_config.get('navigate', 'account'),
                                  login_config.get('navigate', 'password'))
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/a').click()
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    '//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/div/a[1]').click()
                # 15為全選、16為第一個checkbox檔案
                self.driver.find_elements_by_class_name("label-checkbox")[16].click()
                # 執行此operation測試對應方法按鈕
                if state == True:
                    self.wait = WebDriverWait(self.driver, 15)
                    self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="responsivetable"]/tbody/tr[1]/td[3]/span/a')))
                    ActionChains(self.driver).context_click(self.driver.find_element_by_xpath('//*[@id="responsivetable"]/tbody/tr[1]/td[3]/span/a')).perform()
                    time.sleep(1)
                    check = False
                    text = "測試-" + i + ":"
                    message_title(text, view)
                    eval("right(self.wait, self.driver, self.type)." + i + "_click()")
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

        # 右鍵-資料夾測試
        print('資料夾測試')
        view.resultlst.append('資料夾測試')
        view.mylist.insert(tk.END, '資料夾測試')
        self.type = 1
        view.resultlst.append('[右鍵功能測試進行]')
        view.mylist.insert(tk.END, '[右鍵功能測試進行]')
        for i in self.get_fun_name():
            try:
                if self.type == 0:
                    # 創建檔案
                    delete_file()
                    cloud_to_trash()
                    add_file()
                    move_to_cloud()
                else:
                    # 創建資料夾
                    delete_file()
                    cloud_to_trash()
                    add_folder()
                    move_to_cloud()

                self.driver = browser(browser_type)  # 取得driver
                state = login_nav(self.driver, login_config.get('navigate', 'account'),
                                  login_config.get('navigate', 'password'))
                time.sleep(1)
                self.driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/a').click()
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    '//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/div/a[1]').click()
                # 15為全選、16為第一個checkbox檔案
                self.driver.find_elements_by_class_name("label-checkbox")[16].click()
                # 執行此operation測試對應方法按鈕
                if state == True:
                    self.wait = WebDriverWait(self.driver, 15)
                    self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="responsivetable"]/tbody/tr[1]/td[3]/span/a')))
                    ActionChains(self.driver).context_click(self.driver.find_element_by_xpath('//*[@id="responsivetable"]/tbody/tr[1]/td[3]/span/a')).perform()
                    time.sleep(1)
                    check = False
                    text = "測試-" + i + ":"
                    message_title(text, view)
                    eval("right(self.wait, self.driver, self.type)." + i + "_click()")
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