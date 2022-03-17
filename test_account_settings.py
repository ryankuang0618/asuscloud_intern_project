from common.util import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import re
import pyautogui
import pyperclip
import sys
import traceback

def self_name_task1(browser_type,view):
    try:
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試狀況1-1:主頁_個人名稱確認'
            message_title(text, view)
            print(text)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_button')).click()
            time.sleep(3)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_name_button'))))
            if account_config.get('account', 'name') in driver.find_element_by_xpath(account_config.get('xpath', 'account_name_button')).text:
                driver.close()
                return True, text
            else:
                driver.close()
                return False, text
        else:
            driver.close()
            return False, 'navigate登入問題'
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


def self_name_task2(browser_type,view):
    try:
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試狀況1-2:個人設定_個人名稱確認'
            message_title(text, view)
            print(text)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_settings_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_settings_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'self_settings_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'self_settings_button')).click()
            time.sleep(3)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_name_inside'))))
            if account_config.get('account', 'name') in driver.find_element_by_xpath(account_config.get('xpath', 'account_name_inside')).text:
                driver.close()
                return True, text
            else:
                driver.close()
                return False, text
        else:
            driver.close()
            return False, 'navigate登入問題'
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

def change_password(text,origin_acc,origin_pas,change_pas,browser_type,confirm_pas=None):
    driver = browser(browser_type)
    state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))

    if confirm_pas is None:
        confirm_pas=change_pas

    if state == True:
        # 登入成功才繼續進行
        print(text)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_button'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'account_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_settings_button'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'account_settings_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'self_settings_button'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'self_settings_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'change_password_button'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'change_password_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'old_password_textarea'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'old_password_textarea')).send_keys(origin_pas)
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'new_password_textarea'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'new_password_textarea')).send_keys(change_pas)
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'again_password_textarea'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'again_password_textarea')).send_keys(confirm_pas)
        run = True
        while run == True:
            captcha = input("請輸入驗證碼:")
            if len(captcha) != 0:
                wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'captcha_pic'))))
                driver.find_element_by_xpath(account_config.get('xpath', 'captcha_pic')).clear()
                driver.find_element_by_xpath(account_config.get('xpath', 'captcha_pic')).send_keys(str(captcha))
                wait.until(
                    EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'change_password_enter'))))
                driver.find_element_by_xpath(account_config.get('xpath', 'change_password_enter')).click()
            # 驗證碼輸入錯誤機制如何??
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'captcha_error_msg'))))
                print("驗證碼輸入錯誤")
            except:
                print("驗證碼輸入成功")
                run = False
        return driver

def change_password_task1(browser_type,view):
    """更改密碼: 舊密碼、新密碼、確認新密碼、驗證碼皆輸入正確
       測試登入: 帳號、密碼皆輸入正確"""
    try:
        origin_acc=login_config.get('navigate', 'account')
        origin_pas=login_config.get('navigate', 'password')
        change_pas=account_config.get('account', 'change_password')
        text='測試狀況2-1:個人設定_變更密碼(更改密碼: 舊密碼、新密碼、確認新密碼、驗證碼皆輸入正確+測試登入)'
        message_title(text, view)
        driver = change_password(text,origin_acc,origin_pas,change_pas,browser_type)
        print('進行登入測試...')
        state = login_nav(driver, origin_acc, change_pas)
        print('進行登入測試...完成')
        if state == True:
            # config新密碼取代舊密碼
            account_config.remove_option('account', 'change_password')
            account_config.set('account', 'change_password', origin_pas)
            account_config.write(open(os.path.join(os.path.dirname(__file__), 'config', 'account_settings_config.ini'), 'w'))
            login_config.remove_option('navigate', 'password')
            login_config.set('navigate', 'password', change_pas)
            login_config.write(open(os.path.join(os.path.dirname(__file__), 'config', 'login_config.ini'), 'w'))
            driver.close()
            return True, text
        else:
            driver.close()
            return False, text
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

