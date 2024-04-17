import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import re
from datetime import datetime
from utils.services.additional_functions.chrome_driver import start_chrome_driver
import getpass
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import os

class Tutnaidut:
    def __init__(self, user_id):
        self.user_id = user_id

    def search(self):
        if 'id' in self.user_id:
            self.user_id = self.user_id[2:]
            self.user_id = self.user_id.strip()
        html = requests.get('http://tutnaidut.com/user' + self.user_id).content
        soup = BeautifulSoup(html, 'lxml')
        if soup.h4.text == 'Пользователь с номером ' + self.user_id + ' отсутствует.':
            print('Пользователь с id{0} отсутствует'.format(self.user_id))
        else:
            information_dict = {}
            name = soup.find('span', itemprop='name')
            gender = soup.find('div', style='padding-bottom:20px;').find(text='Пол:')
            birthDate = soup.find('span', itemprop='birthDate')
            city = soup.find('div', style='padding-bottom:20px;').find(text='Город:')
            picture = soup.find('img')['src']
            resource = requests.get(picture)
            photo = open(self.user_id + '.jpg', 'wb')
            photo.write(resource.content)
            photo.close()
            photo_path = os.path.abspath(self.user_id + '.jpg')
            if name != None:
                information_dict['vk-name'] = name.text
            if gender != None:
                information_dict['vk-gender'] = gender.next
            if birthDate != None:
                information_dict['vk-date_of_birth'] = birthDate.text
            if city != None:
                information_dict['vk-residential_address'] = city.next
            if picture != None:
                information_dict['photo-path'] = photo_path
            self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Vk_photo:
    def __init__(self, user_id):
        self.user_id = user_id

    def search(self):
        information_dict = {}
        try:
            driver = start_chrome_driver()
            driver.get('https://vk-photo.xyz')
            driver.find_element_by_class_name(r"form-control").send_keys(self.user_id)
            driver.find_element_by_name(r"user").click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.find('h1', class_='profile')
            if name != None:
                name = name.text
                name = name[:name.find('\n')]
            unknown_city = soup.find('a', href='/unknown')
            h5 = soup.find_all('h5')
            if unknown_city is None:
                city = h5[1].text
                if len(h5) == 4:
                    birthDate = h5[2].text
                    birthDate = birthDate[birthDate.find(':') + 2:birthDate.find('г') - 1]
                else:
                    birthDate = None
            else:
                city = None
                if len(h5) == 2:
                    birthDate = None
                else:
                    birthDate = h5[1].text
                    birthDate = birthDate[birthDate.find(':') + 2:birthDate.find('г') - 1]
            picture = soup.find('a', class_='image-link')
            if picture != None:
                resource = requests.get(picture['href'])
                photo = open(self.user_id + '.jpg', 'wb')
                photo.write(resource.content)
                photo.close()
                photo_path = os.path.abspath(self.user_id + '.jpg')
            if name != None:
                information_dict['vk-name'] = name
            if birthDate != None:
                information_dict['vk-date_of_birth'] = birthDate
            if city != None:
                information_dict['vk-residential_address'] = city
            if picture != None:
                information_dict['vk-place_of_birth'] = photo_path
        except:
            pass
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Rusfinder:
    def __init__(self, surname, name):
        self.surname = surname
        self.name = name

    def search(self):
        html = requests.get('https://rusfinder.pro/search/surname/' + self.surname + '/name/' + self.name).content
        soup = BeautifulSoup(html, 'lxml')
        information_list = []
        if soup.find('div', class_='pagination'):
            count_pages = int(soup.find('div', class_='pagination').find_all('a')[-1].text)
        else:
            count_pages = 1

        driver = start_chrome_driver()

        for page in range(count_pages):
            driver.get('https://rusfinder.pro/search/surname/' + self.surname + '/name/' + self.name + '/page/' + str(page + 1))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            all_users = soup.find_all('div', class_='vk_user')
            for user in all_users:
                user_id = 'id' + user['data-vk_id']
                picture = user.find('img')
                if picture != None:
                    picture = picture['src']

                # Скачивание аватарок
                    resource = requests.get(picture)
                    photo = open(user_id + '.jpg', 'wb')
                    photo.write(resource.content)
                    photo.close()
                    photo_path = os.path.abspath(user_id + '.jpg')

                country = user.find('span', class_='country')
                city = user.find('span', class_='city')
                home_city = user.find('span', class_='home_town_str')
                birthDate = user.find('span', class_='bdate')
                university = user.find('span', class_='universities_str')
                school = user.find('span', class_='schools_str')
                job = user.find('span', class_='occupation_str')
                instagram = user.find('span', class_='instagram')
                skype = user.find('span', class_='skype')
                phone = user.find('span', class_='home_phone')
                temp_dict = {}
                temp_dict['vk-surname'] = self.surname
                temp_dict['vk-name'] = self.name
                if user_id != None:
                    temp_dict['vk-id'] = user_id
                if self.name != None:
                    temp_dict['photo-path'] = photo_path
                if country != None:
                    temp_dict['vk-country'] = country.text
                if city != None:
                    temp_dict['vk-residential_address'] = city.text
                if home_city != None:
                    temp_dict['vk-place_of_birth'] = home_city.text
                if birthDate != None:
                    temp_dict['vk-date_of_birth'] = birthDate.text
                if university != None:
                    temp_dict['vk-university'] = university.text
                if school != None:
                    temp_dict['vk-school'] = school.text
                if job != None:
                    temp_dict['vk-job'] = job.text
                if instagram != None:
                    temp_dict['vk-instagram'] = instagram.text
                if skype != None:
                    temp_dict['vk-skype'] = skype.text
                if phone != None:
                    temp_dict['vk-phone'] = phone.text
                information_list.append(temp_dict)
            self.information_list = information_list

    def get_info(self):
        return self.information_list


