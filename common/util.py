import configparser
import os
from selenium import webdriver
import tkinter as tk
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import sys
import traceback
from datetime import datetime

# 共用config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini'), encoding='utf8')
login_config=configparser.ConfigParser()
login_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'login_config.ini'), encoding='utf8')
account_config=configparser.ConfigParser()
account_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'account_settings_config.ini'), encoding='utf8')
main_test_config=configparser.ConfigParser()
main_test_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'main_test_config.ini'), encoding='utf8')
folder_config=configparser.ConfigParser()
folder_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'file_folder_config.ini'), encoding='utf8')
move_copy_rename_config=configparser.ConfigParser()
move_copy_rename_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'move_copy_rename.ini'), encoding='utf8')
project_folder_config=configparser.ConfigParser()
project_folder_config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'project_folder.ini'), encoding='utf8')
config.remove_option('driver', 'folder_path')
config.set('driver', 'folder_path',os.path.join(os.path.dirname(__file__),'selenium_driver'))
config.write(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini'), 'w',encoding='utf8'))

def check_state(url):
    if 'cathay' in url:
        login_config.remove_option('xpath', 'account')
        login_config.set('xpath', 'account', login_config.get('cathay_login_xpath', 'account'))
        login_config.remove_option('xpath', 'password')
        login_config.set('xpath', 'password', login_config.get('cathay_login_xpath', 'password'))
        login_config.remove_option('xpath', 'enter_button')
        login_config.set('xpath', 'enter_button', login_config.get('cathay_login_xpath', 'enter_button'))
        login_config.remove_option('xpath', 'check_login_fail_point')
        login_config.set('xpath', 'check_login_fail_point', login_config.get('cathay_login_xpath', 'check_login_fail_point'))
        login_config.write(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'login_config.ini'), 'w'))
    else:
        login_config.remove_option('xpath', 'account')
        login_config.set('xpath', 'account', login_config.get('origin_login_xpath', 'account'))
        login_config.remove_option('xpath', 'password')
        login_config.set('xpath', 'password', login_config.get('origin_login_xpath', 'password'))
        login_config.remove_option('xpath', 'enter_button')
        login_config.set('xpath', 'enter_button', login_config.get('origin_login_xpath', 'enter_button'))
        login_config.remove_option('xpath', 'check_login_fail_point')
        login_config.set('xpath', 'check_login_fail_point', login_config.get('origin_login_xpath', 'check_login_fail_point'))
        login_config.write(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'login_config.ini'), 'w'))

def browser(type):
    if str(type).lower()=="chrome":
        driver = webdriver.Chrome(executable_path=config.get('driver','folder_path')+config.get('driver',str(type).lower()+'_driver_path'))
    elif str(type).lower()=="edge":
        driver = webdriver.Edge(executable_path=config.get('driver', 'folder_path') + config.get('driver', str(type).lower() + '_driver_path'))
    elif str(type).lower()=="firefox":
        driver = webdriver.Firefox(executable_path=config.get('driver', 'folder_path') + config.get('driver', str(type).lower() + '_driver_path'))

    return driver
def message_title(text,view):
    time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    view.resultlst.append(time)
    view.resultlst.append(text)
    view.mylist.insert(tk.END, text)
def message_template(text,state,view):
    try:
        if state==True:
            print(text + '[成功]')
            view.resultlst.append(text + '[成功]')
            view.mylist.insert(tk.END, text + '[成功]')
            view.mylist.itemconfig("end", bg="green")
        elif state==False:
            print(text + '[失敗]')
            view.resultlst.append(text + '[失敗]')
            view.mylist.insert(tk.END, text + '[失敗]')
            view.mylist.itemconfig("end", bg="red")
    except Exception as e:
        print(e)
        view.resultlst.append(text + '[失敗]')
        view.mylist.insert(tk.END, text + '[失敗]')
        view.mylist.itemconfig("end", bg="red")
        view.mylist.insert(tk.END, str(e))
        view.mylist.itemconfig("end", bg="red")

def login_nav(driver,account,password):
    try:
        driver.get(login_config.get('navigate', 'url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'account'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).clear()
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).send_keys(account)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'password'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).clear()
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).send_keys(password)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'enter_button'))))
        time.sleep(5)
        driver.find_element_by_xpath(login_config.get('xpath', 'enter_button')).click()
        Lock = 'lock'
        while Lock=='lock':
            try:
                if(driver.find_element_by_xpath(login_config.get('xpath', 'checklogin_error')).text == '帳號或密碼錯誤，請重新輸入。'):
                    Lock = 'False'
            except:
                if(driver.current_url == login_config.get('navigate', 'check_url')):
                    Lock = 'True'

        if(Lock == 'True'):
            return True
        else:
            return False

    except Exception as e:
        print(e)
        print('系統發生錯誤')
        return False

