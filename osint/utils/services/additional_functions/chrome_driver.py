from selenium import webdriver
from fake_useragent import UserAgent


def start_chrome_driver():
    options = webdriver.ChromeOptions()
    ua = UserAgent(verify_ssl=False)
    userAgent = ua.random
    executable_path = r"./utils/services/additional_functions/chromedriver"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument(f'user-agent={userAgent}')
    return webdriver.Chrome(chrome_options=options, executable_path=executable_path)


