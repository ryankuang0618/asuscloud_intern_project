from common.util import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import tkinter as tk
import clipboard
import getpass
import os
import sys
import traceback

"""
base_test: 基本檔案測試測項
menu: 執行選單操作
right: 執行右鍵操作
symbol: 執行符號操作
p.s: MySyncFolder需要再執行operation前進行remove_all+create_file+create_folder...，
     需依照選單特性去進行，而operation單純只是執行動作。
"""

class base_test:
    def __init__(self,type=None):
        self.type=type
    def share(self,wait,driver):
        try:
            # 分享
            print('share...')
            # 操作方法寫在這
            print('公開分享')
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'link_settings'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'link_settings')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'public_share'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'public_share')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'copy'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'copy')).click()
            temp_driver=browser('chrome')
            temp_driver.get(clipboard.paste())
            time.sleep(3)
            text=temp_driver.find_element_by_xpath(main_test_config.get('share', 'link_name_check')).text
            temp_driver.close()
            # 以連結檔名與創建檔名來比對
            if self.type==0:
                if folder_config.get('file_info', 'name') not in text:
                    return False
            else:
                if folder_config.get('folder_info', 'name') not in text:
                    return False
            print('私人分享')
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'link_settings'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'link_settings')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'private_share'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'private_share')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'add_member'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'add_member')).send_keys(main_test_config.get('share', 'private_share_memebr_id'))
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('share', 'private_add_button'))))
            driver.find_element_by_xpath(main_test_config.get('share', 'private_add_button')).click()
            temp_driver_1=browser('chrome')
            login_nav(temp_driver_1, main_test_config.get('share', 'account'), main_test_config.get('share', 'password'))
            temp_driver_1.find_element_by_xpath(main_test_config.get('share', 'share')).click()
            temp_driver_1.find_element_by_xpath(main_test_config.get('share', 'share_me')).click()
            time.sleep(3)
            html=temp_driver_1.page_source
            # 登入分享對象帳號確認是否分享成功
            temp_driver_1.close()
            if self.type==0:
                if folder_config.get('file_info', 'name') not in html:
                    return False
            else:
                if folder_config.get('folder_info', 'name') not in html:
                    return False
            return True
        except Exception as e:
            print(e)
            print('系統發生錯誤')
    def download(self,wait,driver):
        try:
            # 下載
            #try:
            file_name = str(folder_config.get('file_info', 'name'))+'.txt'

            if self.type==1:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/bs-modal[13]/div/div/bs-modal-body/div/input')))
                driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[13]/div/div/bs-modal-body/div/input').clear()
                driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[13]/div/div/bs-modal-body/div/input').send_keys(folder_config.get('folder_info', 'name'))
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/bs-modal[13]/div/div/bs-modal-footer/div/button[2]')))
                driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[13]/div/div/bs-modal-footer/div/button[2]').click()
                file_name=str(folder_config.get('folder_info', 'name'))+'.7z'
            time.sleep(3)
            if os.path.isfile('C:\\Users\\' + getpass.getuser() + '\\\Downloads' + '\\' + file_name):
                print('找到檔案...')
                return True
            else:
                return False
        except Exception as e:
            print(e)
            print('系統發生錯誤')
        #except:
        #    return False
    def markstar(self, wait, driver):
        # 標記星號
        try:
            print('markstar...')
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('markstar', 'fuc_markstar'))))
            driver.find_element_by_xpath(main_test_config.get('markstar', 'fuc_markstar')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('markstar', 'name'))))
            if (self.type == 0):
                checkname = 'TestFile.txt'
            else:
                checkname = 'TestFolder'
            time.sleep(5)
            table_id = driver.find_element_by_id('responsivetable')
            rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
            for i in range(1, len(rows)):
                cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
                print(cols.text)
                if (cols.text == checkname):
                    return True
            return False
        except:
            return False

    def remove(self, wait, driver):
        try:
            # 刪除
            print('remove...')
            if (self.type == 0):
                checkname = 'TestFile'
            else:
                checkname = 'TestFolder'
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('remove', 'yes_button'))))
            driver.find_element_by_xpath(main_test_config.get('remove', 'yes_button')).click()
            time.sleep(5)
            try:
                table_id = driver.find_element_by_id('responsivetable')
                rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
                for i in range(1, len(rows)):
                    cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
                    if (cols.text == checkname):
                        print('刪除失敗')
                        return False
                    else:
                        print('刪除成功')
                        return True
            except:
                print("未找到資料欄位...")
                print('刪除成功')
                return True
        except Exception as e:
            print(e)
            print('系統發生錯誤')
    def detail(self, wait, driver):
        try:
            # 詳細資訊
            print('detail...')
            if (self.type == 0):
                checkname = folder_config.get('file_info','name')
            else:
                checkname = folder_config.get('folder_info','name')
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('detail', 'name'))))
                if checkname in driver.find_element_by_xpath(main_test_config.get('detail', 'name')).text:
                    return True
                else:
                    return False
            except:
                return False
        except Exception as e:
            print(e)
            print('系統發生錯誤')
    def msg(self, wait, driver):
        try:
            # 留言
            print('msg...')
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('msg', 'msg_input'))))
            driver.find_element_by_xpath(main_test_config.get('msg', 'msg_input')).clear()
            driver.find_element_by_xpath(main_test_config.get('msg', 'msg_input')).send_keys('ANDY IS BIGGGGGGg')
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('msg', 'enter'))))
            driver.find_element_by_xpath(main_test_config.get('msg', 'enter')).click()
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('msg', 'msg_word'))))
                if (driver.find_element_by_xpath(main_test_config.get('msg', 'msg_word')).text == 'ANDY IS BIGGGGGGg'):
                    return True
                else:
                    return False
            except:
                return False
        except Exception as e:
            print(e)
            print('系統發生錯誤')
    def get_fun_name(self):
        # 回傳此類別方法名稱，思考如何自動回傳? 否則只能手打
        temp = list()
        for i in list(dir(base_test)):  # 取得class name再取所有function name
            if '__' not in i and 'get_fun_name' not in i and 'main' not in i:
                temp.append(i)
        print('bt', temp)
        return temp