class Iplogger:
    def __init__(self, ip):
        self.ip = ip

    def search(self):
        html = requests.get('https://iplogger.ru/ip-lookup/?d=' + self.ip).content
        soup = BeautifulSoup(html, 'lxml')
        information_dict = {}
        country = soup.find('img', title='Страна')
        city = soup.find('img', title='Город')
        status = soup.find('img', title='Статус')
        port = soup.find(text='Порт')
        region = soup.find('img', title='Регион')
        provider = soup.find('img', title='Провайдер')
        date_time = soup.find_all('img', title='Провайдер')
        map = soup.find('a', class_='map')['onclick']
        map = re.findall('\(([\d\.\s,]+),\s{1}\{', map)

        information_dict['IP_addresses-ip'] = self.ip
        if map != None:
            information_dict['IP_addresses-position'] = map
        if country != None:
            information_dict['IP_addresses-country'] = str(country.next).strip()
        if city != None:
            information_dict['IP_addresses-city'] = str(city.next).strip()
        if status != None:
            information_dict['IP_addresses-status'] = str(status.next).strip()
        if port != None:
            information_dict['IP_addresses-port'] = str(port.next).strip()
        if region != None:
            information_dict['IP_addresses-region'] = str(region.next).strip()
        if provider != None:
            information_dict['IP_addresses-provider'] = str(provider.next).strip()
        if date_time != None and len(date_time) == 2:
            information_dict['IP_addresses-time zone'] = str(date_time[1].next).strip()
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Urllogger:
    def __init__(self, url):
        self.url = url

    def search(self):
        html = requests.get('https://iplogger.ru/url-checker/?d=' + self.url).content
        soup = BeautifulSoup(html, 'lxml')
        information_dict = {}
        ip = soup.find_all('div', class_='copyimg')
        country = soup.find('img', title='Страна')
        city = soup.find('img', title='Город')
        status = soup.find('img', title='Статус')
        port = soup.find(text='Порт')
        region = soup.find('img', title='Регион')
        provider = soup.find('img', title='Провайдер')
        date_time = soup.find_all('img', title='Провайдер')
        map = soup.find('a', class_='map')['onclick']
        map = re.findall('\(([\d\.\s,]+),\s{1}\{', map)

        information_dict['URL_addresses-url'] = self.url
        if map != None:
            information_dict['URL_addresses-position'] = map
        if ip != None and len(ip) == 2:
            information_dict['URL_addresses-ip'] = ip[1]['data-clipboard-text']
        if country != None:
            information_dict['URL_addresses-country'] = str(country.next).strip()
        if city != None:
            information_dict['URL_addresses-city'] = str(city.next).strip()
        if status != None:
            information_dict['URL_addresses-status'] = str(status.next).strip()
        if port != None:
            information_dict['URL_addresses-port'] = str(port.next).strip()
        if region != None:
            information_dict['URL_addresses-region'] = str(region.next).strip()
        if provider != None:
            information_dict['URL_addresses-provider'] = str(provider.next).strip()
        if date_time != None and len(date_time) == 2:
            information_dict['URL_addresses-time-zone'] = str(date_time[1].next).strip()
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Whatifmyipaddress:
    def __init__(self, ip):
        self.ip = ip

    def search(self):
        html = requests.get('https://whatismyipaddress.com/ip/' + self.ip).content
        soup = BeautifulSoup(html, 'lxml')
        information_dict = {}
        all_data = soup.find_all('td')

        information_dict['IP_addresses-ip'] = all_data[0].text
        information_dict['IP_addresses-hostname'] = all_data[2].text
        information_dict['IP_addresses-ASN'] = all_data[3].text
        information_dict['IP_addresses-ISP'] = all_data[4].text
        information_dict['IP_addresses-provider'] = all_data[5].text
        information_dict['IP_addresses-service'] = all_data[6].text
        information_dict['IP_addresses-type'] = all_data[7].text
        information_dict['IP_addresses-Assignment'] = all_data[8].text
        information_dict['IP_addresses-continent'] = all_data[10].text
        information_dict['IP_addresses-country'] = all_data[11].text
        information_dict['IP_addresses-region'] = all_data[12].text
        information_dict['IP_addresses-city'] = all_data[13].text
        latitude = str(all_data[14].text).strip()
        longitude = str(all_data[15].text).strip()
        position = re.findall('([\d\.]+)', latitude)[0] + ', ' + re.findall('([\d\.]+)', longitude)[0]
        information_dict['IP_addresses-position'] = position
        information_dict['IP_addresses-postal_code'] = all_data[16].text
        self.information_dict = information_dict

    def get_info(self):
        return  self.information_dict