def login_osm(driver,account,password):
    try:
        driver.get(config.get('osm','url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_login_xpath', 'account'))))
        driver.find_element_by_xpath(config.get('osm_login_xpath', 'account')).clear()
        driver.find_element_by_xpath(config.get('osm_login_xpath', 'account')).send_keys(account)
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_login_xpath', 'password'))))
        driver.find_element_by_xpath(config.get('osm_login_xpath', 'password')).clear()
        driver.find_element_by_xpath(config.get('osm_login_xpath', 'password')).send_keys(password)
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_login_xpath', 'enter_button'))))
        driver.find_element_by_xpath(config.get('osm_login_xpath', 'enter_button')).click()
    except Exception as e:
        print(e)
        print('系統發生錯誤')
def create_test_group():
    try:
        driver=browser('chrome')
        login_osm(driver,config.get('osm','account'),config.get('osm','password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'user_management'))))
        driver.find_element_by_xpath(config.get('osm_xpath', 'user_management')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'group_list'))))
        driver.find_element_by_xpath(config.get('osm_xpath', 'group_list')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'group_list_check'))))
        time.sleep(5)
        html=driver.page_source
        objSoup=BeautifulSoup(html,'lxml')
        group_name=list()
        objTag=objSoup.find('table','table-b rwd-table').find('tbody').find_all('tr','ng-scope')
        for i in objTag:
            group_name.append(i.find('td').text)
        print('目前已存在osm群組:',group_name)
        group_list_name=str(config.get('osm_group', 'group_name')).split(',')
        for i in group_list_name:
            if i not in group_name:
                msg=input('請手動增加['+str(i)+']群組，增加完成後請輸入OK:')
                while msg.lower()  not in 'ok':
                    msg = input('請手動增加[' + str(i) + ']群組，增加完成後請輸入OK:')
        driver.close()
    except Exception as e:
        print(e)
        print('系統發生錯誤')

def create_test_account(group):
    try:
        driver = browser('chrome')
        login_osm(driver, config.get('osm', 'account'), config.get('osm', 'password'))
        wait = WebDriverWait(driver, 15)
        # 選單點擊
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'user_management'))))
        driver.find_element_by_xpath(config.get('osm_xpath', 'user_management')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'account_info'))))
        driver.find_element_by_xpath(config.get('osm_xpath', 'account_info')).click()

        count=1
        account='test'+str(count)
        password = config.get('osm_account', 'default_password')
        name = account+'_name'
        run=True

        wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'create_account'))))
        driver.find_element_by_xpath(config.get('osm_xpath', 'create_account')).click()
        # 輸入資訊
        while run == True:
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'account'))))
                driver.find_element_by_xpath(config.get('osm_xpath', 'account')).clear()
                driver.find_element_by_xpath(config.get('osm_xpath', 'account')).send_keys(account)
                wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'name'))))
                driver.find_element_by_xpath(config.get('osm_xpath', 'name')).clear()
                driver.find_element_by_xpath(config.get('osm_xpath', 'name')).send_keys(name)
                wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'email'))))
                driver.find_element_by_xpath(config.get('osm_xpath', 'email')).clear()
                driver.find_element_by_xpath(config.get('osm_xpath', 'email')).send_keys(config.get('osm_account','email'))
                wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'password'))))
                driver.find_element_by_xpath(config.get('osm_xpath', 'password')).clear()
                driver.find_element_by_xpath(config.get('osm_xpath', 'password')).send_keys(password)
                wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'confirm_password'))))
                driver.find_element_by_xpath(config.get('osm_xpath', 'confirm_password')).clear()
                driver.find_element_by_xpath(config.get('osm_xpath', 'confirm_password')).send_keys(password)
                select = Select(driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/form/div[7]/div/select'))
                select.select_by_value("string:" + group)
            except Exception as e:
                print(e)
                continue
            # 送出
            wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath','send'))))
            driver.find_element_by_xpath(config.get('osm_xpath','send')).click()
            # 操作原因
            wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath','msg'))))
            driver.find_element_by_xpath(config.get('osm_xpath','msg')).send_keys('test')
            # OK
            wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath','ok'))))
            driver.find_element_by_xpath(config.get('osm_xpath','ok')).click()
            time.sleep(5)
            # 狀態訊息
            wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath', 'state_msg'))))
            state_msg=driver.find_element_by_xpath(config.get('osm_xpath', 'state_msg')).text
            print('狀態訊息:',str(state_msg).strip())
            if '帳號重複' in str(state_msg).strip():
                print(str(account) + ',' + str(password) + ',' + str(name)+','+str(group))
                count+=1
                account = 'test' + str(count)
                name = account + '_name'
                run=True
            else:
                print(str(account)+','+str(password)+','+str(name)+','+str(group))
                run=False
                login_config.remove_option('navigate', 'account')
                login_config.set('navigate', 'account', account)
                login_config.remove_option('navigate', 'password')
                login_config.set('navigate', 'password', password)
                login_config.write(
                    open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'login_config.ini'), 'w'))
                account_config.remove_option('account', 'name')
                account_config.set('account', 'name', name)
                account_config.remove_option('account', 'change_password')
                account_config.set('account', 'change_password', config.get('osm_account', 'default_password2'))
                account_config.write(
                    open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'account_settings_config.ini'),
                         'w'))
            # 完成
            wait.until(EC.visibility_of_element_located((By.XPATH, config.get('osm_xpath','finish'))))
            driver.find_element_by_xpath(config.get('osm_xpath','finish')).click()
        driver.close()
    except Exception as e:
        print(e)
        print('系統發生錯誤')
