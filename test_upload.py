from common.util import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def changeuploadsize(browser_type,size):
    print('修該單檔上傳大小限制...')
    driver = browser('chrome')
    driver.get(login_config.get('osm', 'url'))
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'osm_account'))))
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_account')).clear()
    # 輸入錯誤帳號(正確帳號的一半)
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_account')).send_keys(
        str(login_config.get('osm', 'account')))
    wait.until(EC.visibility_of_element_located((By.XPATH, login_config.get('xpath', 'osm_password'))))
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_password')).clear()
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_password')).send_keys(
        str(login_config.get('osm', 'password')))
    time.sleep(2)
    driver.find_element_by_xpath(login_config.get('xpath', 'osm_enter')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'osm_usermanage'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'osm_usermanage')).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, account_config.get('xpath', 'group_manage'))))
    driver.find_element_by_xpath(account_config.get('xpath', 'group_manage')).click()
    wait.until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr[2]/td[1]')))
    time.sleep(2)
    table_id = driver.find_elements_by_class_name('table-b rwd-table')
    rows = driver.find_elements_by_tag_name("tr")  # get all of the rows in the table
    for i in range(2, len(rows)):
        cols = rows[i].find_elements_by_tag_name("td")[0]  # note: index start from 0, 1 is col 2
        if (cols.text == account_config.get('account_data', 'group_name')):
            group_count = i
            break
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[5]/input')))
    driver.find_element_by_xpath(
        '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[5]/input').clear()
    driver.find_element_by_xpath(
        '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[5]/input').send_keys(str(size))
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[7]/button[1]')))
    driver.find_element_by_xpath(
        '/html/body/div/div/div/div[1]/div/table/tbody/tr[' + str(group_count) + ']/td[7]/button[1]').click()
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, account_config.get('xpath', 'reason_input'))))
    driver.find_element_by_xpath(
        account_config.get('xpath', 'reason_input')).clear()
    driver.find_element_by_xpath(
        account_config.get('xpath', 'reason_input')).send_keys(str(size))
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, account_config.get('xpath', 'reason_button'))))
    driver.find_element_by_xpath(
        account_config.get('xpath', 'reason_button')).click()
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, account_config.get('xpath', 'changeuploadsize_check'))))
    time.sleep(3)
    if('成功' in driver.find_element_by_xpath(account_config.get('xpath', 'changeuploadsize_check')).text):
        print('修該單檔上傳大小限制成功')
    else:
        print('修該單檔上傳大小限制失敗')
    driver.close()
def tomb(number):
    MB = 1 * 1024 * 1024
    return (number+100)*MB
def task1(browser_type,view,number):
    driver = browser(browser_type)
    state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
    if state == True:
        # 登入成功才繼續進行
        text = '測試狀況1-1:單檔上傳大小限制測試'
        message_title(text, view)
        print(text)
        changeuploadsize(browser_type, number)
        print(str(tomb(number)))
        cmd = '''cd ..&fsutil file createnew UploadTest %s''' % (str(tomb(number)))
        os.system(cmd)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="breadcrumb"]/ul[2]/li[4]/a')))
        driver.find_element_by_xpath('//*[@id="breadcrumb"]/ul[2]/li[4]/a').click()
        time.sleep(3)
        upload = driver.find_element_by_id('uploadfile')
        upload.send_keys(os.path.join(os.path.dirname(__file__),'UploadTest'))
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-top"]/app-root/app-layout/div[1]/app-alert/div')))
            os.remove(os.path.join(os.path.dirname(__file__), 'UploadTest'))
            driver.close()
            return True,text

        except:
            os.remove(os.path.join(os.path.dirname(__file__), 'UploadTest'))
            driver.close()
            return False,text

def upload(view,browser_type):
    print('[上傳測試]')
    state,text = task1(browser_type,view,100)
    message_template(text, state, view)
