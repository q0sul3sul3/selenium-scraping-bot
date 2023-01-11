import crawling.config as const
from bs4 import BeautifulSoup

import pymysql.cursors
import json
import datetime


# Connect to the database
connection = pymysql.connect(host=const.HOST,
                             port=const.PORT,
                             user=const.USER,
                             password=const.DBPASSWORD,
                             database=const.DATABASE,
                             cursorclass=pymysql.cursors.DictCursor)

class Parsing:
    def __init__(self, soup):
        self.soup = soup

    def get_table_data(self, id_value):
        tabledata = self.soup.find('table', id=id_value)
        data = tabledata.find_all('tr', class_='ui-widget-content')
        
        data_list = []
        for i in data:
            data_dict = {}
            for j in i.find_all('td', role='gridcell'):
                if j.find('input'):
                    data_dict[j.get('aria-describedby')] = j.find('input').get('value')
                else:
                    data_dict[j.get('aria-describedby')] = j.text.replace(u'\xa0', u'')
            data_list.append(data_dict)
        return data_list

    def get_textarea_data(self):
        textareadata = self.soup.find_all('textarea')
        
        data_dict = {}
        for i in textareadata:
            data_dict[i.get('id')] = i.text
        return data_dict

    def get_select_data(self):
        selectdata = self.soup.find_all('select')
        
        data_dict = {}
        for i in selectdata:
            if i.find('option', selected='selected'):
                data_dict[i.get('id')] = i.find('option', selected='selected').text
            else:
                data_dict[i.get('id')] = ''
        return data_dict

    def get_input_data(self):
        inputdata = self.soup.find_all('input')
        
        data_dict = {}
        for i in inputdata:
            if i.get('type') == 'checkbox' and i.get('checked') != 'checked':
                data_dict[i.get('id')] = ''
            elif i.get('id') and i.get('type') != 'button' and i.get('type') != 'hidden' and i.get('id')[0:2] != 'rb':
                data_dict[i.get('id')] = i.get('value')
        return data_dict

    def get_patient_data(self):
        patient_data = {}
        patient_data.update(self.get_input_data())
        patient_data.update(self.get_select_data())
        patient_data['Chronicilness'] = self.get_table_data('jqGrid_PatientChronic')
        patient_data['Mediclaimpayer'] = self.get_table_data('patientMediPayerGridGP')
        patient_data['Medallergy'] = self.get_table_data('patientAllergyGrid')
        patient_data['Medallergyother'] = self.get_table_data('patientAllergyOtherGrid')
        patient_data['Family'] = self.get_table_data('patientFamilyGrid')
        patient_data.update(self.get_textarea_data())
        patient_data['ReferralLetter'] = self.get_table_data('patientReferralGrid')
        # print(patient_data)
        return patient_data

    def retore_to_database(self, table_name, type_name, id_name, data):
        data_json = json.dumps(data)
        now = datetime.datetime.now()
        cursor = connection.cursor()
        sql = 'INSERT INTO `{}` (`type`, `given_id`, `data`, `format`, `synced_on`) VALUES (%s, %s, %s, %s, %s)'.format(table_name)
        cursor.execute(sql, (type_name, id_name, data_json, 'JSON', now))
        connection.commit()