class Propfr:
    def __init__(self, nineDigitsSnils):
        # self.snils = snils
        self.nineDigitsSnils = nineDigitsSnils

    def search(self):
        driver = start_chrome_driver()
        driver.get('https://propfr.ru/check_snils.html')

        # if self.snils != None:
        #     one_snils = str(self.snils)[:3]
        #     two_snils = str(self.snils)[3:6]
        #     three_snils = str(self.snils)[6:9]
        #     third_snils = str(self.snils)[9:11]
        #     driver.find_element_by_id(r"snils1").send_keys(one_snils)
        #     driver.find_element_by_id(r"snils2").send_keys(two_snils)
        #     driver.find_element_by_id(r"snils3").send_keys(three_snils)
        #     driver.find_element_by_id(r"snils4").send_keys(third_snils)
        sleep(2)
        if self.nineDigitsSnils != None:
            one_snils = str(self.nineDigitsSnils)[:3]
            two_snils = str(self.nineDigitsSnils)[3:6]
            three_snils = str(self.nineDigitsSnils)[6:9]
            for letter in one_snils:
                sleep(0.1)
                driver.find_element_by_id(r"snils_calc1").send_keys(letter)
            for letter in two_snils:
                sleep(0.1)
                driver.find_element_by_id(r"snils_calc2").send_keys(letter)
            for letter in three_snils:
                sleep(0.1)
                driver.find_element_by_id(r"snils_calc3").send_keys(letter)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        information_dict = {}
        answer = soup.find('div', class_='snils_ok_text').text
        checksum = re.findall('\s+([\d]{2})$', answer)[0]
        SNILS = self.nineDigitsSnils + checksum
        information_dict['insurance_certificate-numbe'] = SNILS
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class ServiceNalog:
    def __init__(self, surname, name, patronymic, birthDay, serialPassport, numberPassport, passports_issue_date):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.birthDay = birthDay
        self.numberCoc = serialPassport + numberPassport
        self.dateDoc = passports_issue_date

    def search(self):
        driver = start_chrome_driver()
        driver.get('https://service.nalog.ru/static/personal-data.html?svc=inn&from=%2Finn.do')
        driver.find_element_by_id(r"unichk_0").click()
        driver.find_element_by_id(r"btnContinue").click()
        sleep(1)
        for letter in self.surname:
            sleep(0.1)
            driver.find_element_by_name(r"fam").send_keys(letter)
        sleep(1)
        for letter in self.name:
            sleep(0.1)
            driver.find_element_by_name(r"nam").send_keys(letter)
        sleep(1)
        for letter in self.patronymic:
            sleep(0.1)
            driver.find_element_by_name(r"otch").send_keys(letter)
        driver.find_element_by_name(r"bdate").send_keys(self.birthDay)
        driver.find_element_by_name(r"docno").send_keys(self.numberCoc)
        driver.find_element_by_name(r"docdt").send_keys(self.dateDoc)
        driver.find_element_by_id(r"btn_send").click()
        sleep(5)
        information_dict = {}
        INN = driver.find_element_by_id(r"resultInn")
        information_dict['ITN'] = INN.text
        sleep(0.5)
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Suip:
    def __init__(self, domain):
        self.domain = domain

    def search(self):
        driver = start_chrome_driver()

        driver.get('https://suip.biz/ru/?act=amass')
        driver.save_screenshot('suip.png')
        sleep(2)
        driver.execute_script("window.scrollTo(0, 850)")
        WebDriverWait(driver, 60).until(ec.presence_of_element_located(('name', "url")))
        driver.find_element_by_name(r'url').send_keys(self.domain)
        driver.execute_script("window.scrollTo(0, 850)")
        driver.find_element_by_name(r'Submit1').click()

        WebDriverWait(driver, 60).until(ec.presence_of_element_located(('tag name', "pre")))
        tag_move = driver.find_element_by_tag_name('pre')
        actions = ActionChains(driver)
        actions.move_to_element(tag_move)
        actions.perform()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        information_dict = {}
        all_subdomains = soup.find('pre').text
        all_subdomains = re.split('\n', all_subdomains)
        information_dict['domain'] = all_subdomains[0]
        information_dict['all_subdomains'] = all_subdomains[1:]
        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Vin01:
    def __init__(self, carNumber=None, VIN=None):
        self.carNumber = carNumber
        self.VIN = VIN

    # Есть еще функции, в дальнейшем нужно расширить
    def search(self):
        driver = start_chrome_driver()

        driver.get('https://vin01.ru')
        information_dict = {}

        if self.carNumber != None and self.carNumber != ' ':
            sleep(1)
            for letter in self.carNumber:
                sleep(0.1)
                driver.find_element_by_id('num').send_keys(letter)
            driver.find_element_by_id('searchByGosNumberButton').click()
            driver.execute_script("window.scrollTo(0, 300)")

        if self.VIN != None and self.VIN != ' ':
            driver.find_element_by_id('vinToggleButton').click()
            sleep(1)
            for letter in self.VIN:
                sleep(0.1)
                driver.find_element_by_id('vinNumber').send_keys(letter)
            driver.find_element_by_id('searchByVinNumberButton').click()
            driver.execute_script("window.scrollTo(0, 300)")
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec
        WebDriverWait(driver, 60).until(ec.presence_of_element_located(('id', "checkType")))

        driver.find_element_by_id('checkType').click()
        driver.find_element_by_xpath('//*[@id="checkType"]/option[1]').click()
        sleep(2)
        driver.find_element_by_id('getCheckButton').click()
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(('tag name', "th")))

        model = driver.find_elements_by_tag_name('th')[1]
        carAttributs = driver.find_elements_by_tag_name('td')

        information_dict['car-VIN'] = carAttributs[15].text
        information_dict['car-model'] = model.text
        information_dict['car-color'] = carAttributs[1].text
        information_dict['car-type'] = carAttributs[3].text
        information_dict['car-year'] = carAttributs[5].text
        information_dict['car-engine_volume'] = carAttributs[7].text
        information_dict['car-engine_number'] = carAttributs[9].text
        information_dict['car-engine_power'] = carAttributs[11].text
        information_dict['car-category'] = carAttributs[13].text
        information_dict['car-body_number'] = carAttributs[17].text
        information_dict['car-count_owners'] = carAttributs[18].text + ' ' + carAttributs[19].text
        information_dict['car-period_own'] = carAttributs[20].text + ' ' + carAttributs[21].text

        driver.find_element_by_id('checkType').click()
        driver.find_element_by_xpath('//*[@id="checkType"]/option[10]').click()
        driver.find_element_by_id('getCheckButton').click()
        WebDriverWait(driver, 30).until(ec.presence_of_element_located(('tag name', "th")))
        DkNumber = driver.find_elements_by_tag_name('th')[1]
        TOAttr = driver.find_elements_by_tag_name('td')

        information_dict['car-diagnostic card_number'] = DkNumber.text
        information_dict['car-validity_mot'] = TOAttr[1].text
        information_dict['car-number'] = TOAttr[3].text

        self.information_dict = information_dict

    def get_info(self):
        return self.information_dict


