import crawling.listing as lst
from crawling.crawling import Crawling
from crawling.parsing import Parsing

import datetime
import logging
from logging.handlers import RotatingFileHandler


date = datetime.date.today().strftime("%Y%m%d")
logging.basicConfig(
    handlers=[RotatingFileHandler('./log_patient_{}.log'.format(date), maxBytes=100*1024*1024, backupCount=5)], 
    level=logging.WARNING, 
    format='[%(asctime)s %(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')

with Crawling() as bot:
    bot.land_first_page()
    bot.login_page()
    bot.click_branch_and_room()
    if bot.find_by_class('sa-confirm-button-container'):
        bot.click_button_by_class('sa-confirm-button-container')
    bot.click_sidebar_menu('SidebarMenuPatient')
    for i in lst.patient_list:
        while True:
            try:
                bot.search_patientid(i)
                bot.patientid_to_be_present(i)
                bot.click_button_by_xpath('//*[@id="{}"]/td[3]/a'.format(i))
                bot.wait_for_ajax()
                bot.click_button_by_id('Pat-tab-li-History')
                bot.wait_for_ajax()
                bot.click_button_by_id('Pat-tab-li-Referral')
                bot.wait_for_ajax()
                parsing = Parsing(bot.get_page_source())
                parsing.retore_to_database('dataset', 'Patient', i, parsing.get_patient_data())
                bot.click_button_by_id('btnPatientBack')
                print('PatientID: {} - {}/{}'.format(i, lst.patient_list.index(i)+1, len(lst.patient_list)))
                logging.warning('PatientID: {} - {}/{}'.format(i, lst.patient_list.index(i)+1, len(lst.patient_list)))
                break
            except:
                bot.refresh()
print('Complete!')
logging.warning('Complete!')