def change_password_task2(browser_type,view):
    """更改密碼: 舊密碼空白，新密碼、確認新密碼、驗證碼皆輸入正確"""
    try:
        origin_acc = login_config.get('navigate', 'account')
        origin_pas = login_config.get('navigate', 'password')
        change_pas = account_config.get('account', 'change_password')
        text = '測試狀況2-2:個人設定_變更密碼(更改密碼: 舊密碼空白，新密碼、確認新密碼、驗證碼皆輸入正確)'
        message_title(text, view)
        driver = change_password(text, origin_acc, "", change_pas,browser_type)
        try:
            if str(driver.find_element_by_xpath(account_config.get('xpath', 'origin_pass_error_msg')).text).strip() =='請輸入舊密碼':
                driver.close()
                return True, text
        except:
            driver.close()
            return False, text
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

def change_password_task3(browser_type,view):
    """更改密碼: 新密碼空白，舊密碼、確認新密碼、驗證碼皆輸入正確"""
    try:
        origin_acc = login_config.get('navigate', 'account')
        origin_pas = login_config.get('navigate', 'password')
        change_pas = account_config.get('account', 'change_password')
        text = '測試狀況2-3:個人設定_變更密碼(更改密碼: 新密碼空白，舊密碼、確認新密碼、驗證碼皆輸入正確)'
        message_title(text, view)
        driver = change_password(text, origin_acc, origin_pas, "",browser_type,confirm_pas=change_pas)
        try:
            if str(driver.find_element_by_xpath(account_config.get('xpath', 'new_pass_error_msg')).text).strip() == '請輸入新密碼' or  '密碼必須至少由' in str(driver.find_element_by_xpath(account_config.get('xpath', 'new_pass_error_msg')).text).strip():
                driver.close()
                return True, text
        except:
            driver.close()
            return False, text
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

def change_password_task4(browser_type,view):
    """更改密碼: 確認新密碼空白，舊密碼、新密碼、驗證碼皆輸入正確"""
    try:
        origin_acc = login_config.get('navigate', 'account')
        origin_pas = login_config.get('navigate', 'password')
        change_pas = account_config.get('account', 'change_password')
        text = '測試狀況2-4:個人設定_變更密碼(更改密碼: 確認新密碼空白，舊密碼、新密碼、驗證碼皆輸入正確")'
        message_title(text, view)
        driver = change_password(text, origin_acc, origin_pas, change_pas, browser_type,confirm_pas="")
        try:
            if str(driver.find_element_by_xpath(
                    account_config.get('xpath', 'confirm_pass_error_msg')).text).strip() == '請再輸入一次新密碼':
                driver.close()
                return True, text
        except:
            driver.close()
            return False, text
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

def check_login_account(browser_type,view):
    try:
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試狀況3-1:目前登入帳號'
            message_title(text, view)
            print(text)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_settings_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_settings_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'self_settings_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'self_settings_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'login_account'))))
            if login_config.get('navigate','account') in driver.find_element_by_xpath(account_config.get('xpath', 'login_account')).text:
                driver.close()
                return True, text
            else:
                driver.close()
                return False, text
        else:
            driver.close()
            return False, 'navigate登入問題'
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

def check_ip(browser_type,view):
    try:
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試狀況1-1:IP位置'
            message_title(text, view)
            print(text)
            # IP有問題
            print('IP issued!!!!!!')
            driver.close()
            return True, text
        else:
            driver.close()
            return False, 'navigate登入問題'
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

def check_system_time(browser_type,view):
    try:
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試狀況1-1:系統時間'
            message_title(text, view)
            print(text)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_settings_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'account_settings_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'login_record_button'))))
            driver.find_element_by_xpath(account_config.get('xpath', 'login_record_button')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'login_record_text'))))
            record=driver.find_element_by_xpath(account_config.get('xpath', 'login_record_text')).text
            login_time = datetime.datetime.now()
            date = str(login_time).split(' ')[0]
            date_time = str(login_time).split(' ')[1].split('.')[0].split(':')
            print(login_time)
            print(date)
            print(date_time)
            print(record)
            if date in record and (date_time[0] + ':' + date_time[1] in record or get_carry_time(date_time[0] + ':' + date_time[1],False) in record):
                driver.close()
                return True, text
            else:
                driver.close()
                return False, text
        else:
            driver.close()
            return False, 'navigate登入問題'
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

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

