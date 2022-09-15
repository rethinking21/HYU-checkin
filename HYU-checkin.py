import selenium
from selenium import webdriver

DRIVER_SHOW: bool = True
DRIVER_PATH = r'./data/chromedriver.exe'
COOKIE_DATA_PATH = r'./data/cookie'

# region var
HYU_main_site = r'https://check.hanyang.ac.kr/'
HYU_login_site = r'https://check.hanyang.ac.kr/login?lang=ko'
HYU_check_site = r'https://check.hanyang.ac.kr/stud/attend/main'

JSESSIONID: str = None
WMONID: str = None
chrome_options: webdriver.ChromeOptions = None
driver: webdriver.Chrome = None
# endregion

# region function


def open_webdriver() -> None:
    global driver, chrome_options, DRIVER_SHOW, DRIVER_PATH

    chrome_options = webdriver.ChromeOptions()
    if not DRIVER_SHOW:
        chrome_options.add_argument("headless")
    try:
        driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
    except selenium.common.exceptions.SessionNotCreatedException:
        print("!! Chrome Driver must be installed in right version.")
        print(f"!! Please check driver in {DRIVER_PATH} than update it\n!!")
        print("!! Check Chrome version in Chrome : chrome://settings/help")
        print("!! Download Chrome : https://chromedriver.chromium.org/downloads")

    driver.set_window_size(300, 100)
    driver.implicitly_wait(2)


def get_cookie_file_data() -> None:
    global JSESSIONID, WMONID, COOKIE_DATA_PATH
    file = open(COOKIE_DATA_PATH, 'r')
    JSESSIONID, WMONID, _ = map(str, file.readline().split())
    file.close()


def change_cookie() -> None:
    global driver
    get_cookie_file_data()

    current_cookie = driver.get_cookies()
    driver.delete_all_cookies()
    add_cookie_list = []
    for cookie in current_cookie:
        if 'name' in cookie:
            if cookie['name'] == 'JSESSIONID':
                cookie['value'] = JSESSIONID
            if cookie['name'] == 'WMONID':
                cookie['value'] = WMONID
                pass
            driver.add_cookie(cookie)


# endregion


open_webdriver()
driver.get(HYU_login_site)
change_cookie()
driver.get(HYU_main_site)

print("@checking opened class")

check_code: int = int(input("Input check code : "))

_ = input()

driver.quit()