def get_carry_time(t,check=True):
    try:
        # 時間進位 True向後，False向前
        h = t.split(":")[0]
        m = t.split(":")[1]

        if check == True:
            m = str(int(m)+1)
            if m == "60":
                m = "00"
                h = str(int(h)+1)
            if h == "24":
                h = "00"

        elif check == False:
            m = str(int(m) - 1)
            if m == "-1":
                m = "59"
                h = str(int(h) - 1)
            if h == "-1":
                h = "23"

        if len(m)<2:
            m='0'+m
        if len(h)<2:
            m='0'+h

        return h+':'+m
    except Exception as e:
        print(e)
        print('系統發生錯誤')
def add_folder():
    try:
        driver = browser('chrome')
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath','add_button'))))
        driver.find_element_by_xpath(folder_config.get('xpath','add_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath', 'add_file_folder'))))
        driver.find_element_by_xpath(folder_config.get('xpath','add_file_folder')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath', 'input_foldername'))))
        driver.find_element_by_xpath(folder_config.get('xpath', 'input_foldername')).clear()
        driver.find_element_by_xpath(folder_config.get('xpath', 'input_foldername')).send_keys(str(folder_config.get('folder_info','name')))
        wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath', 'enter_button'))))
        time.sleep(3)
        driver.find_element_by_xpath(folder_config.get('xpath', 'enter_button')).click()
        wait.until(EC.visibility_of_element_located((By.ID, 'responsivetable')))
        time.sleep(3)
        table_id = driver.find_element_by_id('responsivetable')
        rows = table_id.find_elements_by_tag_name("tr") # get all of the rows in the table
        for i in range(1, len(rows)):
            cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
            if(cols.text == str(folder_config.get('folder_info','name'))):
                print('新增成功')
                driver.close()
                break
            else:
                print('新增失敗')
                driver.close()
                break
    except Exception as e:
        print(e)
        print('系統發生錯誤')
def delete_folder():
    try:
        driver = browser('chrome')
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath','add_button'))))
        table_id = driver.find_element_by_id('responsivetable')
        rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
        for i in range(1, len(rows)):
            cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
            print(cols.text)
            if(cols.text == folder_config.get('folder_info','name')):
                folder_order = i
                driver.close()
                break
        actionChains = ActionChains(driver)
        actionChains.context_click(driver.find_element_by_xpath('//*[@id="responsivetable"]/tbody/tr['+str(folder_order)+']/td[4]')).perform()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="cdk-overlay-0"]/context-menu-content/div/ul/li[7]/a')))
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="cdk-overlay-0"]/context-menu-content/div/ul/li[7]/a').click()
        wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]')))
        driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]').click()
        time.sleep(3)
        try:
            table_id = driver.find_element_by_id('responsivetable')
            rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
            for i in range(1, len(rows)):
                cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
                if (cols.text == str(folder_config.get('folder_info', 'name'))):
                    print('刪除失敗')
                    driver.close()
                    break
                else:
                    print('刪除成功')
                    driver.close()
                    break
        except:
            driver.close()
            print("未找到資料欄位...")
    except Exception as e:
        print(e)
        print('系統發生錯誤')
def add_file():
    try:
        print('新增檔案')
        with open(str(folder_config.get('file_info','name'))+'.txt','w',encoding='utf8') as f:
            f.write("test")
        driver = browser('chrome')
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[4]/a')))
        driver.find_element_by_xpath('//*[@id="breadcrumb"]/ul[2]/li[4]/a').click()
        time.sleep(3)
        upload = driver.find_element_by_id('uploadfile')
        upload.send_keys(os.path.join(os.path.dirname(__file__),folder_config.get('file_info','name')+'.txt'))  # send_keys
        while True:
            wait.until(EC.visibility_of_element_located((By.XPATH, folder_config.get('xpath','check_upload'))))
            try:
                if('成功' in driver.find_element_by_xpath(folder_config.get('xpath','check_upload')).text):
                    break
            except:
                pass
        os.remove(os.path.join(os.path.dirname(__file__),folder_config.get('file_info','name')+'.txt'))
        driver.close()
    except Exception as e:
        print(e)
        print('系統發生錯誤')