def getnumber(num):
    result_num=''
    for i in range(0,len(num)):
        if(is_number(num[i]) == False):
            break
        else:
            result_num+=num[i]
    result_num2 = int(result_num)
    if(result_num2<1024):
        return result_num2
    else:
        return result_num2//1024

def osm_accinfo():
    driver = browser('chrome')
    driver.get(login_config.get('osm', 'url'))
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'osm_account'))))
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_account')).clear()
    # 輸入錯誤帳號(正確帳號的一半)
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_account')).send_keys(str(login_config.get('osm', 'account')))
    wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'osm_password'))))
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_password')).clear()
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_password')).send_keys(str(login_config.get('osm', 'password')))
    time.sleep(2)
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_enter')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'osm_usermanage'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'osm_usermanage')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'user_info'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'user_info')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'search_account'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'search_account')).clear()
    driver.find_element_by_xpath(account_config.get('xpath', 'search_account')).send_keys(str(login_config.get('navigate', 'account')))
    time.sleep(2)
    driver.find_element_by_xpath(account_config.get('xpath', 'search_account_enter')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'account_info'))))
    time.sleep(2)
    driver.find_element_by_link_text(str(login_config.get('navigate', 'account'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'group_name'))))
    account_config.set("account_data",'group_name',str(driver.find_element_by_xpath(account_config.get('xpath', 'group_name')).text))
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'all_space'))))
    time.sleep(2)
    account_config.set("account_data", 'allspaces', str(getnumber(driver.find_element_by_xpath(account_config.get('xpath', 'all_space')).text)))
    account_config.set("account_data", 'usedspaces', str(getnumber(driver.find_element_by_xpath(account_config.get('xpath', 'used_space')).text)))
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'group_manage'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'group_manage')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr[2]/td[1]')))
    time.sleep(2)
    table_id = driver.find_elements_by_class_name('table-b rwd-table')
    rows = driver.find_elements_by_tag_name("tr")  # get all of the rows in the table
    for i in range(2,len(rows)):
        cols = rows[i].find_elements_by_tag_name("td")[0]# note: index start from 0, 1 is col 2
        if(cols.text == account_config.get('account_data', 'group_name')):
            group_count = i
            break
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr['+str(group_count)+']/td[5]/input')))
    driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/table/tbody/tr['+str(group_count)+']/td[5]/input').click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    single_upload_word = str(pyperclip.paste())
    print(single_upload_word)
    account_config.set("account_data", 'single_upload', str(getnumber(single_upload_word)))
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[6]/button')))
    driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[6]/button').click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'daily_download_check'))))
    print(str(driver.find_element_by_xpath(account_config.get('xpath', 'daily_download_check')).get_attribute('class')))
    if(str(driver.find_element_by_xpath(account_config.get('xpath', 'daily_download_check')).get_attribute('class')) == 'ng-pristine ng-untouched ng-valid ng-not-empty'):
        wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'daily_download'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'daily_download')).click()
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        daily_download_word = str(pyperclip.paste())
        print(daily_download_word)
        account_config.set("account_data", 'daily_download', str(getnumber(daily_download_word)))
        print(str(getnumber(daily_download_word)))
    else:
        account_config.set("account_data", 'daily_download', '1')
    account_config.write(open(os.path.join(os.path.dirname(__file__),'config', 'account_settings_config.ini'), "r+", encoding="utf-8"))
    driver.close()