class Fmsgov:
    def __init__(self, series, number):
        self.series = series
        self.number = number

    def search(self):
        from PIL import Image
        from io import BytesIO
        from matplotlib import pyplot as plt

        driver = start_chrome_driver()

        driver.get('http://services.fms.gov.ru/info-service.htm?sid=2000')
        driver.find_element_by_id(r"form_DOC_SERIE").send_keys(self.series)
        driver.find_element_by_id(r"form_DOC_NUMBER").send_keys(self.number)
        driver.execute_script("window.scrollTo(0, 1000)")

        scroll = driver.execute_script("return window.scrollY;")
        captcha = driver.find_element_by_id("captcha_image")
        location = captcha.location
        size = captcha.size
        png = driver.find_element_by_id("captcha_image").screenshot_as_png
        im = Image.open(BytesIO(png))
        im.save('captcha.png')

        captcha = input()
        driver.find_element_by_id('form_captcha-input').send_keys(captcha)
        driver.find_element_by_id('form_submit').click()
        sleep(2)
        answer = driver.find_element_by_class_name('ct-h4').text
        information_dict = {}
        information_dict['time_search'] = str(datetime.now())
        information_dict['initiator_search'] = getpass.getuser()
        information_dict['answer'] = answer
        self.information_dict = information_dict

    def get_info(self):
        pprint.pprint(self.information_dict)


# information = Fmsgov(6112, 770537)
# information.search()
# information.get_info()


# Сайт не дает искать, когда пользуешься Selenium
def kadarbitr(participantsСase=None, judge=None, court=None, caseNumber=None, dateSince=None, dateBefore=None):
    driver = start_chrome_driver()

    driver.get('http://kad.arbitr.ru')
    # if driver.find_element_by_css_selector(".b-promo_notification-popup-close.js-promo_notification-popup-close"):
    #     driver.find_element_by_css_selector(".b-promo_notification-popup-close.js-promo_notification-popup-close").click()
    if participantsСase != None:
        driver.find_element_by_xpath(r'//*[@id="sug-participants"]/div/textarea').send_keys(participantsСase)
    sleep(1)
    driver.find_element_by_xpath(r'//*[@id="b-form-submit"]/div/button').click()
    sleep(10)
    # driver.find_element_by_class_name()
    # if judge != None:
    #
    # if court != None:
    #
    # if caseNumber != None:
    #
    # if dateSince != None:
    #
    # if dateBefore != None:

# information = kadarbitr(participantsСase='Илья Феколин')



