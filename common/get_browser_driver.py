import os
import requests
import zipfile
import sys
from bs4 import BeautifulSoup
from common.get_browser_version import *
from common.util import config

folder_path = str(config.get('driver','folder_path'))

# 檢查資料夾
def check_folder():
    if os.path.exists(folder_path):
        print("Driver資料夾存在。")
        print('-'*10)
        return True
    else:
        print("Driver資料夾不存在。")
        os.mkdir(folder_path)
        print('-' * 10)
        return False

# 解壓縮檔案
def unzip(zip_path,browser_name):
    print('解壓縮...')
    zip_name = zip_path  # 壓縮後的文件名
    with zipfile.ZipFile(zip_name, 'r') as myzip:
        if str(browser_name).lower()=='chrome':
            myzip.extract('chromedriver.exe',folder_path+'/')
        elif str(browser_name).lower()=='edge':
            myzip.extract('msedgedriver.exe',folder_path+'/')
        elif str(browser_name).lower()=='firefox':
            myzip.extract('geckodriver.exe', folder_path+'/')
    print('解壓縮...完成')

# 下載driver至目標存取位置
def download_driver(target_url,name,browser_name):
    print("driver下載...")
    print(target_url)
    r = requests.get(target_url)
    with open(folder_path+'/'+name, "wb") as code:
        code.write(r.content)
    unzip(folder_path+'/'+name,browser_name)

# 取得瀏覽器driver
def get_driver(type):
    if str(type).lower()=="chrome":
        get_chrome_driver(type)
    elif str(type).lower()=="firefox":
        get_firefox_driver(type)
    elif str(type).lower()=="edge":
        get_edge_driver(type)

def get_chrome_driver(type):
    check_folder()
    version_num=get_browser_version(type)
    # chrome_driver連結
    print("chrome_driver連結...")
    driver_url = str(config.get('driver','chrome_driver_url'))
    r = requests.get(driver_url)
    objSoup = BeautifulSoup(r.text, 'lxml')
    objTag = objSoup.find('td', 'sites-layout-tile sites-tile-name-content-1').find('div').find('div').find_all('li')
    print("本機作業系統:", sys.platform)

    for i in objTag:
        try:
            target_url = None
            if version_num.split('.')[0].split('=')[1] in i.find('span').text:
                driver_download_url = i.find('a').get('href')
                print(driver_download_url)
                if sys.platform == 'win32':
                    # windows
                    target_url = str(driver_download_url).split('index.html?')[0] + str(driver_download_url).split('path=')[1] + 'chromedriver_win32.zip'
                    print("chrome_driver連結...完成")
                    download_driver(target_url, 'chromedriver_win32.zip', type)
                    print("driver下載...完成")
        except:
            pass

def get_firefox_driver(type):
    check_folder()
    version_num = get_browser_version(type)
    print("firefox連結...")
    print("本機作業系統:", sys.platform)
    driver_url=str(config.get('driver','firefox_driver_url'))
    print(driver_url)
    r = requests.get(driver_url)
    objSoup = BeautifulSoup(r.text, 'lxml')
    objTag = objSoup.find('div', 'f1 flex-auto min-width-0 text-normal').text.strip()
    target_url = None
    if sys.platform == 'win32':
        target_url = driver_url+'/download/v' + objTag + '/geckodriver-v' + objTag + '-win64.zip'
        print("firefox_driver連結...完成")
        download_driver(target_url, 'firefox_win64.zip', type)
        print("driver下載...完成")

def get_edge_driver(type):
    check_folder()
    version_num = get_browser_version(type).split('=')[1]
    # edge_driver連結
    print("edege_driver連結...")
    print("本機作業系統:", sys.platform)
    driver_url = str(config.get('driver', 'edge_driver_url'))
    print(driver_url)
    target_url = driver_url + version_num + '/'
    if sys.platform == 'win32':
        target_url += 'edgedriver_win64.zip'
        print("edge_driver連結...完成")
        download_driver(target_url, 'edgedriver_win64.zip', type)
        print("driver下載...完成")

if __name__ == '__main__':
    get_chrome_driver()
    print('-'*10)
    get_firefox_driver()
    print('-' * 10)
    get_edge_driver()