class menu:
    def __init__(self,wait,driver):
        self.driver=driver
        self.wait=wait

    def share_click(self):
        # 操作方法寫在這
        print('run share click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'share'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'share')).click()

    def move_click(self):
        print('run move click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'move'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'move')).click()

    def copy_click(self):
        print('run copy click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'copy'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'copy')).click()

    def rename_click(self):
        print('run rename click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'rename'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'rename')).click()

    def remove_click(self):
        print('run remove click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'remove'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'remove')).click()

    def detail_click(self):
        print('run detail click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'detail'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'detail')).click()

    def markstar_click(self):
        print('run markstar click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'markstar'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'markstar')).click()

    def download_click(self):
        print('run download click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'download'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'download')).click()

    def msg_click(self):
        print('run msg click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'detail'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'detail')).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'msg'))))
        self.driver.find_element_by_xpath(main_test_config.get('menu', 'msg')).click()

class right:

    def __init__(self,wait,driver,type):
        self.driver=driver
        self.wait=wait
        self.type=type
        self.order=check_function_order(self.wait, self.driver)
    def decide_order(self,name):
        print(self.order)
        for i in range(len(self.order)):
            if(self.order[i] == name):
                return i+1

    def share_click(self):
        print('run share click')
        xpath=main_test_config.get('right', 'share')
        if self.type == 0:
            temp=xpath.split('li')
            xpath=temp[0]+"li["+str(self.decide_order('分享'))+']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def download_click(self):
        print('run download click')
        xpath = main_test_config.get('right', 'download')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(self.decide_order('下載')) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def move_click(self):
        print('run move click')
        xpath = main_test_config.get('right', 'move')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('搬移至'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def copy_click(self):
        print('run copy click')
        xpath = main_test_config.get('right', 'copy')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('複製至'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def rename_click(self):
        print('run rename click')
        xpath = main_test_config.get('right', 'rename')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('重新命名'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def remove_click(self):
        print('run remove click')
        xpath = main_test_config.get('right', 'remove')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('刪除'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def detail_click(self):
        print('run detail click')
        xpath = main_test_config.get('right', 'detail')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('詳細資訊'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def markstar_click(self):
        print('run markstar click')
        xpath = main_test_config.get('right', 'markstar')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('標記星號'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def msg_click(self):
        print('run msg click')
        xpath = main_test_config.get('right', 'detail')
        if self.type == 0:
            temp = xpath.split('li')
            xpath = temp[0] + "li[" + str(str(self.decide_order('詳細資訊'))) + ']'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('right', 'msg'))))
        self.driver.find_element_by_xpath(main_test_config.get('right', 'msg')).click()

class symbol:
    def __init__(self, wait, driver, type):
        self.driver = driver
        self.wait = wait
        self.type = type

    def share_click(self):
        print('run symbol share click')
        xpath = main_test_config.get('symbol','share')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def markstar_click(self):
        print('run symbol markstar click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="responsivetable"]/tbody/tr/td[4]')))
        location = self.driver.find_element_by_xpath('//*[@id="responsivetable"]/tbody/tr/td[4]')
        action = ActionChains(self.driver)
        # 滑鼠移動到元素上,懸浮perform()
        action.move_to_element(location).perform()
        xpath = main_test_config.get('symbol', 'markstar')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def msg_click(self):
        print('run symbol msg click')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="responsivetable"]/tbody/tr/td[4]')))
        location = self.driver.find_element_by_xpath('//*[@id="responsivetable"]/tbody/tr/td[4]')
        action = ActionChains(self.driver)
        # 滑鼠移動到元素上,懸浮perform()
        action.move_to_element(location).perform()
        xpath = '//button[@data-original-title="留言"]'
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()