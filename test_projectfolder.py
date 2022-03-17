from common.util import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
global timee
def create_pf(browser_type):
    try:
        global timee
        timee = time.time()
        print('創建專案資料夾...')
        driver = browser(browser_type)
        login_osm(driver, login_config.get('osm', 'account'), login_config.get('osm', 'password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'share_manage'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'share_manage')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_manage'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_manage')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_add'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_add')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_name'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_name')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_name')).send_keys('ProjectFolder_test'+str(timee))
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_size'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_size')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_size')).send_keys('10')
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_owner'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_owner')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_owner')).send_keys(login_config.get('navigate', 'account'))
        time.sleep(5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="expireTime"]')))
        driver.execute_script('document.getElementsByName("expireTime")[0].removeAttribute("readonly")')
        driver.find_element_by_name('expireTime').clear()
        driver.find_element_by_name('expireTime').send_keys('2021-06-18')
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_single_upload'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_single_upload')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_single_upload')).send_keys('500')
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'add_button'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'add_button')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'reason_input'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'reason_input')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'reason_input')).send_keys('test')
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'reason_ok'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'reason_ok')).click()
        try:
            if('成功' in driver.find_element_by_xpath(project_folder_config.get('xpath', 'check_sucess')).text):
                print('osm專案資料夾新增成功')
                driver.close()
                return True
            else:
                driver.close()
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
            driver.close()
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
        return False
def delete_pf(browser_type):
    global timee
    try:
        print('刪除專案資料夾...')
        driver = browser(browser_type)
        login_osm(driver, login_config.get('osm', 'account'), login_config.get('osm', 'password'))
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'share_manage'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'share_manage')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pf_manage'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pf_manage')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'search_point'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'search_point')).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'pj_search'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pj_search')).clear()
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'pj_search')).send_keys('ProjectFolder_test'+str(timee))
        wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'search_entry'))))
        driver.find_element_by_xpath(project_folder_config.get('xpath', 'search_entry')).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[3]/table')))
        time.sleep(3)
        try:
            table_xpath = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[3]/table')
            rows = table_xpath.find_elements_by_tag_name("tr")  # get all of the rows in the table
            for i in range(1, len(rows)):
                cols = rows[i].find_elements_by_tag_name("td")[0]  # note: index start from 0, 1 is col 2
                print(cols.text)

                if(cols.text == 'ProjectFolder_test'+str(timee)):
                    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/div[3]/table/tbody/tr['+str(i)+']/td[7]/button[3]')))
                    driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[3]/table/tbody/tr['+str(i)+']/td[7]/button[3]').click()
                    break
            wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'delete_enter'))))
            driver.find_element_by_xpath(project_folder_config.get('xpath', 'delete_enter')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'delete_reason'))))
            driver.find_element_by_xpath(project_folder_config.get('xpath', 'delete_reason')).clear()
            driver.find_element_by_xpath(project_folder_config.get('xpath', 'delete_reason')).send_keys('test')
            wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'delete_ok'))))
            driver.find_element_by_xpath(project_folder_config.get('xpath', 'delete_ok')).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'result_word'))))
            if('success' in driver.find_element_by_xpath(project_folder_config.get('xpath', 'result_word')).get_attribute('src')):
                print('刪除專案資料夾成功')
                driver.close()
            else:
                print('刪除專案資料夾失敗')
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
            driver.close()
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
        driver.close()
        return False
def task1(browser_type):
    global timee
    try:
        create_pf(browser_type)
        driver = browser(browser_type)
        state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
        if state == True:
            # 登入成功才繼續進行
            text = '測試是否成功創建專案資料夾'
            print(text)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.visibility_of_element_located((By.XPATH, project_folder_config.get('xpath', 'nav_projectfolder'))))
            driver.find_element_by_xpath(project_folder_config.get('xpath', 'nav_projectfolder')).click()
            wait.until(EC.presence_of_element_located((By.ID, 'responsivetable')))
            time.sleep(3)
            try:
                table_id = driver.find_element_by_id('responsivetable')
                rows = table_id.find_elements_by_tag_name("tr")  # get all of the rows in the table
                for i in range(1, len(rows)):
                    cols = rows[i].find_elements_by_tag_name("td")[2]  # note: index start from 0, 1 is col 2
                    print(cols.text)
                    if ('ProjectFolder_test'+str(timee) in cols.text):
                        print('專案資料夾新增成功')
                        driver.close()
                        return True, text
                    else:
                        print('專案資料夾新增失敗')
                        driver.close()
                        return False,text
            except Exception as e:
                driver.close()
                print(e)
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

def projectfolder(view,browser_type):
    print('[專案資料夾測試]')
    state, text = task1(browser_type)
    message_template(text, state, view)
    delete_pf(browser_type)