def delete_file():
    try:
        print('刪除檔案')
        driver = browser('chrome')
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        wait = WebDriverWait(driver, 15)
        try:
            time.sleep(3)
            driver.find_elements_by_class_name("label-checkbox")[15].click()
            wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'remove'))))
            driver.find_element_by_xpath(main_test_config.get('menu', 'remove')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]')))
            driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]').click()
            driver.close()
        except:
            print("未找到資料欄位...")
            driver.close()
    except Exception as e:
        print(e)
        print('系統發生錯誤')

def cloud_to_trash():
    driver = browser('chrome')
    login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="wrapper"]/app-aside/aside/div/div[2]/ul/li[2]/div/a[1]').click()
    wait = WebDriverWait(driver, 15)
    try:
        time.sleep(3)
        driver.find_elements_by_class_name("label-checkbox")[15].click()
        wait.until(EC.visibility_of_element_located((By.XPATH, main_test_config.get('menu', 'remove'))))
        driver.find_element_by_xpath(main_test_config.get('menu', 'remove')).click()
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]')))
        driver.find_element_by_xpath('//*[@id="page-top"]/bs-modal[9]/div/div/bs-modal-footer/div/button[2]').click()
        driver.close()
    except:
        print("未找到資料欄位...")
        driver.close()

def move(wait,driver,type):
    try:
        print('執行搬移動作')
        cloud_to_trash()
        if(type == 'mysyncfolder'):
            print('mysncfolder to cloud')
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'backup_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'backup_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'cloud_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'cloud_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'move_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'move_button')).click()
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div')))
                word = driver.find_element_by_xpath('//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div').text
                print(word)
                time.sleep(4)
                if('成功' in word):
                    return True
                else:
                    return False
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
        elif (type == 'cloud'):
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'mysncfolder_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'mysncfolder_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'copy_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'copy_button')).click()
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span')))
                word = driver.find_element_by_xpath('//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span').text
                if ('成功' in word):
                    return True
                else:
                    return False
            except Exception as e:
                error_class = e.__class__.__name__  # 取得錯誤類型
                detail = e.args[0]  # 取得詳細內容
                cl, exc, tb = sys.exc_info()  # 取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
                fileName = lastCallStack[0]  # 取得發生的檔案名稱
                lineNum = lastCallStack[1]  # 取得發生的行號
                funcName = lastCallStack[2]  # 取得發生的函數名稱
                errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class,
                                                                detail)
                print(errMsg)
                return False
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
        print('系統發生錯誤')


def copy(wait,driver,type):
    try:
        print('執行複製動作')
        if (type == 'mysyncfolder'):
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'c_backup_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'c_backup_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'c_cloud_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'c_cloud_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'copy_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'copy_button')).click()
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span')))
                word = driver.find_element_by_xpath('//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span').text
                if ('成功' in word):
                    return True
                else:
                    return False
            except:
                return False
        elif (type == 'cloud'):
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'c_mysncfolder_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'c_mysncfolder_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'copy_button'))))
            driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'copy_button')).click()
            try:
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span')))
                word = driver.find_element_by_xpath('//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span').text
                if ('成功' in word):
                    return True
                else:
                    return False
            except:
                return False
    except Exception as e:
        print(e)
        print('系統發生錯誤')


def rename(wait,driver):
    try:
        print('執行重新命名動作')
        wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'rename_input'))))
        driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'rename_input')).clear()
        driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'rename_input')).send_keys('rename_test')
        wait.until(EC.visibility_of_element_located((By.XPATH, move_copy_rename_config.get('xpath', 'rename_enter'))))
        driver.find_element_by_xpath(move_copy_rename_config.get('xpath', 'rename_enter')).click()
        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span')))
            word = driver.find_element_by_xpath('//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div/span').text
            if ('成功' in word):
                return True
            else:
                return False
        except:
            return False
    except Exception as e:
        print(e)

def check_function_order(wait,driver):
    try:
        temp=[]
        wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@class="dropdown-menu show"]')))
        time.sleep(3)
        ul = driver.find_element_by_xpath('//ul[@class="dropdown-menu show"]')
        lis = ul.find_elements_by_tag_name("li")
        for i in range(0, len(lis)):
            name = lis[i].find_element_by_tag_name("a")
            temp.append(name.text)
        return temp
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




