from common.util import *

def task1(browser_type):
    driver = browser(browser_type)
    state = login_nav(driver, login_config.get('navigate', 'account'), login_config.get('navigate', 'password'))
    if state == True:
        # 登入成功才繼續進行
        text = ''
        print(text)
        return True,text

def trash(view,browser_type):
    print('[資源回收桶測試]')
    state, text = task1(browser_type)
    message_template(text, state, view)