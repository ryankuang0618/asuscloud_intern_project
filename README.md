# AsusCloud_QA_Intern_Project

## 運行方法
**1. 執行檔案**
```
run common/main.py 即可開始執行
```
**2. 選擇瀏覽器**
```
依照表單進行選取勾選

```
**3. 選擇測試項目**
```
依照表單進行選取勾選
```

## 專案結構
    ```
     AsusCloud_QA_Intern_Project
    .
     ├─common
     │  ├─selenium_driver
     │  │  ├─chromedriver.exe   Chrome網頁驅動程式
     │  │  ├─geckodriver.exe    Firefox網頁驅動程式
     │  │  └─msedgedriver.exe   Edge/IE網頁驅動程式
     │  ├─get_browser_driver.py     自動取得網頁驅動程式
     │  ├─get_browser_version.py    自動取得本地端網頁版本
     │  ├─main.py   主要執行程式    
     │  ├─ui.py     視窗
     │  └─util.py   共用程式
     ├─config
     │  ├─account_settings_config.ini 帳號資訊config
     │  ├─config.ini                  主要config
     │  ├─file_folder_config.ini      建檔資訊config
     │  ├─login_config.ini            登入頁面config
     │  └─main_test_config.ini        檔案/資料夾測試config
     ├─test_account_settings.py 帳號資訊
     ├─test_function.py         檔案/資料夾測試
     ├─test_login_page.py       登入頁面
     └─test_mysyncfolder.py     MySyncFolder
