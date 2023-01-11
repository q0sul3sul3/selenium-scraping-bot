import crawling.config as const
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json


class Crawling(webdriver.Chrome):
    def __init__(self, driver_path=const.WEBDRIVER_PATH):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Crawling, self).__init__(options=options)

    def land_first_page(self):
        self.get(const.URL)

    def login_page(self):
        username_element = self.find_element(By.ID, 'txtLoginID')
        username_element.send_keys(const.USERNAME)
        password_element = self.find_element(By.ID, 'txtPasswordFake')
        password_element.send_keys(const.PASSWORD)
        branch_element = self.find_element(By.ID, 'txtClinic')
        branch_element.send_keys(const.BRANCH)
        login_element = self.find_element(By.ID, 'btnLogin')
        login_element.click()

    def save_cookies(self):
        cookies = self.get_cookies()
        # print(cookies)
        with open('cookies.json', 'w') as file:
            file.write(json.dumps(cookies))

    def clear_cookies(self):
        cookies = self.get_cookies()
        for cookie in cookies:
            # print(cookie)
            self.delete_cookie(cookie['name'])

    def set_cookies(self):
        with open('cookies.json', 'r') as file:
            data = json.loads(file.read())
            for i in data:
                # print(i)
                self.add_cookie(i)

    def go_queue(self):
        self.execute_script('window.location="{}Home/Reception"'.format(const.URL))
   
    def click_branch_and_room(self):
        try:
            WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.ID, 'btnRoom0'))).click()
        except:
            WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.ID, 'btnRoom1'))).click()

    def click_sidebar_menu(self, sidebarmenu='SidebarmenuPatient'):
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.ID, sidebarmenu))).click()

    def search_patientid(self, patientid):
        search_element = WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "patientfilterItemSearch")))
        search_element.clear()
        search_element.send_keys(patientid)
        self.wait_for_ajax()
        search_element.send_keys(Keys.RETURN)

    def patientid_to_be_present(self, patientid):
        PCNO_XPATH = '//*[@id="{}"]/td[2]'.format(patientid)
        # PCNO_CSS = 'td[title="{}"]'.format(patientid)
        WebDriverWait(self, 10).until(EC.text_to_be_present_in_element((By.XPATH, PCNO_XPATH), patientid))

    def find_by_class(self, class_name):
        return self.find_elements(By.CLASS_NAME, class_name)

    def click_button_by_id(self, id_name):
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.ID, id_name))).click()

    def click_button_by_class(self, class_name):
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()
    
    def click_button_by_xpath(self, xpath_name):
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_name))).click()

    def wait_for_ajax(self):
        try:
            WebDriverWait(self, 10).until(lambda self: self.execute_script('return jQuery.active') == 0)
            WebDriverWait(self, 10).until(lambda self: self.execute_script('return document.readyState') == 'complete')
        except Exception as e:
            print(e)
    
    def get_page_source(self):
        soup = BeautifulSoup(self.page_source, 'html.parser')
        return soup