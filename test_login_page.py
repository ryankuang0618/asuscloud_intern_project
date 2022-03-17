from common.util import *
import os
import pickle
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
import sys
import traceback

def task1(browser_type,view):
    # 輸入正確帳號、密碼
    try:
        text='測試狀況1-1:輸入正確帳號、密碼'
        message_title(text,view)
        print(text)
        driver = browser(browser_type)
        state = login_nav(driver,login_config.get('navigate', 'account'),login_config.get('navigate', 'password'))
        if state==True:
            driver.close()
            return True,text
        else:
            driver.close()
            return False,text
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

def task2(browser_type,view):
    # 輸入正確帳號、錯誤密碼
    try:
        text='測試狀況1-2:輸入正確帳號、錯誤密碼'
        message_title(text,view)
        print(text)
        driver = browser(browser_type)
        driver.get(login_config.get('navigate', 'url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'account'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).clear()
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).send_keys(login_config.get('navigate', 'account'))
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'password'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).clear()
        # 輸入錯誤密碼(正確密碼的一半)
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).send_keys(str(login_config.get('navigate', 'password'))[:int(len(str(login_config.get('navigate', 'password')))/2)])
        driver.find_element_by_xpath(login_config.get('xpath', 'enter_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'check_login_fail_point'))))
        if (driver.current_url == login_config.get('navigate', 'url')) and (driver.find_element_by_xpath(login_config.get('xpath', 'check_login_fail_point')).text=='帳號或密碼錯誤，請重新輸入。'):
            driver.close()
            return True,text
        else:
            driver.close()
            return False,text
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

def task3(browser_type,view):
    # 輸入錯誤帳號、正確密碼
    try:
        text='測試狀況1-3:輸入錯誤帳號、正確密碼'
        message_title(text,view)
        print(text)
        driver = browser(browser_type)
        driver.get(login_config.get('navigate', 'url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'account'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).clear()
        # 輸入錯誤帳號(正確帳號的一半)
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).send_keys(str(login_config.get('navigate', 'account'))[:int(len(str(login_config.get('navigate', 'account'))) / 2)])
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'password'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).clear()
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).send_keys(login_config.get('navigate', 'password'))
        driver.find_element_by_xpath(login_config.get('xpath', 'enter_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'check_login_fail_point'))))
        if (driver.current_url == login_config.get('navigate', 'url')) and (
                driver.find_element_by_xpath(login_config.get('xpath', 'check_login_fail_point')).text == '帳號或密碼錯誤，請重新輸入。'):
            driver.close()
            return True, text
        elif '驗證碼' in driver.find_element_by_xpath(login_config.get('xpath', 'check_login_fail_point')).text:
            driver.close()
            return True, text + "[驗證碼需待驗證]"
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


def task4(browser_type,view):
    # 輸入錯誤帳號、密碼
    try:
        text='測試狀況1-4:輸入錯誤帳號、密碼'
        message_title(text,view)
        print(text)
        driver = browser(browser_type)
        driver.get(login_config.get('navigate', 'url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'account'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).clear()
        # 輸入錯誤帳號(正確帳號的一半)
        driver.find_element_by_xpath(login_config.get('xpath', 'account')).send_keys(str(login_config.get('navigate', 'account'))[:int(len(str(login_config.get('navigate', 'account'))) / 2)])
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'password'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).clear()
        # 輸入錯誤密碼(正確密碼的一半)
        driver.find_element_by_xpath(login_config.get('xpath', 'password')).send_keys(str(login_config.get('navigate', 'password'))[:int(len(str(login_config.get('navigate', 'password'))) / 2)])
        driver.find_element_by_xpath(login_config.get('xpath', 'enter_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'check_login_fail_point'))))
        if (driver.current_url == login_config.get('navigate', 'url')) and (driver.find_element_by_xpath(login_config.get('xpath', 'check_login_fail_point')).text=='帳號或密碼錯誤，請重新輸入。'):
            driver.close()
            return True,text
        elif  '驗證碼' in driver.find_element_by_xpath(login_config.get('xpath', 'check_login_fail_point')).text:
            driver.close()
            return True, text+"[驗證碼需待驗證]"
        else:
            driver.close()
            return False,text
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


def forget_password(browser_type,view):
    try:
        text = '測試狀況五:測試是否有收到忘記密碼信件'
        message_title(text, view)
        print(text)
        driver = browser(browser_type)
        driver.get(login_config.get('navigate', 'url'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'forget_button'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'forget_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'forget_id'))))
        driver.find_element_by_xpath(login_config.get('xpath', 'forget_id')).clear()
        driver.find_element_by_xpath(login_config.get('xpath', 'forget_id')).send_keys(str(login_config.get('navigate', 'account')))
        while(True):
            captcha_word = str(input('請輸入驗證碼:'))
            wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'forget_captcha'))))
            driver.find_element_by_xpath(login_config.get('xpath', 'forget_captcha')).clear()
            driver.find_element_by_xpath(login_config.get('xpath', 'forget_captcha')).send_keys(captcha_word)
            time.sleep(2)
            driver.find_element_by_xpath(login_config.get('xpath', 'forget_enter')).click()
            time.sleep(2)
            try:
                WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'error'))))
                print("忘記密碼信件寄出成功")
                break
            except:
                print("驗證碼錯誤")
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print(os.path.join(os.path.dirname(__file__), 'common', 'credentials.json'))
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(__file__), 'common', 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        # Call the Gmail API
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])

        message_count = 2

        if not messages:
            print('No messages found.')
        else:
            print('messages:')
            for message in messages[:message_count]:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(msg['snippet'])
                if ('重新設定密碼' in msg['snippet']):
                    return True,text
                    driver.close()
                else:
                    continue
            return False,text
            driver.close()
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


def login(view,browser_type):
    print('[登入測試網址]:', login_config.get('navigate', 'url'))
    state, text = task1(browser_type,view)
    message_template(text, state, view)
    state, text = task2(browser_type,view)
    message_template(text, state, view)
    state, text = task3(browser_type,view)
    message_template(text, state, view)
    state, text = task4(browser_type,view)
    message_template(text, state, view)
    state, text = forget_password(browser_type,view)
    message_template(text, state, view)
    time.sleep(5)