def spaces(browser_type,view):
    try:
        text = '測試狀況一:空間明細測試'
        message_title(text, view)
        print(text)
        driver = browser(browser_type)
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH,account_config.get('xpath', 'imageurl'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'imageurl')).click()
        WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH,account_config.get('xpath', 'acount_setting'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'acount_setting')).click()
        WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'spaces_word'))))
        time.sleep(3)
        spaces = str(driver.find_element_by_xpath(account_config.get('xpath', 'spaces_word')).text)
        allspaces = ''
        for i in range(0,len(spaces)):
            if(is_number(spaces[i])==True):
                allspaces+=spaces[i]
            elif(spaces[i] == '.'):
                allspaces += '.'
            elif(spaces[i] == 'B'):
                allspaces += ' '
        print(allspaces)
        allspaces_2 = allspaces.split(' ')
        print(allspaces_2[0],end='')
        print(account_config.get('account_data', 'allspaces'))
        print(allspaces_2[1],end='')
        print(account_config.get('account_data', 'usedspaces'))
        if(float(allspaces_2[0])==float(account_config.get('account_data', 'allspaces')) and float(allspaces_2[1])==float(account_config.get('account_data', 'usedspaces'))):
            driver.close()
            return True, text
        else:
            driver.close()
            return False, text
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

def single_upload(browser_type,view):
    try:
        text = '測試狀況二:單檔上傳限制測試'
        message_title(text, view)
        print(text)
        driver = browser(browser_type)
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'imageurl'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'imageurl')).click()
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'acount_setting'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'acount_setting')).click()
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'single_upload_word'))))
        time.sleep(3)
        single = str(driver.find_element_by_xpath(account_config.get('xpath', 'single_upload_word')).text)
        single_upload = ''
        for i in range(0, len(single)):
            if (is_number(single[i]) == True):
                single_upload += single[i]
            elif (single[i] == '.'):
                single_upload += '.'
        print(single_upload)
        if(float(single_upload) ==  float(account_config.get('account_data', 'single_upload'))):
            driver.close()
            return True, text
        else:
            driver.close()
            return False, text
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

def daily_download(browser_type,view):
    try:
        text = '測試狀況三:單檔上傳限制測試'
        message_title(text, view)
        print(text)
        driver = browser(browser_type)
        login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'imageurl'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'imageurl')).click()
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'acount_setting'))))
        driver.find_element_by_xpath(account_config.get('xpath', 'acount_setting')).click()
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'daily_limit_word'))))
        time.sleep(3)
        limit = str(driver.find_element_by_xpath(account_config.get('xpath', 'daily_limit_word')).text)
        daily_limit = ''
        for i in range(0, len(limit)):
            if (is_number(limit[i]) == True):
                daily_limit += limit[i]
            elif (limit[i] == '.'):
                daily_limit += '.'
        print(daily_limit)
        print('r')
        if (float(daily_limit) == float(account_config.get('account_data', 'daily_download'))):
            driver.close()
            return True, text
        else:
            driver.close()
            return False, text
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

def account(view,browser_type):
    print('[帳號設定測試]')
    # 個人名稱
    state,text=self_name_task1(browser_type,view)
    message_template(text, state, view)
    state, text = self_name_task2(browser_type,view)
    message_template(text, state, view)
    # 變更密碼
    state, text = change_password_task1(browser_type,view)
    message_template(text, state, view)
    state, text = change_password_task2(browser_type,view)
    message_template(text, state, view)
    state, text = change_password_task3(browser_type,view)
    message_template(text, state, view)
    state, text = change_password_task4(browser_type,view)
    message_template(text, state, view)
    # 目前登入帳號
    state, text = check_login_account(browser_type,view)
    message_template(text, state, view)
    # 語系
    # IP
    state, text = check_ip(browser_type,view)
    message_template(text, state, view)
    # 系統時間
    state, text = check_system_time(browser_type,view)
    message_template(text, state, view)
    osm_accinfo()
    state, text = spaces(browser_type,view)
    message_template(text, state, view)
    state, text = single_upload(browser_type,view)
    message_template(text, state, view)
    state, text = daily_download(browser_type,view)
    message_template(text, state, view)